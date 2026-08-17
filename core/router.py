from typing import Optional, Dict, Any

from core.result import ToolResult
from core.registry import ToolRegistry, registry
from core.memory import SahviaMemory
from brain.ollama_brain import OllamaBrain


class CommandRouter:

    def __init__(
        self,
        registry: ToolRegistry,
        brain: Optional[OllamaBrain] = None,
        memory: Optional[SahviaMemory] = None
    ):

        self.registry = registry

        self.brain = brain or OllamaBrain()

        self.memory = memory or SahviaMemory(
            max_entries=12
        )

        self.command_map = {

            "maximize":
                "maximize_window",

            "maximize window":
                "maximize_window",

            "maximize this window":
                "maximize_window",

            "minimize":
                "minimize_window",

            "minimize window":
                "minimize_window",

            "minimize this window":
                "minimize_window",

            "close window":
                "close_window",

            "close this window":
                "close_window",

            "show desktop":
                "show_desktop",

            "new tab":
                "new_tab",

            "open new tab":
                "new_tab",

            "new window":
                "new_window",

            "open new window":
                "new_window",

            "close tab":
                "close_tab",

            "close this tab":
                "close_tab",

            "next tab":
                "next_tab",

            "switch tab":
                "next_tab",

            "go back":
                "go_back",

            "go forward":
                "go_forward",

            "refresh":
                "refresh_page",

            "refresh page":
                "refresh_page",
        }

    # ==========================================
    # NORMALIZE
    # ==========================================

    def normalize(
        self,
        command: str
    ) -> str:

        if not isinstance(
            command,
            str
        ):

            return ""

        command = command.lower().strip()

        command = " ".join(
            command.split()
        )

        for character in [
            ".",
            "!",
            "?"
        ]:

            command = command.replace(
                character,
                ""
            )

        return command

    # ==========================================
    # FIND DIRECT TOOL
    # ==========================================

    def find_direct_tool(
        self,
        command: str
    ) -> Optional[str]:

        return self.command_map.get(
            self.normalize(command)
        )

    # ==========================================
    # EXECUTE TOOL
    # ==========================================

    def execute_tool(
        self,
        tool_name: str,
        arguments: Optional[Dict[str, Any]] = None
    ) -> ToolResult:

        arguments = arguments or {}

        if not self.registry.exists(
            tool_name
        ):

            return ToolResult.fail(
                error=f"Tool '{tool_name}' is not registered."
            )

        return self.registry.execute(
            tool_name,
            **arguments
        )

    # ==========================================
    # SAVE USER MESSAGE
    # ==========================================

    def remember_user(
        self,
        command: str
    ):

        self.memory.add_user_message(
            command
        )

    # ==========================================
    # SAVE ASSISTANT RESPONSE
    # ==========================================

    def remember_assistant(
        self,
        message: str
    ):

        self.memory.add_assistant_message(
            message
        )

    # ==========================================
    # ROUTE
    # ==========================================

    def route(
        self,
        command: str
    ) -> ToolResult:

        command = self.normalize(
            command
        )

        if not command:

            return ToolResult.fail(
                error="Empty command."
            )

        print(
            f"\n🧠 SAHVIA routing: {command}"
        )

        # ======================================
        # SAVE USER MESSAGE
        # ======================================

        self.remember_user(
            command
        )

        # ======================================
        # DIRECT TOOL
        # ======================================

        tool_name = self.find_direct_tool(
            command
        )

        if tool_name:

            print(
                f"🔧 Direct tool: {tool_name}"
            )

            result = self.execute_tool(
                tool_name
            )

            self.memory.record_tool(
                tool_name=tool_name,
                arguments={},
                result=str(result)
            )

            self.remember_assistant(
                str(result)
            )

            return result

        # ======================================
        # OLLAMA
        # ======================================

        print(
            "🤖 Sending command to SAHVIA brain..."
        )

        tools = self.registry.list_tools()

        memory_context = self.memory.get_context()

        decision = self.brain.ask(
            command,
            tools,
            memory_context
        )

        if not decision:

            error_message = (
                "SAHVIA brain did not return a decision."
            )

            self.remember_assistant(
                error_message
            )

            return ToolResult.fail(
                error=error_message
            )

        print(
            f"🧠 Brain decision: {decision}"
        )

        # ======================================
        # GET DECISION
        # ======================================

        selected_tool = decision.get(
            "tool"
        )

        arguments = decision.get(
            "arguments",
            {}
        )

        if not isinstance(
            arguments,
            dict
        ):

            arguments = {}

        # ======================================
        # CONVERSATION
        # ======================================

        if selected_tool is None:

            response = decision.get(
                "response",
                ""
            )

            if not response:

                response = (
                    "I'm here. How can I help you?"
                )

            self.remember_assistant(
                response
            )

            return ToolResult.ok(
                message=response
            )

        # ======================================
        # TOOL EXECUTION
        # ======================================

        print(
            f"⚙️ Executing: {selected_tool}"
        )

        result = self.execute_tool(
            selected_tool,
            arguments
        )

        # ======================================
        # SAVE TOOL MEMORY
        # ======================================

        self.memory.record_tool(
            tool_name=selected_tool,
            arguments=arguments,
            result=str(result)
        )

        self.remember_assistant(
            str(result)
        )

        return result

    # ==========================================
    # MEMORY ACCESS
    # ==========================================

    def get_memory(
        self
    ) -> SahviaMemory:

        return self.memory

    # ==========================================
    # CLEAR MEMORY
    # ==========================================

    def clear_memory(self):

        self.memory.clear()


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    from tools.register_tools import (
        register_computer_tools,
        register_browser_tools,
        register_system_tools
    )

    register_computer_tools()
    register_browser_tools()
    register_system_tools()

    memory = SahviaMemory(
        max_entries=12
    )

    router = CommandRouter(
        registry=registry,
        memory=memory
    )

    print(
        "\n======================================"
    )

    print(
        "       SAHVIA MEMORY ROUTER TEST"
    )

    print(
        "======================================"
    )

    command = input(
        "\nEnter command: "
    )

    result = router.route(
        command
    )

    print(
        "\n======================================"
    )

    print(
        "RESULT:"
    )

    print(
        result
    )

    print(
        "SUCCESS:",
        result.success
    )

    memory.debug_print()