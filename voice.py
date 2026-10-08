import asyncio
import os
import tempfile
import threading
import time

import edge_tts
import pygame
import speech_recognition as sr


# ============================================================
# SETTINGS
# ============================================================

VOICE_NAME = "en-IN-NeerjaNeural"

STOP_COMMANDS = [
    "stop",
    "stop speaking",
    "stop talking",
    "aira stop",
    "hey aira stop",
    "be quiet",
    "quiet",
    "silence"
]


# ============================================================
# SPEECH CORRECTIONS
# ============================================================

SPEECH_CORRECTIONS = {

    # Palworld
    "pagalworld": "palworld",
    "pagal world": "palworld",
    "pal world": "palworld",
    "pal word": "palworld",
    "pal words": "palworld",

    # A.I.R.A.
    "ai ra": "aira",
    "ai-rah": "aira",
    "hira": "aira",
}


# ============================================================
# SPEECH RECOGNIZER
# ============================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300

recognizer.dynamic_energy_threshold = True

recognizer.pause_threshold = 0.8

recognizer.phrase_threshold = 0.3

recognizer.non_speaking_duration = 0.5


# ============================================================
# CORRECT SPEECH
# ============================================================

def correct_speech(text):

    text = text.lower().strip()

    for wrong, correct in SPEECH_CORRECTIONS.items():

        text = text.replace(
            wrong,
            correct
        )

    return text


# ============================================================
# LISTEN
# ============================================================

def listen(timeout=None):

    with sr.Microphone() as source:

        print("\nListening...")

        try:

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=15
            )

        except sr.WaitTimeoutError:

            return None

    try:

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        text = correct_speech(text)

        print("Heard:", text)

        return text

    except sr.UnknownValueError:

        print("I couldn't understand that.")

        return None

    except sr.RequestError as error:

        print(
            "Speech recognition error:",
            error
        )

        return None


# ============================================================
# STOP LISTENER
# ============================================================

def stop_listener_callback(
    recognizer_instance,
    audio
):

    try:

        text = recognizer_instance.recognize_google(
            audio,
            language="en-IN"
        )

        text = correct_speech(text)

        print(
            "\nStop listener heard:",
            text
        )

        for command in STOP_COMMANDS:

            if command in text:

                print(
                    "🛑 Stop command detected."
                )

                try:

                    pygame.mixer.music.stop()

                except Exception:
                    pass

                break

    except Exception:
        pass


# ============================================================
# SPEAK
# ============================================================

def speak(text):

    if not text:
        return

    temp_file = None

    try:

        # ----------------------------------------------------
        # Create temporary MP3
        # ----------------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as file:

            temp_file = file.name

        # ----------------------------------------------------
        # Generate speech
        # ----------------------------------------------------

        async def generate():

            communicate = edge_tts.Communicate(
                text,
                VOICE_NAME
            )

            await communicate.save(
                temp_file
            )

        asyncio.run(generate())

        # ----------------------------------------------------
        # Initialize pygame
        # ----------------------------------------------------

        if not pygame.mixer.get_init():

            pygame.mixer.init()

        # ----------------------------------------------------
        # Load audio
        # ----------------------------------------------------

        pygame.mixer.music.load(
            temp_file
        )

        pygame.mixer.music.play()

        # ----------------------------------------------------
        # Start background stop listener
        # ----------------------------------------------------

        stop_listener = recognizer.listen_in_background(
            sr.Microphone(),
            stop_listener_callback,
            phrase_time_limit=3
        )

        # ----------------------------------------------------
        # Wait while speaking
        # ----------------------------------------------------

        while pygame.mixer.music.get_busy():

            time.sleep(0.1)

        # ----------------------------------------------------
        # Stop background listener
        # ----------------------------------------------------

        stop_listener(
            wait_for_stop=False
        )

        pygame.mixer.music.stop()

    except Exception as error:

        print(
            "TTS error:",
            error
        )

    finally:

        # ----------------------------------------------------
        # Delete temporary file
        # ----------------------------------------------------

        if temp_file:

            try:

                if os.path.exists(temp_file):

                    os.remove(temp_file)

            except Exception:
                pass