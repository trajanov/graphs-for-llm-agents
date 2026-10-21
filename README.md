# Where Do Knowledge Graphs Help LLM Agents?

Notebooks and report for the 2nd SMASHING Workshop lecture *LLM-Based Agentic Systems and Knowledge Graphs*
(October 2026). Nineteen experiments compare graph-based methods with strong vector-retrieval and other cheap
baselines: multi-hop questions, corpus-wide sensemaking, time-aware knowledge, agent memory, ontology-checked query
generation and guardrails.

| Path | Contents |
| :--- | :--- |
| [`paper/graphs-for-llm-agents-evaluation.pdf`](paper/graphs-for-llm-agents-evaluation.pdf) | The report (LaTeX source and `references.bib` alongside) |
| [`examples/`](examples/) | Notebooks 01–19 with their saved outputs; see [`examples/README.md`](examples/README.md) |
| `examples/smash_batch.py` | Shared OpenAI helper for notebooks 11–19 (Batch API, response cache, statistics) |
| `examples/export_llm_io.py` | Archives every LLM request and response of the scaled runs |

- Notebooks 01–10 use `gpt-4o-mini`.
- Notebooks 11–19 are the confidence runs, using `gpt-6-luna` without reasoning through the OpenAI Batch API.

## What is not in this repository

The repository holds code, notebooks and the report only. It leaves out three things, about 6 GB in total:

- the benchmark data;
- the response caches that let a notebook replay without API calls;
- the archive of LLM requests and responses.

Some of the benchmarks are licensed for non-commercial research only, e.g. LoCoMo (CC BY-NC 4.0) and BenchmarkQED
(Microsoft Research License).

All benchmarks are public: MetaQA, WikiMovies, MuSiQue, 2WikiMultiHopQA, HoH, InjecAgent, GraphRAG-Bench,
LongMemEval, LoCoMo, BenchmarkQED and Spider4SSC. The notebooks expect them under `examples/data/benchmarks/<name>/`.
The caches and the archive are available from the author on request.

To re-run a notebook without the cache:

- `SMASH_MODE=test` runs a small sample live.
- `SMASH_MODE=batch` recomputes everything through the Batch API.
- Both need `OPENAI_API_KEY`.
