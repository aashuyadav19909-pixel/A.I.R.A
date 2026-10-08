import customtkinter as ctk
import tkinter as tk
import math
import threading
import time
import random
import os
import sys

# Optional project integrations
try:
    from ai import ask_ai
except Exception:
    ask_ai = None

try:
    from commands import execute_command
except Exception:
    execute_command = None

try:
    from gaming import get_gaming_stats, get_cpu_usage, get_ram_usage, get_gpu_stats, detect_game
except Exception:
    get_gaming_stats = get_cpu_usage = get_ram_usage = get_gpu_stats = detect_game = None


# ============================================================
# A.I.R.A. HUD
# Futuristic transparent JARVIS-style interface for your AIRA
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#02070D"
PANEL = "#06131E"
PANEL_2 = "#081B28"
CYAN = "#00D9FF"
CYAN2 = "#38F1FF"
TEXT = "#E8FBFF"
MUTED = "#75A8B8"
GREEN = "#32FF8A"
WARNING = "#FFD166"
RED = "#FF5577"


class AiraHUD(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("A.I.R.A. — Artificial Intelligence Robotics Assistant")
        self.geometry("1500x900")
        self.minsize(1150, 720)
        self.configure(fg_color=BG)

        self.running = True
        self.listening = False
        self.speaking = False
        self.last_game = "No game detected"
        self.session_start = time.time()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_header()
        self.build_main()
        self.build_bottom_bar()

        self.after(50, self.animate)
        self.after(1000, self.refresh_stats)
        self.after(2000, self.refresh_game)

        self.protocol("WM_DELETE_WINDOW", self.close)

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------
    def build_header(self):
        header = ctk.CTkFrame(
            self,
            height=75,
            fg_color=PANEL,
            corner_radius=20,
            border_width=1,
            border_color="#0B5267"
        )
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=(15, 8))
        header.grid_columnconfigure(1, weight=1)

        # Logo
        logo = ctk.CTkLabel(
            header,
            text="◉  A.I.R.A.",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=CYAN
        )
        logo.grid(row=0, column=0, padx=25, pady=10)

        version = ctk.CTkLabel(
            header,
            text="ARTIFICIAL INTELLIGENCE ROBOTICS ASSISTANT  •  v2.0",
            font=ctk.CTkFont(size=11),
            text_color=MUTED
        )
        version.grid(row=0, column=1, sticky="w")

        self.online_label = ctk.CTkLabel(
            header,
            text="●  ONLINE",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=GREEN
        )
        self.online_label.grid(row=0, column=2, padx=20)

        self.time_label = ctk.CTkLabel(
            header,
            text="--:--",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT
        )
        self.time_label.grid(row=0, column=3, padx=(5, 25))

    # --------------------------------------------------------
    # MAIN LAYOUT
    # --------------------------------------------------------
    def build_main(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=18, pady=5)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=2)
        main.grid_columnconfigure(2, weight=1)
        main.grid_rowconfigure(0, weight=1)

        self.build_left_panel(main)
        self.build_center_panel(main)
        self.build_right_panel(main)

    # --------------------------------------------------------
    # LEFT
    # --------------------------------------------------------
    def build_left_panel(self, parent):
        left = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=22,
            border_width=1,
            border_color="#0A4253"
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left,
            text="SYSTEM STATUS",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=CYAN
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 15))

        self.cpu_value = self.stat_row(left, 1, "CPU", "0%")
        self.ram_value = self.stat_row(left, 2, "RAM", "0%")
        self.gpu_value = self.stat_row(left, 3, "GPU", "0%")
        self.vram_value = self.stat_row(left, 4, "VRAM", "0%")

        ctk.CTkFrame(left, height=1, fg_color="#0C3948").grid(
            row=5, column=0, sticky="ew", padx=20, pady=18
        )

        self.mode_value = self.stat_row(left, 6, "MODE", "NORMAL")
        self.game_value = self.stat_row(left, 7, "GAME", "None")

        ctk.CTkLabel(
            left,
            text="QUICK ACTIONS",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=CYAN
        ).grid(row=8, column=0, sticky="w", padx=20, pady=(25, 10))

        self.action_button(left, 9, "⚡  Gaming Mode", "gaming mode")
        self.action_button(left, 10, "▣  Open Apps", "open apps")
        self.action_button(left, 11, "⌕  YouTube", "open youtube")
        self.action_button(left, 12, "⌘  VS Code", "open vs code")
        self.action_button(left, 13, "◉  System Info", "system status")

    def stat_row(self, parent, row, name, value):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", padx=20, pady=7)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame, text=name, width=55,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=MUTED
        ).grid(row=0, column=0, sticky="w")

        bar = ctk.CTkProgressBar(
            frame, height=7, corner_radius=5,
            fg_color="#09212D",
            progress_color=CYAN
        )
        bar.grid(row=0, column=1, sticky="ew", padx=8)
        bar.set(0)

        value_label = ctk.CTkLabel(
            frame, text=value, width=65,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT
        )
        value_label.grid(row=0, column=2)

        return value_label, bar

    def action_button(self, parent, row, text, command_text):
        btn = ctk.CTkButton(
            parent,
            text=text,
            height=40,
            corner_radius=12,
            fg_color="#081D29",
            hover_color="#0B3547",
            border_width=1,
            border_color="#0D5165",
            text_color=TEXT,
            anchor="w",
            command=lambda: self.run_command(command_text)
        )
        btn.grid(row=row, column=0, sticky="ew", padx=18, pady=5)

    # --------------------------------------------------------
    # CENTER / HOLOGRAM
    # --------------------------------------------------------
    def build_center_panel(self, parent):
        center = ctk.CTkFrame(
            parent,
            fg_color="#020A11",
            corner_radius=25,
            border_width=1,
            border_color="#0A5268"
        )
        center.grid(row=0, column=1, sticky="nsew", padx=8)

        self.canvas = tk.Canvas(
            center,
            bg="#020A11",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Configure>", self.center_resized)

        self.status_label = ctk.CTkLabel(
            center,
            text="READY",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=CYAN
        )
        self.status_label.place(relx=0.5, rely=0.075, anchor="center")

        self.hint_label = ctk.CTkLabel(
            center,
            text='Say "Hey Aira" to activate',
            font=ctk.CTkFont(size=12),
            text_color=MUTED
        )
        self.hint_label.place(relx=0.5, rely=0.115, anchor="center")

        self.aira_name = ctk.CTkLabel(
            center,
            text="A . I . R . A",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=TEXT
        )
        self.aira_name.place(relx=0.5, rely=0.78, anchor="center")

        self.subtitle = ctk.CTkLabel(
            center,
            text="ARTIFICIAL INTELLIGENCE ROBOTICS ASSISTANT",
            font=ctk.CTkFont(size=10),
            text_color=MUTED
        )
        self.subtitle.place(relx=0.5, rely=0.825, anchor="center")

        self.speak_label = ctk.CTkLabel(
            center,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=CYAN2
        )
        self.speak_label.place(relx=0.5, rely=0.93, anchor="center")

    def center_resized(self, event=None):
        self.draw_hologram()

    def draw_hologram(self):
        """Realistic sci-fi HUD: restrained glow, glassy core, fine technical rings."""
        if not hasattr(self, "canvas"):
            return

        self.canvas.delete("holo")

        w = max(self.canvas.winfo_width(), 500)
        h = max(self.canvas.winfo_height(), 500)
        cx = w / 2
        cy = h * 0.46

        t = time.time()
        pulse = (math.sin(t * 2.4) + 1) / 2
        listening_boost = 1.25 if self.listening else 1.0
        speaking_boost = 1.15 if self.speaking else 1.0

        # Very subtle ambient halo — no cartoon-style solid shapes.
        for i in range(9, 0, -1):
            r = 155 + i * 11 + pulse * 4
            alpha_hint = max(1, 12 - i)
            self.canvas.create_oval(
                cx-r, cy-r,
                cx+r, cy+r,
                outline="#063544",
                width=1,
                tags="holo"
            )

        # Precision circular HUD rings.
        rings = [
            (158, "#08708A", 1),
            (172, "#0B4555", 1),
            (188, "#0B6579", 1),
            (205, "#073542", 1),
        ]

        for r, outline, width in rings:
            self.canvas.create_oval(
                cx-r, cy-r,
                cx+r, cy+r,
                outline=outline,
                width=width,
                tags="holo"
            )

        # Broken technical arcs.
        for i, extent in enumerate((55, 38, 75, 44)):
            r = 170 + i * 13
            start_angle = (t * (7 + i * 2) + i * 83) % 360
            self.canvas.create_arc(
                cx-r, cy-r,
                cx+r, cy+r,
                start=start_angle,
                extent=extent,
                style=tk.ARC,
                outline=CYAN if i < 2 else "#0A7085",
                width=2 if i == 0 else 1,
                tags="holo"
            )

        # Fine radial ticks, like a real instrumentation display.
        for i in range(48):
            angle = math.radians(i * 7.5)
            r1 = 208
            r2 = 214 if i % 4 == 0 else 211
            x1 = cx + math.cos(angle) * r1
            y1 = cy + math.sin(angle) * r1
            x2 = cx + math.cos(angle) * r2
            y2 = cy + math.sin(angle) * r2

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="#0A5364" if i % 4 else "#0EA8C4",
                width=1,
                tags="holo"
            )

        # Rotating scan line.
        scan_angle = math.radians((t * 35) % 360)
        scan_r = 196
        self.canvas.create_line(
            cx,
            cy,
            cx + math.cos(scan_angle) * scan_r,
            cy + math.sin(scan_angle) * scan_r,
            fill="#08788E",
            width=1,
            tags="holo"
        )

        # Core: layered glass-like wireframe rather than a cartoon face.
        core_r = 92 + pulse * 3

        # Vertical longitude curves.
        for offset in (-0.55, -0.28, 0, 0.28, 0.55):
            xoff = offset * core_r
            self.canvas.create_oval(
                cx - core_r * 0.55 + xoff,
                cy - core_r,
                cx + core_r * 0.55 + xoff,
                cy + core_r,
                outline="#08798D",
                width=1,
                tags="holo"
            )

        # Horizontal latitude curves.
        for scale in (0.35, 0.62, 0.82):
            rr = core_r * scale
            self.canvas.create_oval(
                cx-core_r,
                cy-rr,
                cx+core_r,
                cy+rr,
                outline="#086278",
                width=1,
                tags="holo"
            )

        # Central glass disc.
        self.canvas.create_oval(
            cx-core_r*0.82,
            cy-core_r*0.82,
            cx+core_r*0.82,
            cy+core_r*0.82,
            outline="#16B9D4",
            width=2,
            tags="holo"
        )

        # Minimal AI eye mark — geometric, not cartoon.
        eye_y = cy - 3
        eye_w = 12 * listening_boost * speaking_boost
        eye_h = 7 * listening_boost

        self.canvas.create_arc(
            cx-eye_w*3.0-eye_w, eye_y-eye_h,
            cx-eye_w*3.0+eye_w, eye_y+eye_h,
            start=200,
            extent=140,
            style=tk.ARC,
            outline="#71F4FF",
            width=2,
            tags="holo"
        )

        self.canvas.create_arc(
            cx+eye_w*2.0, eye_y-eye_h,
            cx+eye_w*4.0, eye_y+eye_h,
            start=200,
            extent=140,
            style=tk.ARC,
            outline="#71F4FF",
            width=2,
            tags="holo"
        )

        # Data particles distributed on the sphere.
        for i in range(80):
            angle = i * 2.39996 + t * 0.08
            radius = core_r * (0.55 + ((i * 17) % 37) / 100)
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius * 0.72
            size = 1 if i % 4 else 2

            self.canvas.create_oval(
                x-size, y-size,
                x+size, y+size,
                fill="#1AB6CC",
                outline="",
                tags="holo"
            )

        # Audio visualization is thin and technical, not a big cartoon waveform.
        if self.listening or self.speaking:
            for i in range(41):
                x = cx - 164 + i * 8
                level = abs(math.sin(t * (10 if self.speaking else 6) + i * 0.62))
                amp = 3 + level * (20 if self.speaking else 12)

                self.canvas.create_line(
                    x,
                    cy + 245 - amp,
                    x,
                    cy + 245 + amp,
                    fill="#17BBD4",
                    width=1,
                    tags="holo"
                )

        # Ground projection: thin concentric technical platform.
        for rx, ry in ((180, 19), (155, 13), (125, 9)):
            self.canvas.create_oval(
                cx-rx,
                cy+220-ry,
                cx+rx,
                cy+220+ry,
                outline="#0B5668",
                width=1,
                tags="holo"
            )

        # Small technical labels around the core.
        self.canvas.create_text(
            cx - 225, cy - 105,
            text="NEURAL CORE  //  ONLINE",
            fill="#32899A",
            font=("Consolas", 8),
            anchor="w",
            tags="holo"
        )
        self.canvas.create_text(
            cx + 120, cy + 120,
            text="AIRA.SYS",
            fill="#277181",
            font=("Consolas", 8),
            anchor="w",
            tags="holo"
        )
        self.canvas.create_text(
            cx - 225, cy + 135,
            text="VOICE LINK",
            fill="#277181",
            font=("Consolas", 8),
            anchor="w",
            tags="holo"
        )

    # --------------------------------------------------------
    # RIGHT
    # --------------------------------------------------------
    def build_right_panel(self, parent):
        right = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        right.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        self.build_game_card(right)
        self.build_memory_card(right)
        self.build_command_card(right)

    def card(self, parent, row, title):
        frame = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=20,
            border_width=1,
            border_color="#0A4253"
        )
        frame.grid(row=row, column=0, sticky="nsew", pady=5)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=CYAN
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(15, 8))

        return frame

    def build_game_card(self, parent):
        frame = self.card(parent, 0, "🎮  ACTIVE GAME")

        self.game_title = ctk.CTkLabel(
            frame,
            text="No game detected",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT
        )
        self.game_title.grid(row=1, column=0, sticky="w", padx=18)

        self.game_stats_label = ctk.CTkLabel(
            frame,
            text="Waiting for game...",
            font=ctk.CTkFont(size=11),
            text_color=MUTED,
            justify="left"
        )
        self.game_stats_label.grid(row=2, column=0, sticky="w", padx=18, pady=(5, 15))

    def build_memory_card(self, parent):
        frame = self.card(parent, 1, "🧠  RECENT MEMORY")

        self.memory_label = ctk.CTkLabel(
            frame,
            text="Memory system connected\n\nReady to recall stored facts.",
            font=ctk.CTkFont(size=11),
            text_color=MUTED,
            justify="left",
            anchor="nw"
        )
        self.memory_label.grid(row=1, column=0, sticky="nsew", padx=18, pady=5)

    def build_command_card(self, parent):
        frame = self.card(parent, 2, "⌁  CURRENT COMMAND")

        self.command_label = ctk.CTkLabel(
            frame,
            text="System ready\n\n• Monitoring system\n• Voice engine ready\n• AI engine ready",
            font=ctk.CTkFont(size=11),
            text_color=MUTED,
            justify="left",
            anchor="nw"
        )
        self.command_label.grid(row=1, column=0, sticky="nsew", padx=18, pady=5)

    # --------------------------------------------------------
    # BOTTOM
    # --------------------------------------------------------
    def build_bottom_bar(self):
        bottom = ctk.CTkFrame(
            self,
            height=70,
            fg_color=PANEL,
            corner_radius=20,
            border_width=1,
            border_color="#0A4253"
        )
        bottom.grid(row=2, column=0, sticky="ew", padx=18, pady=(8, 15))
        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_columnconfigure(1, weight=4)
        bottom.grid_columnconfigure(2, weight=1)

        self.mic_button = ctk.CTkButton(
            bottom,
            text="🎙  LISTEN",
            width=130,
            height=40,
            corner_radius=15,
            fg_color="#082536",
            hover_color="#0D4B61",
            border_width=1,
            border_color=CYAN,
            command=self.toggle_listening
        )
        self.mic_button.grid(row=0, column=0, padx=15)

        self.input_box = ctk.CTkEntry(
            bottom,
            height=42,
            placeholder_text="Type a command to A.I.R.A...",
            fg_color="#04111A",
            border_color="#0D5368",
            text_color=TEXT
        )
        self.input_box.grid(row=0, column=1, sticky="ew", padx=10)
        self.input_box.bind("<Return>", lambda e: self.submit_text())

        self.send_button = ctk.CTkButton(
            bottom,
            text="SEND  ➤",
            width=120,
            height=40,
            corner_radius=15,
            command=self.submit_text
        )
        self.send_button.grid(row=0, column=2, padx=15)

    # --------------------------------------------------------
    # COMMANDS
    # --------------------------------------------------------
    def submit_text(self):
        text = self.input_box.get().strip()
        if not text:
            return

        self.input_box.delete(0, "end")
        self.set_command(text)
        self.run_command(text)

    def run_command(self, command):
        self.set_command(command)

        def worker():
            response = None

            try:
                if execute_command:
                    response = execute_command(command)
            except Exception as e:
                response = f"Command error: {e}"

            if response is None:
                try:
                    if ask_ai:
                        response = ask_ai(command)
                    else:
                        response = "AI module is not connected."
                except Exception as e:
                    response = f"AI error: {e}"

            self.after(0, lambda: self.show_response(str(response)))

        threading.Thread(target=worker, daemon=True).start()

    def show_response(self, response):
        self.set_command(response[:120])
        self.speaking = True
        self.status_label.configure(text="A.I.R.A. SPEAKING")
        self.speak_label.configure(text=response[:140])

        # Visual speaking effect lasts briefly.
        self.after(3500, self.stop_speaking)

    def stop_speaking(self):
        self.speaking = False
        self.status_label.configure(text="READY")
        self.speak_label.configure(text="")

    def toggle_listening(self):
        self.listening = not self.listening

        if self.listening:
            self.status_label.configure(text="LISTENING...")
            self.hint_label.configure(text="Listening for your command")
            self.mic_button.configure(text="■  STOP")
        else:
            self.status_label.configure(text="READY")
            self.hint_label.configure(text='Say "Hey Aira" to activate')
            self.mic_button.configure(text="🎙  LISTEN")

    def set_command(self, text):
        self.command_label.configure(
            text=f"• Processing...\n\n{text[:160]}"
        )

    # --------------------------------------------------------
    # SYSTEM MONITORING
    # --------------------------------------------------------
    def refresh_stats(self):
        if not self.running:
            return

        try:
            if get_cpu_usage:
                cpu = float(get_cpu_usage())
            else:
                cpu = 0
        except Exception:
            cpu = 0

        try:
            if get_ram_usage:
                ram_result = get_ram_usage()
                ram = float(ram_result)
            else:
                ram = 0
        except Exception:
            ram = 0

        self.cpu_value[0].configure(text=f"{cpu:.0f}%")
        self.cpu_value[1].set(max(0, min(cpu / 100, 1)))

        self.ram_value[0].configure(text=f"{ram:.0f}%")
        self.ram_value[1].set(max(0, min(ram / 100, 1)))

        try:
            gpu = get_gpu_stats() if get_gpu_stats else None

            if isinstance(gpu, dict):
                gpu_usage = gpu.get("gpu_usage", gpu.get("utilization", 0))
                vram_usage = gpu.get("vram_usage", gpu.get("memory_percent", 0))
            else:
                gpu_usage = 0
                vram_usage = 0

            self.gpu_value[0].configure(text=f"{float(gpu_usage):.0f}%")
            self.gpu_value[1].set(max(0, min(float(gpu_usage) / 100, 1)))

            self.vram_value[0].configure(text=f"{float(vram_usage):.0f}%")
            self.vram_value[1].set(max(0, min(float(vram_usage) / 100, 1)))

        except Exception:
            self.gpu_value[0].configure(text="N/A")
            self.vram_value[0].configure(text="N/A")

        self.time_label.configure(text=time.strftime("%H:%M:%S"))
        self.after(1500, self.refresh_stats)

    def refresh_game(self):
        if not self.running:
            return

        try:
            game = detect_game() if detect_game else None

            if not game:
                game = "No game detected"

            self.last_game = str(game)
            self.game_title.configure(text=self.last_game)

            if get_gaming_stats:
                stats = get_gaming_stats()
                if isinstance(stats, dict):
                    self.game_stats_label.configure(
                        text=(
                            f"CPU   {stats.get('cpu', 'N/A')}\n"
                            f"RAM   {stats.get('ram', 'N/A')}\n"
                            f"GPU   {stats.get('gpu', 'N/A')}\n"
                            f"VRAM  {stats.get('vram', 'N/A')}"
                        )
                    )

        except Exception:
            pass

        self.after(2500, self.refresh_game)

    # --------------------------------------------------------
    # ANIMATION
    # --------------------------------------------------------
    def animate(self):
        if not self.running:
            return

        self.draw_hologram()
        self.after(60, self.animate)

    def close(self):
        self.running = False
        self.destroy()


def run_gui():
    app = AiraHUD()
    app.mainloop()


if __name__ == "__main__":
    run_gui()