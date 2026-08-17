import json
import re
import requests


# ==========================================
# SAHVIA OLLAMA BRAIN
# ==========================================

class OllamaBrain:

    def __init__(
        self,
        model="llama3.2:3b",
        host="http://localhost:11434"
    ):

        self.model = model
        self.host = host.rstrip("/")


    # ==========================================
    # OLLAMA REQUEST
    # ==========================================

    def _generate(self, prompt):

        response = requests.post(

            f"{self.host}/api/generate",

            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },

            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        )


    # ==========================================
    # TOOL DESCRIPTIONS
    # ==========================================

    def _tool_text(self, tools):

        descriptions = []

        for name, info in tools.items():

            if isinstance(info, dict):

                description = info.get(
                    "description",
                    ""
                )

            else:

                description = getattr(
                    info,
                    "description",
                    ""
                )

            descriptions.append(
                f"- {name}: {description}"
            )

        return "\n".join(
            descriptions
        )


    # ==========================================
    # DIRECT SCREEN COMMANDS
    # ==========================================

    def detect_screen_command(self, command):

        text = command.strip()

        patterns = [

            (
                r"^(?:find|locate|look for)\s+(.+?)"
                r"(?:\s+on\s+(?:my\s+)?screen)?[.!?]?$",
                "find_on_screen"
            ),

            (
                r"^where\s+is\s+(.+?)"
                r"(?:\s+on\s+(?:my\s+)?screen)?[.!?]?$",
                "find_on_screen"
            ),

            (
                r"^(?:click|press)\s+(?:on\s+)?(.+?)"
                r"(?:\s+on\s+(?:my\s+)?screen)?[.!?]?$",
                "click_on_screen"
            ),

            (
                r"^move\s+(?:the\s+)?(?:mouse\s+)?to\s+(.+?)"
                r"(?:\s+on\s+(?:my\s+)?screen)?[.!?]?$",
                "move_to_screen_text"
            )
        ]


        for pattern, tool in patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                target = match.group(
                    1
                ).strip()

                target = target.rstrip(
                    ".,?!"
                )

                if target:

                    return {

                        "tool": tool,

                        "arguments": {
                            "text": target
                        },

                        "reason":
                            f"Screen command targeting {target}.",

                        "response":
                            ""
                    }


        # ======================================
        # READ SCREEN
        # ======================================

        lower = text.lower()

        screen_phrases = [

            "what can you see",

            "what do you see",

            "read my screen",

            "read the screen",

            "what is on my screen",

            "what's on my screen",

            "what is visible on my screen",

            "what's visible on my screen"
        ]


        for phrase in screen_phrases:

            if phrase in lower:

                return {

                    "tool":
                        "read_screen",

                    "arguments":
                        {},

                    "reason":
                        "The user wants to know what is visible on the screen.",

                    "response":
                        ""
                }


        # ======================================
        # SCREENSHOT
        # ======================================

        screenshot_phrases = [

            "take a screenshot",

            "capture the screen",

            "capture my screen",

            "screenshot my screen"
        ]


        for phrase in screenshot_phrases:

            if phrase in lower:

                return {

                    "tool":
                        "capture_screen",

                    "arguments":
                        {},

                    "reason":
                        "The user requested a screenshot.",

                    "response":
                        ""
                }


        return None


    # ==========================================
    # BUILD TOOL PROMPT
    # ==========================================

    def build_tool_prompt(
        self,
        command,
        tools,
        context=None
    ):

        tools_text = self._tool_text(
            tools
        )


        context_text = ""

        if context:

            context_text = f"""

PREVIOUS CONTEXT:

{context}
"""


        return f"""
You are SAHVIA, a voice-controlled computer assistant.

Select exactly ONE tool from the available tools.

AVAILABLE TOOLS:

{tools_text}

{context_text}

========================================
OUTPUT FORMAT
========================================

Return ONLY JSON:

{{
    "tool": "tool_name",
    "arguments": {{}},
    "reason": "short reason",
    "response": "short response"
}}

========================================
ARGUMENT RULES
========================================

IMPORTANT:

Use the EXACT argument names required by the tool.

Never use:
"q"
"text_query"
"search"
"input"
"command"

unless that exact name is shown by the tool.

For YouTube:

play_youtube requires:

{{
    "query": "song or video name"
}}

youtube_search requires:

{{
    "query": "search text"
}}

google_search requires:

{{
    "query": "search text"
}}

open_first_search_result requires:

{{
    "query": "search text"
}}

For screen tools:

find_on_screen requires:

{{
    "text": "visible text"
}}

click_on_screen requires:

{{
    "text": "visible text"
}}

move_to_screen_text requires:

{{
    "text": "visible text"
}}

read_screen requires:

{{}}

capture_screen requires:

{{}}

========================================
EXAMPLES
========================================

User:
play Teri Aakhya Ka Yo Kajal from YouTube

Correct:

{{
    "tool": "play_youtube",
    "arguments": {{
        "query": "Teri Aakhya Ka Yo Kajal"
    }},
    "reason": "The user wants to play the song on YouTube.",
    "response": "Playing Teri Aakhya Ka Yo Kajal."
}}

WRONG:

{{
    "tool": "play_youtube",
    "arguments": {{
        "q": "Teri Aakhya Ka Yo Kajal"
    }}
}}

User:
Search Google for Python tutorials

Correct:

{{
    "tool": "google_search",
    "arguments": {{
        "query": "Python tutorials"
    }}
}}

User:
Find YouTube on my screen

Correct:

{{
    "tool": "find_on_screen",
    "arguments": {{
        "text": "YouTube"
    }}
}}

========================================
USER COMMAND
========================================

{command}

Return ONLY JSON.
"""


    # ==========================================
    # REPAIR ARGUMENTS
    # ==========================================

    def repair_arguments(
        self,
        tool,
        arguments,
        command
    ):

        if not isinstance(
            arguments,
            dict
        ):

            arguments = {}


        # ======================================
        # UNIVERSAL ALIASES
        # ======================================

        aliases = [

            "q",
            "search",
            "query_text",
            "text_query",
            "input",
            "value"
        ]


        # ======================================
        # QUERY TOOLS
        # ======================================

        query_tools = [

            "play_youtube",
            "youtube_search",
            "google_search",
            "open_first_search_result"
        ]


        if tool in query_tools:

            # Already correct
            if arguments.get("query"):

                return {
                    "query":
                        arguments["query"]
                }


            # Convert q -> query
            for alias in aliases:

                if arguments.get(alias):

                    return {

                        "query":
                            arguments[alias]
                    }


            # Last-resort extraction from command
            query = self.extract_query(
                command,
                tool
            )


            if query:

                return {

                    "query":
                        query
                }


        # ======================================
        # SCREEN TOOLS
        # ======================================

        screen_tools = [

            "find_on_screen",
            "click_on_screen",
            "move_to_screen_text"
        ]


        if tool in screen_tools:

            if arguments.get("text"):

                return {

                    "text":
                        arguments["text"]
                }


            for alias in aliases:

                if arguments.get(alias):

                    return {

                        "text":
                            arguments[alias]
                    }


            target = self.extract_screen_target(
                command
            )


            if target:

                return {

                    "text":
                        target
                }


        return arguments


    # ==========================================
    # EXTRACT QUERY
    # ==========================================

    def extract_query(
        self,
        command,
        tool
    ):

        text = command.strip()


        if tool == "play_youtube":

            patterns = [

                r"play\s+(.+?)(?:\s+from\s+youtube)?$",

                r"play\s+(.+?)\s+on\s+youtube$"
            ]


        elif tool == "youtube_search":

            patterns = [

                r"search\s+(?:youtube\s+)?for\s+(.+)$",

                r"search\s+(.+?)\s+on\s+youtube$"
            ]


        elif tool == "google_search":

            patterns = [

                r"search\s+google\s+for\s+(.+)$",

                r"google\s+search\s+for\s+(.+)$"
            ]


        elif tool == "open_first_search_result":

            patterns = [

                r"open\s+the\s+first\s+(?:site|result)"
                r"(?:\s+from\s+)?(?:this\s+)?search"
            ]

        else:

            return None


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                if match.groups():

                    query = match.group(
                        1
                    ).strip()

                    return query


        return None


    # ==========================================
    # EXTRACT SCREEN TARGET
    # ==========================================

    def extract_screen_target(
        self,
        command
    ):

        text = command.strip()


        patterns = [

            r"find\s+(.+?)(?:\s+on\s+(?:my\s+)?screen)?$",

            r"locate\s+(.+?)(?:\s+on\s+(?:my\s+)?screen)?$",

            r"click\s+(?:on\s+)?(.+?)(?:\s+on\s+(?:my\s+)?screen)?$",

            r"move\s+(?:the\s+)?(?:mouse\s+)?to\s+(.+?)(?:\s+on\s+(?:my\s+)?screen)?$"
        ]


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                target = match.group(
                    1
                ).strip()

                return target.rstrip(
                    ".,?!"
                )


        return None


    # ==========================================
    # ASK
    # ==========================================

    def ask(
        self,
        command,
        tools=None,
        context=None
    ):

        # ======================================
        # DIRECT VISION
        # ======================================

        if tools is not None:

            vision_decision = (
                self.detect_screen_command(
                    command
                )
            )


            if vision_decision:

                print(
                    "👁️ Vision command detected directly."
                )

                print(
                    "🧠 Brain decision:",
                    vision_decision
                )

                return vision_decision


        if tools is None:

            tools = {}


        print(
            "🤖 Sending command to SAHVIA brain..."
        )


        try:

            prompt = self.build_tool_prompt(

                command,

                tools,

                context
            )


            raw_response = self._generate(
                prompt
            )


            print(
                "🧠 Raw brain response:",
                raw_response
            )


            if not raw_response.strip():

                raise ValueError(
                    "Brain returned an empty response."
                )


            decision = json.loads(
                raw_response
            )


            if not isinstance(
                decision,
                dict
            ):

                raise ValueError(
                    "Brain response is not an object."
                )


            tool = decision.get(
                "tool"
            )


            if not tool:

                raise ValueError(
                    "Brain did not select a tool."
                )


            if tools and tool not in tools:

                raise ValueError(
                    f"Unknown tool selected: {tool}"
                )


            arguments = decision.get(
                "arguments",
                {}
            )


            # ==================================
            # REPAIR ARGUMENTS
            # ==================================

            arguments = self.repair_arguments(

                tool,

                arguments,

                command
            )


            result = {

                "tool":
                    tool,

                "arguments":
                    arguments,

                "reason":
                    decision.get(
                        "reason",
                        ""
                    ),

                "response":
                    decision.get(
                        "response",
                        ""
                    )
            }


            print(
                "🧠 Brain decision:",
                result
            )


            return result


        except json.JSONDecodeError:

            print(
                "❌ Brain returned invalid JSON."
            )


            return {

                "tool":
                    None,

                "arguments":
                    {},

                "reason":
                    "Invalid JSON from brain.",

                "response":
                    ""
            }


        except Exception as error:

            print(
                "❌ Brain decision error:",
                error
            )


            return {

                "tool":
                    None,

                "arguments":
                    {},

                "reason":
                    str(error),

                "response":
                    ""
            }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    brain = OllamaBrain()


    tools = {

        "play_youtube": {
            "description":
                "Play a YouTube video."
        },

        "youtube_search": {
            "description":
                "Search YouTube."
        },

        "google_search": {
            "description":
                "Search Google."
        },

        "find_on_screen": {
            "description":
                "Find text on the screen."
        },

        "click_on_screen": {
            "description":
                "Click visible text on the screen."
        },

        "read_screen": {
            "description":
                "Read the screen."
        }
    }


    tests = [

        "play Teri Aakhya Ka Yo Kajal",

        "search YouTube for Python tutorials",

        "Search Google for Python tutorials",

        "Find SAHVIA on my screen",

        "Click YouTube on my screen",

        "What can you see on my screen?"
    ]


    for command in tests:

        print()
        print(
            "=========================================="
        )

        print(
            "COMMAND:",
            command
        )

        print(
            "=========================================="
        )


        decision = brain.ask(
            command,
            tools
        )


        print(
            json.dumps(
                decision,
                indent=4
            )
        )