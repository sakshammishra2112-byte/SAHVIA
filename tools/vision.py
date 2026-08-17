import os
import time
from typing import Any, Dict, List, Optional

import pyautogui
from PIL import Image

from core.result import ToolResult

import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ==========================================
# SAHVIA VISION
# ==========================================

class SahviaVision:
    """
    SAHVIA's screen observation layer.

    Responsibilities:
    - Capture screenshots
    - Read screen dimensions
    - Perform OCR
    - Store the latest observation
    """

    def __init__(
        self,
        screenshot_directory: Optional[str] = None
    ):

        if screenshot_directory:

            self.screenshot_directory = (
                screenshot_directory
            )

        else:

            self.screenshot_directory = os.path.join(
                os.path.expanduser("~"),
                "Pictures",
                "SAHVIA"
            )

        os.makedirs(
            self.screenshot_directory,
            exist_ok=True
        )

        self.last_screenshot_path: Optional[str] = None

        self.last_image: Optional[Image.Image] = None

        self.last_ocr_text: str = ""

        self.last_screen_size = None


    # ==========================================
    # SCREEN SIZE
    # ==========================================

    def get_screen_size(self):

        try:

            width, height = pyautogui.size()

            self.last_screen_size = (
                width,
                height
            )

            return ToolResult.ok(
                message=(
                    f"Screen resolution is "
                    f"{width} by {height} pixels."
                ),
                data={
                    "width": width,
                    "height": height
                }
            )

        except Exception as error:

            return ToolResult.fail(
                error=(
                    f"Could not determine screen size: "
                    f"{error}"
                )
            )


    # ==========================================
    # TAKE SCREENSHOT
    # ==========================================

    def capture_screen(
        self,
        save: bool = True
    ):

        try:

            image = pyautogui.screenshot()

            self.last_image = image

            width, height = image.size

            self.last_screen_size = (
                width,
                height
            )


            filepath = None


            if save:

                filename = (
                    "screen_"
                    + time.strftime(
                        "%Y%m%d_%H%M%S"
                    )
                    + ".png"
                )

                filepath = os.path.join(
                    self.screenshot_directory,
                    filename
                )

                image.save(
                    filepath
                )

                self.last_screenshot_path = (
                    filepath
                )


            return ToolResult.ok(

                message=(
                    f"Screen captured "
                    f"({width}x{height})."
                ),

                data={

                    "width":
                        width,

                    "height":
                        height,

                    "path":
                        filepath
                }
            )


        except Exception as error:

            return ToolResult.fail(
                error=(
                    f"Could not capture screen: "
                    f"{error}"
                )
            )


    # ==========================================
    # OCR
    # ==========================================

    def read_screen_text(self):

        if self.last_image is None:

            capture_result = self.capture_screen(
                save=False
            )

            if not capture_result.success:

                return capture_result


        try:

            import pytesseract

            text = pytesseract.image_to_string(
                self.last_image
            )

            text = text.strip()

            self.last_ocr_text = text


            if not text:

                return ToolResult.ok(
                    message=(
                        "I couldn't detect readable "
                        "text on the screen."
                    ),
                    data={
                        "text": "",
                        "found_text": False
                    }
                )


            return ToolResult.ok(

                message=(
                    "I detected text on the screen."
                ),

                data={

                    "text":
                        text,

                    "found_text":
                        True
                }
            )


        except ImportError:

            return ToolResult.fail(
                error=(
                    "pytesseract is not installed. "
                    "Run: pip install pytesseract"
                )
            )


        except Exception as error:

            return ToolResult.fail(
                error=(
                    f"OCR failed: {error}"
                )
            )


    # ==========================================
    # OCR WITH POSITIONS
    # ==========================================

    def read_screen_elements(self):

        if self.last_image is None:

            capture_result = self.capture_screen(
                save=False
            )

            if not capture_result.success:

                return capture_result


        try:

            import pytesseract

            from pytesseract import Output


            data = pytesseract.image_to_data(
                self.last_image,
                output_type=Output.DICT
            )


            elements: List[
                Dict[str, Any]
            ] = []


            count = len(
                data["text"]
            )


            for index in range(count):

                text = data["text"][
                    index
                ].strip()


                if not text:

                    continue


                try:

                    confidence = float(
                        data["conf"][
                            index
                        ]
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    confidence = -1


                x = int(
                    data["left"][
                        index
                    ]
                )

                y = int(
                    data["top"][
                        index
                    ]
                )

                width = int(
                    data["width"][
                        index
                    ]
                )

                height = int(
                    data["height"][
                        index
                    ]
                )


                center_x = (
                    x + width // 2
                )

                center_y = (
                    y + height // 2
                )


                elements.append({

                    "text":
                        text,

                    "confidence":
                        confidence,

                    "x":
                        x,

                    "y":
                        y,

                    "width":
                        width,

                    "height":
                        height,

                    "center_x":
                        center_x,

                    "center_y":
                        center_y
                })


            self.last_ocr_text = " ".join(
                element["text"]
                for element in elements
            )


            return ToolResult.ok(

                message=(
                    f"Detected "
                    f"{len(elements)} "
                    f"text elements."
                ),

                data={

                    "elements":
                        elements,

                    "screen_size":
                        self.last_screen_size
                }
            )


        except ImportError:

            return ToolResult.fail(
                error=(
                    "pytesseract is not installed. "
                    "Run: pip install pytesseract"
                )
            )


        except Exception as error:

            return ToolResult.fail(
                error=(
                    f"Could not analyze screen "
                    f"elements: {error}"
                )
            )


    # ==========================================
    # FIND TEXT
    # ==========================================

    def find_text(
        self,
        target: str
    ):

        if not target or not target.strip():

            return ToolResult.fail(
                error="No text was provided to find."
            )


        target = target.strip().lower()


        elements_result = (
            self.read_screen_elements()
        )


        if not elements_result.success:

            return elements_result


        elements = elements_result.data.get(
            "elements",
            []
        )


        matches = []


        for element in elements:

            text = element[
                "text"
            ].lower()


            if target in text:

                matches.append(
                    element
                )


        if not matches:

            return ToolResult.ok(

                message=(
                    f"I couldn't find "
                    f"'{target}' on the screen."
                ),

                data={
                    "found": False,
                    "matches": []
                }
            )


        return ToolResult.ok(

            message=(
                f"Found '{target}' "
                f"on the screen."
            ),

            data={
                "found": True,
                "matches": matches
            }
        )


    # ==========================================
    # CLICK TEXT
    # ==========================================

    def click_text(
        self,
        target: str
    ):

        find_result = self.find_text(
            target
        )


        if not find_result.success:

            return find_result


        matches = find_result.data.get(
            "matches",
            []
        )


        if not matches:

            return ToolResult.fail(
                error=(
                    f"Could not find "
                    f"'{target}' on the screen."
                )
            )


        # --------------------------------------
        # Use first match
        # --------------------------------------

        element = matches[0]


        x = element[
            "center_x"
        ]

        y = element[
            "center_y"
        ]


        try:

            pyautogui.click(
                x,
                y
            )


            return ToolResult.ok(

                message=(
                    f"Clicked '{target}' "
                    f"at ({x}, {y})."
                ),

                data={
                    "text": target,
                    "x": x,
                    "y": y
                }
            )


        except Exception as error:

            return ToolResult.fail(
                error=(
                    f"Could not click "
                    f"'{target}': {error}"
                )
            )


    # ==========================================
    # MOVE TO TEXT
    # ==========================================

    def move_to_text(
        self,
        target: str
    ):

        find_result = self.find_text(
            target
        )


        if not find_result.success:

            return find_result


        matches = find_result.data.get(
            "matches",
            []
        )


        if not matches:

            return ToolResult.fail(
                error=(
                    f"Could not find "
                    f"'{target}' on the screen."
                )
            )


        element = matches[0]


        x = element[
            "center_x"
        ]

        y = element[
            "center_y"
        ]


        try:

            pyautogui.moveTo(
                x,
                y,
                duration=0.2
            )


            return ToolResult.ok(

                message=(
                    f"Moved cursor to "
                    f"'{target}'."
                ),

                data={
                    "x": x,
                    "y": y
                }
            )


        except Exception as error:

            return ToolResult.fail(
                error=(
                    f"Could not move cursor: "
                    f"{error}"
                )
            )


    # ==========================================
    # LAST OBSERVATION
    # ==========================================

    def get_last_observation(self):

        return {

            "screenshot":
                self.last_screenshot_path,

            "screen_size":
                self.last_screen_size,

            "ocr_text":
                self.last_ocr_text
        }


# ==========================================
# GLOBAL VISION INSTANCE
# ==========================================

vision = SahviaVision()


# ==========================================
# TOOL FUNCTIONS
# ==========================================

def capture_screen():

    return vision.capture_screen(
        save=True
    )


def get_screen_size():

    return vision.get_screen_size()


def read_screen():

    return vision.read_screen_text()


def read_screen_elements():

    return vision.read_screen_elements()


def find_on_screen(
    text: str
):

    return vision.find_text(
        text
    )


def click_on_screen(
    text: str
):

    return vision.click_text(
        text
    )


def move_to_screen_text(
    text: str
):

    return vision.move_to_text(
        text
    )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print(
        "\n=========================================="
    )

    print(
        "          SAHVIA VISION TEST"
    )

    print(
        "=========================================="
    )


    # --------------------------------------
    # Screen size
    # --------------------------------------

    result = get_screen_size()

    print(
        "\nSCREEN SIZE:"
    )

    print(
        result
    )


    # --------------------------------------
    # Screenshot
    # --------------------------------------

    result = capture_screen()

    print(
        "\nSCREENSHOT:"
    )

    print(
        result
    )


    # --------------------------------------
    # OCR
    # --------------------------------------

    result = read_screen()

    print(
        "\nSCREEN TEXT:"
    )

    print(
        result
    )


    # --------------------------------------
    # Elements
    # --------------------------------------

    result = read_screen_elements()

    print(
        "\nSCREEN ELEMENTS:"
    )

    if result.success:

        elements = result.data.get(
            "elements",
            []
        )

        for element in elements[:20]:

            print(
                element
            )

    else:

        print(
            result
        )


    print(
        "\n=========================================="
    )

    print(
        "Vision test completed."
    )

    print(
        "=========================================="
    )