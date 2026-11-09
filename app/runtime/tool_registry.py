
class ToolRegistry:
    """
    Central registry for registering and executing agent tools.
    """

    def __init__(self):
        self.tools = {}

    def register_tool(self, name, tool_function):
        """Register a tool using a unique name."""

        if not name:
            raise ValueError("Tool name is required")

        if not callable(tool_function):
            raise TypeError("Tool must be a callable function")

        if name in self.tools:
            raise ValueError(f"Tool '{name}' is already registered")

        self.tools[name] = tool_function

        return {
            "status": "success",
            "message": f"Tool '{name}' registered successfully"
        }

    def get_tool(self, name):
        """Retrieve a registered tool."""

        if name not in self.tools:
            raise KeyError(f"Tool '{name}' not found")

        return self.tools[name]

    def execute_tool(self, name, **kwargs):
        """Execute a registered tool."""

        tool = self.get_tool(name)

        return tool(**kwargs)

    def list_tools(self):
        """Return all registered tool names."""

        return list(self.tools.keys())


# Create the central tool registry
tool_registry = ToolRegistry()

# Import existing project tools
from app.tools.student_tools import (
    get_student_data,
    get_all_student_data
)
from app.tools.academic_tools import get_academic_data
from app.tools.attendance_tools import get_attendance
from app.tools.internship_tools import get_internship_status
from app.tools.placement_tools import get_placement_status


# Register existing tools
tool_registry.register_tool("get_student_data", get_student_data)
tool_registry.register_tool("get_all_student_data", get_all_student_data)
tool_registry.register_tool("get_academic_data", get_academic_data)
tool_registry.register_tool("get_attendance", get_attendance)
tool_registry.register_tool("get_internship_status", get_internship_status)
tool_registry.register_tool("get_placement_status", get_placement_status)
