# SMASH Workshop — Hands-On Notebook Examples

Jupyter notebooks, each testing one claim of **`SMASH-LLM-Agents-and-Knowledge-Graphs.pptx`** on real
data. Every notebook compares a graph-based method with a **strong vector-RAG baseline** (the comparison the lecture
says matters), computes its metrics against gold answers instead of asserting them, and ends with a
**RESULTS SUMMARY** cell plus the lecture message it supports. All use OpenAI `gpt-4o-mini` (temperature 0, seed 7)
and `text-embedding-3-small`; each runs in about 0.5–1.5 minutes.

A companion deck with the results, **`../SMASH-Examples-Results.pptx`** (built by
`../deck/build_examples_results.py`), shows how each result supports the lecture.

## Notebooks and headline results (saved run)

| Notebook | Lecture slides | What it tests | Headline result |
| :--- | :--- | :--- | :--- |
| [`01_vector_rag_vs_graph_rag`](01_vector_rag_vs_graph_rag.ipynb) | 32, 36, 38, 43 | Vector RAG vs graph agent on the Aura helpdesk graph, 22 questions in three families | Lookup: vector 5/5, graph 4/5 · verified fix: 7/11 vs **11/11** · relational: 1/6 vs **5/6** |
| [`02_react_agent_graph_traversal`](02_react_agent_graph_traversal.ipynb) | 20, 40–44, 61 | ReAct agent with templated read-only tools over a ServiceNow incident graph (893 nodes) built from the warehouse | Multi-hop accuracy **80%** vs 10% for flat top-10 RAG, at 6.5× the tokens; write attempts refused |
| [`03_agents_building_graphs_and_kb`](03_agents_building_graphs_and_kb.ipynb) | 45–50 | LLM graph construction over PlanetCare tickets: schema-light vs schema-first, an entity-resolution cascade, validation, provenance | 62 → 45 modules using 45 LLM calls instead of 1,891 · 19 → 6 pattern labels · shape-valid 100% vs source-supported 93% |
| [`04_temporal_memory_and_stale_runbooks`](04_temporal_memory_and_stale_runbooks.ipynb) | 38, 49, 52–55 | Bi-temporal runbook graph (56 questions) incl. superseded and conflicting runbooks; episodic → semantic agent memory | Stale questions: 62% → **88%** correct · conflicts flagged 33% → **100%** · superseded runbook in context 88% → 0% · answerable questions tie (96%) |
| [`05_guardrails_and_graph_poisoning`](05_guardrails_and_graph_poisoning.ipynb) | 8, 28, 61, 62 | Poisoned comments vs provenance-verified retrieval; a `.dot` workflow graph enforced on a tool-calling agent | Malicious instruction repeated: 90% → **0%** (0/12 real fixes rejected) · out-of-order actions: 19 → **0** |
| [`06_graphrag_global_sensemaking`](06_graphrag_global_sensemaking.ipynb) *(new)* | 33, 34, 36, 38 | GraphRAG-style community reports + map-reduce vs top-k RAG on global questions over 183 tickets | Comprehensiveness win rate **100%**, 10 vs 5 hospitals covered · index price 29 calls / 44k tokens, ~10× tokens per query |
| [`07_ontology_checked_graph_queries`](07_ontology_checked_graph_queries.ipynb) *(new)* | 27, 43, 44, 50, 59–61 | Text-to-SPARQL over an RDF version of the helpdesk graph, with a deterministic ontology checker, ≤3 repairs, then "unknown", and a read-only gate | Accuracy 20% → **67%**, 7% "unknown", 0 writes executed; 4 queries passed every check but were still wrong |

### Scaled runs on standard benchmarks (cached; `RUN_LIVE = False` replays in seconds)

| Notebook | Lecture slides | Benchmark (sample) | Headline result (95% CI) |
| :--- | :--- | :--- | :--- |
| [`08_scaled_metaqa_multihop`](08_scaled_metaqa_multihop.ipynb) | 32, 36, 38, 41 | MetaQA test, 100 questions per hop; KG of 43K entities / 134K triples | Hits@1 vector → graph: 1-hop 91% → 99% · 2-hop **39% → 97%** · 3-hop **36% → 80%**, at 1.7–6.6× the tokens |
| [`09_scaled_graphrag_bench`](09_scaled_graphrag_bench.ipynb) | 33–38 | GraphRAG-Bench medical corpus, 180 questions in 4 types | **No resolvable difference** on any type (e.g. reasoning 72.5 vs 73.0); vector top-8 already found 93–99% of the gold evidence for fact, reasoning and summary questions (64% for creative). Slide 36's gaps did not reproduce |
| [`10_scaled_longmemeval_memory`](10_scaled_longmemeval_memory.ipynb) | 52–56 | LongMemEval-S, 108 questions, 13.2M tokens of chat history | Overall 77% → **83%**; multi-session 69% → 88%, preference 19% → 50%, assistant recall 94% → 88%, temporal tie; graph beats full context (89% vs 75%, n = 28) with ~2% of the tokens |

### Confidence runs on larger and harder benchmarks (`gpt-6-luna`, no reasoning, OpenAI Batch API)

Notebooks 11-18 re-test the claims of 01-10 on public benchmarks large enough for tight 95% intervals, with strong
baselines. All calls go through `smash_batch.py` (temperature 0, seed 7, results cached). `SMASH_MODE=replay` (the
default) re-runs the saved results in seconds without the API. `SMASH_MODE=test` runs a small live sample. `SMASH_MODE=batch`
recomputes anything missing through the Batch API.

| Notebook | Re-tests | Benchmark (n) | Headline result (95% CI) | Cost |
| :--- | :--- | :--- | :--- | ---: |
| [`11_scaled_musique_2wiki_multihop`](11_scaled_musique_2wiki_multihop.ipynb) | 08 | MuSiQue + 2WikiMultiHopQA, 2 × 1,000; graph extracted from text | F1 graph − vector: MuSiQue **+4.7** [+2.1, +7.4], 2Wiki **+11.7** [+8.6, +14.8]; the gain shrinks with hops (2-hop +7.9, 4-hop −1.7) | $2.52 |
| [`12_scaled_hoh_outdated_knowledge`](12_scaled_hoh_outdated_knowledge.ipynb) | 04 | HoH outdated Wikipedia facts, 500 | vector 63% → temporal graph 90% (+27 [+23, +31]), but vector + dates also 90% (graph − dated vector −0.2 [−2.4, +2.0]) | $0.18 |
| [`13_scaled_injecagent_prompt_injection`](13_scaled_injecagent_prompt_injection.ipynb) | 05 | InjecAgent 1,054 attacks × 3 strengths (incl. AgentDojo template) | attack success: no defence 0.4% (13 of 3,162), prompt rule 0.03%, enforced plan graph **0%**; the plan blocks 0.2% of legitimate tasks | $0.71 |
| [`14_scaled_graphrag_bench_both_domains`](14_scaled_graphrag_bench_both_domains.ipynb) | 09 | GraphRAG-Bench, all 4,072 questions, medical + novel | correctness graph − vector: medical **−1.5** [−2.5, −0.4], novel −0.7 [−1.9, +0.5]; only novel complex reasoning favours the graph (+2.8 [+1.3, +4.4]); fact lookup favours vector in both domains | $3.34 |
| [`15_scaled_memory_longmemeval_locomo`](15_scaled_memory_longmemeval_locomo.ipynb) | 10 | LongMemEval-S 500 + LoCoMo 1,540; full context on every question | LongMemEval: graph 79% vs vector 75% vs full 71%. LoCoMo: full 79% vs graph 73% vs vector 67%. Assistant recall: graph 52% vs vector 91% | $12.12 |
| [`16_scaled_benchmarkqed_global_sensemaking`](16_scaled_benchmarkqed_global_sensemaking.ipynb) | 06 | BenchmarkQED podcast corpus, 50 global + 50 local questions | global questions: assertions covered 57% → **77%** (+19.8 [+14.9, +24.6]), judge prefers GraphRAG 90-92% on 3 of 4 criteria; local control: vector 100% vs graph 70% | $4.7* |
| [`17_scaled_spider4ssc_ontology_checked_sparql`](17_scaled_spider4ssc_ontology_checked_sparql.ipynb) | 07 | Spider4SSC text-to-SPARQL, 563 questions / 19 graphs | one-shot 17%, error/empty retry 22%, ontology checker **84%**; the gain is almost all vocabulary (prefix) errors | $0.10 |
| [`18_scaled_aura_template_questions`](18_scaled_aura_template_questions.ipynb) | 01 | Aura helpdesk, 156 template questions | lookup: vector 97% vs graph 47%; verified fix 73% vs **89%**; relational 46% vs **98%** | $0.05 |

\* includes one re-run after a reproducibility fix.

**Every LLM input and output of notebooks 11-18 is archived** in `data/llm_io/` for later analysis (`python export_llm_io.py`
refreshes it):
- `raw_batches/<batch_id>/{input,output}.jsonl.gz` hold OpenAI's own Batch files: exact requests and full response bodies.
- `<cache>/<stage>.jsonl.gz` holds one row per call with the full request (messages, model, settings) and the response
  (text, tool calls, tokens).
- `manifest.json` maps every batch to its notebook and stage and gives call and token counts.

Embedding calls and the small test-mode runs are not archived. Notebooks 01-10 cached outputs only.

Benchmark data and caches live in `data/benchmarks/` (≈580 MB; MetaQA via the `camazlucas/MetaQA` HF mirror,
GraphRAG-Bench MIT, LongMemEval MIT). Re-running live (`RUN_LIVE = True`) re-calls the API: notebook 10's full
run used ≈20M LLM tokens.

LLM outputs vary slightly between runs even at temperature 0 (typically ±1 question per benchmark). Notebooks 01–07
(small hand-built question sets) illustrate the lecture's claims; notebooks 11-18 re-test them at scale.

## Datasets (`data/`)

Except for the generated PlanetCare tickets, the data is not part of the repository. `python download_data.py` fetches every dataset from its original
publisher into `data/` (about 1.5 GB). `python download_data.py <name> ...` fetches only some datasets, and
`python download_data.py --list` shows the datasets, the notebooks that use them and their licences. Existing
files are skipped.

| Name | Path | Notebooks | Source | Licence |
| :--- | :--- | :--- | :--- | :--- |
| `aura` | `aura_helpdesk.json` | 01, 05, 07, 18 | [AlexisBalayre/AuraHelpdeskGraph](https://github.com/AlexisBalayre/AuraHelpdeskGraph): the sample CSVs, with relationships rebuilt from its Neo4j load script | none stated |
| — | `planetcare_*` | 03, 06 | **Generated (synthetic) dataset** created by the author for teaching, included in this repository; see [`data/PLANETCARE.md`](data/PLANETCARE.md) | — |
| `runbooks` | `runbooks/` | 04 | [AriaAICompany/incident-rag-runbooks](https://huggingface.co/datasets/AriaAICompany/incident-rag-runbooks) | CC BY 4.0 |
| `telecom` | `telecom_workflow/` | 05 | [τ²-bench](https://github.com/sierra-research/tau2-bench) telecom domain | MIT |
| `incidents` | `servicenow_incidents.duckdb` | 02 | [UCI incident management event log](https://archive.ics.uci.edu/dataset/498/incident+management+process+enriched+event+log): its first 119,998 rows, 20,769 incidents | CC BY 4.0 |
| `metaqa` | `benchmarks/metaqa/` | 08, 19 | [MetaQA](https://github.com/yuyuz/MetaQA) (Hugging Face copy `camazlucas/MetaQA`) | Creative Commons |
| `wikimovies` | `benchmarks/metaqa/wikimovies_text/` | 19 | WikiMovies article text from the MovieQA release (Miller et al., 2016), via the Internet Archive | CC BY 3.0 |
| `musique_2wiki` | `benchmarks/musique_2wiki/` | 11 | [HippoRAG 2 release](https://huggingface.co/datasets/osunlp/HippoRAG_2) of MuSiQue and 2WikiMultiHopQA | CC BY 4.0 / Apache-2.0 |
| `graphrag_bench` | `benchmarks/graphrag_bench/` | 09, 14 | [GraphRAG-Bench](https://huggingface.co/datasets/GraphRAG-Bench/GraphRAG-Bench) | MIT |
| `hoh` | `benchmarks/hoh/` | 12 | [HoH-QAs](https://huggingface.co/datasets/russwest404/HoH-QAs) | Apache-2.0 |
| `injecagent` | `benchmarks/injecagent/` | 13 | [InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent) | MIT |
| `longmemeval` | `benchmarks/longmemeval/` | 10, 15 | [LongMemEval-S, cleaned](https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned) | MIT |
| `locomo` | `benchmarks/locomo/` | 15 | [LoCoMo](https://github.com/snap-research/locomo) | **CC BY-NC 4.0** |
| `benchmarkqed` | `benchmarks/benchmarkqed_podcast/` | 16 | [BenchmarkQED](https://github.com/microsoft/benchmark-qed) podcast transcripts and questions | **Microsoft Research License** (non-commercial) |
| `spider4ssc` | `benchmarks/spider4ssc/` | 17 | [Spider4SSC](https://data.mendeley.com/datasets/4dnvv92trn), Mendeley Data v2 | CC BY 4.0 (Spider: CC BY-SA 4.0) |

Notebooks 08-19 also keep their LLM responses and embeddings in cache folders next to the data
(`cache*/`, `data/cache_18/`). These are not in the repository. Without them, run a notebook with `SMASH_MODE=test`
for a small live sample, or with `SMASH_MODE=batch` to recompute everything (needs `OPENAI_API_KEY`).

## Quick start

The notebooks read `OPENAI_API_KEY` from the environment and use the course venv. That venv has a Jupyter kernel
registered as **`smash-workshop-venv`**.

```bash
# Course venv (openai, networkx, duckdb, pydantic, numpy, scikit-learn, pydot, rdflib, nbclient):
"/Users/dt/cc/AI and Data Utilization - WS/.venv/bin/python" -V
"/Users/dt/cc/AI and Data Utilization - WS/.venv/bin/jupyter" kernelspec list
```

Open a notebook, select the `smash-workshop-venv` kernel, and run all cells top to bottom. Every notebook is
self-contained.
