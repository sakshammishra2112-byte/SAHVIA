import pyautogui

from core.result import ToolResult


# ==========================================
# WINDOW CONTROL
# ==========================================

def maximize_window():
    """
    Maximize the currently active window.
    """

    try:
        pyautogui.hotkey("alt", "space")
        pyautogui.press("x")

        return ToolResult.ok(
            "The current window has been maximized."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not maximize the window: {error}"
        )


def minimize_window():
    """
    Minimize the currently active window.
    """

    try:
        pyautogui.hotkey("alt", "space")
        pyautogui.press("n")

        return ToolResult.ok(
            "The current window has been minimized."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not minimize the window: {error}"
        )


def close_window():
    """
    Close the currently active window.
    """

    try:
        pyautogui.hotkey("alt", "f4")

        return ToolResult.ok(
            "The current window has been closed."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not close the window: {error}"
        )


def show_desktop():
    """
    Show the Windows desktop.
    """

    try:
        pyautogui.hotkey("win", "d")

        return ToolResult.ok(
            "The desktop is now visible."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not show the desktop: {error}"
        )


# ==========================================
# BROWSER / TAB CONTROL
# ==========================================

def new_tab():
    """
    Open a new browser tab.
    """

    try:
        pyautogui.hotkey("ctrl", "t")

        return ToolResult.ok(
            "A new tab has been opened."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not open a new tab: {error}"
        )


def new_window():
    """
    Open a new browser window.
    """

    try:
        pyautogui.hotkey("ctrl", "n")

        return ToolResult.ok(
            "A new window has been opened."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not open a new window: {error}"
        )


def close_tab():
    """
    Close the current browser tab.
    """

    try:
        pyautogui.hotkey("ctrl", "w")

        return ToolResult.ok(
            "The current tab has been closed."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not close the tab: {error}"
        )


def next_tab():
    """
    Switch to the next browser tab.
    """

    try:
        pyautogui.hotkey("ctrl", "tab")

        return ToolResult.ok(
            "Switched to the next tab."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not switch tabs: {error}"
        )


def go_back():
    """
    Navigate back.
    """

    try:
        pyautogui.hotkey("alt", "left")

        return ToolResult.ok(
            "Went back to the previous page."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not go back: {error}"
        )


def go_forward():
    """
    Navigate forward.
    """

    try:
        pyautogui.hotkey("alt", "right")

        return ToolResult.ok(
            "Went forward to the next page."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not go forward: {error}"
        )


def refresh_page():
    """
    Refresh the current page.
    """

    try:
        pyautogui.hotkey("ctrl", "r")

        return ToolResult.ok(
            "The page has been refreshed."
        )

    except Exception as error:
        return ToolResult.fail(
            error=f"Could not refresh the page: {error}"
        )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("SAHVIA Computer Tools")
    print("---------------------")

    result = maximize_window()

    print(result)
    print("Success:", result.success)