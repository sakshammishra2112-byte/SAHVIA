import os
import subprocess
import platform
import shutil
import ctypes
import time

from core.result import ToolResult


# ==========================================
# SYSTEM INFORMATION
# ==========================================

def get_system_info():
    """
    Return basic information about the computer.
    """

    try:

        info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node()
        }

        message = (
            f"You are running Windows {platform.release()} "
            f"on a {platform.machine()} computer."
        )

        return ToolResult.ok(
            message=message,
            data=info
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not retrieve system information: {error}"
        )


# ==========================================
# OPEN APPLICATION
# ==========================================

def open_application(application: str):
    """
    Open a Windows application.

    Examples:
        chrome
        notepad
        calculator
        paint
        explorer
    """

    if not application or not application.strip():

        return ToolResult.fail(
            error="No application name was provided."
        )

    application = application.strip().lower()

    # --------------------------------------
    # Safe application aliases
    # --------------------------------------

    applications = {

        "chrome": "chrome",
        "google chrome": "chrome",

        "edge": "msedge",
        "microsoft edge": "msedge",

        "notepad": "notepad",

        "calculator": "calc",
        "calc": "calc",

        "paint": "mspaint",

        "file explorer": "explorer",
        "explorer": "explorer",

        "command prompt": "cmd",
        "cmd": "cmd",

        "powershell": "powershell",

        "settings": "ms-settings:",
    }

    executable = applications.get(
        application
    )

    if executable is None:

        return ToolResult.fail(
            error=(
                f"I don't have a safe launch rule "
                f"for '{application}'."
            )
        )

    try:

        if executable.endswith(":"):

            os.startfile(executable)

        else:

            subprocess.Popen(
                executable,
                shell=True
            )

        return ToolResult.ok(
            f"{application.title()} is opening."
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not open {application}: {error}"
        )


# ==========================================
# OPEN FILE EXPLORER
# ==========================================

def open_file_explorer():
    """
    Open Windows File Explorer.
    """

    try:

        subprocess.Popen(
            "explorer.exe"
        )

        return ToolResult.ok(
            "File Explorer is open."
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not open File Explorer: {error}"
        )


# ==========================================
# OPEN WINDOWS SETTINGS
# ==========================================

def open_settings():
    """
    Open Windows Settings.
    """

    try:

        os.startfile(
            "ms-settings:"
        )

        return ToolResult.ok(
            "Windows Settings is open."
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not open Windows Settings: {error}"
        )


# ==========================================
# VOLUME UP
# ==========================================

def volume_up():
    """
    Increase system volume.
    """

    try:

        import pyautogui

        for _ in range(5):

            pyautogui.press(
                "volumeup"
            )

        return ToolResult.ok(
            "System volume increased."
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not increase volume: {error}"
        )


# ==========================================
# VOLUME DOWN
# ==========================================

def volume_down():
    """
    Decrease system volume.
    """

    try:

        import pyautogui

        for _ in range(5):

            pyautogui.press(
                "volumedown"
            )

        return ToolResult.ok(
            "System volume decreased."
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not decrease volume: {error}"
        )


# ==========================================
# MUTE / UNMUTE
# ==========================================

def mute_volume():
    """
    Toggle system mute.
    """

    try:

        import pyautogui

        pyautogui.press(
            "volumemute"
        )

        return ToolResult.ok(
            "System mute has been toggled."
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not toggle mute: {error}"
        )


# ==========================================
# TAKE SCREENSHOT
# ==========================================

def take_screenshot():
    """
    Take a screenshot and save it to the
    user's Pictures/Screenshots folder.
    """

    try:

        import pyautogui

        pictures = os.path.join(
            os.path.expanduser("~"),
            "Pictures"
        )

        screenshots = os.path.join(
            pictures,
            "Screenshots"
        )

        os.makedirs(
            screenshots,
            exist_ok=True
        )

        filename = time.strftime(
            "sahvia_%Y%m%d_%H%M%S.png"
        )

        filepath = os.path.join(
            screenshots,
            filename
        )

        screenshot = pyautogui.screenshot()

        screenshot.save(
            filepath
        )

        return ToolResult.ok(
            f"Screenshot saved as {filename}.",
            data={
                "path": filepath
            }
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not take screenshot: {error}"
        )


# ==========================================
# OPEN DOWNLOADS
# ==========================================

def open_downloads():
    """
    Open the user's Downloads folder.
    """

    try:

        downloads = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        os.startfile(
            downloads
        )

        return ToolResult.ok(
            "Downloads folder is open."
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not open Downloads: {error}"
        )


# ==========================================
# OPEN DESKTOP
# ==========================================

def open_desktop_folder():
    """
    Open the user's Desktop folder.
    """

    try:

        desktop = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )

        os.startfile(
            desktop
        )

        return ToolResult.ok(
            "Desktop folder is open."
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not open Desktop: {error}"
        )


# ==========================================
# LOCK COMPUTER
# ==========================================

def lock_computer():
    """
    Lock the Windows computer.

    This action immediately locks the workstation.
    """

    try:

        ctypes.windll.user32.LockWorkStation()

        return ToolResult.ok(
            "The computer has been locked."
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not lock the computer: {error}"
        )


# ==========================================
# CHECK APPLICATION
# ==========================================

def is_application_installed(application: str):
    """
    Check whether a command/application exists
    on the system PATH.
    """

    if not application or not application.strip():

        return ToolResult.fail(
            error="No application name was provided."
        )

    application = application.strip()

    try:

        result = shutil.which(
            application
        )

        if result:

            return ToolResult.ok(
                f"{application} is installed.",
                data={
                    "path": result
                }
            )

        return ToolResult.ok(
            f"{application} was not found on the system."
        )

    except Exception as error:

        return ToolResult.fail(
            error=f"Could not check the application: {error}"
        )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print(
        "SAHVIA System Tools"
    )

    print(
        "-------------------"
    )

    result = get_system_info()

    print(
        result
    )

    print(
        "Success:",
        result.success
    )