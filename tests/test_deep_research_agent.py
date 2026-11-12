from app.agents.deep_research_agent import (
    collect_sources,
    compare,
    synthesize,
    run_deep_research
)


SOURCES = [
    {
        "id": "S1",
        "type": "peer-reviewed paper",
        "date": "2026-02",
        "author": "Sample Author 1",
        "claim": "RAG improves answer accuracy.",
        "evidence": "Illustrative evaluation of 200 questions.",
        "limitation": "Single-domain evaluation.",
        "relevance": "Academic evidence."
    },
    {
        "id": "S2",
        "type": "vendor blog",
        "date": "2026-04",
        "author": "Sample Organization 2",
        "claim": "RAG improves answer accuracy.",
        "evidence": "Illustrative internal evaluation.",
        "limitation": "No independent replication.",
        "relevance": "Industry evidence."
    },
    {
        "id": "S3",
        "type": "independent benchmark",
        "date": "2026-05",
        "author": "Sample Organization 3",
        "claim": "RAG adds processing latency.",
        "evidence": "Illustrative benchmark.",
        "limitation": "Limited benchmark scope.",
        "relevance": "Performance evidence."
    }
]


def test_collect_sources():
    result = collect_sources(SOURCES)
    assert len(result) == 3
    assert result[0]["id"] == "S1"


def test_source_validation():
    try:
        collect_sources(SOURCES[:2])
        assert False, "Expected validation error"
    except ValueError:
        pass


def test_compare_sources():
    result = compare(
        SOURCES,
        agreements=[
            {
                "source_ids": ["S1", "S2"],
                "note": "Both report improved accuracy."
            }
        ],
        gaps=[
            {
                "source_ids": ["S1", "S2", "S3"],
                "note": "Non-English performance is not evaluated."
            }
        ]
    )

    assert len(result["agreements"]) == 1
    assert len(result["gaps"]) == 1


def test_synthesize_summary():
    comparison = compare(SOURCES)

    result = synthesize(
        "Benefits and limitations of RAG",
        SOURCES,
        comparison
    )

    assert len(result["executive_summary"]) == 3
    assert "[S1]" in result["executive_summary"][0]


def test_complete_research_workflow():
    result = run_deep_research(
        topic="Benefits and limitations of RAG",
        sources=SOURCES
    )

    assert result["status"] == "success"
    assert len(result["evidence_table"]) == 3
    assert "comparison" in result
    assert "executive_summary" in result


if __name__ == "__main__":
    test_collect_sources()
    test_source_validation()
    test_compare_sources()
    test_synthesize_summary()
    test_complete_research_workflow()

    print("ALL LAB 9 TESTS PASSED")
