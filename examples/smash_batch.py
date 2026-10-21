"""Shared OpenAI helper for the scaled benchmark notebooks 11-17.

Every LLM call in those notebooks goes through `LLM.run(stage, requests)`:

* model `gpt-6-luna` with `reasoning_effort="none"` (no hidden reasoning tokens), temperature 0, seed 7;
* results are cached per request in `<cache>/<stage>.jsonl` (keyed by request id + a hash of the request body),
  so a notebook replays its saved run in seconds and never pays twice for the same request;
* `MODE` decides what happens to requests that are not cached yet:
    - "replay" (default): raise - nothing is sent to the API;
    - "test":   send them synchronously (standard tier) - used for small end-to-end test runs;
    - "batch":  send them through the OpenAI Batch API (50% price, results within 24 h). Submitted batch ids are
                stored in `<cache>/<stage>.pending.json`, so an interrupted run resumes polling instead of
                re-submitting.

The notebooks select the mode with the environment variable SMASH_MODE (replay | test | batch).
"""
import gzip
import hashlib
import io
import json
import math
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

MODEL, EMBED_MODEL = "gpt-6-luna", "text-embedding-3-small"
REASONING = "none"
# USD per 1M tokens (input, output); Batch API = 50% of standard. Embeddings: $0.02 / 1M.
PRICE = {"standard": (0.10, 0.50), "batch": (0.05, 0.25)}
EMBED_PRICE = 0.02
MAX_LINES, MAX_BYTES = 40_000, 150_000_000          # per batch input file (API limits: 50k lines, 200 MB)


def mode_from_env():
    m = os.environ.get("SMASH_MODE", "replay")
    assert m in ("replay", "test", "batch"), m
    return m


def schema_format(model_cls):
    # Pydantic class -> strict json_schema response_format (the request body Batch needs).
    from openai.lib._parsing._completions import type_to_response_format_param
    return type_to_response_format_param(model_cls)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def paired_boot(a, b, n=5000, seed=7):
    # Mean of b - a with a 95% paired-bootstrap interval.
    d = np.asarray(b, float) - np.asarray(a, float)
    rs = np.random.default_rng(seed)
    m = rs.choice(d, (n, len(d))).mean(1)
    return d.mean(), np.percentile(m, 2.5), np.percentile(m, 97.5)


class LLM:
    def __init__(self, cache_dir, mode=None, workers=16, poll=30):
        self.cache, self.mode = cache_dir, mode or mode_from_env()
        self.workers, self.poll = workers, poll
        os.makedirs(cache_dir, exist_ok=True)
        self._client = None
        self._rows = {}                               # stage -> {key: row}

    @property
    def client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "missing"), max_retries=3, timeout=300)
        return self._client

    # ---- request bodies ------------------------------------------------------------------------------------
    @staticmethod
    def body(messages, max_tokens=2000, schema=None, tools=None, tool_choice=None):
        b = {"model": MODEL, "reasoning_effort": REASONING, "temperature": 0, "seed": 7,
             "max_completion_tokens": max_tokens, "messages": messages}
        if schema is not None:
            b["response_format"] = schema_format(schema)
        if tools:
            b["tools"] = tools
            if tool_choice:
                b["tool_choice"] = tool_choice
        return b

    # ---- cache ---------------------------------------------------------------------------------------------
    def _path(self, stage, ext="jsonl"):
        return f"{self.cache}/{stage}.{ext}"

    def rows(self, stage):
        if stage not in self._rows:
            rows = {}
            if os.path.exists(self._path(stage)):
                for line in open(self._path(stage)):
                    r = json.loads(line)
                    rows[r["key"]] = r
            self._rows[stage] = rows
        return self._rows[stage]

    def _save(self, stage, new_rows):
        with open(self._path(stage), "a") as f:
            for r in new_rows:
                f.write(json.dumps(r) + "\n")
                self._rows[stage][r["key"]] = r

    @staticmethod
    def _hash(body):
        return hashlib.sha1(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]

    @staticmethod
    def _result(resp, tier):
        # Compact result row from a chat.completions response (dict form).
        ch = resp["choices"][0]
        msg, u = ch["message"], resp.get("usage") or {}
        calls = [{"id": t["id"], "name": t["function"]["name"], "arguments": t["function"]["arguments"]}
                 for t in (msg.get("tool_calls") or [])]
        return {"text": msg.get("content") or "", "tool_calls": calls, "finish": ch.get("finish_reason"),
                "in": u.get("prompt_tokens", 0), "out": u.get("completion_tokens", 0),
                "reasoning": (u.get("completion_tokens_details") or {}).get("reasoning_tokens", 0), "tier": tier}

    # ---- main entry point ----------------------------------------------------------------------------------
    def run(self, stage, requests, parse=None):
        """requests: {key: body}. Returns {key: result}; result["parsed"] holds the parsed JSON when `parse`
        (a Pydantic class) is given, None if the output did not parse."""
        rows = self.rows(stage)
        todo = {k: b for k, b in requests.items()
                if k not in rows or rows[k]["h"] != self._hash(b) or "error" in rows[k]["r"]}
        if todo:
            if self.mode == "replay":
                raise RuntimeError(f"stage '{stage}': {len(todo)} of {len(requests)} requests are not cached - "
                                   "run with SMASH_MODE=test or SMASH_MODE=batch to compute them (uses the API).")
            print(f"[{stage}] {len(todo):,} new requests -> {self.mode} "
                  f"({len(requests) - len(todo):,} cached)", flush=True)
            if self.mode == "test":
                self._run_sync(stage, todo)
            else:
                self._run_batch(stage, todo)
        self._log_io(stage, requests)
        out = {}
        for k in requests:
            r = dict(rows[k]["r"])
            if parse is not None:
                try:
                    r["parsed"] = json.loads(r["text"]) if r.get("text") else None
                    if r["parsed"] is not None:
                        r["parsed"] = parse.model_validate(r["parsed"]).model_dump()
                except Exception:
                    r["parsed"] = None
            out[k] = r
        return out

    # ---- full input/output log (for later reports): <cache>/io/<stage>.jsonl.gz -------------------------------
    def _log_io(self, stage, requests):
        """Append every (request body, response) pair of this stage that is not logged yet. Runs on cached
        requests too, so replaying a notebook completes the log for calls made before logging existed."""
        os.makedirs(f"{self.cache}/io", exist_ok=True)
        path = f"{self.cache}/io/{stage}.jsonl.gz"
        if stage not in getattr(self, "_logged", {}):
            self._logged = getattr(self, "_logged", {})
            seen = set()
            if os.path.exists(path):
                with gzip.open(path, "rt") as f:
                    for line in f:
                        r = json.loads(line); seen.add((r["key"], r["h"]))
            self._logged[stage] = seen
        seen, rows = self._logged[stage], self.rows(stage)
        new = []
        for k, b in requests.items():
            h = self._hash(b)
            if (k, h) in seen or k not in rows or rows[k]["h"] != h:
                continue
            new.append({"stage": stage, "key": k, "h": h, "request": b, "response": rows[k]["r"]})
            seen.add((k, h))
        if new:
            with gzip.open(path, "at") as f:                # gzip members append cleanly
                for r in new:
                    f.write(json.dumps(r) + "\n")

    def _run_sync(self, stage, todo):
        def one(item):
            k, b = item
            for attempt in range(6):
                try:
                    resp = self.client.chat.completions.create(**b).model_dump()
                    return {"key": k, "h": self._hash(b), "r": self._result(resp, "standard")}
                except Exception as e:
                    if attempt == 5:
                        return {"key": k, "h": self._hash(b), "r": {"error": str(e)[:300], "in": 0, "out": 0,
                                                                   "tier": "standard"}}
                    time.sleep(2 ** attempt + random.random())
        with ThreadPoolExecutor(self.workers) as ex:
            new = list(ex.map(one, todo.items()))
        self._save(stage, new)

    # ---- Batch API -----------------------------------------------------------------------------------------
    def _upload(self, stage, items):
        # Split the requests into batch input files and upload them; returns the file ids.
        buf, files = io.BytesIO(), []
        def flush():
            if buf.tell():
                files.append(buf.getvalue()); buf.seek(0); buf.truncate()
        n = 0
        for k, b in items:
            line = (json.dumps({"custom_id": k, "method": "POST", "url": "/v1/chat/completions", "body": b}) + "\n").encode()
            if n >= MAX_LINES or buf.tell() + len(line) > MAX_BYTES:
                flush(); n = 0
            buf.write(line); n += 1
        flush()
        ids = []
        for i, data in enumerate(files):
            ids.append(self.client.files.create(file=(f"{stage}_{i}.jsonl", data), purpose="batch").id)
            print(f"[{stage}] uploaded input file {i + 1}/{len(files)} ({data.count(b'\n'):,} requests, "
                  f"{len(data) / 1e6:.0f} MB)", flush=True)
        return ids

    def _start(self, stage, file_id):
        bt = self.client.batches.create(input_file_id=file_id, endpoint="/v1/chat/completions",
                                        completion_window="24h", metadata={"stage": stage, "cache": self.cache[-480:]})
        print(f"[{stage}] started batch {bt.id}", flush=True)
        return bt.id

    def _run_batch(self, stage, todo, retries=2, max_running=4):
        # Input files wait in a queue; at most `max_running` batches run at once. A batch rejected because the
        # model's Batch queue is full (token_limit_exceeded) goes back into the queue and the limit is lowered.
        pend_path = self._path(stage, "pending.json")
        if os.path.exists(pend_path):
            st = json.load(open(pend_path))
            print(f"[{stage}] resuming: {len(st['running'])} running, {len(st['queued'])} queued", flush=True)
        else:
            st = {"running": {}, "queued": self._upload(stage, list(todo.items())), "max": max_running}
        save = lambda: json.dump(st, open(pend_path, "w"))
        hashes = {k: self._hash(b) for k, b in todo.items()}
        t0, last_print = time.time(), 0
        while st["running"] or st["queued"]:
            while st["queued"] and len(st["running"]) < st["max"]:
                fid = st["queued"].pop(0)
                st["running"][self._start(stage, fid)] = fid
            save()
            time.sleep(self.poll)
            for bid, fid in list(st["running"].items()):
                bt = self.client.batches.retrieve(bid)
                if bt.status not in ("completed", "expired", "cancelled", "failed"):
                    continue
                del st["running"][bid]
                codes = [e.code for e in (bt.errors.data if bt.errors and bt.errors.data else [])]
                if bt.status == "failed" and "token_limit_exceeded" in codes:
                    st["queued"].append(fid)
                    st["max"] = max(1, len(st["running"]))
                    print(f"[{stage}] batch {bid} rejected: Batch queue full; re-queued, now at most {st['max']} "
                          f"running", flush=True)
                    if not st["running"]:
                        time.sleep(120)
                    continue
                if bt.status == "failed":
                    print(f"[{stage}] batch {bid} failed: {codes or bt.errors}", flush=True)
                self._collect(stage, bt, hashes)
            save()
            if time.time() - last_print > 300:
                done = len(self.rows(stage))
                print(f"[{stage}] {(time.time() - t0) / 60:.0f} min: {len(st['running'])} running, "
                      f"{len(st['queued'])} queued, {done:,} results cached", flush=True)
                last_print = time.time()
        os.remove(pend_path)
        rows = self.rows(stage)
        failed = {k: b for k, b in todo.items() if k not in rows or "error" in rows[k]["r"]}
        if failed and retries:
            print(f"[{stage}] re-submitting {len(failed)} failed request(s)", flush=True)
            self._run_batch(stage, failed, retries - 1)
        print(f"[{stage}] done in {(time.time() - t0) / 60:.1f} min", flush=True)

    def _collect(self, stage, bt, hashes):
        new = []
        if bt.output_file_id:
            for line in self.client.files.content(bt.output_file_id).text.splitlines():
                o = json.loads(line)
                k = o["custom_id"]
                resp = (o.get("response") or {})
                if resp.get("status_code") == 200:
                    new.append({"key": k, "h": hashes.get(k, ""), "r": self._result(resp["body"], "batch")})
                else:
                    new.append({"key": k, "h": hashes.get(k, ""),
                                "r": {"error": json.dumps(resp.get("body") or o.get("error"))[:300], "in": 0, "out": 0,
                                      "tier": "batch"}})
        if bt.error_file_id:
            for line in self.client.files.content(bt.error_file_id).text.splitlines():
                o = json.loads(line)
                new.append({"key": o["custom_id"], "h": hashes.get(o["custom_id"], ""),
                            "r": {"error": json.dumps(o.get("error") or o.get("response"))[:300], "in": 0, "out": 0,
                                  "tier": "batch"}})
        self._save(stage, new)
        rc = bt.request_counts
        print(f"[{stage}] batch {bt.id} {bt.status}: {rc.completed:,} ok, {rc.failed:,} failed", flush=True)

    # ---- embeddings (synchronous; cached as .npy next to a hash of the inputs) -----------------------------
    def embed(self, name, texts, cap=8000):
        texts = [(t or " ")[:cap] for t in texts]
        h = hashlib.sha1("\x1f".join(texts).encode()).hexdigest()[:16]
        npy, meta = self._path(name, "npy"), self._path(name, "embed.json")
        if os.path.exists(npy) and os.path.exists(meta) and json.load(open(meta))["h"] == h:
            return np.load(npy)
        if self.mode == "replay":
            raise RuntimeError(f"embeddings '{name}' are not cached - run with SMASH_MODE=test or batch.")
        chunks, cur, size = [], [], 0
        for t in texts:
            if cur and (len(cur) >= 512 or size + len(t) > 400_000):
                chunks.append(cur); cur, size = [], 0
            cur.append(t); size += len(t)
        if cur:
            chunks.append(cur)
        def one(batch):
            for attempt in range(12):                    # rate limits: back off up to a minute per try
                try:
                    r = self.client.embeddings.create(model=EMBED_MODEL, input=batch)
                    return [d.embedding for d in r.data], r.usage.total_tokens
                except Exception:
                    if attempt == 11:
                        raise
                    time.sleep(min(60, 2 ** attempt) + random.random())
        with ThreadPoolExecutor(4) as ex:
            res = list(ex.map(one, chunks))
        v = np.array([e for vecs, _ in res for e in vecs], dtype=np.float32)
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        np.save(npy, v)
        json.dump({"h": h, "n": len(texts), "tokens": sum(t for _, t in res)}, open(meta, "w"))
        return v

    # ---- cost ledger ---------------------------------------------------------------------------------------
    def ledger(self, stages=None):
        """Token use and cost per stage from the cache (what this run actually paid)."""
        out = {}
        names = stages or sorted(f[:-6] for f in os.listdir(self.cache) if f.endswith(".jsonl"))
        for s in names:
            agg = {"calls": 0, "in": 0, "out": 0, "usd": 0.0, "batch_share": 0.0}
            nb = 0
            rows = self.rows(s).values()
            if rows and "r" not in next(iter(rows)):
                continue                                 # not an LLM stage (e.g. a retrieval cache)
            for r in rows:
                r = r["r"]
                tier = r.get("tier", "batch")
                agg["calls"] += 1; agg["in"] += r.get("in", 0); agg["out"] += r.get("out", 0)
                pi, po = PRICE[tier]
                agg["usd"] += (r.get("in", 0) * pi + r.get("out", 0) * po) / 1e6
                nb += tier == "batch"
            agg["batch_share"] = nb / max(agg["calls"], 1)
            out[s] = agg
        emb = sum(json.load(open(f"{self.cache}/{f}"))["tokens"] for f in os.listdir(self.cache) if f.endswith(".embed.json"))
        out["(embeddings)"] = {"calls": 0, "in": emb, "out": 0, "usd": emb * EMBED_PRICE / 1e6, "batch_share": 0.0}
        return out

    def print_ledger(self, stages=None):
        led = self.ledger(stages)
        print(f"{'stage':<28}{'calls':>9}{'input tok':>14}{'output tok':>13}{'USD':>9}{'via Batch':>11}")
        for s, a in led.items():
            print(f"{s:<28}{a['calls']:>9,}{a['in']:>14,}{a['out']:>13,}{a['usd']:>9.2f}{a['batch_share']:>11.0%}")
        tot = sum(a["usd"] for a in led.values())
        print(f"{'TOTAL':<28}{sum(a['calls'] for a in led.values()):>9,}"
              f"{sum(a['in'] for a in led.values()):>14,}{sum(a['out'] for a in led.values()):>13,}{tot:>9.2f}")
        return led
