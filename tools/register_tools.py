from core.registry import registry

from tools.computer import (
    maximize_window,
    minimize_window,
    close_window,
    show_desktop,
    new_tab,
    new_window,
    close_tab,
    next_tab,
    go_back,
    go_forward,
    refresh_page
)

from tools.browser import (
    open_youtube,
    youtube_search,
    play_youtube,
    google_search,
    open_first_search_result,
    open_google,
    open_github,
    open_gmail,
    open_chatgpt,
    open_edge,
    wikipedia_search
)

from tools.vision import (
    capture_screen,
    get_screen_size,
    read_screen,
    read_screen_elements,
    find_on_screen,
    click_on_screen,
    move_to_screen_text
)


# ==========================================
# COMPUTER TOOLS
# ==========================================

def register_computer_tools():

    registry.register(
        "maximize_window",
        maximize_window,
        "Maximize the currently active window."
    )

    registry.register(
        "minimize_window",
        minimize_window,
        "Minimize the currently active window."
    )

    registry.register(
        "close_window",
        close_window,
        "Close the currently active window."
    )

    registry.register(
        "show_desktop",
        show_desktop,
        "Show the Windows desktop."
    )

    registry.register(
        "new_tab",
        new_tab,
        "Open a new browser tab."
    )

    registry.register(
        "new_window",
        new_window,
        "Open a new browser window."
    )

    registry.register(
        "close_tab",
        close_tab,
        "Close the current browser tab."
    )

    registry.register(
        "next_tab",
        next_tab,
        "Switch to the next browser tab."
    )

    registry.register(
        "go_back",
        go_back,
        "Go back to the previous page."
    )

    registry.register(
        "go_forward",
        go_forward,
        "Go forward to the next page."
    )

    registry.register(
        "refresh_page",
        refresh_page,
        "Refresh the current browser page."
    )


# ==========================================
# BROWSER TOOLS
# ==========================================

def register_browser_tools():

    registry.register(
        "open_google",
        open_google,
        "Open Google."
    )

    registry.register(
        "google_search",
        google_search,
        "Search Google for something."
    )

    registry.register(
        "open_first_search_result",
        open_first_search_result,
        "Open the first Google search result."
    )

    registry.register(
        "open_youtube",
        open_youtube,
        "Open YouTube."
    )

    registry.register(
        "youtube_search",
        youtube_search,
        "Search YouTube for something."
    )

    registry.register(
        "play_youtube",
        play_youtube,
        "Find and open the first matching YouTube video."
    )

    registry.register(
        "open_github",
        open_github,
        "Open GitHub."
    )

    registry.register(
        "open_gmail",
        open_gmail,
        "Open Gmail."
    )

    registry.register(
        "open_chatgpt",
        open_chatgpt,
        "Open ChatGPT."
    )

    registry.register(
        "open_edge",
        open_edge,
        "Open Microsoft Edge."
    )

    registry.register(
        "wikipedia_search",
        wikipedia_search,
        "Search Wikipedia."
    )


# ==========================================
# VISION TOOLS
# ==========================================

def register_vision_tools():

    registry.register(
        "capture_screen",
        capture_screen,
        "Take a screenshot of the current screen."
    )

    registry.register(
        "get_screen_size",
        get_screen_size,
        "Get the current screen resolution."
    )

    registry.register(
        "read_screen",
        read_screen,
        "Read visible text from the current screen."
    )

    registry.register(
        "read_screen_elements",
        read_screen_elements,
        "Detect visible text and their screen coordinates."
    )

    registry.register(
        "find_on_screen",
        find_on_screen,
        "Find specific text on the current screen."
    )

    registry.register(
        "click_on_screen",
        click_on_screen,
        "Find specific text on the screen and click it."
    )

    registry.register(
        "move_to_screen_text",
        move_to_screen_text,
        "Move the mouse to specific text on the screen."
    )


# ==========================================
# REGISTER EVERYTHING
# ==========================================

def register_all_tools():

    register_computer_tools()

    register_browser_tools()

    register_vision_tools()


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    register_all_tools()

    print()
    print("SAHVIA registered tools:")
    print("------------------------")

    for tool_name in registry.list_tools():

        tool_info = registry.get(
            tool_name
        )

        if isinstance(
            tool_info,
            dict
        ):

            description = tool_info.get(
                "description",
                "No description available."
            )

        else:

            description = getattr(
                tool_info,
                "description",
                "No description available."
            )

        print(
            f"{tool_name} -> {description}"
        )

    print()
    print(
        "Total tools:",
        len(
            registry.list_tools()
        )
    )