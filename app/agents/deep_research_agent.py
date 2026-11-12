def collect_sources(sources):
    """Validate and organize the research sources."""

    if len(sources) < 3:
        raise ValueError("At least 3 sources are required.")

    required_fields = [
        "id", "type", "date", "author",
        "claim", "evidence", "limitation", "relevance"
    ]

    source_ids = set()

    for source in sources:
        for field in required_fields:
            if not source.get(field):
                raise ValueError(f"Source is missing: {field}")

        if source["id"] in source_ids:
            raise ValueError("Source IDs must be unique.")

        source_ids.add(source["id"])

    return sources


def compare(sources, agreements=None, conflicts=None, gaps=None):
    """Organize evidence comparisons supplied by the researcher."""

    valid_ids = {source["id"] for source in sources}

    agreements = agreements or []
    conflicts = conflicts or []
    gaps = gaps or []

    for item in agreements + conflicts + gaps:
        for source_id in item.get("source_ids", []):
            if source_id not in valid_ids:
                raise ValueError(f"Unknown source ID: {source_id}")

    return {
        "agreements": agreements,
        "conflicts": conflicts,
        "gaps": gaps
    }


def synthesize(topic, sources, comparison, next_questions=None):
    """Create an executive summary with source traceability."""

    summary = []

    for source in sources:
        summary.append(
            f'[{source["id"]}] {source["claim"]}'
        )

    for item in comparison["agreements"]:
        ids = ",".join(item["source_ids"])
        summary.append(f'[{ids}] {item["note"]}')

    for item in comparison["conflicts"]:
        ids = ",".join(item["source_ids"])
        summary.append(f'[{ids}] {item["note"]}')

    for item in comparison["gaps"]:
        summary.append(f'[gap] {item["note"]}')

    return {
        "topic": topic,
        "executive_summary": summary,
        "recommended_next_questions": next_questions or []
    }


def run_deep_research(
    topic,
    sources,
    agreements=None,
    conflicts=None,
    gaps=None,
    next_questions=None
):
    """Run the complete Deep Research Agent workflow."""

    if not topic:
        return {"status": "error", "message": "Research topic is required."}

    try:
        evidence = collect_sources(sources)

        comparison = compare(
            evidence,
            agreements,
            conflicts,
            gaps
        )

        summary = synthesize(
            topic,
            evidence,
            comparison,
            next_questions
        )

        return {
            "status": "success",
            "research_question": topic,
            "sources": evidence,
            "evidence_table": evidence,
            "comparison": comparison,
            "executive_summary": summary["executive_summary"],
            "recommended_next_questions": summary[
                "recommended_next_questions"
            ]
        }

    except (ValueError, TypeError) as error:
        return {
            "status": "error",
            "message": str(error)
        }
