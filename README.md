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

## Data

The only data stored in this repository is the PlanetCare tickets used by notebooks 03 and 06. This is a
generated (synthetic) dataset; see [`examples/data/PLANETCARE.md`](examples/data/PLANETCARE.md). To fetch every other
dataset from its original publisher into `examples/data/`
(about 1.5 GB), run:

```bash
cd examples
python download_data.py            # all datasets
python download_data.py --list     # datasets, notebooks and licences
```

[`examples/README.md`](examples/README.md#datasets-data) lists the sources and licences. Two benchmarks allow
non-commercial research only: LoCoMo (CC BY-NC 4.0) and BenchmarkQED (Microsoft Research License).

The response caches and the archive of LLM requests and responses (about 5 GB) are not in the repository either;
they are available from the author on request. Without them a notebook shows its saved outputs, and you can re-run
it as follows (both need `OPENAI_API_KEY`):

- `SMASH_MODE=test` runs a small live sample;
- `SMASH_MODE=batch` recomputes everything through the Batch API.
