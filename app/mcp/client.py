import asyncio
import json
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from app.runtime.audit_logger import log_action

BASE_DIR = Path(__file__).resolve().parents[2]


async def call_mcp_tool(tool_name: str, arguments: dict):
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.server"],
        cwd=str(BASE_DIR),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            try:
                result = await session.call_tool(tool_name, arguments)

                if result.is_error:
                    output = {
                        "error": f"MCP tool failed: {tool_name}"
                    }
                    log_action(
                        arguments.get("student_id"),
                        "mcp_client",
                        "tool_call",
                        {
                            "tool_name": tool_name,
                            "tool_input": arguments,
                            "tool_output": output,
                        },
                    )
                    raise RuntimeError(
                        f"MCP tool failed: {tool_name}"
                    )

                if not result.content:
                    output = None
                else:
                    output = json.loads(result.content[0].text)

                log_action(
                    arguments.get("student_id"),
                    "mcp_client",
                    "tool_call",
                    {
                        "tool_name": tool_name,
                        "tool_input": arguments,
                        "tool_output": output,
                    },
                )

                return output

            except Exception as error:
                if not isinstance(error, RuntimeError):
                    log_action(
                        arguments.get("student_id"),
                        "mcp_client",
                        "tool_call_error",
                        {
                            "tool_name": tool_name,
                            "tool_input": arguments,
                            "error": str(error),
                        },
                    )
                raise

async def read_mcp_resource(resource_uri: str):
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.server"],
        cwd=str(BASE_DIR),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.read_resource(resource_uri)

            if not result.contents:
                return ""

            return result.contents[0].text


# 1. Get one student from MongoDB Atlas through MCP
async def get_student_from_mcp(student_id: str):
    return await call_mcp_tool(
        "get_student_from_database",
        {"student_id": student_id},
    )


def get_student(student_id: str):
    try:
        return asyncio.run(get_student_from_mcp(student_id))
    except Exception as error:
        return {"error": str(error)}


# 2. Get all students through MCP
async def get_all_students_from_mcp():
    return await call_mcp_tool(
        "get_all_students_from_database",
        {},
    )


def get_all_students():
    try:
        result = asyncio.run(get_all_students_from_mcp())

        if isinstance(result, dict) and "students" in result:
            return result["students"]

        return result
    except Exception as error:
        return {"error": str(error)}


# 3. Read the students CSV resource through MCP
async def get_student_file_from_mcp():
    return await read_mcp_resource("file://students")


def get_student_file():
    try:
        return asyncio.run(get_student_file_from_mcp())
    except Exception as error:
        return {"error": str(error)}


# 4. Get student data from the mock API tool through MCP
async def get_student_api_data_from_mcp(student_id: str):
    return await call_mcp_tool(
        "get_student_api_data",
        {"student_id": student_id},
    )


def get_student_api_data(student_id: str):
    try:
        return asyncio.run(
            get_student_api_data_from_mcp(student_id)
        )
    except Exception as error:
        return {"error": str(error)}