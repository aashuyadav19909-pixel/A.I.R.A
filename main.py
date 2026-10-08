import threading

from voice import listen, speak
from ai import ask_ai
from commands import execute_command
from aira_hud import AiraHUD


# ==============================
# WAKE COMMANDS
# ==============================

WAKE_COMMANDS = [
    "hello aira",
    "hello ira",
    "hello hira",
    "hey aira",
    "hey ira",
    "hey hira",
    "aira",
    "ira",
    "hira",
    "hello ai ra",
    "hey ai ra"
]


# ==============================
# SETTINGS
# ==============================

WAIT_TIME = 60

EXIT_COMMANDS = [
    "exit",
    "quit",
    "shutdown",
    "goodbye"
]


# ==============================
# WAIT FOR WAKE
# ==============================

def wait_for_wake():

    print("\n" + "=" * 50)
    print("A.I.R.A. is sleeping...")
    print("Say 'Hello Aira' to wake me.")
    print("=" * 50)

    while True:

        command = listen()

        if not command:
            continue

        command_clean = command.lower().strip()

        print("Heard:", command_clean)

        wake_detected = any(
            wake_word in command_clean
            for wake_word in WAKE_COMMANDS
        )

        if wake_detected:

            print("Wake command detected!")

            return


# ==============================
# AWAKE MODE
# ==============================

def awake_mode():

    print("\n" + "=" * 50)
    print("A.I.R.A. ACTIVATED")
    print("=" * 50)

    speak("Yes Aashu?")

    while True:

        print("\nWaiting for your question...")
        print("You have 1 minute.")

        command = listen(timeout=WAIT_TIME)

        # ==========================
        # NO QUESTION
        # ==========================

        if not command:

            print("\nNo question for 1 minute.")

            speak("Going to sleep.")

            return


        print("\nYou:", command)

        command_clean = command.lower().strip()


        # ==========================
        # SHUTDOWN
        # ==========================

        if command_clean in EXIT_COMMANDS:

            speak("Goodbye Aashu.")

            print("A.I.R.A. shutting down.")

            return "EXIT"


        # ==========================
        # MANUAL SLEEP
        # ==========================

        if command_clean in [
            "sleep",
            "go to sleep",
            "sleep now"
        ]:

            speak("Going to sleep.")

            print("A.I.R.A. sleeping.")

            return


        # ==========================
        # COMPUTER COMMAND
        # ==========================

        response = execute_command(command)


        # ==========================
        # AI
        # ==========================

        if response is None:

            print("Thinking...")

            try:

                response = ask_ai(command)

            except Exception as error:

                print("AI ERROR:", error)

                response = (
                    "Sorry Aashu, "
                    "I couldn't connect to the AI."
                )


        # ==========================
        # RESPONSE
        # ==========================

        print("\nA.I.R.A.:")
        print(response)

        speak(response)

        print("Response completed.")


# ==============================
# VOICE SYSTEM
# ==============================

def voice_system():

    print("\nVOICE SYSTEM STARTED")

    speak("A.I.R.A. is online.")

    while True:

        result = None

        # Sleep mode
        wait_for_wake()

        # Awake mode
        result = awake_mode()

        # Completely shut down
        if result == "EXIT":

            print("Voice system shutting down.")

            return

        print("\nReturning to sleep mode...")


# ==============================
# MAIN
# ==============================

def main():

    print("=" * 50)
    print("A.I.R.A.")
    print("Artificial Intelligence Robotics Assistant")
    print("=" * 50)

    # =========================================
    # START VOICE SYSTEM IN BACKGROUND
    # =========================================

    voice_thread = threading.Thread(
        target=voice_system,
        daemon=True
    )

    voice_thread.start()


    # =========================================
    # START GUI
    # GUI stays on MAIN THREAD
    # =========================================

    app = AiraHUD()

    app.mainloop()


# ==============================
# START
# ==============================

if __name__ == "__main__":
    main()