import webbrowser
import subprocess
import urllib.parse
import requests
import re

from core.result import ToolResult


# ==========================================
# OPEN BROWSER
# ==========================================

def open_browser():

    try:

        webbrowser.open(
            "https://www.google.com"
        )

        return ToolResult.ok(
            "Your browser is open."
        )

    except Exception as error:

        return ToolResult.fail(
            f"Could not open the browser: {error}"
        )


# ==========================================
# OPEN GOOGLE
# ==========================================

def open_google():

    try:

        webbrowser.open(
            "https://www.google.com"
        )

        return ToolResult.ok(
            "Google is open."
        )

    except Exception as error:

        return ToolResult.fail(
            f"Could not open Google: {error}"
        )


# ==========================================
# OPEN YOUTUBE
# ==========================================

def open_youtube(
    url: str = None,
    query: str = None
):

    try:

        # --------------------------------------
        # Open specific YouTube URL
        # --------------------------------------

        if url:

            url = str(url).strip()

            if (
                "youtube.com/" in url
                or
                "youtu.be/" in url
            ):

                webbrowser.open(
                    url
                )

                return ToolResult.ok(
                    "Opening YouTube video.",
                    data={
                        "url": url
                    }
                )

        # --------------------------------------
        # Search YouTube
        # --------------------------------------

        if query:

            return youtube_search(
                query
            )

        # --------------------------------------
        # Homepage
        # --------------------------------------

        webbrowser.open(
            "https://www.youtube.com"
        )

        return ToolResult.ok(
            "YouTube is open."
        )

    except Exception as error:

        return ToolResult.fail(
            f"Could not open YouTube: {error}"
        )


# ==========================================
# YOUTUBE SEARCH
# ==========================================

def youtube_search(
    query: str
):

    if not query or not str(query).strip():

        return ToolResult.fail(
            "No YouTube search query was provided."
        )

    query = str(
        query
    ).strip()

    try:

        encoded = urllib.parse.quote_plus(
            query
        )

        url = (
            "https://www.youtube.com/results?search_query="
            + encoded
        )

        webbrowser.open(
            url
        )

        return ToolResult.ok(
            f"Searching YouTube for {query}.",
            data={
                "query": query,
                "url": url
            }
        )

    except Exception as error:

        return ToolResult.fail(
            f"Could not search YouTube: {error}"
        )


# ==========================================
# FIND FIRST YOUTUBE VIDEO
# ==========================================

def find_first_youtube_video(
    query: str
):

    if not query or not str(query).strip():

        return None


    query = str(
        query
    ).strip()


    encoded = urllib.parse.quote_plus(
        query
    )


    url = (
        "https://www.youtube.com/results?search_query="
        + encoded
    )


    headers = {

        "User-Agent":
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36",

        "Accept-Language":
            "en-US,en;q=0.9"
    }


    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )


    response.raise_for_status()


    html = response.text


    # ======================================
    # Extract YouTube video IDs
    # ======================================

    video_ids = re.findall(
        r'"videoId":"([A-Za-z0-9_-]{11})"',
        html
    )


    # Remove duplicates while preserving order

    unique_ids = []

    for video_id in video_ids:

        if video_id not in unique_ids:

            unique_ids.append(
                video_id
            )


    if not unique_ids:

        return None


    first_video_id = unique_ids[0]


    video_url = (
        "https://www.youtube.com/watch?v="
        + first_video_id
    )


    return {

        "video_id":
            first_video_id,

        "url":
            video_url,

        "query":
            query
    }


# ==========================================
# PLAY YOUTUBE
# ==========================================

def play_youtube(
    query: str
):
    """
    Find the first matching YouTube video
    and open it directly.
    """

    if not query or not str(query).strip():

        return ToolResult.fail(
            "I need the name of the song or video."
        )


    query = str(
        query
    ).strip()


    try:

        print(
            f"🔎 Finding YouTube video: {query}"
        )


        video = find_first_youtube_video(
            query
        )


        if not video:

            # ----------------------------------
            # Fallback to search page
            # ----------------------------------

            encoded = urllib.parse.quote_plus(
                query
            )

            search_url = (
                "https://www.youtube.com/results"
                "?search_query="
                + encoded
            )

            webbrowser.open(
                search_url
            )

            return ToolResult.ok(
                f"I couldn't identify the exact video, "
                f"so I opened YouTube search for {query}.",
                data={
                    "query": query,
                    "fallback": True,
                    "url": search_url
                }
            )


        video_url = video[
            "url"
        ]


        print(
            f"▶️ Opening: {video_url}"
        )


        webbrowser.open(
            video_url
        )


        return ToolResult.ok(
            f"Playing {query} on YouTube.",
            data={
                "query":
                    query,

                "video_id":
                    video["video_id"],

                "url":
                    video_url,

                "action":
                    "play"
            }
        )


    except Exception as error:

        return ToolResult.fail(
            f"Could not play {query}: {error}"
        )


# ==========================================
# GOOGLE SEARCH
# ==========================================

def google_search(
    query: str
):

    if not query or not str(query).strip():

        return ToolResult.fail(
            "No search query was provided."
        )


    query = str(
        query
    ).strip()


    try:

        encoded = urllib.parse.quote_plus(
            query
        )

        url = (
            "https://www.google.com/search?q="
            + encoded
        )

        webbrowser.open(
            url
        )

        return ToolResult.ok(
            f"Searching Google for {query}.",
            data={
                "query": query,
                "url": url
            }
        )

    except Exception as error:

        return ToolResult.fail(
            f"Could not search Google: {error}"
        )


# ==========================================
# OPEN FIRST GOOGLE RESULT
# ==========================================

def open_first_search_result(
    query: str
):

    if not query or not str(query).strip():

        return ToolResult.fail(
            "No search query was provided."
        )


    query = str(
        query
    ).strip()


    try:

        encoded = urllib.parse.quote_plus(
            query
        )

        url = (
            "https://www.google.com/search"
            "?q="
            + encoded
            + "&btnI=1"
        )

        webbrowser.open(
            url
        )

        return ToolResult.ok(
            f"Opening the first result for {query}.",
            data={
                "query": query,
                "url": url,
                "result_number": 1
            }
        )

    except Exception as error:

        return ToolResult.fail(
            f"Could not open the first result: {error}"
        )


# ==========================================
# GITHUB
# ==========================================

def open_github():

    try:

        webbrowser.open(
            "https://github.com"
        )

        return ToolResult.ok(
            "GitHub is open."
        )

    except Exception as error:

        return ToolResult.fail(
            f"Could not open GitHub: {error}"
        )


# ==========================================
# CHATGPT
# ==========================================

def open_chatgpt():

    try:

        webbrowser.open(
            "https://chatgpt.com"
        )

        return ToolResult.ok(
            "ChatGPT is open."
        )

    except Exception as error:

        return ToolResult.fail(
            f"Could not open ChatGPT: {error}"
        )


# ==========================================
# GMAIL
# ==========================================

def open_gmail():

    try:

        webbrowser.open(
            "https://mail.google.com"
        )

        return ToolResult.ok(
            "Gmail is open."
        )

    except Exception as error:

        return ToolResult.fail(
            f"Could not open Gmail: {error}"
        )


# ==========================================
# EDGE
# ==========================================

def open_edge():

    try:

        subprocess.Popen(
            [
                "cmd",
                "/c",
                "start",
                "",
                "msedge"
            ],
            shell=True
        )

        return ToolResult.ok(
            "Microsoft Edge is open."
        )

    except Exception as error:

        return ToolResult.fail(
            f"Could not open Microsoft Edge: {error}"
        )


# ==========================================
# WIKIPEDIA
# ==========================================

def wikipedia_search(
    topic: str
):

    if not topic or not str(topic).strip():

        return ToolResult.fail(
            "No Wikipedia topic was provided."
        )

    topic = str(
        topic
    ).strip()

    try:

        import wikipedia

        result = wikipedia.summary(
            topic,
            sentences=2
        )

        return ToolResult.ok(
            result,
            data={
                "topic":
                    topic,

                "source":
                    "Wikipedia"
            }
        )

    except Exception as error:

        return ToolResult.fail(
            f"Wikipedia search failed: {error}"
        )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print(
        "SAHVIA YouTube Test"
    )

    print(
        "==================="
    )

    result = play_youtube(
        "Aankhen Khuli"
    )

    print(
        result
    )

    print(
        "Success:",
        result.success
    )

    print(
        "Data:",
        result.data
    )