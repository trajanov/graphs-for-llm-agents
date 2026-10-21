"""Re-judge NB14 (sample) and NB16 (all) answers with a second judge model and compare with gpt-6-luna.

Request bodies come from the LLM I/O archive (data/llm_io/, available on request); only the model changes.
Results are cached in data/second_judge/ (resumable); the report is written to data/second_judge/second_judge_report.txt.
Usage: python second_judge.py [--score-only]      (needs OPENAI_API_KEY unless --score-only)
"""
import gzip, json, os, random, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np

EX = os.path.dirname(os.path.abspath(__file__))
OUT = f"{EX}/data/second_judge"
SCORE_ONLY = "--score-only" in sys.argv
JUDGE = "gpt-4.1-2025-04-14"
N_PER_DOMAIN = 200
sys.path.insert(0, EX)
from smash_batch import paired_boot  # noqa: E402

ARCH = f"{EX}/data/llm_io/benchmarks"
os.makedirs(OUT, exist_ok=True)


def load(p):
    return {r["key"]: r for r in (json.loads(l) for l in gzip.open(f"{ARCH}/{p}.jsonl.gz"))}


# ---- second-judge calls (cached) -------------------------------------------------------------------------
CACHE = f"{OUT}/judge2.jsonl"
done = {}
if os.path.exists(CACHE):
    for l in open(CACHE):
        r = json.loads(l); done[r["id"]] = r
usage = {"in": sum(r["in"] for r in done.values()), "out": sum(r["out"] for r in done.values())}


def call(item):
    from openai import OpenAI
    rid, body = item
    b = {k: v for k, v in body.items() if k not in ("reasoning_effort", "max_completion_tokens")}
    b["model"], b["max_tokens"] = JUDGE, body.get("max_completion_tokens", 2000)
    for _ in range(4):
        try:
            x = OpenAI(max_retries=3, timeout=300).chat.completions.create(**b)
            return {"id": rid, "text": x.choices[0].message.content or "", "in": x.usage.prompt_tokens,
                    "out": x.usage.completion_tokens}
        except Exception as e:  # noqa: BLE001
            err = str(e)
    return {"id": rid, "error": err, "text": "", "in": 0, "out": 0}


def judge2(reqs):
    todo = [(k, b) for k, b in reqs.items() if k not in done or "error" in done[k]]
    if todo and not SCORE_ONLY:
        print(f"sending {len(todo)} requests to {JUDGE}", flush=True)
        with ThreadPoolExecutor(16) as ex, open(CACHE, "a") as f:
            for r in ex.map(call, todo):
                f.write(json.dumps(r) + "\n"); f.flush(); done[r["id"]] = r
    return {k: done.get(k, {}).get("text", "") for k in reqs}


def js(t):
    try:
        return json.loads(t)
    except Exception:  # noqa: BLE001
        return None


def fmt(d):
    return f"{100 * d[0]:+.1f} [{100 * d[1]:+.1f}, {100 * d[2]:+.1f}]"


report = []
def out(s=""):
    print(s); report.append(s)


# ---- NB14: GraphRAG-Bench answer correctness ------------------------------------------------------------
BASE = f"{EX}/data/benchmarks/graphrag_bench"
TYPES = ["Fact Retrieval", "Complex Reasoning", "Contextual Summarize", "Creative Generation"]
out(f"NB14 GraphRAG-Bench: second judge {JUDGE} on {N_PER_DOMAIN} random questions per domain (seed 7)")
agree_all = []
for dom in ("medical", "novel"):
    qs = sorted(json.load(open(f"{BASE}/Datasets/Questions/{dom}_questions.json")), key=lambda q: q["id"])
    st = {k: (js(r["response"]["text"]) or {"statements": []})["statements"]
          for p in (f"{dom}_statements", f"{dom}_statements_hippo") for k, r in load(f"graphrag_bench/cache_luna/{p}").items()}
    jr = {**load(f"graphrag_bench/cache_luna/{dom}_judge"), **load(f"graphrag_bench/cache_luna/{dom}_judge_hippo")}
    A = np.load(f"{BASE}/cache_luna/{dom}_answer_vecs.npy"); AH = np.load(f"{BASE}/cache_luna/{dom}_answer_vecs_hippo.npy")
    G = np.load(f"{BASE}/cache_luna/{dom}_gold_vecs.npy")
    sim = {}
    for i, q in enumerate(qs):
        sim[f"vec|{q['id']}"] = float(A[2 * i] @ G[i]); sim[f"graph|{q['id']}"] = float(A[2 * i + 1] @ G[i])
        sim[f"hippo|{q['id']}"] = float(AH[i] @ G[i])

    def corr(m, q, c):
        gold, a = st.get(f"gold|{q['id']}", []), st.get(f"{m}|{q['id']}", [])
        if not a and not gold:
            f1 = 1.0
        elif not c:
            f1 = 0.0
        else:
            tp, fp, fn = len(c["TP"]), len(c["FP"]), len(c["FN"])
            p, r = tp / (tp + fp + 1e-10), tp / (tp + fn + 1e-10)
            f1 = 2 * p * r / (p + r + 1e-10)
        return 0.75 * f1 + 0.25 * (sim[f"{m}|{q['id']}"] + 1) / 2

    M = ("vec", "graph", "hippo")
    old = {(m, q["id"]): corr(m, q, js(jr[f"cls|{m}|{q['id']}"]["response"]["text"])) for q in qs for m in M}
    full = {m: 100 * np.mean([old[(m, q["id"])] for q in qs]) for m in M}
    out(f"  {dom}: full-set check with archived judge: vector {full['vec']:.1f}, graph {full['graph']:.1f}, hippo {full['hippo']:.1f}")
    sample = sorted(random.Random(7).sample(qs, N_PER_DOMAIN), key=lambda q: q["id"])
    new_txt = judge2({f"{dom}|cls|{m}|{q['id']}": jr[f"cls|{m}|{q['id']}"]["request"] for q in sample for m in M})
    new = {(m, q["id"]): corr(m, q, js(new_txt[f"{dom}|cls|{m}|{q['id']}"])) for q in sample for m in M}
    o = np.array([old[k] for k in new]); n = np.array([new[k] for k in new])
    agree_all += list(zip(o, n))
    out(f"  {dom}: per-answer correlation old vs new judge r = {np.corrcoef(o, n)[0, 1]:.2f}; "
        f"mean old {100 * o.mean():.1f}, new {100 * n.mean():.1f}")
    for t in ["ALL"] + TYPES:
        s = [q for q in sample if t == "ALL" or q["question_type"] == t]
        if t != "ALL" and len(s) < 30:
            continue
        row = [f"    {t:<22} n={len(s):>3}"]
        for b in ("graph", "hippo"):
            for lab, sc in (("luna", old), ("4.1", new)):
                d = paired_boot([sc[("vec", q["id"])] for q in s], [sc[(b, q["id"])] for q in s])
                row.append(f"{b}-vec {lab} {fmt(d)}")
        out(" | ".join(row))

# ---- NB16: BenchmarkQED assertions and pairwise ----------------------------------------------------------
QB = f"{EX}/data/benchmarks/benchmarkqed_podcast"
GQ = {q["question_text"] for q in json.load(open(f"{QB}/data_global_questions_assertions.json"))}
LQ = {q["question_text"] for q in json.load(open(f"{QB}/data_local_questions_assertions.json"))}
arch = {**load("benchmarkqed_podcast/cache/assertions"), **load("benchmarkqed_podcast/cache/local_assertions")}


def kind(req):
    c = req["messages"][0]["content"]
    q = c.split("Question: ", 1)[1].split("\n\nResponse:", 1)[0]
    return "global" if q in GQ else "local" if q in LQ else "?"


def rate(txt, req):
    n = req["messages"][0]["content"].split("Assertions:\n", 1)[1].count("\n") + 1
    p = (js(txt) or {"passed": []}).get("passed", [])
    return sum(1 for x in (p + [0] * n)[:n] if x) / n


new_txt = judge2({f"qed|{k}": r["request"] for k, r in arch.items()})
qidx = sorted({int(k.split("|")[1]) for k in arch})
kinds = {i: kind(arch[f"vector|{i}"]["request"]) for i in qidx}
out(f"\nNB16 BenchmarkQED: second judge {JUDGE} on all assertion checks; kinds {dict((k, list(kinds.values()).count(k)) for k in set(kinds.values()))}")
o_all, n_all = [], []
for kd in ("global", "local"):
    idx = [i for i in qidx if kinds[i] == kd]
    sc = {}
    for lab, src in (("luna", lambda k: arch[k]["response"]["text"]), ("4.1", lambda k: new_txt[f"qed|{k}"])):
        for m in ("vector", "graph", "local"):
            sc[(lab, m)] = [rate(src(f"{m}|{i}"), arch[f"{m}|{i}"]["request"]) for i in idx]
    for m in ("vector", "graph", "local"):
        o_all += sc[("luna", m)]; n_all += sc[("4.1", m)]
    out(f"  {kd} (n={len(idx)}): " + "; ".join(f"{m} luna {100 * np.mean(sc[('luna', m)]):.1f} / 4.1 {100 * np.mean(sc[('4.1', m)]):.1f}"
                                         for m in ("vector", "graph", "local")))
    for a, b in (("vector", "graph"), ("vector", "local"), ("graph", "local")):
        out(f"    {b}-{a}: luna {fmt(paired_boot(sc[('luna', a)], sc[('luna', b)]))} | 4.1 {fmt(paired_boot(sc[('4.1', a)], sc[('4.1', b)]))}")
out(f"  per-answer correlation of pass rates r = {np.corrcoef(o_all, n_all)[0, 1]:.2f}")

pw = load("benchmarkqed_podcast/cache/pairwise")
pnew = judge2({f"pw|{k}": r["request"] for k, r in pw.items()})
gidx = sorted({int(k.split("|")[1]) for k in pw})
for lab, src in (("luna", lambda k: pw[k]["response"]["text"]), ("4.1", lambda k: pnew[f"pw|{k}"])):
    res = []
    for crit in ("comprehensiveness", "diversity", "empowerment", "relevance"):
        s = []
        for qi in gidx:
            v = 0.0
            for order in ("gv", "vg"):
                x = (js(src(f"{order}|{qi}")) or {}).get(crit, "tie")
                v += 1.0 if x == ("1" if order == "gv" else "2") else 0.5 if x == "tie" else 0.0
            s.append(v / 2)
        bt = np.random.default_rng(7).choice(s, (5000, len(s))).mean(1)
        res.append(f"{crit} {100 * np.mean(s):.0f}% [{np.percentile(bt, 2.5) * 100:.0f}, {np.percentile(bt, 97.5) * 100:.0f}]")
    out(f"  pairwise graph win rate ({lab}): " + "; ".join(res))

errs = sum(1 for r in done.values() if "error" in r)
tin = sum(r["in"] for r in done.values()); tout = sum(r["out"] for r in done.values())
out(f"\n{JUDGE}: {len(done)} calls, {errs} errors, {tin:,} input / {tout:,} output tokens "
    f"(~${tin * 2e-6 + tout * 8e-6:.2f} at $2/$8 per 1M)")
open(f"{OUT}/second_judge_report.txt", "w").write("\n".join(report) + "\n")
