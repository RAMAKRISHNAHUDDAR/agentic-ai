
"""
Lab 4 - Assignment 1
A Second, Isolated Topic

Demonstrates topic-scoped retrieval so database and hosting
decisions do not leak into each other's answers.
"""

from dataclasses import dataclass


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
    def __init__(self, memory):
        self.memory = memory

    def answer(self, topic):
        hits = self.memory.retrieve(topic)

        if not hits:
            return f"[session] No stored decision on '{topic}' yet."

        latest = hits[-1]

        return (
            f"[memory, dated {latest.date}] "
            f"Per the decision on {latest.date}, {latest.fact}"
        )


if __name__ == "__main__":
    memory = ProjectMemory()

    # Store two independent topic records.
    memory.write(
        MemoryRecord(
            topic="database",
            fact="we chose PostgreSQL",
            date="2026-07-03",
        )
    )

    memory.write(
        MemoryRecord(
            topic="hosting",
            fact="we chose AWS for hosting",
            date="2026-07-04",
        )
    )

    assistant = ProjectAssistant(memory)

    print("=== Database question ===")
    print(assistant.answer("database"))

    print("\n=== Hosting question ===")
    print(assistant.answer("hosting"))

    print("\n=== Topic isolation check ===")

    database_hits = memory.retrieve("database")
    hosting_hits = memory.retrieve("hosting")

    database_isolated = (
        len(database_hits) == 1
        and database_hits[0].fact == "we chose PostgreSQL"
    )

    hosting_isolated = (
        len(hosting_hits) == 1
        and hosting_hits[0].fact == "we chose AWS for hosting"
    )

    print("Database contains only its own record:", database_isolated)
    print("Hosting contains only its own record:", hosting_isolated)

    print(
        "Conclusion:",
        "TOPIC ISOLATION SUCCESSFUL"
        if database_isolated and hosting_isolated
        else "TOPIC ISOLATION FAILED",
    )
