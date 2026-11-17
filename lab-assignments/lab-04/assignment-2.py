
"""
Lab 4 - Assignment 2
A Staleness / Retention Policy

Warns when retrieved memory is older than the configured
retention period.
"""

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class MemoryRecord:
    topic: str
    fact: str
    date: str
    source: str = "memory"


class ProjectMemory:
    def __init__(self):
        self.records = []

    def write(self, record):
        self.records.append(record)

    def retrieve(self, topic):
        return [
            record for record in self.records
            if record.topic == topic
        ]


class ProjectAssistant:
    def __init__(self, memory, retention_days=30):
        self.memory = memory
        self.retention_days = retention_days

    def answer(self, topic):
        hits = self.memory.retrieve(topic)

        if not hits:
            return f"[session] No stored decision on '{topic}' yet."

        latest = hits[-1]

        record_date = date.fromisoformat(latest.date)
        age_days = (date.today() - record_date).days

        if age_days < 0:
            return (
                f"[warning] The memory date for '{topic}' "
                "is in the future. Please verify it before use."
            )

        if age_days > self.retention_days:
            return (
                f"[warning] This decision is from {age_days} days ago "
                f"and may be out of date. "
                f"Stored decision: {latest.fact}"
            )

        return (
            f"[memory, dated {latest.date}] "
            f"Per the decision on {latest.date}, {latest.fact}"
        )


if __name__ == "__main__":
    memory = ProjectMemory()

    # Fresh record: one day old.
    fresh_date = date.today() - timedelta(days=1)

    memory.write(
        MemoryRecord(
            topic="database",
            fact="we chose PostgreSQL",
            date=fresh_date.isoformat(),
        )
    )

    # Old record: 90 days old.
    old_date = date.today() - timedelta(days=90)

    memory.write(
        MemoryRecord(
            topic="hosting",
            fact="we chose AWS for hosting",
            date=old_date.isoformat(),
        )
    )

    assistant = ProjectAssistant(
        memory,
        retention_days=30,
    )

    print("Retention period:", assistant.retention_days, "days")

    print("\n=== Fresh memory test ===")
    print(assistant.answer("database"))

    print("\n=== Old memory test ===")
    print(assistant.answer("hosting"))
