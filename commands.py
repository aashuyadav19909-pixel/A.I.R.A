import os
import shutil
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from memory import (
    remember,
    recall,
    forget,
    get_all_memory,
    clear_memory
)

from gaming import (
    start_gaming_mode,
    stop_gaming_mode,
    get_gaming_status,
    game_status,
    get_cpu_usage,
    get_ram_usage,
    get_gpu_stats,
    get_gaming_stats,
    get_session_time,
    launch_steam,
    launch_palworld
)

from system_control import system_control



# ============================================================
# BASIC HELPERS
# ============================================================

def launch_exe(paths, args=None):
    """Try multiple executable paths."""

    if args is None:
        args = []

    for path in paths:
        try:
            if path and Path(path).exists():
                subprocess.Popen([path] + args)
                return True
        except Exception as error:
            print("Launch error:", error)

    return False


# ============================================================
# CHROME
# ============================================================

def get_chrome_path():
    """Find Google Chrome."""

    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        )
    ]

    for path in possible_paths:
        if Path(path).exists():
            return path

    chrome_command = shutil.which("chrome.exe")

    if chrome_command:
        return chrome_command

    return None


def open_chrome(url=None):
    """Open Chrome, optionally with a URL."""

    chrome_path = get_chrome_path()

    if not chrome_path:
        return "I couldn't find Google Chrome."

    try:
        if url:
            subprocess.Popen([
                chrome_path,
                url
            ])
        else:
            subprocess.Popen([
                chrome_path
            ])

        if url:
            return "Opening Chrome."
        return "Opening Google Chrome."

    except Exception as error:
        print("Chrome error:", error)
        return "I couldn't open Google Chrome."


# ============================================================
# WEBSITE IN CHROME
# ============================================================

def open_url_in_chrome(url, name):
    """Open a specific website directly in Chrome."""

    chrome_path = get_chrome_path()

    if not chrome_path:
        return "I couldn't find Google Chrome."

    try:
        subprocess.Popen([
            chrome_path,
            url
        ])

        return f"Opening {name} in Chrome."

    except Exception as error:
        print("Chrome website error:", error)
        return f"I couldn't open {name} in Chrome."


# ============================================================
# YOUTUBE
# ============================================================

def play_youtube(query):
    """Search YouTube and open the first result."""

    try:
        command = [
            "python",
            "-m",
            "yt_dlp",
            "--flat-playlist",
            "--print",
            "webpage_url",
            f"ytsearch1:{query}"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=20
        )

        urls = result.stdout.strip().splitlines()

        if urls:
            url = urls[0]

            chrome_path = get_chrome_path()

            if chrome_path:
                subprocess.Popen([
                    chrome_path,
                    url
                ])
            else:
                webbrowser.open(url)

            return f"Playing {query} on YouTube."

        return "I couldn't find that on YouTube."

    except Exception as error:
        print("YouTube error:", error)
        return "I couldn't open YouTube."


def youtube_search(query):
    """Search YouTube in Chrome."""

    url = f"https://www.youtube.com/results?search_query={quote(query)}"

    return open_url_in_chrome(
        url,
        f"YouTube search for {query}"
    )


# ============================================================
# GOOGLE SEARCH
# ============================================================

def google_search(query):
    """Search Google in Chrome."""

    url = f"https://www.google.com/search?q={quote(query)}"

    return open_url_in_chrome(
        url,
        f"Google search for {query}"
    )


# ============================================================
# WEBSITE COMMANDS
# ============================================================

def open_website(command):
    """
    Open explicitly requested websites in Chrome.
    """

    command = command.lower().strip()

    websites = {
        "open youtube website": (
            "https://www.youtube.com",
            "YouTube"
        ),

        "open google website": (
            "https://www.google.com",
            "Google"
        ),

        "open gmail website": (
            "https://mail.google.com",
            "Gmail"
        ),

        "open github website": (
            "https://github.com",
            "GitHub"
        ),

        "open chatgpt website": (
            "https://chatgpt.com",
            "ChatGPT"
        ),

        "open openrouter website": (
            "https://openrouter.ai",
            "OpenRouter"
        ),

        "open instagram website": (
            "https://www.instagram.com",
            "Instagram"
        ),

        "open reddit website": (
            "https://www.reddit.com",
            "Reddit"
        ),

        "open steam website": (
            "https://store.steampowered.com",
            "Steam website"
        ),

        "open discord website": (
            "https://discord.com/app",
            "Discord website"
        ),

        "open spotify website": (
            "https://open.spotify.com",
            "Spotify website"
        )
    }

    if command in websites:

        url, name = websites[command]

        return open_url_in_chrome(url, name)

    return None


# ============================================================
# VISUAL STUDIO CODE
# ============================================================

def open_vscode():
    """Open Visual Studio Code."""

    code_command = shutil.which("code")

    if code_command:
        try:
            subprocess.Popen([code_command])
            return "Opening Visual Studio Code."
        except Exception as error:
            print("VS Code error:", error)

    possible_paths = [
        os.path.expandvars(
            r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
        ),
        os.path.expandvars(
            r"%PROGRAMFILES%\Microsoft VS Code\Code.exe"
        ),
        os.path.expandvars(
            r"%PROGRAMFILES(X86)%\Microsoft VS Code\Code.exe"
        ),
        os.path.expandvars(
            r"%APPDATA%\Local\Programs\Microsoft VS Code\Code.exe"
        )
    ]

    if launch_exe(possible_paths):
        return "Opening Visual Studio Code."

    try:
        powershell_command = (
            "Get-StartApps | "
            "Where-Object {$_.Name -like '*Visual Studio Code*'} | "
            "Select-Object -First 1 | "
            "ForEach-Object { Start-Process $_.AppID }"
        )

        subprocess.Popen([
            "powershell",
            "-NoProfile",
            "-Command",
            powershell_command
        ])

        return "Opening Visual Studio Code."

    except Exception as error:
        print("VS Code error:", error)
        return "I couldn't find Visual Studio Code."


# ============================================================
# STEAM
# ============================================================

def open_steam():
    """Open the Steam desktop application."""

    possible_paths = [
        r"C:\Program Files (x86)\Steam\steam.exe",
        r"C:\Program Files\Steam\steam.exe",
        os.path.expandvars(
            r"%LOCALAPPDATA%\Steam\steam.exe"
        )
    ]

    if launch_exe(possible_paths):
        return "Opening Steam."

    steam_command = shutil.which("steam.exe")

    if steam_command:
        try:
            subprocess.Popen([steam_command])
            return "Opening Steam."
        except Exception as error:
            print("Steam error:", error)

    try:
        powershell_command = (
            "Get-StartApps | "
            "Where-Object {$_.Name -like '*Steam*'} | "
            "Select-Object -First 1 | "
            "ForEach-Object { Start-Process $_.AppID }"
        )

        subprocess.Popen([
            "powershell",
            "-NoProfile",
            "-Command",
            powershell_command
        ])

        return "Opening Steam."

    except Exception as error:
        print("Steam error:", error)

    return "I couldn't find the Steam desktop application."


# ============================================================
# PALWORLD
# ============================================================

def open_palworld():
    """Launch Palworld through Steam."""

    try:
        subprocess.Popen(
            [
                "cmd",
                "/c",
                "start",
                "",
                "steam://rungameid/1623730"
            ],
            shell=False
        )

        return "Launching Palworld."

    except Exception as error:
        print("Palworld error:", error)
        return "I couldn't launch Palworld."


# ============================================================
# WINDOWS START MENU APPS
# ============================================================

def open_minecraft():
    """Open Minecraft / Minecraft Launcher."""

    # Try Minecraft Launcher executable locations
    possible_paths = [
        os.path.expandvars(
            r"%PROGRAMFILES%\Minecraft Launcher\MinecraftLauncher.exe"
        ),
        os.path.expandvars(
            r"%PROGRAMFILES(X86)%\Minecraft Launcher\MinecraftLauncher.exe"
        ),
        os.path.expandvars(
            r"%LOCALAPPDATA%\Programs\Minecraft Launcher\MinecraftLauncher.exe"
        )
    ]

    if launch_exe(possible_paths):
        return "Opening Minecraft."

    # Try Windows Minecraft Launcher URI
    try:
        subprocess.Popen([
            "cmd",
            "/c",
            "start",
            "",
            "minecraft:"
        ])

        return "Opening Minecraft."

    except Exception as error:
        print("Minecraft error:", error)

    return "I couldn't find Minecraft."


# ============================================================
# DISCORD
# ============================================================

def open_discord():
    """Open Discord desktop application."""

    update_path = os.path.expandvars(
        r"%LOCALAPPDATA%\Discord\Update.exe"
    )

    if Path(update_path).exists():

        try:
            subprocess.Popen([
                update_path,
                "--processStart",
                "Discord.exe"
            ])

            return "Opening Discord."

        except Exception as error:
            print("Discord error:", error)

    discord_command = shutil.which("Discord.exe")

    if discord_command:

        try:
            subprocess.Popen([discord_command])
            return "Opening Discord."

        except Exception:
            pass

    return "I couldn't find Discord."


# ============================================================
# SPOTIFY
# ============================================================

def open_spotify():
    """Open Spotify desktop application."""

    possible_paths = [
        os.path.expandvars(
            r"%APPDATA%\Spotify\Spotify.exe"
        ),
        os.path.expandvars(
            r"%LOCALAPPDATA%\Microsoft\WindowsApps\Spotify.exe"
        )
    ]

    if launch_exe(possible_paths):
        return "Opening Spotify."

    spotify_command = shutil.which("Spotify.exe")

    if spotify_command:

        try:
            subprocess.Popen([spotify_command])
            return "Opening Spotify."

        except Exception:
            pass

    result = open_windows_store_app("Spotify")

    if result:
        return result

    return "I couldn't find Spotify."


# ============================================================
# EDGE
# ============================================================

def open_edge():
    """Open Microsoft Edge."""

    possible_paths = [
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    ]

    if launch_exe(possible_paths):
        return "Opening Microsoft Edge."

    edge_command = shutil.which("msedge.exe")

    if edge_command:

        try:
            subprocess.Popen([edge_command])
            return "Opening Microsoft Edge."

        except Exception:
            pass

    return "I couldn't find Microsoft Edge."


# ============================================================
# NORMAL WINDOWS APPS
# ============================================================

def open_normal_app(command):

    command = command.lower().strip()

    # NOTEPAD
    if command in [
        "open notepad",
        "start notepad",
        "launch notepad"
    ]:
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad."

    # CALCULATOR
    if command in [
        "open calculator",
        "open calc",
        "start calculator",
        "launch calculator"
    ]:
        subprocess.Popen(["calc.exe"])
        return "Opening Calculator."

    # PAINT
    if command in [
        "open paint",
        "start paint",
        "launch paint"
    ]:
        subprocess.Popen(["mspaint.exe"])
        return "Opening Paint."

    # FILE EXPLORER
    if command in [
        "open file explorer",
        "open explorer",
        "start file explorer",
        "launch file explorer"
    ]:
        subprocess.Popen(["explorer.exe"])
        return "Opening File Explorer."

    # TASK MANAGER
    if command in [
        "open task manager",
        "start task manager",
        "launch task manager"
    ]:
        subprocess.Popen(["taskmgr.exe"])
        return "Opening Task Manager."

    # COMMAND PROMPT
    if command in [
        "open command prompt",
        "open cmd",
        "start cmd",
        "launch cmd"
    ]:
        subprocess.Popen(["cmd.exe"])
        return "Opening Command Prompt."

    # POWERSHELL
    if command in [
        "open powershell",
        "start powershell",
        "launch powershell"
    ]:
        subprocess.Popen(["powershell.exe"])
        return "Opening PowerShell."

    # CONTROL PANEL
    if command in [
        "open control panel",
        "start control panel"
    ]:
        subprocess.Popen(["control.exe"])
        return "Opening Control Panel."

    # MINECRAFT
    if command in [
        "open minecraft",
        "start minecraft",
        "launch minecraft"
    ]:
        result = open_windows_store_app("Minecraft")

        if result:
            return result

        return "I couldn't find Minecraft."

    return None


# ============================================================
# MEMORY
# ============================================================

def handle_memory(command):

    command_lower = command.lower().strip()

    # SHOW MEMORY
    if command_lower in [
        "what do you remember about me",
        "what do you remember",
        "show my memories",
        "show memories",
        "list my memories",
        "what do you know about me"
    ]:

        memories = get_all_memory()

        if not memories:
            return "I don't have any saved memories yet."

        lines = ["Here is what I remember:"]

        for key, value in memories.items():
            lines.append(f"{key}: {value}")

        return "\n".join(lines)

    # CLEAR MEMORY
    if command_lower in [
        "clear all memories",
        "clear memory",
        "delete all memories",
        "forget everything you remember",
        "forget everything"
    ]:
        return clear_memory()

    # REMEMBER
    remember_prefixes = [
        "remember that ",
        "remember ",
        "save that ",
        "save "
    ]

    for prefix in remember_prefixes:

        if command_lower.startswith(prefix):

            content = command[len(prefix):].strip()

            if not content:
                return "What should I remember?"

            if " is " in content.lower():

                key, value = content.split(" is ", 1)

                return remember(key, value)

            return (
                "Tell me what to remember. "
                "For example: remember my favorite game is Palworld."
            )

    # FORGET
    forget_prefixes = [
        "forget my ",
        "forget ",
        "delete my ",
        "delete "
    ]

    for prefix in forget_prefixes:

        if command_lower.startswith(prefix):

            key = command[len(prefix):].strip()

            if not key:
                return "What should I forget?"

            return forget(key)

    # RECALL
    recall_prefixes = [
        "what is my ",
        "what's my ",
        "what was my ",
        "do you remember my "
    ]

    for prefix in recall_prefixes:

        if command_lower.startswith(prefix):

            key = command[len(prefix):].strip()

            value = recall(key)

            if value:
                return f"Your {key} is {value}."

            return f"I don't have anything saved about your {key}."

    return None


# ============================================================
# AUTOMATIC MEMORY
# ============================================================

def automatic_memory(command):

    command_lower = command.lower().strip()

    patterns = [
        "my favorite game is ",
        "my favourite game is ",
        "my favorite song is ",
        "my favourite song is ",
        "my favorite anime is ",
        "my favourite anime is ",
        "my favorite movie is ",
        "my favourite movie is ",
        "my favorite color is ",
        "my favourite color is ",
        "my favorite colour is ",
        "my favourite colour is ",
        "my name is "
    ]

    for pattern in patterns:

        if command_lower.startswith(pattern):

            value = command[len(pattern):].strip()

            if not value:
                return None

            if "game" in pattern:
                key = "favorite game"

            elif "song" in pattern:
                key = "favorite song"

            elif "anime" in pattern:
                key = "favorite anime"

            elif "movie" in pattern:
                key = "favorite movie"

            elif "color" in pattern or "colour" in pattern:
                key = "favorite color"

            elif "name" in pattern:
                key = "name"

            else:
                key = "personal fact"

            return remember(key, value)

    return None


# ============================================================
# TIME / DATE
# ============================================================

def handle_time_date(command):

    command_lower = command.lower().strip()

    now = datetime.now()

    # TIME
    if command_lower in [
        "what time is it",
        "what is the time",
        "tell me the time",
        "current time",
        "time"
    ]:

        return f"It is {now.strftime('%I:%M %p')}."

    # DATE
    if command_lower in [
        "what is today's date",
        "what's today's date",
        "what date is it",
        "today's date",
        "current date",
        "date"
    ]:

        return f"Today is {now.strftime('%d %B %Y')}."

    # DAY
    if command_lower in [
        "what day is it",
        "what day is today",
        "today's day",
        "day today"
    ]:

        return f"Today is {now.strftime('%A')}."

    return None


# ============================================================
# MAIN COMMAND ROUTER
# ============================================================
def execute_command(command):
    if not command:
        return None

    command_clean = command.lower().strip()

    # =========================
    # MEMORY
    # =========================

    result = handle_memory(command)
    if result:
        return result

    result = automatic_memory(command)
    if result:
        return result

    # =========================
    # TIME / DATE
    # =========================

    result = handle_time_date(command)
    if result:
        return result

    # =========================
    # GAMING MODE
    # =========================

    if command_clean in [
        "gaming mode",
        "start gaming mode",
        "activate gaming mode",
        "turn on gaming mode",
        "enable gaming mode"
    ]:
        return start_gaming_mode()

    if command_clean in [
        "exit gaming mode",
        "stop gaming mode",
        "deactivate gaming mode",
        "turn off gaming mode",
        "disable gaming mode"
    ]:
        return stop_gaming_mode()

    if command_clean in [
        "gaming status",
        "gaming mode status",
        "is gaming mode on"
    ]:
        return get_gaming_status()

    # =========================
    # GAME DETECTION
    # =========================

    if command_clean in [
        "what game am i playing",
        "what game is running",
        "which game is running",
        "game status",
        "check game"
    ]:
        return game_status()

    # =========================
    # CPU
    # =========================

    if (
        "cpu" in command_clean
        and any(word in command_clean for word in [
            "check",
            "usage",
            "status",
            "using",
            "how much",
            "show"
        ])
    ):
        return get_cpu_usage()

    # =========================
    # RAM
    # =========================

    if (
        ("ram" in command_clean or "memory usage" in command_clean)
        and any(word in command_clean for word in [
            "check",
            "usage",
            "status",
            "using",
            "how much",
            "show"
        ])
    ):
        return get_ram_usage()

    # =========================
    # GPU
    # =========================

    if (
        ("gpu" in command_clean or "graphics card" in command_clean)
        and any(word in command_clean for word in [
            "check",
            "usage",
            "status",
            "using",
            "how much",
            "show"
        ])
    ):
        return get_gpu_stats()

    # =========================
    # VRAM
    # =========================

    if (
        "vram" in command_clean
        and any(word in command_clean for word in [
            "check",
            "usage",
            "status",
            "using",
            "how much",
            "show"
        ])
    ):
        return get_gpu_stats()

    # =========================
    # GAMING STATS
    # =========================

    if (
        "gaming stats" in command_clean
        or "gaming statistics" in command_clean
        or "game statistics" in command_clean
        or "game stats" in command_clean
    ):
        return get_gaming_stats()

    # =========================
    # GAMING SESSION
    # =========================

    if (
        "gaming session" in command_clean
        or "how long have i been gaming" in command_clean
        or "gaming time" in command_clean
    ):
        return get_session_time()

    # =========================
    # SYSTEM CONTROL
    # =========================

    result = system_control(command)
    if result:
        return result

    # =========================
    # YOUTUBE
    # =========================

    if command_clean in [
        "open youtube in chrome",
        "open youtube on chrome",
        "launch youtube in chrome",
        "start youtube in chrome",
        "open youtube using chrome"
    ]:
        return open_url_in_chrome(
            "https://www.youtube.com",
            "YouTube"
        )

    if command_clean.startswith("play "):
        query = command[5:].strip()

        if query:
            return play_youtube(query)

    if command_clean.startswith("search youtube for "):
        query = command[len("search youtube for "):].strip()

        if query:
            return youtube_search(query)

    if command_clean.startswith("youtube search "):
        query = command[len("youtube search "):].strip()

        if query:
            return youtube_search(query)

    # =========================
    # GOOGLE
    # =========================

    if command_clean.startswith("search google for "):
        query = command[len("search google for "):].strip()

        if query:
            return google_search(query)

    if command_clean.startswith("google search "):
        query = command[len("google search "):].strip()

        if query:
            return google_search(query)

    if command_clean.startswith("search for "):
        query = command[len("search for "):].strip()

        if query:
            return google_search(query)

    # =========================
    # VS CODE
    # =========================

    if command_clean in [
        "open vs code",
        "open vscode",
        "open visual studio code",
        "start vs code",
        "start vscode",
        "start visual studio code",
        "launch vs code",
        "launch vscode",
        "launch visual studio code"
    ]:
        return open_vscode()

    # =========================
    # STEAM
    # =========================

    if command_clean in [
        "open steam",
        "start steam",
        "launch steam",
        "open the steam app",
        "start the steam app",
        "launch the steam app"
    ]:
        return open_steam()

    # =========================
    # PALWORLD
    # =========================

    if command_clean in [
        "open palworld",
        "start palworld",
        "launch world",
        "open pal world",
        "start pal world",
        "launch pal world"
    ]:
        return open_palworld()

    # =========================
    # CHROME
    # =========================

    if command_clean in [
        "open chrome",
        "start chrome",
        "launch chrome",
        "open google chrome",
        "start google chrome",
        "launch google chrome"
    ]:
        return open_chrome()

    # =========================
    # EDGE
    # =========================

    if command_clean in [
        "open edge",
        "start edge",
        "launch edge",
        "open microsoft edge",
        "start microsoft edge",
        "launch microsoft edge"
    ]:
        return open_edge()

    # =========================
    # DISCORD
    # =========================

    if command_clean in [
        "open discord",
        "start discord",
        "launch discord",
        "open the discord app",
        "start the discord app",
        "launch the discord app"
    ]:
        return open_discord()

    # =========================
    # SPOTIFY
    # =========================

    if command_clean in [
        "open spotify",
        "start spotify",
        "launch spotify",
        "open the spotify app",
        "start the spotify app",
        "launch the spotify app"
    ]:
        return open_spotify()

    # =========================
    # NORMAL WINDOWS APPS
    # =========================

    result = open_normal_app(command_clean)

    if result:
        return result

    # =========================
    # WEBSITES
    # =========================

    result = open_website(command_clean)

    if result:
        return result

    return None