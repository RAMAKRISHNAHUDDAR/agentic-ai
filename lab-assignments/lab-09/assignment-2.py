
"""
Lab 9 - Assignment 2
Weight Sources by Quality
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
]

QUALITY_WEIGHTS = {
    "peer-reviewed paper": 3,
    "independent benchmark report": 2,
    "vendor engineering blog": 1
}


def assign_quality_tiers(sources):
    for source in sources:
        source_type = source["type"]
        source["quality_weight"] = QUALITY_WEIGHTS.get(source_type, 1)

        if source["quality_weight"] == 3:
            source["quality_tier"] = "High"
        elif source["quality_weight"] == 2:
            source["quality_tier"] = "Medium"
        else:
            source["quality_tier"] = "Low"

    return sources


def build_evidence_table(sources):
    return assign_quality_tiers(sources)


def compare(sources):
    agreements = []
    conflicts = []
    gaps = []

    accuracy_sources = [
        s for s in sources
        if "reduces" in s["claim"] or "improves" in s["claim"]
    ]

    if len(accuracy_sources) >= 2:
        agreements.append({
            "source_ids": [s["id"] for s in accuracy_sources],
            "description": (
                "Both sources report improved accuracy or reduced hallucinations."
            )
        })

    latency_sources = [
        s for s in sources if "latency" in s["claim"]
    ]

    if latency_sources and accuracy_sources:
        conflicts.append({
            "source_ids": (
                [s["id"] for s in accuracy_sources + latency_sources]
            ),
            "description": (
                "Accuracy improvements are reported alongside a measurable "
                "latency overhead."
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

    ranked_sources = sorted(
        evidence_table,
        key=lambda s: s["quality_weight"],
        reverse=True
    )

    lines.append("Evidence weighted by source quality:")

    for source in ranked_sources:
        lines.append(
            f"[{source['id']}] [{source['quality_tier']} quality, "
            f"weight {source['quality_weight']}] {source['claim']}"
        )

    lines.append(
        "The synthesis gives greater weight to peer-reviewed evidence, "
        "followed by independent benchmarks and vendor blogs."
    )

    for source in ranked_sources:
        if source["quality_tier"] == "Low":
            lines.append(
                f"[Down-weighted, not discarded: {source['id']}] "
                f"The vendor source is retained, but its claim receives "
                f"less weight because it is an internal evaluation without "
                f"independent replication."
            )

    for agreement in comparison["agreements"]:
        lines.append(f"[Agreement] {agreement['description']}")

    for conflict in comparison["conflicts"]:
        lines.append(f"[Comparison] {conflict['description']}")

    for gap in comparison["gaps"]:
        lines.append(f"[Gap] {gap}")

    return lines


if __name__ == "__main__":
    print("=== Question ===")
    print(QUESTION)

    table = build_evidence_table(SOURCES)

    print("\n=== Evidence table with quality tiers ===")
    for row in table:
        print(row)

    comparison = compare(table)

    print("\n=== Comparison ===")
    print(comparison)

    print("\n=== Weighted executive summary ===")
    for line in synthesize(table, comparison):
        print(line)
