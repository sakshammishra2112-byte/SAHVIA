from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MemoryEntry:

    role: str

    content: str

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


class SahviaMemory:

    def __init__(
        self,
        max_entries: int = 12
    ):

        self.max_entries = max_entries

        self.entries: List[
            MemoryEntry
        ] = []

        self.last_tool: Optional[str] = None

        self.last_arguments: Dict[
            str, Any
        ] = {}

        self.last_result: Optional[str] = None


    # ==========================================
    # ADD MESSAGE
    # ==========================================

    def add_message(
        self,
        role: str,
        content: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None
    ):

        if not content:
            return

        self.entries.append(
            MemoryEntry(
                role=role,
                content=content,
                metadata=metadata or {}
            )
        )

        self._trim()


    def add_user_message(
        self,
        content: str
    ):

        self.add_message(
            "user",
            content
        )


    def add_assistant_message(
        self,
        content: str
    ):

        self.add_message(
            "assistant",
            content
        )


    # ==========================================
    # RECORD TOOL
    # ==========================================

    def record_tool(
        self,
        tool_name: str,
        arguments: Optional[
            Dict[str, Any]
        ] = None,
        result: Optional[str] = None
    ):

        self.last_tool = tool_name

        self.last_arguments = (
            arguments or {}
        )

        self.last_result = result


    # ==========================================
    # TRIM
    # ==========================================

    def _trim(self):

        if len(self.entries) > self.max_entries:

            self.entries = self.entries[
                -self.max_entries:
            ]


    # ==========================================
    # CONTEXT FOR OLLAMA
    # ==========================================

    def get_context(
        self
    ) -> str:

        lines = []

        for entry in self.entries:

            lines.append(
                f"{entry.role.upper()}: "
                f"{entry.content}"
            )


        # --------------------------------------
        # Add active tool context
        # --------------------------------------

        if self.last_tool:

            lines.append(
                "\nACTIVE TOOL CONTEXT:"
            )

            lines.append(
                f"LAST TOOL: {self.last_tool}"
            )

            lines.append(
                "LAST ARGUMENTS: "
                + str(
                    self.last_arguments
                )
            )

            if self.last_result:

                lines.append(
                    "LAST RESULT: "
                    + self.last_result
                )


        if not lines:

            return (
                "No previous conversation "
                "or tool context."
            )


        return "\n".join(
            lines
        )


    # ==========================================
    # RECENT MESSAGES
    # ==========================================

    def get_recent_messages(
        self
    ):

        return [

            {
                "role": entry.role,
                "content": entry.content
            }

            for entry in self.entries
        ]


    # ==========================================
    # GET LAST TOOL
    # ==========================================

    def get_last_tool(
        self
    ):

        return self.last_tool


    # ==========================================
    # GET LAST ARGUMENTS
    # ==========================================

    def get_last_arguments(
        self
    ):

        return self.last_arguments.copy()


    # ==========================================
    # GET LAST RESULT
    # ==========================================

    def get_last_result(
        self
    ):

        return self.last_result


    # ==========================================
    # CLEAR
    # ==========================================

    def clear(self):

        self.entries.clear()

        self.last_tool = None

        self.last_arguments = {}

        self.last_result = None


    # ==========================================
    # SIZE
    # ==========================================

    def size(self):

        return len(
            self.entries
        )


    # ==========================================
    # DEBUG
    # ==========================================

    def debug_print(self):

        print(
            "\n=========================================="
        )

        print(
            "           SAHVIA MEMORY"
        )

        print(
            "=========================================="
        )

        for entry in self.entries:

            print(
                f"{entry.role}: {entry.content}"
            )


        print(
            "\nLast tool:",
            self.last_tool
        )

        print(
            "Last arguments:",
            self.last_arguments
        )

        print(
            "Last result:",
            self.last_result
        )

        print(
            "==========================================")


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    memory = SahviaMemory()

    memory.add_user_message(
        "Search Google for Python tutorials."
    )

    memory.add_assistant_message(
        "Searching Google for Python tutorials."
    )

    memory.record_tool(
        "google_search",
        {
            "query": "Python tutorials"
        },
        "Searching Google for Python tutorials."
    )

    memory.add_user_message(
        "Open the first site from the search."
    )

    memory.debug_print()

    print(
        "\nCONTEXT SENT TO OLLAMA:"
    )

    print(
        memory.get_context()
    )