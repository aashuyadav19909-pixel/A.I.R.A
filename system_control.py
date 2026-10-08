import os
import subprocess
from pathlib import Path


# ============================================================
# SYSTEM CONTROL
# ============================================================


def lock_pc():

    subprocess.run(
        [
            "rundll32.exe",
            "user32.dll,LockWorkStation"
        ]
    )

    return "Locking your computer."


def shutdown_pc():

    subprocess.run(
        [
            "shutdown",
            "/s",
            "/t",
            "0"
        ]
    )

    return "Shutting down the computer."


def restart_pc():

    subprocess.run(
        [
            "shutdown",
            "/r",
            "/t",
            "0"
        ]
    )

    return "Restarting the computer."


def cancel_shutdown():

    subprocess.run(
        [
            "shutdown",
            "/a"
        ]
    )

    return "Shutdown cancelled."


def open_task_manager():

    subprocess.Popen(
        "taskmgr.exe"
    )

    return "Opening Task Manager."


def open_settings():

    subprocess.Popen(
        [
            "cmd",
            "/c",
            "start",
            "ms-settings:"
        ]
    )

    return "Opening Windows Settings."


def open_downloads():

    downloads = Path.home() / "Downloads"

    if downloads.exists():

        os.startfile(downloads)

        return "Opening Downloads."

    return "I couldn't find your Downloads folder."


def open_documents():

    documents = Path.home() / "Documents"

    if documents.exists():

        os.startfile(documents)

        return "Opening Documents."

    return "I couldn't find your Documents folder."


def open_desktop():

    desktop = Path.home() / "Desktop"

    if desktop.exists():

        os.startfile(desktop)

        return "Opening Desktop."

    return "I couldn't find your Desktop folder."


def system_control(command):

    command = command.lower().strip()

    # ========================================================
    # LOCK
    # ========================================================

    if command in [
        "lock my pc",
        "lock my computer",
        "lock computer",
        "lock pc"
    ]:

        return lock_pc()

    # ========================================================
    # SHUTDOWN
    # ========================================================

    if command in [
        "shutdown",
        "shut down",
        "shutdown computer",
        "shut down computer",
        "turn off computer"
    ]:

        return "CONFIRM_SHUTDOWN"

    # ========================================================
    # RESTART
    # ========================================================

    if command in [
        "restart",
        "restart computer",
        "restart my computer"
    ]:

        return "CONFIRM_RESTART"

    # ========================================================
    # CANCEL SHUTDOWN
    # ========================================================

    if command in [
        "cancel shutdown",
        "cancel shut down"
    ]:

        return cancel_shutdown()

    # ========================================================
    # TASK MANAGER
    # ========================================================

    if command in [
        "open task manager",
        "start task manager"
    ]:

        return open_task_manager()

    # ========================================================
    # SETTINGS
    # ========================================================

    if command in [
        "open settings",
        "open windows settings",
        "start settings"
    ]:

        return open_settings()

    # ========================================================
    # FOLDERS
    # ========================================================

    if command in [
        "open downloads",
        "open my downloads"
    ]:

        return open_downloads()

    if command in [
        "open documents",
        "open my documents"
    ]:

        return open_documents()

    if command in [
        "open desktop",
        "open my desktop"
    ]:

        return open_desktop()

    return None