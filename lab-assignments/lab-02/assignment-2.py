
"""
Lab 2 - Assignment 2
A Three-Tool Chain

Read CSV -> Filter by category -> Calculate average
"""

import csv
import io


SIGNUPS_CSV = """event,signups,category
AI Club Talk,12,technical
Hackathon Kickoff,9,technical
Robotics Demo,15,technical
GenAI Workshop,7,technical
Capstone Expo,20,technical
Career Panel,11,social
"""


def read_csv(source_text=SIGNUPS_CSV):
    reader = csv.DictReader(io.StringIO(source_text))
    rows = list(reader)

    if not rows:
        return {
            "error": "empty file",
            "rows": [],
            "row_count": 0,
        }

    return {
        "rows": rows,
        "row_count": len(rows),
    }


def filter_rows(rows, category):
    filtered = [
        row for row in rows
        if row["category"].strip().lower() == category.lower()
    ]

    return {
        "rows": filtered,
        "row_count": len(filtered),
        "category": category,
    }


def calculator(operation, values):
    if operation == "average":
        if not values:
            return {"error": "no values supplied"}

        return {"result": sum(values) / len(values)}

    if operation == "sum":
        return {"result": sum(values)}

    return {"error": f"unsupported operation: {operation}"}


TOOLS = {
    "read_csv": read_csv,
    "filter_rows": filter_rows,
    "calculator": calculator,
}


class CampusDataAssistant:
    def __init__(self):
        self.trace = []

    def _call(self, tool_name, reason, **kwargs):
        result = TOOLS[tool_name](**kwargs)

        entry = {
            "tool": tool_name,
            "reason": reason,
            "input": kwargs,
            "output": result,
        }

        self.trace.append(entry)

        if "error" in result:
            raise RuntimeError(
                f"{tool_name} failed: {result['error']}"
            )

        return result

    def answer(self, question):
        q = question.lower()

        if "average" in q and "technical" in q:
            # Tool 1: Read CSV
            csv_result = self._call(
                "read_csv",
                "read event sign-up data from the CSV file",
            )

            # Tool 2: Filter by category
            filtered_result = self._call(
                "filter_rows",
                "select only technical category events",
                rows=csv_result["rows"],
                category="technical",
            )

            # Validate filter output before calculating
            if not filtered_result["rows"]:
                return (
                    "No technical events were found. "
                    "Average cannot be calculated."
                )

            # Tool 3: Calculate average
            values = [
                int(row["signups"])
                for row in filtered_result["rows"]
            ]

            average_result = self._call(
                "calculator",
                "calculate average sign-ups for filtered technical events",
                operation="average",
                values=values,
            )

            return (
                f"Average sign-ups for technical events: "
                f"{average_result['result']:.2f} "
                f"(across {filtered_result['row_count']} events)."
            )

        return "I don't have a tool path configured for that question."


if __name__ == "__main__":
    assistant = CampusDataAssistant()

    question = (
        "What's the average sign-up for technical events only?"
    )

    print("Q:", question)
    print("A:", assistant.answer(question))

    print("\n=== Full Three-Tool Trace ===")

    for i, entry in enumerate(assistant.trace, 1):
        print(f"\n{i}. Tool: {entry['tool']}")
        print("   Reason:", entry["reason"])
        print("   Input:", entry["input"])
        print("   Output:", entry["output"])
