
import json
import re
from itertools import combinations
from pathlib import Path


STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "what", "which", "who", "how", "why", "when",
    "does", "do", "did", "can", "could", "would",
    "should", "of", "to", "for", "in", "on", "with",
    "and", "or", "our", "their", "this", "that",
    "these", "those", "about", "contribute",
    "contributes", "influence", "influences",
    "explain", "student", "students"
}


def tokenize(text):
    """Normalize text into meaningful searchable terms."""
    words = re.findall(r"[a-z0-9]+", text.lower())

    return {
        word for word in words
        if word not in STOP_WORDS and len(word) > 2
    }


def collect_sources(sources):
    """Validate and organize research sources."""

    if not isinstance(sources, list) or len(sources) < 3:
        raise ValueError("At least 3 research sources are required.")

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

        if not isinstance(source.get("keywords", []), list):
            raise ValueError("Source keywords must be a list.")

    return sources


def retrieve_sources(topic, catalog):
    """Retrieve and rank sources using keyword and phrase relevance."""

    query_terms = tokenize(topic)
    query_text = " ".join(re.findall(r"[a-z0-9]+", topic.lower()))

    if not query_terms:
        return []

    ranked = []

    for source in catalog:
        keywords = source.get("keywords", [])
        topics = source.get("topics", [])

        searchable_fields = [
            source.get("claim", ""),
            source.get("evidence", ""),
            source.get("limitation", ""),
            source.get("relevance", "")
        ]

        keyword_terms = set()
        for keyword in keywords:
            keyword_terms.update(tokenize(keyword))

        topic_terms = set()
        for item in topics:
            topic_terms.update(tokenize(item))

        content_terms = set()
        for field in searchable_fields:
            content_terms.update(tokenize(field))

        keyword_matches = query_terms.intersection(keyword_terms)
        topic_matches = query_terms.intersection(topic_terms)
        content_matches = query_terms.intersection(content_terms)

        score = (
            len(keyword_matches) * 3
            + len(topic_matches) * 4
            + len(content_matches)
        )

        phrases = keywords + topics

        for phrase in phrases:
            normalized = " ".join(
                re.findall(r"[a-z0-9]+", phrase.lower())
            )

            if len(normalized.split()) > 1 and normalized in query_text:
                score += 5

        if score > 0:
            ranked.append((score, source))

    ranked.sort(key=lambda item: item[0], reverse=True)

    return [
        {**source, "relevance_score": score}
        for score, source in ranked
    ]


def normalize_claim(claim):
    """Normalize claims while preserving negation."""

    return tokenize(claim)


def compare(sources, agreements=None, conflicts=None, gaps=None):
    """Compare claims and identify evidence limitations."""

    valid_ids = {source["id"] for source in sources}

    derived_agreements = []
    derived_conflicts = []

    for left, right in combinations(sources, 2):
        first = normalize_claim(left["claim"])
        second = normalize_claim(right["claim"])

        ids = [left["id"], right["id"]]

        if first == second:
            derived_agreements.append({
                "source_ids": ids,
                "note": left["claim"]
            })

        else:
            # Check whether claims have the same core wording
            # but opposite negation.
            first_without_negation = first - {"not", "no", "never"}
            second_without_negation = second - {"not", "no", "never"}

            first_negated = bool(first.intersection({"not", "no", "never"}))
            second_negated = bool(second.intersection({"not", "no", "never"}))

            if (
                first_without_negation == second_without_negation
                and first_negated != second_negated
            ):
                derived_conflicts.append({
                    "source_ids": ids,
                    "note": (
                        "Opposing claims: "
                        + left["claim"] + " / " + right["claim"]
                    )
                })

    agreements = (
        derived_agreements if agreements is None else agreements
    )

    conflicts = (
        derived_conflicts if conflicts is None else conflicts
    )

    gaps = (
        [
            {"source_ids": [s["id"]], "note": s["limitation"]}
            for s in sources
        ]
        if gaps is None else gaps
    )

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
    """Generate a source-traceable executive summary."""

    summary = []

    for source in sources:
        summary.append(
            f'[{source["id"]}] {source["claim"]}'
        )

    for category, items in comparison.items():
        for item in items:
            refs = item.get("source_ids", [])

            if refs:
                index = next(
                    (
                        i for i, source in enumerate(sources)
                        if source["id"] == refs[0]
                    ),
                    None
                )

                if index is not None:
                    summary[index] += (
                        f' ({category}, {",".join(refs)}: '
                        f'{item["note"]})'
                    )

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
    """Execute the complete rule-based research workflow."""

    if not isinstance(topic, str) or not topic.strip():
        return {
            "status": "error",
            "message": "Research topic is required."
        }

    try:
        if sources is None:
            catalog_path = Path(__file__).with_name(
                "research_sources.json"
            )

            catalog = json.loads(
                catalog_path.read_text(encoding="utf-8")
            )

            sources = retrieve_sources(topic, catalog)

        evidence = collect_sources(sources)

        comparison = compare(
            evidence,
            agreements,
            conflicts,
            gaps
        )

        if next_questions is None:
            questions = [
                f'What evidence would address "{gap["note"]}"?'
                for gap in comparison["gaps"]
            ]

            if len(evidence) < 3:
                questions.append(
                    f'What additional sources are available about "{topic}"?'
                )
        else:
            questions = next_questions

        summary = synthesize(
            topic,
            evidence,
            comparison,
            questions
        )

        return {
            "status": "success",
            "research_question": topic,
            "sources": evidence,
            "evidence_table": evidence,
            "comparison": comparison,
            "executive_summary": summary["executive_summary"],
            "recommended_next_questions":
                summary["recommended_next_questions"],
            "retrieval": {
                "total_sources_found": len(evidence),
                "source_ids": [s["id"] for s in evidence]
            }
        }

    except (ValueError, TypeError, OSError, json.JSONDecodeError) as error:
        return {
            "status": "error",
            "message": str(error)
        }
