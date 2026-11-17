
"""
Lab 5 - Assignment 1
Add a Fourth, Discoverable Capability

Adds list_files as a resource capability.
The client discovers and calls it through the manifest.
"""

import sqlite3


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
    "README.md": "Agentic AI Systems - mini MCP server demo.",
    "notes.txt": "Fourth capability demonstration.",
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
    {
        "name": "list_files",
        "kind": "resource",
        "input": {},
        "output": {"files": "list"},
    },
]


ALLOWED_CALLERS = {"planning_agent"}


class MCPServer:

    def list_capabilities(self):
        return CAPABILITIES

    def read_file(self, path):
        if path not in MOCK_FILES:
            return {"error": f"file not found: {path}"}

        return {"content": MOCK_FILES[path]}

    def list_files(self):
        return {"files": list(MOCK_FILES.keys())}

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
            c["name"]: c for c in self.discover()
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

    print("=== Discover all capabilities ===")

    for capability in client.discover():
        print(
            f"{capability['name']} "
            f"({capability['kind']})"
        )

    print("\n=== Discover and call fourth capability ===")

    discovered_names = [
        capability["name"]
        for capability in client.discover()
    ]

    if "list_files" in discovered_names:
        print(client.call("list_files"))
    else:
        print("list_files capability not discovered.")
