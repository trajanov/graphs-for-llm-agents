# Where Do Knowledge Graphs Help LLM Agents?

Notebooks for the 2nd SMASHING Workshop lecture *LLM-Based Agentic Systems and Knowledge Graphs*
(October 2026). Thirty notebooks compare graph-based methods with strong vector-retrieval and other cheap baselines:
multi-hop questions, corpus-wide sensemaking, time-aware knowledge, agent memory, ontology-checked query generation,
guardrails and attributed answers, and, with frozen protocols, the nine tasks added in the second version of the
report plus an ontology generated from metadata. Each notebook is named after the task it measures (for example
`1.2b_metaqa_curated_vs_extracted_graph.ipynb`, formerly notebook 19); [`examples/README.md`](examples/README.md)
lists all of them with their old numbers.

| Path | Contents |
| :--- | :--- |
| [`examples/`](examples/) | The 30 notebooks with their saved outputs, in five folders by task group plus `archive/`; see [`examples/README.md`](examples/README.md) |
| `examples/smash_batch.py` | Shared OpenAI helper for the scaled notebooks (Batch API, response cache, statistics) |
| `examples/export_llm_io.py` | Archives every LLM request and response of the scaled runs |
| `examples/second_judge.py` | Re-scores notebooks 1.4b and 1.3b with a second judge model (`gpt-4.1`) from that archive |

- The seven teaching notebooks (`*_teaching.ipynb`) and the archived early runs A1–A3 use `gpt-4o-mini`.
- The confidence runs of the first version (1.1b, 1.2b, 1.3b, 1.4a, 1.4b, 1.5, 2.1b, 2.2, 3.1b, 3.4) use `gpt-6-luna`
  without reasoning through the OpenAI Batch API.
- The new experiments (1.6, 2.3, 3.1c, 3.5, 3.6, 4.1–4.5) test the tasks added in the second version of the report (grounding, environment models, access
  control, audit trails, planning, tool selection, recovery, outcome verification, shared graphs between agents, and an
  ontology generated from database metadata). Each starts with a frozen protocol, and its saved outputs are those of
  its confidence run (finished November 2026).

## Data

The only data stored in this repository is the PlanetCare tickets used by notebooks 5.1 and 1.3a. This is a
generated (synthetic) dataset; see [`examples/data/PLANETCARE.md`](examples/data/PLANETCARE.md). To fetch every other
dataset of the first-version notebooks from its original publisher into `examples/data/`
(about 1.5 GB), run:

```bash
cd examples
python download_data.py            # all datasets
python download_data.py --list     # datasets, notebooks and licences
```

[`examples/README.md`](examples/README.md#datasets-data) lists the sources and licences. The new experiments also use ALFWorld, TaskBench,
ToolBench and the full τ²-bench checkout, which `download_data.py` does not fetch yet; the same table lists them. Two benchmarks allow
non-commercial research only: LoCoMo (CC BY-NC 4.0) and BenchmarkQED (Microsoft Research License).

The response caches and the archive of LLM requests and responses (about 5 GB) are not in the repository either;
they are available from the author on request. Without them a notebook shows its saved outputs, and you can re-run
it as follows (both need `OPENAI_API_KEY`):

- `SMASH_MODE=test` runs a small live sample;
- `SMASH_MODE=batch` recomputes everything through the Batch API.

## Licence

- Code (notebooks and scripts): [Apache 2.0](LICENSE); keep the [`NOTICE`](NOTICE) file with its attribution
  when you redistribute the code or a derivative.
- The report and the PlanetCare data set: [CC BY 4.0](LICENSE-CC-BY-4.0.md).
- Data sets fetched by `download_data.py` keep their publishers' licences.

Both licences allow reuse, including commercial use, and require credit to the author. To cite this work:

> Dimitar Trajanov. *Where Do Knowledge Graphs Help LLM Agents? Nineteen Experiments, from Hand-Built Examples to
> Benchmarks with Thousands of Questions.* Companion report to the 2nd SMASHING Workshop, October 2026.
> https://github.com/trajanov/graphs-for-llm-agents
