"""Download the public data that the notebooks expect under data/.

    python download_data.py                 # everything (about 1.5 GB)
    python download_data.py metaqa hoh      # only some datasets
    python download_data.py --list          # what is available, and for which notebooks

Files that already exist are skipped. Every dataset is fetched from its original publisher; the licences differ
(see the table printed by --list) and two of them allow non-commercial research only.

Needs Python 3.10+ and `duckdb` (for the incident warehouse of notebook 02 and to convert HoH from Parquet). The PlanetCare tickets of notebooks 03 and 06 are not public and are not downloaded.
"""
import argparse
import csv
import json
import os
import shutil
import sys
import tarfile
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = f"{ROOT}/data"
BENCH = f"{DATA}/benchmarks"
HF = "https://huggingface.co/datasets"
GH = "https://raw.githubusercontent.com"


def fetch(url, path):
    if os.path.exists(path):
        print(f"  exists  {os.path.relpath(path, ROOT)}")
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(f"  get     {os.path.relpath(path, ROOT)}  <-  {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "smash-workshop-download/1.0"})
    with urllib.request.urlopen(req, timeout=600) as r, open(path + ".part", "wb") as f:
        shutil.copyfileobj(r, f, 1 << 20)
    os.replace(path + ".part", path)
    return path


# ---- one function per dataset ------------------------------------------------------------------------------------
def aura():
    # Notebooks 01, 05, 07, 18: the Aura helpdesk sample of AlexisBalayre/AuraHelpdeskGraph (pinned commit), turned
    # into one JSON file with the relationships of the repository's Neo4j load script (datasets/setup_database.cypher).
    out = f"{DATA}/aura_helpdesk.json"
    if os.path.exists(out):
        print("  exists  data/aura_helpdesk.json")
        return
    src, tmp = f"{GH}/AlexisBalayre/AuraHelpdeskGraph/d9e901578bfde35a99c8dd7875bcf370a913327a/datasets/data", f"{DATA}/aura_src"
    d = {}
    for key, name in [("categories", "category"), ("priorities", "priority"), ("statuses", "status"), ("users", "users"),
                      ("tickets", "tickets"), ("comments", "comments"), ("documentation", "documentation")]:
        with open(fetch(f"{src}/{name}_sample.csv", f"{tmp}/{name}_sample.csv"), encoding="utf-8") as f:
            d[key] = list(csv.DictReader(f))
    R = []
    def rel(t, a, al, b, bl):
        if a and b:
            R.append({"type": t, "from": a, "from_label": al, "to": b, "to_label": bl})
    for t in d["tickets"]:
        rel("SUBMITS", t["createdByUserId"], "User", t["ticketId"], "Ticket")
        rel("ASSIGNED_TO", t["assignedToUserId"], "User", t["ticketId"], "Ticket")
        rel("HAS_STATUS", t["ticketId"], "Ticket", t["statusId"], "Status")
        rel("HAS_PRIORITY", t["ticketId"], "Ticket", t["priorityId"], "Priority")
        rel("HAS_CATEGORY", t["ticketId"], "Ticket", t["categoryId"], "Category")
    for c in d["comments"]:
        rel("CONTAINS", c["ticketId"], "Ticket", c["commentId"], "Comment")
        rel("POSTS", c["authorUserId"], "User", c["commentId"], "Comment")
        rel("REFERENCED_BY", c["articleId"], "DocumentationArticle", c["commentId"], "Comment")
    for a in d["documentation"]:
        rel("HAS_CATEGORY", a["categoryId"], "Category", a["articleId"], "DocumentationArticle")
    meta = {"source_repo": "AlexisBalayre/AuraHelpdeskGraph",
            "source_path": "datasets/data/*.csv + datasets/setup_database.cypher",
            "description": "Synthetic IT helpdesk knowledge graph dataset (3DS 'Aura' support chatbot domain): tickets, "
                           "comments, documentation, users, and category/priority/status taxonomies, with graph "
                           "relationships reconstructed from the Neo4j Cypher load script.",
            "counts": {**{k: len(v) for k, v in d.items()}, "relationships": len(R)}}
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"_metadata": meta, **d, "relationships": R}, f, ensure_ascii=False, indent=2)
    shutil.rmtree(tmp)
    print(f"  wrote   data/aura_helpdesk.json ({len(R)} relationships)")


def telecom():
    # Notebook 05: the tau2-bench telecom domain at the commit the notebook was written against.
    b = f"{GH}/sierra-research/tau2-bench/96a3ef92329baf908ffe9dfe188cea34e8701d2a/data/tau2/domains/telecom"
    for f in ("db.toml", "main_policy.md", "tasks_small.json", "tech_support_manual.md", "tech_support_workflow.md",
              "workflows/tech_support_path1_no_service.dot", "workflows/tech_support_path2_mobile_data.dot",
              "workflows/tech_support_path3_mms.dot"):
        fetch(f"{b}/{f}", f"{DATA}/telecom_workflow/{os.path.basename(f)}")


def runbooks():
    # Notebook 04: IncidentRAG synthetic runbooks (Hugging Face AriaAICompany/incident-rag-runbooks).
    b = f"{HF}/AriaAICompany/incident-rag-runbooks/resolve/main"
    for f in ("data/documents.jsonl", "data/questions.jsonl", "data/evaluation.json", "data/schema.json", "README.md"):
        fetch(f"{b}/{f}", f"{DATA}/runbooks/{os.path.basename(f)}")


def metaqa():
    d = f"{BENCH}/metaqa"
    fetch(f"{HF}/camazlucas/MetaQA/resolve/main/kb/kb.txt", f"{d}/kb.txt")
    for h in (1, 2, 3):
        fetch(f"{HF}/camazlucas/MetaQA/resolve/main/{h}-hop/vanilla/qa_test.txt", f"{d}/qa_test_{h}hop.txt")


def wikimovies():
    # The WikiMovies / MovieQA release of Miller et al. (2016); the original host is offline, so the Internet Archive
    # copy is used. Only the article text (wiki.txt) and the licence are kept.
    d = f"{BENCH}/metaqa/wikimovies_text"
    if os.path.exists(f"{d}/movieqa/knowledge_source/wiki.txt"):
        print("  exists  data/benchmarks/metaqa/wikimovies_text/movieqa/knowledge_source/wiki.txt")
        return
    tgz = fetch("http://web.archive.org/web/20220615183146id_/http://www.thespermwhale.com/jaseweston/babi/movieqa.tar.gz",
                f"{d}/movieqa.tar.gz")
    keep = {"movieqa/LICENSE.txt", "movieqa/README.txt", "movieqa/knowledge_source/wiki.txt"}
    with tarfile.open(tgz) as t:
        t.extractall(d, members=[m for m in t.getmembers() if m.name in keep and m.isfile()])
    os.remove(tgz)


def musique_2wiki():
    for f in ("musique.json", "musique_corpus.json", "2wikimultihopqa.json", "2wikimultihopqa_corpus.json"):
        fetch(f"{HF}/osunlp/HippoRAG_2/resolve/main/{f}", f"{BENCH}/musique_2wiki/{f}")


def graphrag_bench():
    for f in ("Corpus/medical.json", "Corpus/novel.json", "Questions/medical_questions.json",
              "Questions/novel_questions.json"):
        fetch(f"{HF}/GraphRAG-Bench/GraphRAG-Bench/resolve/main/Datasets/{f}", f"{BENCH}/graphrag_bench/Datasets/{f}")


def hoh():
    d = f"{BENCH}/hoh"
    pq = fetch(f"{HF}/russwest404/HoH-QAs/resolve/main/hoh_qas_240601_241201.parquet", f"{d}/hoh_qas_240601_241201.parquet")
    out = f"{d}/hoh_qas.jsonl"
    if os.path.exists(out):
        print("  exists  data/benchmarks/hoh/hoh_qas.jsonl")
        return
    import duckdb
    cur = duckdb.connect().execute(f"SELECT * FROM read_parquet('{pq}')")
    cols = [c[0] for c in cur.description]
    with open(out + ".part", "w") as f:
        while rows := cur.fetchmany(5000):
            for r in rows:
                f.write(json.dumps(dict(zip(cols, r)), default=str, ensure_ascii=False) + "\n")
    os.replace(out + ".part", out)
    print("  wrote   data/benchmarks/hoh/hoh_qas.jsonl")


def injecagent():
    for f in ("tools.json", "test_cases_dh_base.json", "test_cases_dh_enhanced.json", "test_cases_ds_base.json",
              "test_cases_ds_enhanced.json", "attacker_cases_dh.jsonl", "attacker_cases_ds.jsonl", "user_cases.jsonl",
              "attacker_simulated_responses.json"):
        fetch(f"{GH}/uiuc-kang-lab/InjecAgent/main/data/{f}", f"{BENCH}/injecagent/{f}")
    fetch(f"{GH}/uiuc-kang-lab/InjecAgent/main/LICENCE", f"{BENCH}/injecagent/LICENSE")


def longmemeval():
    fetch(f"{HF}/xiaowu0162/longmemeval-cleaned/resolve/main/longmemeval_s_cleaned.json",
          f"{BENCH}/longmemeval/longmemeval_s_cleaned.json")


def locomo():
    fetch(f"{GH}/snap-research/locomo/main/data/locomo10.json", f"{BENCH}/locomo/locomo10.json")
    fetch(f"{GH}/snap-research/locomo/main/LICENSE.txt", f"{BENCH}/locomo/LICENSE")


def benchmarkqed():
    b, d = f"{GH}/microsoft/benchmark-qed/main/datasets", f"{BENCH}/benchmarkqed_podcast"
    fetch(f"{b}/podcast/raw_data.zip", f"{d}/raw_data.zip")
    for f in ("data_global_questions_assertions.json", "data_local_questions_assertions.json"):
        fetch(f"{b}/podcast/generated_questions_v2/{f}", f"{d}/{f}")
    fetch(f"{b}/LICENSE", f"{d}/LICENSE")


def spider4ssc():
    # Mendeley Data 4dnvv92trn, version 2 (Vejvar et al.).
    m, d = "https://data.mendeley.com/public-files/datasets/4dnvv92trn/files", f"{BENCH}/spider4ssc"
    fetch(f"{m}/fcb66a6b-50e4-4952-8458-78b8adb17e70/file_downloaded", f"{d}/dev.json")
    fetch(f"{m}/f4bdf756-c6d3-4807-93a1-b70f66f1d4ec/file_downloaded", f"{d}/LICENSE.md")
    z = fetch(f"{m}/9d82e209-b6df-4c70-b1c1-927b6d0cf63a/file_downloaded", f"{d}/database.zip")
    if not os.path.isdir(f"{d}/database"):
        with zipfile.ZipFile(z) as f:
            f.extractall(d)
        print("  unzip   data/benchmarks/spider4ssc/database/")


def incidents():
    # Notebook 02: the UCI "Incident management process enriched event log" (ServiceNow), loaded into DuckDB as
    # incidents.incident_events plus the incident_summary view. The notebook's saved run used the first 119,998 rows
    # of the CSV (20,769 incidents); the same subset is loaded here so that its numbers reproduce.
    db = f"{DATA}/servicenow_incidents.duckdb"
    if os.path.exists(db):
        print("  exists  data/servicenow_incidents.duckdb")
        return
    z = fetch("https://archive.ics.uci.edu/static/public/498/incident+management+process+enriched+event+log.zip",
              f"{DATA}/uci_incidents.zip")
    with zipfile.ZipFile(z) as f:
        f.extract("incident_event_log.csv", DATA)
    import duckdb
    con = duckdb.connect(f"{DATA}/servicenow_build.duckdb")
    con.execute("CREATE SCHEMA incidents")
    con.execute(f"""
        CREATE TABLE incidents.incident_events AS
        SELECT * EXCLUDE (rn) FROM (
            SELECT *, row_number() OVER () AS rn
            FROM read_csv('{DATA}/incident_event_log.csv', header = true, nullstr = '?',
                          timestampformat = '%d/%m/%Y %H:%M',
                          types = {{'reassignment_count': 'BIGINT', 'reopen_count': 'BIGINT', 'sys_mod_count': 'BIGINT'}}))
        WHERE rn <= 119998""")
    con.execute("""
        CREATE VIEW incidents.incident_summary AS
        WITH final AS (
            SELECT DISTINCT ON (number) number, incident_state, priority, made_sla, assignment_group,
                   reassignment_count, reopen_count
            FROM incidents.incident_events
            ORDER BY number, (incident_state = 'Closed') DESC, sys_updated_at DESC),
        agg AS (
            SELECT number, count(*) AS event_count, min(opened_at) AS opened_at, max(resolved_at) AS resolved_at
            FROM incidents.incident_events GROUP BY number)
        SELECT f.number AS incident, a.event_count, a.opened_at, a.resolved_at, f.incident_state AS final_state,
               f.priority, f.made_sla, f.assignment_group, f.reassignment_count, f.reopen_count,
               date_diff('minute', a.opened_at, a.resolved_at) / 60.0 AS ttr_hours
        FROM final f JOIN agg a USING (number)""")
    n = con.execute("SELECT count(*), count(DISTINCT number) FROM incidents.incident_events").fetchone()
    con.close()
    os.replace(f"{DATA}/servicenow_build.duckdb", db)
    os.remove(f"{DATA}/incident_event_log.csv")
    os.remove(z)
    print(f"  built   data/servicenow_incidents.duckdb ({n[0]:,} events, {n[1]:,} incidents)")


DATASETS = {   # name: (function, notebooks, source, licence)
    "aura": (aura, "01,05,07,18", "GitHub AlexisBalayre/AuraHelpdeskGraph", "no licence stated by the author"),
    "runbooks": (runbooks, "04", "HF AriaAICompany/incident-rag-runbooks", "CC BY 4.0"),
    "telecom": (telecom, "05", "GitHub sierra-research/tau2-bench", "MIT"),
    "incidents": (incidents, "02", "UCI ML Repository 498 (ServiceNow event log)", "CC BY 4.0"),
    "metaqa": (metaqa, "08, 19", "HF camazlucas/MetaQA (copy of yuyuz/MetaQA)", "Creative Commons (version not stated)"),
    "wikimovies": (wikimovies, "19", "MovieQA/WikiMovies release (Internet Archive)", "CC BY 3.0"),
    "musique_2wiki": (musique_2wiki, "11", "HF osunlp/HippoRAG_2", "MuSiQue CC BY 4.0; 2Wiki Apache-2.0"),
    "graphrag_bench": (graphrag_bench, "09, 14", "HF GraphRAG-Bench/GraphRAG-Bench", "MIT (GitHub repository)"),
    "hoh": (hoh, "12", "HF russwest404/HoH-QAs", "Apache-2.0"),
    "injecagent": (injecagent, "13", "GitHub uiuc-kang-lab/InjecAgent", "MIT"),
    "longmemeval": (longmemeval, "10, 15", "HF xiaowu0162/longmemeval-cleaned", "MIT"),
    "locomo": (locomo, "15", "GitHub snap-research/locomo", "CC BY-NC 4.0 (non-commercial)"),
    "benchmarkqed": (benchmarkqed, "16", "GitHub microsoft/benchmark-qed", "Microsoft Research License (non-commercial)"),
    "spider4ssc": (spider4ssc, "17", "Mendeley Data 4dnvv92trn v2", "CC BY 4.0 (Spider: CC BY-SA 4.0)"),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("names", nargs="*", help=f"datasets to fetch (default: all): {', '.join(DATASETS)}")
    ap.add_argument("--list", action="store_true", help="list the datasets and exit")
    a = ap.parse_args()
    if a.list:
        for k, (_, nb, src, lic) in DATASETS.items():
            print(f"{k:<15} notebooks {nb:<12} {src:<48} {lic}")
        return
    bad = [n for n in a.names if n not in DATASETS]
    if bad:
        sys.exit(f"unknown dataset(s): {', '.join(bad)}; choose from {', '.join(DATASETS)}")
    for n in a.names or DATASETS:
        print(f"[{n}]")
        DATASETS[n][0]()


if __name__ == "__main__":
    main()
