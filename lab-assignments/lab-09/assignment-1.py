
"""
Lab 9 - Assignment 1
Add a Directly Contradicting Source
"""

QUESTION = ("What are the demonstrated benefits and limitations of retrieval-augmented "
            "generation (RAG) for domain-specific question answering, as of the last year?")

SOURCES = [
    {"id": "S1", "type": "peer-reviewed paper", "date": "2026-02",
     "claim": "RAG reduces hallucination rate by 41% on domain QA vs a non-retrieval baseline.",
     "evidence": "200 held-out questions from a medical knowledge base.",
     "limitation": "Small, single-domain evaluation set; may not generalize."},

    {"id": "S2", "type": "vendor engineering blog", "date": "2026-04",
     "claim": "RAG improves answer accuracy by 35% in an internal support-ticket QA system.",
     "evidence": "Internal A/B test over 10,000 tickets.",
     "limitation": "Funded/internal evaluation; no independent replication reported."},

    {"id": "S3", "type": "independent benchmark report", "date": "2026-05",
     "claim": "RAG introduces a measurable latency overhead of 200-400ms per query.",
     "evidence": "Benchmarked across 5 open-source RAG pipelines.",
     "limitation": "Latency depends heavily on retrieval index size; not tested at scale."},

    {"id": "S4", "type": "independent evaluation", "date": "2026-06",
     "claim": "RAG showed no measurable reduction in hallucination rate compared with a non-retrieval baseline.",
     "evidence": "Evaluation across a different domain using a separate dataset.",
     "limitation": "Different evaluation methodology and dataset size may affect comparability."},
]


def build_evidence_table(sources):
    return sources


def compare(sources):
    agreements = []
    conflicts = []
    gaps = []

    accuracy_claims = [
        s for s in sources
        if "reduces" in s["claim"] or "improves" in s["claim"]
    ]

    if len(accuracy_claims) >= 2:
        agreements.append(
            "S1 and S2 report improvements in accuracy in their respective domains."
        )

    source_1 = next(s for s in sources if s["id"] == "S1")
    source_4 = next(s for s in sources if s["id"] == "S4")

    if "reduces hallucination" in source_1["claim"] and \
       "no measurable reduction" in source_4["claim"]:
        conflicts.append({
            "source_ids": ["S1", "S4"],
            "description": (
                "S1 reports a 41% reduction in hallucinations, while S4 "
                "reports no measurable reduction."
            ),
            "possible_reason": (
                "The studies may differ in evaluation methodology, domain, "
                "or dataset size."
            )
        })

    gaps.append(
        "No source in this set reports on RAG performance for non-English languages."
    )

    return {
        "agreements": agreements,
        "conflicts": conflicts,
        "gaps": gaps
    }


def synthesize(evidence_table, comparison):
    lines = []

    for source in evidence_table:
        lines.append(f"[{source['id']}] {source['claim']}")

    for agreement in comparison["agreements"]:
        lines.append(f"[Agreement] {agreement}")

    for conflict in comparison["conflicts"]:
        lines.append(
            f"[Conflict: {','.join(conflict['source_ids'])}] "
            f"{conflict['description']}"
        )
        lines.append(
            f"[Possible explanation] {conflict['possible_reason']}"
        )

    for gap in comparison["gaps"]:
        lines.append(f"[Gap] {gap}")

    return lines


if __name__ == "__main__":
    print("=== Question ===")
    print(QUESTION)

    table = build_evidence_table(SOURCES)

    print("\n=== Evidence table ===")
    for row in table:
        print(row)

    comparison = compare(table)

    print("\n=== Comparison ===")
    print(comparison)

    print("\n=== Executive summary ===")
    for line in synthesize(table, comparison):
        print(line)
