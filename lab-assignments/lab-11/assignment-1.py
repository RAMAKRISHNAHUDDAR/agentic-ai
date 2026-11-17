"""
Lab 11 Assignment 1:
A Second, Concurrent Story

Processes CSV and PDF export stories through the same SDLC pipeline.
Each artifact is linked to its corresponding story ID.
"""

FEATURE_REQUEST = "Add CSV and PDF export to the reports page."


def requirement_agent(request):
    return [
        {
            "id": "US-1",
            "text": "Export the filtered report as CSV.",
            "acceptance_criteria": [
                "CSV file is produced",
                "CSV contains only filtered rows",
                "CSV headers match visible columns"
            ]
        },
        {
            "id": "US-2",
            "text": "Export the filtered report as PDF.",
            "acceptance_criteria": [
                "PDF file is produced",
                "PDF contains only filtered rows",
                "PDF includes visible column names"
            ]
        }
    ]


def human_confirms_stories(stories):
    print("[HUMAN CHECKPOINT] Reviewing stories...")

    for story in stories:
        print(f"Confirmed {story['id']}: {story['text']}")

    return True


def design_agent(stories):
    designs = {}

    for story in stories:
        if story["id"] == "US-1":
            components = [
                "csv_export_endpoint",
                "csv_serializer",
                "csv_export_button"
            ]
        else:
            components = [
                "pdf_export_endpoint",
                "pdf_generator",
                "pdf_export_button"
            ]

        designs[story["id"]] = {
            "story_id": story["id"],
            "components": components
        }

    return designs


def coding_agent(designs, stories):
    implementations = {}

    def csv_export(rows, filters, columns):
        filtered = [
            row for row in rows
            if all(row.get(k) == v for k, v in filters.items())
        ]

        output = [",".join(columns)]

        for row in filtered:
            output.append(
                ",".join(str(row.get(c, "")) for c in columns)
            )

        return "\n".join(output)

    def pdf_export(rows, filters, columns):
        filtered = [
            row for row in rows
            if all(row.get(k) == v for k, v in filters.items())
        ]

        output = ["PDF REPORT", " | ".join(columns)]

        for row in filtered:
            output.append(
                " | ".join(str(row.get(c, "")) for c in columns)
            )

        return "\n".join(output)

    for story in stories:
        story_id = story["id"]

        if story_id == "US-1":
            function = csv_export
        else:
            function = pdf_export

        implementations[story_id] = {
            "story_id": story_id,
            "design_ref": designs[story_id]["components"],
            "export_function": function
        }

    return implementations


def testing_agent(stories):
    """
    Tests are derived from acceptance criteria,
    not from implementation code.
    """

    test_artifacts = {}

    def test_csv(export_fn):
        rows = [
            {"region": "North", "sales": 100},
            {"region": "South", "sales": 200},
            {"region": "North", "sales": 150}
        ]

        output = export_fn(
            rows,
            {"region": "North"},
            ["region", "sales"]
        )

        return [
            ("CSV output produced", output.startswith("region,sales")),
            ("Filtered rows only", "South" not in output),
            ("Header included", output.splitlines()[0] == "region,sales")
        ]

    def test_pdf(export_fn):
        rows = [
            {"region": "North", "sales": 100},
            {"region": "South", "sales": 200},
            {"region": "North", "sales": 150}
        ]

        output = export_fn(
            rows,
            {"region": "North"},
            ["region", "sales"]
        )

        return [
            ("PDF output produced", output.startswith("PDF REPORT")),
            ("Filtered rows only", "South" not in output),
            ("Header included", "region | sales" in output)
        ]

    for story in stories:
        story_id = story["id"]

        if story_id == "US-1":
            test_function = test_csv
        else:
            test_function = test_pdf

        test_artifacts[story_id] = {
            "story_id": story_id,
            "acceptance_criteria": story["acceptance_criteria"],
            "test_function": test_function
        }

    return test_artifacts


def review_agent(designs, implementations, test_artifacts):
    reviews = {}

    for story_id in designs:
        implementation = implementations[story_id]
        tests = test_artifacts[story_id]

        results = tests["test_function"](
            implementation["export_function"]
        )

        issues = []

        if implementation["story_id"] != story_id:
            issues.append("Incorrect implementation lineage")

        if not all(passed for _, passed in results):
            issues.append("One or more tests failed")

        reviews[story_id] = {
            "story_id": story_id,
            "test_results": results,
            "issues": issues,
            "clean": len(issues) == 0
        }

    return reviews


def human_final_decision(reviews):
    print("\n[HUMAN CHECKPOINT] Reviewing both stories...")

    decisions = {}

    for story_id, review in reviews.items():
        decisions[story_id] = (
            "accept" if review["clean"] else "reject"
        )

        print(f"{story_id}: {decisions[story_id]}")

    return decisions


def release_agent(decisions):
    releases = {}

    for story_id, decision in decisions.items():
        releases[story_id] = {
            "story_id": story_id,
            "released": decision == "accept"
        }

    return releases


if __name__ == "__main__":

    stories = requirement_agent(FEATURE_REQUEST)

    human_confirms_stories(stories)

    designs = design_agent(stories)
    implementations = coding_agent(designs, stories)
    tests = testing_agent(stories)

    reviews = review_agent(
        designs,
        implementations,
        tests
    )

    decisions = human_final_decision(reviews)
    releases = release_agent(decisions)

    print("\n=== Test Results ===")

    for story_id, review in reviews.items():
        print(f"\n{story_id}")

        for name, passed in review["test_results"]:
            print(f" [{'PASS' if passed else 'FAIL'}] {name}")

    print("\n=== Artifact Lineage ===")

    for story_id in designs:
        print(f"\nStory: {story_id}")
        print(f"Design: {designs[story_id]['story_id']}")
        print(f"Code: {implementations[story_id]['story_id']}")
        print(f"Tests: {tests[story_id]['story_id']}")
        print(f"Review: {reviews[story_id]['story_id']}")
        print(f"Release: {releases[story_id]['story_id']}")

    print("\n=== Final Releases ===")
    for story_id, release in releases.items():
        print(story_id, release)