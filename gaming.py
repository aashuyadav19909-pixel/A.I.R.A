import psutil
import subprocess
import time
import win32gui
import win32process

gaming_mode = False
gaming_start_time = None


# ==========================================
# GAME NAMES
# ==========================================

GAME_NAMES = {
    "Palworld": ["palworld"],
    "Minecraft": ["minecraft"],
    "Valorant": ["valorant"],
    "GTA V": ["grand theft auto v", "gta v"],
    "Roblox": ["roblox"],
    "Fortnite": ["fortnite"],
    "Counter-Strike 2": ["counter-strike 2", "cs2"],
    "ARK": ["ark"],
    "Subnautica": ["subnautica"],
    "Rocket League": ["rocket league"],
    "Apex Legends": ["apex legends"],
}


# ==========================================
# GAMING MODE
# ==========================================

def start_gaming_mode():

    global gaming_mode
    global gaming_start_time

    if gaming_mode:
        return "Gaming mode is already active."

    gaming_mode = True
    gaming_start_time = time.time()

    return "Gaming mode activated."


def stop_gaming_mode():

    global gaming_mode
    global gaming_start_time

    if not gaming_mode:
        return "Gaming mode is not active."

    gaming_mode = False
    gaming_start_time = None

    return "Gaming mode deactivated."


def is_gaming_mode():

    return gaming_mode


def get_gaming_status():

    if gaming_mode:
        return "Gaming mode is currently active."

    return "Gaming mode is currently inactive."


# ==========================================
# ACTIVE WINDOW
# ==========================================

def get_active_window():

    try:

        hwnd = win32gui.GetForegroundWindow()

        if not hwnd:
            return None

        title = win32gui.GetWindowText(hwnd)

        if not title:
            return None

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        return {
            "title": title,
            "pid": pid
        }

    except Exception as error:

        print("Window detection error:", error)

        return None


# ==========================================
# GAME DETECTION
# ==========================================

def detect_game():

    window = get_active_window()

    if not window:
        return None

    title = window["title"].lower()

    for game, names in GAME_NAMES.items():

        for name in names:

            if name in title:
                return game

    try:

        process = psutil.Process(window["pid"])
        process_name = process.name().lower()

        if "palworld" in process_name:
            return "Palworld"

        if "valorant" in process_name:
            return "Valorant"

        if "gta5" in process_name:
            return "GTA V"

        if "roblox" in process_name:
            return "Roblox"

        if "fortnite" in process_name:
            return "Fortnite"

        if process_name == "cs2.exe":
            return "Counter-Strike 2"

        if process_name == "javaw.exe":
            return "Minecraft"

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied
    ):
        pass

    return None


# ==========================================
# GAME STATUS
# ==========================================

def game_status():

    game = detect_game()

    if game:
        return f"You are currently playing {game}."

    window = get_active_window()

    if window:
        return (
            f"I don't recognize the current game. "
            f"The active window is {window['title']}."
        )

    return "I couldn't detect the active game."


# ==========================================
# CPU
# ==========================================

def get_cpu_usage():

    cpu = psutil.cpu_percent(interval=1)

    return f"CPU usage is {cpu} percent."


# ==========================================
# RAM
# ==========================================

def get_ram_usage():

    ram = psutil.virtual_memory()

    used_gb = ram.used / (1024 ** 3)
    total_gb = ram.total / (1024 ** 3)

    return (
        f"RAM usage is {ram.percent} percent. "
        f"{used_gb:.1f} GB of {total_gb:.1f} GB is being used."
    )


# ==========================================
# NVIDIA GPU
# ==========================================

def get_gpu_stats():

    try:

        import pynvml

        pynvml.nvmlInit()

        handle = pynvml.nvmlDeviceGetHandleByIndex(0)

        name = pynvml.nvmlDeviceGetName(handle)

        if isinstance(name, bytes):
            name = name.decode()

        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)

        memory = pynvml.nvmlDeviceGetMemoryInfo(handle)

        temperature = pynvml.nvmlDeviceGetTemperature(
            handle,
            pynvml.NVML_TEMPERATURE_GPU
        )

        used_vram = memory.used / (1024 ** 3)
        total_vram = memory.total / (1024 ** 3)

        pynvml.nvmlShutdown()

        return (
            f"GPU is {name}. "
            f"GPU usage is {utilization.gpu} percent. "
            f"VRAM usage is {used_vram:.1f} GB "
            f"of {total_vram:.1f} GB. "
            f"Temperature is {temperature} degrees Celsius."
        )

    except Exception as error:

        print("GPU monitoring error:", error)

        return "I couldn't read the NVIDIA GPU information."


# ==========================================
# FULL GAMING STATS
# ==========================================

def get_gaming_stats():

    game = detect_game()

    cpu = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory()

    result = []

    if game:
        result.append(f"Game: {game}")
    else:
        result.append("Game: Not detected")

    result.append(f"CPU: {cpu}%")
    result.append(f"RAM: {ram.percent}%")

    try:

        import pynvml

        pynvml.nvmlInit()

        handle = pynvml.nvmlDeviceGetHandleByIndex(0)

        name = pynvml.nvmlDeviceGetName(handle)

        if isinstance(name, bytes):
            name = name.decode()

        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)

        memory = pynvml.nvmlDeviceGetMemoryInfo(handle)

        temperature = pynvml.nvmlDeviceGetTemperature(
            handle,
            pynvml.NVML_TEMPERATURE_GPU
        )

        used_vram = memory.used / (1024 ** 3)
        total_vram = memory.total / (1024 ** 3)

        result.append(f"GPU: {name}")
        result.append(f"GPU Usage: {utilization.gpu}%")
        result.append(
            f"VRAM: {used_vram:.1f} / {total_vram:.1f} GB"
        )
        result.append(f"GPU Temperature: {temperature}°C")

        pynvml.nvmlShutdown()

    except Exception:

        result.append("GPU: NVIDIA information unavailable")

    return " | ".join(result)


# ==========================================
# SESSION TIME
# ==========================================

def get_session_time():

    if not gaming_mode or gaming_start_time is None:
        return "There is no active gaming session."

    elapsed = int(time.time() - gaming_start_time)

    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    return (
        f"Gaming session time is "
        f"{hours} hours, "
        f"{minutes} minutes, "
        f"{seconds} seconds."
    )


# ==========================================
# STEAM
# ==========================================

def launch_steam():

    try:

        subprocess.Popen(
            [
                "cmd",
                "/c",
                "start",
                "",
                "steam://open/main"
            ],
            shell=False
        )

        return "Opening Steam."

    except Exception as error:

        print("Steam error:", error)

        return "I couldn't open Steam."


# ==========================================
# PALWORLD
# ==========================================

def launch_palworld():

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