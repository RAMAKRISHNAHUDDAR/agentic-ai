
"""
Lab 3 - Assignment 1
Handle a Multi-Claim Source
"""

ARTICLE_C = {
    "title": "Campus AI Platform: Cost and Accuracy Evaluation",
    "text": (
        "The campus AI platform reduced operating costs by 25%. "
        "The cost reduction was measured using six months of verified "
        "infrastructure billing records before and after deployment. "
        "The platform also improved answer accuracy by 40%. "
        "The accuracy improvement was based on informal feedback from "
        "three students and was not measured using a formal benchmark."
    ),
}


def apply_research_summary_skill(article):
    text = article["text"]
    sentences = [s.strip() for s in text.split(".") if s.strip()]

    # Identify separate claims and their supporting evidence.
    claims = [
        sentence for sentence in sentences
        if "reduced" in sentence.lower()
        or "improved" in sentence.lower()
    ]

    evidence_sentences = [
        sentence for sentence in sentences
        if "measured" in sentence.lower()
        or "records" in sentence.lower()
        or "feedback" in sentence.lower()
        or "benchmark" in sentence.lower()
    ]

    # Select the claim supported by stronger, more verifiable evidence.
    selected_claim = claims[0]
    selected_evidence = evidence_sentences[0]

    selection_note = (
        "Two competing claims were identified: cost reduction and "
        "accuracy improvement. The cost-reduction claim was selected "
        "because it is supported by verified infrastructure billing "
        "records, whereas the accuracy claim relies on informal feedback."
    )

    limitation = (
        "The accuracy improvement was based on informal feedback from "
        "three students and was not measured using a formal benchmark."
    )

    takeaway = (
        f"Undergraduate takeaway: {selected_claim} "
        "is supported by stronger evidence, but the accuracy claim "
        "needs formal evaluation."
    )

    return {
        "claim": selected_claim,
        "evidence": selected_evidence,
        "limitation": limitation,
        "takeaway": takeaway,
        "selection_note": selection_note,
    }


def print_skill_output(article, output):
    print(f"\n--- {article['title']} ---")
    print(f"Selected Claim: {output['claim']}")
    print(f"Evidence: {output['evidence']}")
    print(f"Limitation: {output['limitation']}")
    print(f"Selection Note: {output['selection_note']}")
    print(f"Takeaway: {output['takeaway']}")


if __name__ == "__main__":
    output = apply_research_summary_skill(ARTICLE_C)
    print_skill_output(ARTICLE_C, output)
