
"""
Lab 5 - Assignment 2
Scope read_file to a Safe Directory

Only paths inside /safe/ are permitted.
Adversarial path attempts return structured errors.
"""

import sqlite3
from pathlib import PurePosixPath


conn = sqlite3.connect(":memory:")

conn.execute("CREATE TABLE signups (event TEXT, count INTEGER)")

conn.executemany(
    "INSERT INTO signups VALUES (?, ?)",
    [
        ("AI Club Talk", 12),
        ("Hackathon Kickoff", 9),
        ("Robotics Demo", 15),
    ],
)

conn.commit()


MOCK_FILES = {
    "/safe/README.md": "Agentic AI Systems - safe directory demo.",
    "/safe/notes.txt": "This file is inside the safe directory.",
    "/secret/passwords.txt": "Confidential information.",
}

MOCK_API = {
    "events_today": ["AI Club Talk", "Robotics Demo"]
}


CAPABILITIES = [
    {
        "name": "read_file",
        "kind": "resource",
        "input": {"path": "str"},
        "output": {"content": "str"},
    },
    {
        "name": "query_db",
        "kind": "tool",
        "input": {"sql": "str"},
        "output": {"rows": "list"},
    },
    {
        "name": "call_api",
        "kind": "tool",
        "input": {"endpoint": "str"},
        "output": {"data": "any"},
    },
]


ALLOWED_CALLERS = {"planning_agent"}
SAFE_DIRECTORY = PurePosixPath("/safe")


class MCPServer:

    def list_capabilities(self):
        return CAPABILITIES

    def read_file(self, path):
        # Reject Windows-style path separators.
        if "\\" in path:
            return {
                "error": "permission denied: invalid path format"
            }

        requested_path = PurePosixPath(path)

        # Reject parent-directory traversal.
        if ".." in requested_path.parts:
            return {
                "error": "permission denied: directory traversal is not allowed"
            }

        # Only allow files directly inside /safe/.
        if (
            not requested_path.is_absolute()
            or requested_path.parent != SAFE_DIRECTORY
        ):
            return {
                "error": "permission denied: read_file only allows paths inside /safe/"
            }

        normalized_path = str(requested_path)

        if normalized_path not in MOCK_FILES:
            return {
                "error": f"file not found: {normalized_path}"
            }

        return {
            "content": MOCK_FILES[normalized_path]
        }

    def query_db(self, sql, caller):
        if caller not in ALLOWED_CALLERS:
            return {
                "error": f"caller '{caller}' is not permitted to use query_db"
            }

        if not sql.strip().upper().startswith("SELECT"):
            return {
                "error": "only SELECT statements are permitted through this tool"
            }

        cur = conn.execute(sql)

        return {"rows": cur.fetchall()}

    def call_api(self, endpoint):
        if endpoint not in MOCK_API:
            return {"error": f"unknown endpoint: {endpoint}"}

        return {"data": MOCK_API[endpoint]}


class MCPClient:

    def __init__(self, server, caller_name):
        self.server = server
        self.caller_name = caller_name

    def discover(self):
        return self.server.list_capabilities()

    def call(self, capability_name, **kwargs):
        manifest = {
            capability["name"]: capability
            for capability in self.discover()
        }

        if capability_name not in manifest:
            raise ValueError(
                f"unknown capability: {capability_name}"
            )

        method = getattr(self.server, capability_name)

        if capability_name == "query_db":
            return method(
                caller=self.caller_name,
                **kwargs,
            )

        return method(**kwargs)


if __name__ == "__main__":

    server = MCPServer()
    client = MCPClient(server, caller_name="planning_agent")

    print("=== Valid read inside safe directory ===")

    result = client.call(
        "read_file",
        path="/safe/README.md",
    )

    print(result)

    print("\n=== Adversarial test: access outside safe directory ===")

    result = client.call(
        "read_file",
        path="/secret/passwords.txt",
    )

    print(result)

    print("\n=== Adversarial test: directory traversal ===")

    result = client.call(
        "read_file",
        path="/safe/../secret/passwords.txt",
    )

    print(result)

    print("\n=== Security test result ===")

    valid_read_allowed = "content" in client.call(
        "read_file",
        path="/safe/notes.txt",
    )

    outside_read_blocked = "error" in client.call(
        "read_file",
        path="/secret/passwords.txt",
    )

    traversal_blocked = "error" in client.call(
        "read_file",
        path="/safe/../secret/passwords.txt",
    )

    print("Valid safe-directory read allowed:", valid_read_allowed)
    print("Outside-directory read blocked:", outside_read_blocked)
    print("Directory traversal blocked:", traversal_blocked)

    print(
        "Conclusion:",
        "SAFE DIRECTORY PERMISSION BOUNDARY PASSED"
        if valid_read_allowed and outside_read_blocked and traversal_blocked
        else "SECURITY TEST FAILED",
    )
