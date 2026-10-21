"""Archive every LLM input and output of the scaled notebooks (11-18) in data/llm_io/ for later reports.

    python export_llm_io.py            # download raw Batch files + collect the request/response logs

What it writes:

* data/llm_io/raw_batches/<batch_id>/{input,output,errors}.jsonl.gz
      OpenAI's own copies of every Batch job: the exact request lines sent and the full response bodies
      (ids, timestamps, usage, finish reasons). Downloaded once; re-running skips batches already saved.
* data/llm_io/<cache>/<stage>.jsonl.gz
      One row per call: {"stage", "key", "h", "request": <full chat.completions body>, "response": <text,
      tool calls, tokens, tier>}. Copied from <cache>/io/, which smash_batch.py fills on every run (replaying a
      notebook with SMASH_MODE=replay completes it for calls made before logging existed; it costs nothing).
* data/llm_io/manifest.json
      Every batch (stage, notebook cache, dates, request counts, files) and every log (calls, tokens).

Embedding calls are not archived (their inputs are the corpus texts, their outputs vectors).
"""
import glob
import gzip
import json
import os
import shutil
import time

from openai import OpenAI

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = f"{ROOT}/data/llm_io"
CACHES = sorted({os.path.dirname(p) for p in glob.glob(f"{ROOT}/data/**/*.jsonl", recursive=True)
                 if "/llm_io/" not in p and "/io/" not in p and os.path.basename(os.path.dirname(p)).startswith(("cache", "cache_"))})


def rel(p):
    return os.path.relpath(p, f"{ROOT}/data")


def stage_keys():
    # (cache, stage) -> set of request keys, used to attribute older batches that carry no cache metadata.
    idx = {}
    for c in CACHES:
        for f in glob.glob(f"{c}/*.jsonl"):
            stage = os.path.basename(f)[:-6]
            keys = set()
            for line in open(f):
                try:
                    keys.add(json.loads(line)["key"])
                except Exception:
                    break
            idx[(c, stage)] = keys
    return idx


def save_gz(client, file_id, path):
    if not file_id or os.path.exists(path):
        return os.path.exists(path)
    data = client.files.content(file_id).content
    with gzip.open(path, "wb") as f:
        f.write(data)
    return True


def main():
    client = OpenAI()
    os.makedirs(f"{OUT}/raw_batches", exist_ok=True)
    man_path = f"{OUT}/manifest.json"
    manifest = json.load(open(man_path)) if os.path.exists(man_path) else {"batches": {}, "logs": {}}
    idx = stage_keys()
    for b in client.batches.list(limit=100):
        stage = (b.metadata or {}).get("stage")
        if not stage or b.status not in ("completed", "expired", "cancelled", "failed"):
            continue
        d = f"{OUT}/raw_batches/{b.id}"
        os.makedirs(d, exist_ok=True)
        save_gz(client, b.input_file_id, f"{d}/input.jsonl.gz")
        got_out = save_gz(client, b.output_file_id, f"{d}/output.jsonl.gz")
        save_gz(client, b.error_file_id, f"{d}/errors.jsonl.gz")
        cache = (b.metadata or {}).get("cache")
        if not cache and got_out:                      # older batch: find the notebook cache by its request keys
            with gzip.open(f"{d}/output.jsonl.gz", "rt") as f:
                first = json.loads(f.readline())["custom_id"]
            cache = next((c for (c, s), keys in idx.items() if s == stage and first in keys), None)
        rc = b.request_counts
        manifest["batches"][b.id] = {"stage": stage, "cache": rel(cache) if cache and os.path.isabs(cache) else cache,
                                     "status": b.status, "model": "gpt-6-luna",
                                     "created": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(b.created_at)),
                                     "completed": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(b.completed_at))
                                     if b.completed_at else None,
                                     "requests": rc.total, "ok": rc.completed, "failed": rc.failed,
                                     "files": sorted(os.listdir(d))}
    for c in CACHES:
        for f in glob.glob(f"{c}/io/*.jsonl.gz"):
            dst = f"{OUT}/{rel(c)}/{os.path.basename(f)}"
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(f, dst)
            n = tin = tout = 0
            with gzip.open(f, "rt") as g:
                for line in g:
                    r = json.loads(line)["response"]
                    n += 1; tin += r.get("in", 0); tout += r.get("out", 0)
            manifest["logs"][rel(dst)] = {"calls": n, "input_tokens": tin, "output_tokens": tout}
    json.dump(manifest, open(man_path, "w"), indent=1)
    nb = len(manifest["batches"]); nl = len(manifest["logs"])
    size = sum(os.path.getsize(os.path.join(dp, fn)) for dp, _, fs in os.walk(OUT) for fn in fs)
    print(f"{nb} batches archived, {nl} stage logs, {sum(v['calls'] for v in manifest['logs'].values()):,} logged calls, "
          f"{size / 1e6:.0f} MB in {OUT}")


if __name__ == "__main__":
    main()
