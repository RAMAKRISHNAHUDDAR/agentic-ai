import asyncio
from pathlib import Path
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


BASE_DIR = Path(__file__).resolve().parents[2]


async def get_student_from_mcp(student_id: str):
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.server"],
        cwd=str(BASE_DIR),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "get_student_from_database",
                {"student_id": student_id},
            )

            return result


def get_student(student_id: str):
    result = asyncio.run(get_student_from_mcp(student_id))

    if result.is_error:
        return {"error": "MCP request failed"}

    return json.loads(result.content[0].text)