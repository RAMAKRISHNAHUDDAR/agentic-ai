"""
Lab 11 Assignment 2:
Prove Test Independence With a Deliberate Bug

The implementation contains an intentional filtering bug.
The independent tests should detect the regression.
"""


FEATURE_REQUEST = "Add CSV export to the reports page, preserving applied filters."


def requirement_agent(request):
    return [
        {
            "id": "US-1",
            "text": "Export the filtered report as CSV.",
            "acceptance_criteria": [
                "CSV file is produced",
                "CSV contains only rows matching applied filters",
                "CSV headers match visible column names"
            ]
        }
    ]


def design_agent(stories):
    return {
        "story_id": stories[0]["id"],
        "components": [
            "export_endpoint",
            "csv_serializer",
            "export_button"
        ]
    }


def coding_agent(design, stories):
    """
    INTENTIONAL BUG:
    The filter condition is inverted.
    Instead of selecting matching rows, it selects non-matching rows.
    """

    def export_endpoint(rows, applied_filters, columns):

        # Deliberate bug: != instead of ==
        filtered = [
            row for row in rows
            if all(
                row.get(k) != v
                for k, v in applied_filters.items()
            )
        ]

        lines = [",".join(columns)]

        for row in filtered:
            lines.append(
                ",".join(str(row.get(c, "")) for c in columns)
            )

        return "\n".join(lines)

    return {
        "design_ref": design["components"],
        "export_endpoint": export_endpoint
    }


def testing_agent(stories):
    """
    Independent tests generated from acceptance criteria.
    This function does not inspect or modify coding_agent.
    """

    def test_suite(export_fn):
        rows = [
            {"region": "North", "sales": 100},
            {"region": "South", "sales": 200},
            {"region": "North", "sales": 150}
        ]

        columns = ["region", "sales"]

        output = export_fn(
            rows,
            {"region": "North"},
            columns
        )

        lines = output.splitlines()

        results = []

        results.append(
            ("produces CSV output", len(output) > 0)
        )

        results.append(
            (
                "header matches visible columns",
                lines[0] == "region,sales"
            )
        )

        results.append(
            (
                "only filtered rows present",
                len(lines) > 1
                and all("North" in line for line in lines[1:])
                and all("South" not in line for line in lines[1:])
            )
        )

        return results

    return test_suite


def review_agent(design, code, test_results):
    issues = []

    if not all(passed for _, passed in test_results):
        issues.append(
            "Regression detected: one or more acceptance tests failed"
        )

    return {
        "issues": issues,
        "clean": len(issues) == 0
    }


def human_final_decision(review):
    print("\n[HUMAN CHECKPOINT] Reviewing test failures...")

    decision = "accept" if review["clean"] else "reject"

    print("Decision:", decision)

    return decision


if __name__ == "__main__":

    stories = requirement_agent(FEATURE_REQUEST)

    design = design_agent(stories)

    code = coding_agent(design, stories)

    test_suite = testing_agent(stories)

    test_results = test_suite(
        code["export_endpoint"]
    )

    print("=== Independent Test Results ===")

    for name, passed in test_results:
        print(f" [{'PASS' if passed else 'FAIL'}] {name}")

    review = review_agent(
        design,
        code,
        test_results
    )

    print("\n=== Review ===")
    print(review)

    decision = human_final_decision(review)

    print("\n=== Final Result ===")
    print("Pipeline decision:", decision)

    assert decision == "reject", (
        "The independent tests should detect the deliberate bug."
    )

    print("\nConfirmed: independent tests detected the filtering bug.")