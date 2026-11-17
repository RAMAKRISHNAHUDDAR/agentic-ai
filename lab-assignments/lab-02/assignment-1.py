
"""
Lab 2 - Assignment 1
Add a Notification Tool with Justified Use

The notification tool only drafts a message.
It does not send anything.
"""

import csv
import io


SIGNUPS_CSV = """event,signups
AI Club Talk,12
Hackathon Kickoff,9
Robotics Demo,15
GenAI Workshop,7
Capstone Expo,20
Career Panel,11
"""

NOTIFICATION_THRESHOLD = 13


def calculator(operation, values):
    if operation == "average":
        if not values:
            return {"error": "no values supplied"}
        return {"result": sum(values) / len(values)}

    if operation == "sum":
        return {"result": sum(values)}

    return {"error": f"unsupported operation: {operation}"}


def read_csv(source_text=SIGNUPS_CSV):
    reader = csv.DictReader(io.StringIO(source_text))
    rows = list(reader)

    if not rows:
        return {"error": "empty file", "rows": [], "row_count": 0}

    return {"rows": rows, "row_count": len(rows)}


def send_notification(message, recipient="Campus Event Team"):
    """
    Draft a notification message only.
    No actual notification is sent.
    """
    return {
        "status": "drafted",
        "recipient": recipient,
        "message": message,
        "sent": False,
    }


TOOLS = {
    "calculator": calculator,
    "read_csv": read_csv,
    "send_notification": send_notification,
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

        if "average" in q and "sign" in q:
            csv_result = self._call(
                "read_csv",
                "sign-up counts are stored in the CSV export",
            )

            values = [
                int(row["signups"])
                for row in csv_result["rows"]
            ]

            avg = self._call(
                "calculator",
                "calculate average sign-ups per event",
                operation="average",
                values=values,
            )

            average = avg["result"]

            if average < NOTIFICATION_THRESHOLD:
                notification = self._call(
                    "send_notification",
                    (
                        f"Average sign-ups {average:.2f} are below "
                        f"the threshold of {NOTIFICATION_THRESHOLD}; "
                        "draft a low-turnout notice for the event team."
                    ),
                    message=(
                        "Low event turnout notice: The average "
                        f"sign-ups per event are {average:.2f}, "
                        f"below the threshold of "
                        f"{NOTIFICATION_THRESHOLD}. Please review "
                        "event promotion and participation."
                    ),
                )

                return (
                    f"Average sign-ups per event: {average:.2f}.\n"
                    f"Threshold: {NOTIFICATION_THRESHOLD}.\n"
                    f"Notification status: {notification['status']}.\n"
                    f"Draft: {notification['message']}\n"
                    "No notification was actually sent."
                )

            return (
                f"Average sign-ups per event: {average:.2f}. "
                f"This is not below the threshold of "
                f"{NOTIFICATION_THRESHOLD}. "
                "No notification draft is needed."
            )

        return "I don't have a tool path configured for that question."


if __name__ == "__main__":
    assistant = CampusDataAssistant()

    question = (
        "What is the average sign-up count for events, "
        "and should a low-turnout notification be drafted?"
    )

    print("Q:", question)
    print("A:", assistant.answer(question))

    print("\n=== Full Tool Trace ===")

    for i, entry in enumerate(assistant.trace, 1):
        print(f"\n{i}. Tool: {entry['tool']}")
        print("   Reason:", entry["reason"])
        print("   Input:", entry["input"])
        print("   Output:", entry["output"])
