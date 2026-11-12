t

# SMASH Workshop — Hands-On Notebook Examples

Jupyter notebooks, each testing one claim of **`SMASH-LLM-Agents-and-Knowledge-Graphs.pptx`** on real
data. Every notebook compares a graph-based method with a **strong vector-RAG baseline** (the comparison the lecture
says matters), computes its metrics against gold answers instead of asserting them, and ends with a
**RESULTS SUMMARY** cell plus the lecture message it supports. All use OpenAI `gpt-4o-mini` (temperature 0, seed 7)
and `text-embedding-3-small`; each runs in about 0.5–1.5 minutes.

A companion deck with the results, **`../SMASH-Examples-Results.pptx`** (built by
`../deck/build_examples_results.py`), shows how each result supports the lecture.

## Folder layout and names

The notebooks are grouped by the five task groups of the paper (see `TASKS.md`) and named after the task they
measure: `<task><letter>_<what it tests>.ipynb`. The letter orders several notebooks on one task, and `_teaching`
marks the small hand-built examples. A notebook that serves two tasks is named after its main one (3.2 also covers
3.3; 5.1 also covers 5.2; 1.2b also measures 5.1). The three early runs that later notebooks repeat in full are in
`archive/` (A1–A3). The old numbers (01–30) are those of the first version of the paper; `NOTEBOOK-REVIEW.md` explains
the change.

| Folder | Notebook | Old number |
| :--- | :--- | :---: |
| `1_retrieval_and_reasoning/` | [`1.1a_helpdesk_graph_agent_vs_vector_teaching`](1_retrieval_and_reasoning/1.1a_helpdesk_graph_agent_vs_vector_teaching.ipynb) | 01 |
| `1_retrieval_and_reasoning/` | [`1.1b_helpdesk_aggregates_graph_vs_vector_vs_sql`](1_retrieval_and_reasoning/1.1b_helpdesk_aggregates_graph_vs_vector_vs_sql.ipynb) | 18 |
| `1_retrieval_and_reasoning/` | [`1.2a_incident_graph_react_traversal_teaching`](1_retrieval_and_reasoning/1.2a_incident_graph_react_traversal_teaching.ipynb) | 02 |
| `1_retrieval_and_reasoning/` | [`1.2b_metaqa_curated_vs_extracted_graph`](1_retrieval_and_reasoning/1.2b_metaqa_curated_vs_extracted_graph.ipynb) | 19 |
| `1_retrieval_and_reasoning/` | [`1.3a_tickets_graphrag_global_summaries_teaching`](1_retrieval_and_reasoning/1.3a_tickets_graphrag_global_summaries_teaching.ipynb) | 06 |
| `1_retrieval_and_reasoning/` | [`1.3b_podcasts_graphrag_global_vs_mapreduce`](1_retrieval_and_reasoning/1.3b_podcasts_graphrag_global_vs_mapreduce.ipynb) | 16 |
| `1_retrieval_and_reasoning/` | [`1.4a_multihop_text_graph_ranking_musique_2wiki`](1_retrieval_and_reasoning/1.4a_multihop_text_graph_ranking_musique_2wiki.ipynb) | 11 |
| `1_retrieval_and_reasoning/` | [`1.4b_graphrag_bench_graph_ranking`](1_retrieval_and_reasoning/1.4b_graphrag_bench_graph_ranking.ipynb) | 14 |
| `1_retrieval_and_reasoning/` | [`1.5_citation_accuracy_graph_vs_vector`](1_retrieval_and_reasoning/1.5_citation_accuracy_graph_vs_vector.ipynb) | 20 |
| `1_retrieval_and_reasoning/` | [`1.6_entity_grounding_linking_cascade`](1_retrieval_and_reasoning/1.6_entity_grounding_linking_cascade.ipynb) | 21 |
| `2_memory_and_state/` | [`2.1a_runbooks_temporal_graph_teaching`](2_memory_and_state/2.1a_runbooks_temporal_graph_teaching.ipynb) | 04 |
| `2_memory_and_state/` | [`2.1b_hoh_outdated_facts_temporal_graph_vs_dates`](2_memory_and_state/2.1b_hoh_outdated_facts_temporal_graph_vs_dates.ipynb) | 12 |
| `2_memory_and_state/` | [`2.2_conversational_memory_longmemeval_locomo`](2_memory_and_state/2.2_conversational_memory_longmemeval_locomo.ipynb) | 15 |
| `2_memory_and_state/` | [`2.3_alfworld_world_graph_vs_history`](2_memory_and_state/2.3_alfworld_world_graph_vs_history.ipynb) | 22 |
| `3_governance_and_control/` | [`3.1a_aura_sparql_ontology_check_teaching`](3_governance_and_control/3.1a_aura_sparql_ontology_check_teaching.ipynb) | 07 |
| `3_governance_and_control/` | [`3.1b_spider4ssc_sparql_ontology_check`](3_governance_and_control/3.1b_spider4ssc_sparql_ontology_check.ipynb) | 17 |
| `3_governance_and_control/` | [`3.1c_spider4ssc_sql_generated_ontology`](3_governance_and_control/3.1c_spider4ssc_sql_generated_ontology.ipynb) | 30 |
| `3_governance_and_control/` | [`3.2_provenance_and_workflow_guardrails_teaching`](3_governance_and_control/3.2_provenance_and_workflow_guardrails_teaching.ipynb) | 05 |
| `3_governance_and_control/` | [`3.4_injecagent_plan_graph_gate`](3_governance_and_control/3.4_injecagent_plan_graph_gate.ipynb) | 13 |
| `3_governance_and_control/` | [`3.5_access_control_permission_graph`](3_governance_and_control/3.5_access_control_permission_graph.ipynb) | 23 |
| `3_governance_and_control/` | [`3.6_audit_trail_provenance_graph`](3_governance_and_control/3.6_audit_trail_provenance_graph.ipynb) | 24 |
| `4_execution_and_coordination/` | [`4.1_dag_planner_vs_react`](4_execution_and_coordination/4.1_dag_planner_vs_react.ipynb) | 25 |
| `4_execution_and_coordination/` | [`4.2_tool_selection_tool_graph`](4_execution_and_coordination/4.2_tool_selection_tool_graph.ipynb) | 26 |
| `4_execution_and_coordination/` | [`4.3_tau2_crash_recovery_checkpoint_graph`](4_execution_and_coordination/4.3_tau2_crash_recovery_checkpoint_graph.ipynb) | 27 |
| `4_execution_and_coordination/` | [`4.4_tau2_outcome_verification_graph_check`](4_execution_and_coordination/4.4_tau2_outcome_verification_graph_check.ipynb) | 28 |
| `4_execution_and_coordination/` | [`4.5_shared_claim_graph_between_agents`](4_execution_and_coordination/4.5_shared_claim_graph_between_agents.ipynb) | 29 |
| `5_graph_construction/` | [`5.1_tickets_build_graph_extraction_resolution_teaching`](5_graph_construction/5.1_tickets_build_graph_extraction_resolution_teaching.ipynb) | 03 |
| `archive/` | [`A1_metaqa_multihop_early_run`](archive/A1_metaqa_multihop_early_run.ipynb) | 08 |
| `archive/` | [`A2_graphrag_bench_medical_early_run`](archive/A2_graphrag_bench_medical_early_run.ipynb) | 09 |
| `archive/` | [`A3_longmemeval_early_run`](archive/A3_longmemeval_early_run.ipynb) | 10 |

`data/`, `smash_batch.py`, the helper scripts and the `.venv-*` environments stay in `examples/`. Every path inside the
notebooks is relative to `examples/`; the first code cell of each notebook (tagged `path-setup`) changes to `examples/`
when the notebook is opened from its own folder, so a notebook runs the same from either place.

## Notebooks and headline results (saved run)

| Notebook                                                                                  | Lecture slides         | What it tests                                                                                                                                      | Headline result                                                                                                                                                       |
| :---------------------------------------------------------------------------------------- | :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`1.1a_helpdesk_graph_agent_vs_vector_teaching`](1_retrieval_and_reasoning/1.1a_helpdesk_graph_agent_vs_vector_teaching.ipynb)                         | 32, 36, 38, 43         | Vector RAG vs graph agent on the Aura helpdesk graph, 22 questions in three families                                                               | Lookup: vector 5/5, graph 4/5 · verified fix: 7/11 vs **11/11** · relational: 1/6 vs **5/6**                                                            |
| [`1.2a_incident_graph_react_traversal_teaching`](1_retrieval_and_reasoning/1.2a_incident_graph_react_traversal_teaching.ipynb)                 | 20, 40–44, 61         | ReAct agent with templated read-only tools over a ServiceNow incident graph (893 nodes) built from the warehouse                                   | Multi-hop accuracy **80%** vs 10% for flat top-10 RAG, at 6.5× the tokens; write attempts refused                                                              |
| [`5.1_tickets_build_graph_extraction_resolution_teaching`](5_graph_construction/5.1_tickets_build_graph_extraction_resolution_teaching.ipynb)             | 45–50                 | LLM graph construction over PlanetCare tickets: schema-light vs schema-first, an entity-resolution cascade, validation, provenance                 | 62 → 45 modules using 45 LLM calls instead of 1,891 · 19 → 6 pattern labels · shape-valid 100% vs source-supported 93%                                            |
| [`2.1a_runbooks_temporal_graph_teaching`](2_memory_and_state/2.1a_runbooks_temporal_graph_teaching.ipynb)   | 38, 49, 52–55         | Bi-temporal runbook graph (56 questions) incl. superseded and conflicting runbooks; episodic → semantic agent memory                              | Stale questions: 62% → **88%** correct · conflicts flagged 33% → **100%** · superseded runbook in context 88% → 0% · answerable questions tie (96%) |
| [`3.2_provenance_and_workflow_guardrails_teaching`](3_governance_and_control/3.2_provenance_and_workflow_guardrails_teaching.ipynb)           | 8, 28, 61, 62          | Poisoned comments vs provenance-verified retrieval; a `.dot` workflow graph enforced on a tool-calling agent                                     | Malicious instruction repeated: 90% → **0%** (0/12 real fixes rejected) · out-of-order actions: 19 → **0**                                             |
| [`1.3a_tickets_graphrag_global_summaries_teaching`](1_retrieval_and_reasoning/1.3a_tickets_graphrag_global_summaries_teaching.ipynb) *(new)*       | 33, 34, 36, 38         | GraphRAG-style community reports + map-reduce vs top-k RAG on global questions over 183 tickets                                                    | Comprehensiveness win rate **100%**, 10 vs 5 hospitals covered · index price 29 calls / 44k tokens, ~10× tokens per query                                     |
| [`3.1a_aura_sparql_ontology_check_teaching`](3_governance_and_control/3.1a_aura_sparql_ontology_check_teaching.ipynb) *(new)* | 27, 43, 44, 50, 59–61 | Text-to-SPARQL over an RDF version of the helpdesk graph, with a deterministic ontology checker, ≤3 repairs, then "unknown", and a read-only gate | Accuracy 20% → **67%**, 7% "unknown", 0 writes executed; 4 queries passed every check but were still wrong                                                     |

### Scaled runs on standard benchmarks (cached; `RUN_LIVE = False` replays in seconds)

| Notebook                                                              | Lecture slides | Benchmark (sample)                                                    | Headline result (95% CI)                                                                                                                                                                                                              |
| :-------------------------------------------------------------------- | :------------- | :-------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`A1_metaqa_multihop_early_run`](archive/A1_metaqa_multihop_early_run.ipynb)       | 32, 36, 38, 41 | MetaQA test, 100 questions per hop; KG of 43K entities / 134K triples | Hits@1 vector → graph: 1-hop 91% → 99% · 2-hop **39% → 97%** · 3-hop **36% → 80%**, at 1.7–6.6× the tokens                                                                                                        |
| [`A2_graphrag_bench_medical_early_run`](archive/A2_graphrag_bench_medical_early_run.ipynb)         | 33–38         | GraphRAG-Bench medical corpus, 180 questions in 4 types               | **No resolvable difference** on any type (e.g. reasoning 72.5 vs 73.0); vector top-8 already found 93–99% of the gold evidence for fact, reasoning and summary questions (64% for creative). Slide 36's gaps did not reproduce |
| [`A3_longmemeval_early_run`](archive/A3_longmemeval_early_run.ipynb) | 52–56         | LongMemEval-S, 108 questions, 13.2M tokens of chat history            | Overall 77% → **83%**; multi-session 69% → 88%, preference 19% → 50%, assistant recall 94% → 88%, temporal tie; graph beats full context (89% vs 75%, n = 28) with ~2% of the tokens                                        |

### Confidence runs on larger and harder benchmarks (`gpt-6-luna`, no reasoning, OpenAI Batch API)

The confidence runs (old 11–20) re-test the claims of the teaching notebooks on public benchmarks large enough for tight 95% intervals, with strong
baselines. The new experiments (old 21–30) test the tasks added in the v2 paper, each with a frozen protocol at the top; their saved
outputs are those of their confidence runs (finished 2026-11-11). Baselines added after the runs (`baselines.md`) are
dated amendment cells at the end of notebooks 2.1a, 3.2, 3.1a, 1.4a, 2.2, 1.3b, 1.1b, 1.2b and 3.6; the full write-up is
`../RESULTS-REPORT.md`. All calls go through `smash_batch.py` (temperature 0, seed 7, results cached). `SMASH_MODE=replay` (the
default) re-runs the saved results in seconds without the API. `SMASH_MODE=test` runs a small live sample. `SMASH_MODE=batch`
recomputes anything missing through the Batch API.

| Notebook                                                                                              | Re-tests | Benchmark (n)                                                                                                                                                                                                                                                                                              | Headline result (95% CI)                                                                                                                                                                                       |   Cost |
| :---------------------------------------------------------------------------------------------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -----: |
| [`1.4a_multihop_text_graph_ranking_musique_2wiki`](1_retrieval_and_reasoning/1.4a_multihop_text_graph_ranking_musique_2wiki.ipynb)                         | A1       | MuSiQue + 2WikiMultiHopQA, 2 × 1,000; graph extracted from text                                                                                                                                                                                                                                           | F1 graph − vector: MuSiQue **+4.7** [+2.1, +7.4], 2Wiki **+11.7** [+8.6, +14.8]; the gain shrinks with hops (2-hop +7.9, 4-hop −1.7)                                                             |  $2.52 |
| [`2.1b_hoh_outdated_facts_temporal_graph_vs_dates`](2_memory_and_state/2.1b_hoh_outdated_facts_temporal_graph_vs_dates.ipynb)                         | 2.1a       | HoH outdated Wikipedia facts, 500                                                                                                                                                                                                                                                                          | vector 63% → temporal graph 90% (+27 [+23, +31]), but vector + dates also 90% (graph − dated vector −0.2 [−2.4, +2.0])                                                                                     |  $0.18 |
| [`3.4_injecagent_plan_graph_gate`](3_governance_and_control/3.4_injecagent_plan_graph_gate.ipynb)               | 3.2       | InjecAgent 1,054 attacks × 3 strengths (incl. AgentDojo template)                                                                                                                                                                                                                                         | attack success: no defence 0.4% (13 of 3,162), prompt rule 0.03%, enforced plan graph **0%**; the plan blocks 0.2% of legitimate tasks                                                                   |  $0.71 |
| [`1.4b_graphrag_bench_graph_ranking`](1_retrieval_and_reasoning/1.4b_graphrag_bench_graph_ranking.ipynb)               | A2       | GraphRAG-Bench, all 4,072 questions, medical + novel                                                                                                                                                                                                                                                       | correctness graph − vector: medical **−1.5** [−2.5, −0.4], novel −0.7 [−1.9, +0.5]; only novel complex reasoning favours the graph (+2.8 [+1.3, +4.4]); fact lookup favours vector in both domains |  $3.34 |
| [`2.2_conversational_memory_longmemeval_locomo`](2_memory_and_state/2.2_conversational_memory_longmemeval_locomo.ipynb)                   | A3       | LongMemEval-S 500 + LoCoMo 1,540; full context on every question                                                                                                                                                                                                                                           | LongMemEval (session ids masked): graph 78% vs vector 75% vs full 69%. LoCoMo: full 79% vs graph 73% vs vector 67%. Assistant recall: graph 52% vs vector 91%                                                                       | $12.12 |
| [`1.3b_podcasts_graphrag_global_vs_mapreduce`](1_retrieval_and_reasoning/1.3b_podcasts_graphrag_global_vs_mapreduce.ipynb)       | 1.3a       | BenchmarkQED podcast corpus, 50 global + 50 local questions                                                                                                                                                                                                                                                | global questions: assertions covered 57% → **77%** (+19.8 [+14.9, +24.6]), judge prefers GraphRAG 90-92% on 3 of 4 criteria; local control: vector 100% vs graph 70%                                    |  $4.7* |
| [`3.1b_spider4ssc_sparql_ontology_check`](3_governance_and_control/3.1b_spider4ssc_sparql_ontology_check.ipynb) | 3.1a       | Spider4SSC text-to-SPARQL, 563 questions / 19 graphs                                                                                                                                                                                                                                                       | one-shot 17%, error/empty retry 22%, ontology checker **84%**; the gain is almost all vocabulary (prefix) errors                                                                                         |  $0.10 |
| [`1.1b_helpdesk_aggregates_graph_vs_vector_vs_sql`](1_retrieval_and_reasoning/1.1b_helpdesk_aggregates_graph_vs_vector_vs_sql.ipynb)                       | 1.1a       | Aura helpdesk, 156 template questions                                                                                                                                                                                                                                                                      | lookup: vector 97% vs graph 47%; verified fix 73% vs **89%**; relational 46% vs **98%**                                                                                                            |  $0.05 |
| [`1.2b_metaqa_curated_vs_extracted_graph`](1_retrieval_and_reasoning/1.2b_metaqa_curated_vs_extracted_graph.ipynb) | A1 | MetaQA 3 × 300; graph agent over the curated KB vs a graph the LLM extracted from 18,127 WikiMovies articles | Hits@1 extracted graph − vector: **+13.3** / **+67.0** / **+56.7** (1/2/3-hop); the curated graph is a further 11–24 points higher | $1.53 |
| [`1.5_citation_accuracy_graph_vs_vector`](1_retrieval_and_reasoning/1.5_citation_accuracy_graph_vs_vector.ipynb) | 1.4a | MuSiQue + 2WikiMultiHopQA, 2 × 1,000; answers must cite sources (vector passages, graph passages, graph facts resolved to their source passage); ALCE-style citation recall and precision | graph passages − vector: ALCE citation recall **+5.9** [+4.1, +7.7], precision **+6.8** [+4.7, +9.0], F1 +8.6; cited facts − vector: F1 **−7.9** [−9.9, −5.9], 10 points more abstentions | $0.44 |
| [`1.6_entity_grounding_linking_cascade`](1_retrieval_and_reasoning/1.6_entity_grounding_linking_cascade.ipynb) | A1, 1.4a | Task 1.6: MetaQA 3 × 300 (brackets removed) + 2Wiki 1,000; entity-linking cascade vs raw question text and LLM-named entities | predicted link − raw text: MetaQA −0.1 [−1.3, +1.1], 2Wiki **−4.4** [−7.5, −1.4]; linking does not help | $0.33 |
| [`2.3_alfworld_world_graph_vs_history`](2_memory_and_state/2.3_alfworld_world_graph_vs_history.ipynb) | — | Task 2.3: ALFWorld, 274 games; world graph vs full history vs vector memory (separate venv `.venv-alfworld`) | success: full history 88.3%, world graph 86.5%, vector memory 63.5%; graph − full −1.8 [−5.5, +1.8], graph − vector **+23.0** [+17.2, +28.8], at twice the tokens | $2.65 |
| [`3.5_access_control_permission_graph`](3_governance_and_control/3.5_access_control_permission_graph.ipynb) | — | Task 3.5: PlanetCare records + synthetic users and permissions, 300 + 300 (user, question) pairs; permission-graph filter vs rules / allowlist in the prompt | total error: graph **2.7%** vs allowlist 16.5%, rules 29.2% (prompt controls over-block 32–58%); the graph's 4% "leaks" are judge false positives (corrected 0.7%) | $0.18 |
| [`3.6_audit_trail_provenance_graph`](3_governance_and_control/3.6_audit_trail_provenance_graph.ipynb) | — | Task 3.6: 1,332 audit questions over the traces of notebooks 3.4, 1.1b, 1.2b (logs of 1–200 runs); PROV-O graph vs full log vs grep agent | graph 93.5% vs full log 87.5% (+5.9) but search agent 96.7% (−3.2) and SQL 99.0% (−5.6, added baseline) | $3.40 |
| [`4.1_dag_planner_vs_react`](4_execution_and_coordination/4.1_dag_planner_vs_react.ipynb) | 1.4a | Task 4.1: MuSiQue + 2Wiki 2 × 1,000, MetaQA 3-hop 300; DAG planner vs ReAct, list decomposition and vector RAG | DAG − ReAct: F1 **−8.2** [−10.1, −6.2], MetaQA Hits@1 −19.7; not faster (+1.0 s) | $1.85 |
| [`4.2_tool_selection_tool_graph`](4_execution_and_coordination/4.2_tool_selection_tool_graph.ipynb) | — | Task 4.2: TaskBench 1,500 + ToolBench 1,000; tool graph vs embedding search and all tools in the prompt | graph − embedding: node-F1 −0.4 [−1.1, +0.4], recall@5 +0.8 [−0.3, +2.0]; all tools in the prompt best (+6 node-F1) | $0.61 |
| [`4.3_tau2_crash_recovery_checkpoint_graph`](4_execution_and_coordination/4.3_tau2_crash_recovery_checkpoint_graph.ipynb) | 3.2 | Task 4.3: τ²-bench, crashes injected into the reference runs of notebook 4.4; checkpoint graph vs restart and message history (separate venv `.venv-tau2`) | resume success: history + note 85.3%, graph 81.3% (−4.0 [−8.8, +0.7]); the note alone stops repeated writes | $6.58 |
| [`4.4_tau2_outcome_verification_graph_check`](4_execution_and_coordination/4.4_tau2_outcome_verification_graph_check.ipynb) | — | Task 4.4: τ²-bench, 278 tasks × 3 recordings, write actions replayed correct / no-op / wrong; graph check vs LLM verifiers (separate venv `.venv-tau2`) | detection F1: LLM with state **0.97**, graph check 0.92 (−0.05 [−0.07, −0.04]) with 0% false alarms; LLM from tool output 0.37 | $4.64 |
| [`4.5_shared_claim_graph_between_agents`](4_execution_and_coordination/4.5_shared_claim_graph_between_agents.ipynb) | 1.4a | Task 4.5: MuSiQue + 2Wiki 2 × 1,000; shared claim graph vs message passing vs a single agent at equal token budget | F1: shared graph 63.6 vs messages 61.0 (+2.6 [+1.3, +4.0]) vs single agent 55.7 (+7.9; it used 30% of its budget) | $6.74 |
| [`3.1c_spider4ssc_sql_generated_ontology`](3_governance_and_control/3.1c_spider4ssc_sql_generated_ontology.ipynb)                   | 3.1b       | Spider4SSC text-to-**SQL**, 563 questions / 19 SQLite databases, with and without declared foreign keys; ontology generated from metadata ([NVIDIA Auto Ontology](https://github.com/NVIDIA/auto-ontology) export, or an LLM-built stand-in) as prompt context and as a deterministic join-path check | ontology + join check − retry: +0.9 [−0.2, +2.0] (declared FKs), −1.2 [−2.7, +0.2] (FKs removed); no difference | $0.14 |

\* includes one re-run after a reproducibility fix.

**Every LLM input and output of the first confidence runs (old 11–18) is archived** in `data/llm_io/` for later analysis (`python export_llm_io.py`
refreshes it):

- `raw_batches/<batch_id>/{input,output}.jsonl.gz` hold OpenAI's own Batch files: exact requests and full response bodies.
- `<cache>/<stage>.jsonl.gz` holds one row per call with the full request (messages, model, settings) and the response
  (text, tool calls, tokens).
- `manifest.json` maps every batch to its notebook and stage and gives call and token counts.

Embedding calls and the small test-mode runs are not archived. The teaching notebooks and A1–A3 cached outputs only.

Benchmark data and caches live in `data/benchmarks/` (≈580 MB; MetaQA via the `camazlucas/MetaQA` HF mirror,
GraphRAG-Bench MIT, LongMemEval MIT). Re-running live (`RUN_LIVE = True`) re-calls the API: notebook A3's full
run used ≈20M LLM tokens.

LLM outputs vary slightly between runs even at temperature 0 (typically ±1 question per benchmark). The teaching notebooks
(small hand-built question sets) illustrate the lecture's claims; the confidence runs re-test them at scale.

## Datasets (`data/`)

Except for the generated PlanetCare tickets, the data is not part of the repository. `python download_data.py` fetches every dataset from its original
publisher into `data/` (about 1.5 GB). `python download_data.py <name> ...` fetches only some datasets, and
`python download_data.py --list` shows the datasets, the notebooks that use them and their licences. Existing
files are skipped.

| Name               | Path                                   | Notebooks      | Source                                                                                                                                                               | Licence                                               |
| :----------------- | :------------------------------------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------- |
| `aura`           | `aura_helpdesk.json`                 | 1.1a, 3.2, 3.1a, 1.1b | [AlexisBalayre/AuraHelpdeskGraph](https://github.com/AlexisBalayre/AuraHelpdeskGraph): the sample CSVs, with relationships rebuilt from its Neo4j load script         | none stated                                           |
| —                 | `planetcare_*`                       | 5.1, 1.3a         | **Generated (synthetic) dataset** created by the author for teaching, included in this repository; see [`data/PLANETCARE.md`](data/PLANETCARE.md)             | CC BY 4.0                                             |
| `runbooks`       | `runbooks/`                          | 2.1a             | [AriaAICompany/incident-rag-runbooks](https://huggingface.co/datasets/AriaAICompany/incident-rag-runbooks)                                                            | CC BY 4.0                                             |
| `telecom`        | `telecom_workflow/`                  | 3.2             | [τ²-bench](https://github.com/sierra-research/tau2-bench) telecom domain                                                                                            | MIT                                                   |
| `incidents`      | `servicenow_incidents.duckdb`        | 1.2a             | [UCI incident management event log](https://archive.ics.uci.edu/dataset/498/incident+management+process+enriched+event+log): its first 119,998 rows, 20,769 incidents | CC BY 4.0                                             |
| `metaqa`         | `benchmarks/metaqa/`                 | A1, 1.2b         | [MetaQA](https://github.com/yuyuz/MetaQA) (Hugging Face copy `camazlucas/MetaQA`)                                                                                   | Creative Commons                                      |
| `wikimovies`     | `benchmarks/metaqa/wikimovies_text/` | 1.2b             | WikiMovies article text from the MovieQA release (Miller et al., 2016), via the Internet Archive                                                                     | CC BY 3.0                                             |
| `musique_2wiki`  | `benchmarks/musique_2wiki/`          | 1.4a             | [HippoRAG 2 release](https://huggingface.co/datasets/osunlp/HippoRAG_2) of MuSiQue and 2WikiMultiHopQA                                                                | CC BY 4.0 / Apache-2.0                                |
| `graphrag_bench` | `benchmarks/graphrag_bench/`         | A2, 1.4b         | [GraphRAG-Bench](https://huggingface.co/datasets/GraphRAG-Bench/GraphRAG-Bench)                                                                                       | MIT                                                   |
| `hoh`            | `benchmarks/hoh/`                    | 2.1b             | [HoH-QAs](https://huggingface.co/datasets/russwest404/HoH-QAs)                                                                                                        | Apache-2.0                                            |
| `injecagent`     | `benchmarks/injecagent/`             | 3.4             | [InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent)                                                                                                             | MIT                                                   |
| `longmemeval`    | `benchmarks/longmemeval/`            | A3, 2.2         | [LongMemEval-S, cleaned](https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned)                                                                              | MIT                                                   |
| `locomo`         | `benchmarks/locomo/`                 | 2.2             | [LoCoMo](https://github.com/snap-research/locomo)                                                                                                                     | **CC BY-NC 4.0**                                |
| `benchmarkqed`   | `benchmarks/benchmarkqed_podcast/`   | 1.3b             | [BenchmarkQED](https://github.com/microsoft/benchmark-qed) podcast transcripts and questions                                                                          | **Microsoft Research License** (non-commercial) |
| `spider4ssc`     | `benchmarks/spider4ssc/`             | 3.1b, 3.1c         | [Spider4SSC](https://data.mendeley.com/datasets/4dnvv92trn), Mendeley Data v2                                                                                         | CC BY 4.0 (Spider: CC BY-SA 4.0)                      |
| —                | `benchmarks/alfworld/`               | 2.3             | [ALFWorld](https://github.com/alfworld/alfworld) game files and TextWorld engine (installed in `.venv-alfworld`); **not fetched by `download_data.py` yet** | to check |
| —                | `benchmarks/taskbench/`              | 4.2             | [TaskBench](https://github.com/microsoft/JARVIS/tree/main/taskbench) tool graphs and samples (3 domains); **not fetched yet** | MIT |
| —                | `benchmarks/toolbench/`              | 4.2             | ToolBench test queries and API corpus, pinned third-party copy (checksums in `SHA256SUMS`); **not fetched yet** | Apache-2.0 |
| —                | `benchmarks/tau2/`                   | 4.3, 4.4         | [τ²-bench](https://github.com/sierra-research/tau2-bench) full checkout at commit `96a3ef9` (installed in `.venv-tau2`); **not fetched yet** | MIT |
| —                | `benchmarks/planetcare_access/`      | 3.5             | Synthetic users, roles and permissions over the PlanetCare tickets, written by notebook 3.5's seeded generator | CC BY 4.0 (ours) |
| —                | `benchmarks/audit_trail/`            | 3.6             | Audit questions built by notebook 3.6 from the cached traces of notebooks 3.4, 1.1b, 1.2b | as its sources |

All scaled notebooks also keep their LLM responses and embeddings in cache folders next to the data
(`cache*/`, `data/cache_18/`). These are not in the repository. Without them, run a notebook with `SMASH_MODE=test`
for a small live sample, or with `SMASH_MODE=batch` to recompute everything (needs `OPENAI_API_KEY`).

## Quick start

The notebooks read `OPENAI_API_KEY` from the environment. The saved runs used Python 3.13 and the package versions
in [`requirements.txt`](requirements.txt).

```bash
cd examples
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name smash-workshop-venv
python download_data.py
```

Open a notebook, select the `smash-workshop-venv` kernel, and run all cells top to bottom. Every notebook is
self-contained.
