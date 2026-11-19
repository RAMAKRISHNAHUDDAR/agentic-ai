from itertools import combinations
import re

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
        if not isinstance(source, dict):
            raise ValueError("Each source must be a record.")
        for field in required_fields:
            if not isinstance(source.get(field), str) or not source[field].strip():
                raise ValueError(f"Source is missing: {field}")

        if source["id"] in source_ids:
            raise ValueError("Source IDs must be unique.")

        source_ids.add(source["id"])

    return sources


def compare(sources, agreements=None, conflicts=None, gaps=None):
    """Organize evidence comparisons supplied by the researcher."""

    valid_ids = {source["id"] for source in sources}

    def normalize(claim):
        return " ".join(re.findall(r"[a-z0-9]+", claim.lower()))

    derived_agreements, derived_conflicts = [], []
    for left, right in combinations(sources, 2):
        first, second = normalize(left["claim"]), normalize(right["claim"])
        ids = [left["id"], right["id"]]
        if first == second:
            derived_agreements.append({"source_ids": ids, "note": left["claim"]})
        elif re.sub(r"\bnot ", "", first) == re.sub(r"\bnot ", "", second):
            derived_conflicts.append({"source_ids": ids, "note": "Opposing claims: " + left["claim"] + " / " + right["claim"]})
    agreements = derived_agreements if agreements is None else agreements
    conflicts = derived_conflicts if conflicts is None else conflicts
    gaps = [{"source_ids": [s["id"]], "note": s["limitation"]} for s in sources] if gaps is None else gaps

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

    for category, items in comparison.items():
        for item in items:
            refs = item.get("source_ids", [])
            if refs:
                index = next(i for i, source in enumerate(sources) if source["id"] == refs[0])
                summary[index] += f' ({category}, {",".join(refs)}: {item["note"]})'

    return {
        "topic": topic,
        "executive_summary": summary,
        "recommended_next_questions": next_questions or []
    }


def run_deep_research(
    topic,
    sources=None,
    agreements=None,
    conflicts=None,
    gaps=None,
    next_questions=None
):
    """Run the complete Deep Research Agent workflow."""

    if not topic:
        return {"status": "error", "message": "Research topic is required."}

    try:
        if sources is None:
            import json
            from pathlib import Path
            catalog = json.loads(Path(__file__).with_name("research_sources.json").read_text())
            terms = set(re.findall(r"[a-z]+", topic.lower()))
            sources = [s for s in catalog if terms.intersection(s["keywords"])]
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
            next_questions if next_questions is not None else [
                f'What evidence would address "{gap["note"]}"?' for gap in comparison["gaps"]
            ]
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
