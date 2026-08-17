from typing import Callable, Dict, Any, Optional

from core.result import ToolResult


class ToolRegistry:
    """
    Central registry for all SAHVIA tools.

    The registry allows SAHVIA to:
    - Register tools
    - Find tools by name
    - Execute tools dynamically
    - List available tools
    """

    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}

    # ==========================================
    # REGISTER TOOL
    # ==========================================

    def register(
        self,
        name: str,
        function: Callable,
        description: str = ""
    ) -> None:
        """
        Register a tool with SAHVIA.
        """

        if not name:
            raise ValueError("Tool name cannot be empty.")

        if not callable(function):
            raise TypeError(
                f"Tool '{name}' must be callable."
            )

        if name in self._tools:
            raise ValueError(
                f"Tool '{name}' is already registered."
            )

        self._tools[name] = {
            "function": function,
            "description": description
        }

    # ==========================================
    # UNREGISTER TOOL
    # ==========================================

    def unregister(self, name: str) -> bool:
        """
        Remove a tool from the registry.
        """

        if name not in self._tools:
            return False

        del self._tools[name]
        return True

    # ==========================================
    # GET TOOL
    # ==========================================

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a registered tool.
        """

        return self._tools.get(name)

    # ==========================================
    # CHECK TOOL
    # ==========================================

    def exists(self, name: str) -> bool:
        """
        Check whether a tool exists.
        """

        return name in self._tools

    # ==========================================
    # LIST TOOLS
    # ==========================================

    def list_tools(self) -> Dict[str, str]:
        """
        Return all registered tools and descriptions.
        """

        return {
            name: info["description"]
            for name, info in self._tools.items()
        }

    # ==========================================
    # EXECUTE TOOL
    # ==========================================

    def execute(self, name: str, *args, **kwargs) -> ToolResult:
        """
        Execute a registered tool.

        Every tool is expected to return ToolResult.
        """

        tool = self.get(name)

        if tool is None:
            return ToolResult.fail(
                error=f"Tool '{name}' was not found."
            )

        function = tool["function"]

        try:
            result = function(*args, **kwargs)

            # ----------------------------------
            # Tool already returned ToolResult
            # ----------------------------------

            if isinstance(result, ToolResult):
                return result

            # ----------------------------------
            # Automatically wrap normal results
            # ----------------------------------

            return ToolResult.ok(
                message=str(result) if result is not None else "Tool executed successfully.",
                data=result
            )

        except Exception as error:
            return ToolResult.fail(
                error=str(error),
                message=f"Tool '{name}' failed."
            )


# ==========================================
# GLOBAL REGISTRY
# ==========================================

registry = ToolRegistry()


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    def test_tool(name: str):
        return f"Hello {name}! SAHVIA tool is working."

    registry.register(
        name="test_tool",
        function=test_tool,
        description="A test tool for SAHVIA."
    )

    print("\nAvailable tools:")
    print(registry.list_tools())

    print("\nTool exists:")
    print(registry.exists("test_tool"))

    print("\nExecuting tool:")

    result = registry.execute(
        "test_tool",
        "Saksham"
    )

    print(result)

    print("\nResult success:")
    print(result.success)