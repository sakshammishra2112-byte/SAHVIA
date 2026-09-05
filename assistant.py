import speech_recognition as sr
import queue
import asyncio
import edge_tts
import pygame
import os
import uuid
import time
import re
import threading

from config import (
    LANGUAGE,
    VOICE_RATE
)


# ==========================================
# SAHVIA INITIALIZATION
# ==========================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 250
recognizer.dynamic_energy_threshold = True

recognizer.pause_threshold = 0.8
recognizer.non_speaking_duration = 0.4

command_queue = queue.Queue()

# Prevent duplicate commands
command_lock = threading.Lock()

# Prevent recognition while SAHVIA is processing
processing_command = False


# ==========================================
# TTS STATE
# ==========================================

speaking = False
stop_requested = False


# ==========================================
# SAHVIA VOICE
# ==========================================

VOICE = "en-US-JennyNeural"


# ==========================================
# NAME VARIATIONS
# ==========================================

SAHVIA_VARIATIONS = [

    "sahvia",
    "sahvya",
    "sahviya",
    "sahviah",

    "savia",
    "savya",
    "saviah",

    "sania",
    "saniya",
    "sanya",

    "sovya",
    "soviah",
    "sovia",

    "sahbiya",
    "sahbya"
]


# ==========================================
# STOP PHRASES
# ==========================================

STOP_PHRASES = [

    "stop",
    "ok stop",
    "okay stop",

    "stop sahvia",
    "sahvia stop",

    "please stop",
    "please stop sahvia",
    "stop please",

    "stop talking",
    "stop speaking",

    "stop it",
    "stop this",
    "stop now",

    "shut up",
    "be quiet",
    "quiet",

    "that's enough",
    "thats enough",
    "enough",

    "terminate",
    "terminate sahvia"
]


# ==========================================
# NORMALIZE TEXT
# ==========================================

def normalize_text(text):

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ==========================================
# NORMALIZE SAHVIA NAME
# ==========================================

def normalize_sahvia_name(command):

    command = normalize_text(
        command
    )

    words = command.split()

    result = []

    for word in words:

        if word in SAHVIA_VARIATIONS:

            result.append(
                "sahvia"
            )

        else:

            result.append(
                word
            )

    return " ".join(
        result
    )


# ==========================================
# REMOVE WAKE WORD
# ==========================================

def remove_wake_word(command):

    command = normalize_sahvia_name(
        command
    )

    patterns = [

        r"^hey sahvia\s*",
        r"^hi sahvia\s*",
        r"^hello sahvia\s*",
        r"^sahvia\s*"
    ]

    for pattern in patterns:

        command = re.sub(
            pattern,
            "",
            command,
            count=1
        )

    return command.strip()


# ==========================================
# STOP DETECTION
# ==========================================

def is_stop_command(command):

    command = normalize_sahvia_name(
        command
    )

    command = normalize_text(
        command
    )

    for phrase in STOP_PHRASES:

        if phrase in command:

            return True

    return False


# ==========================================
# STOP SPEAKING
# ==========================================

def stop_speaking():

    global speaking
    global stop_requested

    stop_requested = True

    try:

        if pygame.mixer.get_init():

            pygame.mixer.music.stop()

    except Exception as error:

        print(
            "Stop voice error:",
            repr(error)
        )

    speaking = False


# ==========================================
# SPEAK
# ==========================================

def speak(text):

    global speaking
    global stop_requested

    if not text:

        return

    print(
        "SAHVIA:",
        text
    )

    stop_requested = False

    filename = os.path.join(

        os.getenv("TEMP"),

        "sahvia_"
        + str(uuid.uuid4())
        + ".mp3"
    )

    try:

        # ==================================
        # GENERATE VOICE
        # ==================================

        async def generate_voice():

            voice = edge_tts.Communicate(

                text=text,

                voice=VOICE,

                rate=VOICE_RATE
            )

            await voice.save(
                filename
            )


        asyncio.run(
            generate_voice()
        )


        if stop_requested:

            try:

                os.remove(
                    filename
                )

            except Exception:

                pass

            return


        # ==================================
        # AUDIO
        # ==================================

        if not pygame.mixer.get_init():

            pygame.mixer.init()


        pygame.mixer.music.load(
            filename
        )

        speaking = True

        pygame.mixer.music.play()


        while pygame.mixer.music.get_busy():

            if stop_requested:

                pygame.mixer.music.stop()

                break

            time.sleep(
                0.01
            )


        speaking = False


        try:

            pygame.mixer.music.unload()

        except Exception:

            pass


        try:

            os.remove(
                filename
            )

        except Exception:

            pass


    except Exception as error:

        speaking = False

        print(
            "Voice error:",
            repr(error)
        )


# ==========================================
# PROCESS AUDIO
# ==========================================

def process_audio(
    recognizer,
    audio
):

    global processing_command

    # ======================================
    # DON'T PROCESS WHILE BUSY
    # ======================================

    if processing_command:

        print(
            "⏳ SAHVIA is busy. Ignoring audio."
        )

        return


    try:

        print(
            "⚡ Recognizing..."
        )


        raw_command = recognizer.recognize_google(

            audio,

            language=LANGUAGE
        )


        raw_command = raw_command.strip()


        print(
            "You:",
            raw_command
        )


        command = normalize_sahvia_name(
            raw_command
        )


        # ==================================
        # STOP HAS HIGHEST PRIORITY
        # ==================================

        if is_stop_command(
            command
        ):

            print(
                "🛑 STOP COMMAND DETECTED"
            )

            stop_speaking()

            with command_lock:

                # Remove stale commands
                while not command_queue.empty():

                    try:

                        command_queue.get_nowait()

                    except queue.Empty:

                        break


                command_queue.put(
                    "__STOP__"
                )

            return


        # ==================================
        # REMOVE WAKE WORD
        # ==================================

        command = remove_wake_word(
            command
        )


        # ==================================
        # EMPTY
        # ==================================

        if not command:

            print(
                "🎤 Wake word detected."
            )

            return


        # ==================================
        # DUPLICATE PROTECTION
        # ==================================

        with command_lock:

            # If the same command is already waiting,
            # don't add it again.

            existing_commands = []

            duplicate = False


            while not command_queue.empty():

                try:

                    existing = (
                        command_queue.get_nowait()
                    )

                    if existing == command:

                        duplicate = True

                    existing_commands.append(
                        existing
                    )

                except queue.Empty:

                    break


            for existing in existing_commands:

                command_queue.put(
                    existing
                )


            if duplicate:

                print(
                    "⚠️ Duplicate command ignored:",
                    command
                )

                return


            command_queue.put(
                command
            )


    except sr.UnknownValueError:

        print(
            "⚠️ Could not understand speech."
        )


    except sr.RequestError as error:

        print(
            "Speech recognition error:",
            error
        )


    except Exception as error:

        print(
            "Audio processing error:",
            repr(error)
        )


# ==========================================
# START LISTENING
# ==========================================

def start_listening():

    microphone = sr.Microphone()


    with microphone as source:

        print(
            "🎤 Calibrating microphone..."
        )


        recognizer.adjust_for_ambient_noise(

            source,

            duration=1
        )


        print(
            "✅ SAHVIA is listening continuously."
        )


    return recognizer.listen_in_background(

        microphone,

        process_audio,

        phrase_time_limit=8
    )


# ==========================================
# GET COMMAND
# ==========================================

def get_command():

    try:

        return command_queue.get(

            timeout=0.05
        )

    except queue.Empty:

        return None