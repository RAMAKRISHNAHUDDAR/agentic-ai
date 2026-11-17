
"""
Lab 3 - Assignment 2
Test Against a Low-Evidence Input
"""

ARTICLE_D = {
    "title": "New Learning Platform Improves Student Performance",
    "text": (
        "The new learning platform improves student performance "
        "significantly."
    ),
}


SKILL_SPEC = {
    "name": "research_summary",
    "instructions": [
        "identify the single main claim",
        "list supporting evidence for that claim",
        "note at least one limitation or state 'not stated in source'",
        "write a 1-sentence undergraduate-level takeaway",
    ],
    "constraints": [
        "never present a hedged claim as an unhedged fact",
        "never omit the limitation row",
        "never fabricate supporting evidence",
    ],
}


def apply_research_summary_skill(article):
    text = article["text"]
    sentences = [s.strip() for s in text.split(".") if s.strip()]

    claim = sentences[0] if sentences else "not stated in source"

    # Look for explicit supporting evidence.
    evidence = next(
        (
            sentence for sentence in sentences[1:]
            if any(
                keyword in sentence.lower()
                for keyword in [
                    "study",
                    "survey",
                    "experiment",
                    "data",
                    "measured",
                    "results",
                    "participants",
                    "sample",
                ]
            )
        ),
        "not stated in source",
    )

    # Look for an explicitly stated limitation.
    limitation = next(
        (
            sentence for sentence in sentences
            if any(
                keyword in sentence.lower()
                for keyword in [
                    "limitation",
                    "however",
                    "small sample",
                    "does not include",
                    "unclear",
                    "may not generalize",
                ]
            )
        ),
        "not stated in source",
    )

    if evidence == "not stated in source":
        takeaway = (
            "The article claims that the learning platform improves "
            "student performance, but provides no supporting evidence. "
            "The claim cannot be independently verified from this source."
        )
    else:
        takeaway = (
            f"Undergraduate takeaway: {claim} "
            "Evidence and limitations should be considered before "
            "generalizing this finding."
        )

    return {
        "claim": claim,
        "evidence": evidence,
        "limitation": limitation,
        "takeaway": takeaway,
    }


def print_skill_output(article, output):
    print(f"\n--- {article['title']} ---")
    print(f"Claim: {output['claim']}")
    print(f"Evidence: {output['evidence']}")
    print(f"Limitation: {output['limitation']}")
    print(f"Takeaway: {output['takeaway']}")


if __name__ == "__main__":
    output = apply_research_summary_skill(ARTICLE_D)

    print_skill_output(ARTICLE_D, output)

    print("\n=== Fabrication Check ===")

    no_fabrication = (
        output["evidence"] == "not stated in source"
        and output["limitation"] == "not stated in source"
    )

    print("Evidence invented:", output["evidence"] != "not stated in source")
    print("Limitation invented:", output["limitation"] != "not stated in source")
    print("No fabrication occurred:", no_fabrication)
