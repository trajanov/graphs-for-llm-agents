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

| Path | Description |
| :--- | :--- |
| `aura_helpdesk.json` | Synthetic IT-helpdesk knowledge graph for the 3DS "Aura" support chatbot (source: `AlexisBalayre/AuraHelpdeskGraph`): 23 tickets, 57 comments, 10 KB articles, 7 statuses, 10 users, 246 Cypher-derived relationships. `cat_010` is referenced but not defined in the source. Used by notebooks 1, 5 and 7. |
| `planetcare_tickets.json` / `planetcare_kb.json` / `planetcare_wiki/` | 183 PlanetCare hospital EHR support tickets across 10 hospitals, 3 existing KB articles, and the team's wiki pages. Used by notebooks 3 and 6. |
| `runbooks/documents.jsonl` / `runbooks/questions.jsonl` | 58 SOC incident-response runbooks (29 English + 29 Farsi) with version and supersession metadata, plus a 100-question benchmark including `ransomware-stale` and `cloud-owner-conflict` families. Used by notebook 4. |
| `telecom_workflow/` | τ²-bench telecom-support Graphviz flowcharts and matching customer scenarios. Used by notebook 5. |
| `/Users/dt/cc/AI and Data Utilization - WS/data/course.duckdb` (`incidents` schema) | The UCI ServiceNow incident-management event log: 119,998 events and 20,769 incidents. Opened read-only by notebook 2. |
| `benchmarks/musique_2wiki/` | MuSiQue and 2WikiMultiHopQA, 1,000 dev questions each with their passage pools (HippoRAG 2 release, `osunlp/HippoRAG_2`). Notebook 11. ≈2.6 GB, mostly cached embedding matrices. |
| `benchmarks/hoh/` | HoH-QAs (`russwest404/HoH-QAs`, Apache-2.0): 111,972 questions with current and outdated Wikipedia evidence. Notebook 12. |
| `benchmarks/injecagent/` | InjecAgent test cases, tool specs and simulated attacker responses (`uiuc-kang-lab/InjecAgent`, MIT). Notebook 13. |
| `benchmarks/graphrag_bench/` | GraphRAG-Bench medical + novel corpora and questions (MIT). Notebooks 9 and 14. |
| `benchmarks/longmemeval/`, `benchmarks/locomo/` | LongMemEval-S cleaned (MIT); LoCoMo 10 conversations (`snap-research/locomo`, **CC BY-NC 4.0**). Notebooks 10 and 15. |
| `benchmarks/benchmarkqed_podcast/` | "Behind the Tech" transcripts with BenchmarkQED global/local questions and assertions (`microsoft/benchmark-qed`, **Microsoft Research License: non-commercial research use**). Notebook 16. |
| `benchmarks/spider4ssc/` | Spider4SSC dev split with RDF graphs and schemas (Mendeley Data `4dnvv92trn`, Apache-2.0; Spider CC BY-SA). Notebook 17. |
| `llm_io/` | Archive of every LLM request and response of notebooks 11-18 (see above). |

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
