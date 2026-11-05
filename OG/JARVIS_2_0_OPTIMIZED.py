"""
JARVIS OG — TikTok Edit Style v4 (18s, 120 BPM beat system, 25 effects)
Beat-driven: every 0.5s a new effect triggers.
Effects: zoom punch, rgb, shake, flash, glitch, invert, sweep,
         whip pan, slowmo->fast, letterbox, film grain, bass drop,
         chromatic, datamosh, slide, spin, mirror, tilt, jitter, pulse
"""
import os
import time
import sys
import math
import random
import subprocess
import shutil

if os.name == "nt":
    try:
        os.system("")
    except Exception:
        pass

try:
    from colorama import init as _cinit
    _cinit(autoreset=True)
except ImportError:
    pass

# ─── RENKLER ─────────────────────────────────────────────
GOLD_BRIGHT = "\033[38;5;226m"
GOLD        = "\033[38;5;220m"
AMBER       = "\033[38;5;214m"
ORANGE      = "\033[38;5;208m"
RED_GOLD    = "\033[38;5;202m"
DEEP_GOLD   = "\033[38;5;178m"
WHITE       = "\033[97m"
RED         = "\033[91m"
CYAN        = "\033[96m"
MAGENTA     = "\033[95m"
BLUE        = "\033[94m"
GREEN       = "\033[92m"
DIM         = "\033[2m"
BOLD        = "\033[1m"
RESET       = "\033[0m"

JARVIS_ART = [
    "      ██  █████  ██████  ██    ██ ██ ███████ ",
    "      ██ ██   ██ ██   ██ ██    ██ ██ ██      ",
    "      ██ ███████ ██████  ██    ██ ██ ███████ ",
    "  ██  ██ ██   ██ ██   ██  ██  ██  ██      ██ ",
    "   ████  ██   ██ ██   ██   ████   ██ ███████ "
]

OG_ART = [
    "  ██████╗  ██████╗ ",
    " ██╔═══██╗██╔════╝ ",
    " ██║   ██║██║  ███╗",
    " ██║   ██║██║   ██║",
    " ╚██████╔╝╚██████╔╝",
    "  ╚═════╝  ╚═════╝ "
]

EDITION = "E D I T I O N"
MATRIX = ["0", "1", "X", "θ", "λ", "§", "#", "Δ", "8", "Z", "¢", "∞"]
BEE_CH = ["✦", "✧", "★", "•", "*", "⋅", "·", "⁕"]
STATIC_CH = ["░", "▒", "▓", "█", "▄", "▀", "■", "□", "▪", "▫"]


# ─── BEAT SİSTEMİ ────────────────────────────────────────
BPM = 120
BEAT = 60.0 / BPM  # 0.5s

# 36 beat için efekt listesi (her beat bir efekt)
BEAT_SEQUENCE = [
    "flash", "zoom", "rgb", "shake",           # 0-2s
    "matrix", "matrix", "glitch", "flash",     # 2-4s
    "drop_jarvis", "drop_jarvis", "drop_jarvis", "drop_jarvis",  # 4-6s (harfler düşer)
    "wave", "color_pulse", "shake", "rgb",     # 6-8s
    "invert", "crt", "freeze", "ghost",        # 8-10s
    "drop_og", "drop_og", "flash", "sweep",    # 10-12s
    "whip", "zoom", "bass_drop", "bass_drop",  # 12-14s (BASS DROP!)
    "shatter", "jitter", "slide", "spin",      # 14-16s
    "mirror", "tilt", "chromatic", "final",    # 16-18s
]


class BeatEngine:
    def __init__(self, total_beats=36):
        self.total = total_beats
        self.current_beat = -1
        self.effect = None
        self.effect_start = 0.0
        self.effect_duration = BEAT * 0.9

    def update(self, elapsed):
        beat_idx = int(elapsed / BEAT)
        if beat_idx != self.current_beat and beat_idx < len(BEAT_SEQUENCE):
            self.current_beat = beat_idx
            self.effect = BEAT_SEQUENCE[beat_idx]
            self.effect_start = elapsed
        return self.effect

    def effect_age(self, elapsed):
        return elapsed - self.effect_start

    def is_active(self, elapsed):
        return self.effect and self.effect_age(elapsed) < self.effect_duration


def jarvis_og_tiktok():
    term = shutil.get_terminal_size(fallback=(120, 35))
    cols, rows = term.columns, term.lines
    if os.name == "nt":
        try:
            os.system(f"mode con: cols={max(cols, 100)} lines={max(rows, 30)}")
        except Exception:
            pass

    T_END = 18.0

    art_rows = len(JARVIS_ART)
    art_cols = len(JARVIS_ART[0])
    og_rows = len(OG_ART)
    og_cols = max(len(line) for line in OG_ART)

    move_home   = "\033[H"
    clear_scr   = "\033[2J"
    hide_cursor = "\033[?25l"
    show_cursor = "\033[?25h"

    sys.stdout.write(hide_cursor + clear_scr)
    sys.stdout.flush()

    start_time = time.time()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    jarvis2_path = os.path.join(script_dir, "JARVIS_2.py")

    # State
    bees = []
    MAX_BEES = 400
    rain = []
    stars = []
    drop_state = {}
    og_drop_state = {}
    for ry in range(art_rows):
        for rx in range(art_cols):
            if rx < len(JARVIS_ART[ry]) and JARVIS_ART[ry][rx] != " ":
                drop_state[(ry, rx)] = {
                    "y": -12.0 - random.uniform(0, 25),
                    "vy": random.uniform(0.8, 2.0),
                    "settled": False,
                }
    for ry in range(og_rows):
        for rx in range(len(OG_ART[ry])):
            if OG_ART[ry][rx] != " ":
                og_drop_state[(ry, rx)] = {
                    "y": -10.0,
                    "vy": random.uniform(1.2, 3.0),
                    "settled": False,
                }

    def add_bee():
        bees.append({
            "x": random.uniform(0, cols - 1), "y": random.uniform(0, rows - 1),
            "vx": random.uniform(-2.5, 2.5), "vy": random.uniform(-2.0, 2.0),
            "life": random.randint(15, 50), "age": 0,
            "char": random.choice(BEE_CH),
            "color": random.choice([GOLD_BRIGHT, GOLD, AMBER, ORANGE]),
        })
    def add_rain():
        rain.append({
            "x": random.randint(0, cols - 1), "y": -1.0,
            "vy": random.uniform(1.5, 4.0),
            "char": random.choice(MATRIX),
            "color": random.choice([GOLD, AMBER, DEEP_GOLD, ORANGE]),
        })

    for _ in range(100):
        stars.append({
            "x": random.randint(0, cols - 1), "y": random.randint(0, rows - 1),
            "bright": random.choice([DIM + GOLD, DIM + AMBER]),
        })

    beat = BeatEngine(36)

    # Shake/zoom/offset (beat'ler arası geçiş için saklanır)
    shake_x = 0; shake_y = 0
    prev_effect = None

    try:
        while True:
            elapsed = time.time() - start_time
            if elapsed > T_END:
                break

            term = shutil.get_terminal_size(fallback=(cols, rows))
            cols, rows = term.columns, term.lines
            cx, cy = cols // 2, rows // 2

            effect = beat.update(elapsed)
            eage = beat.effect_age(elapsed)
            active = beat.is_active(elapsed)

            # Geçiş: yeni efekt başlarsa shake sıfırla
            if effect != prev_effect:
                prev_effect = effect
                shake_x = 0; shake_y = 0

            # ─── Partiküller ─────────────────────────────
            target_bees = int(MAX_BEES * min(1.0, elapsed / 2.0))
            while len(bees) < target_bees:
                add_bee()
            alive = []
            for b in bees:
                b["vx"] += random.uniform(-0.3, 0.3)
                b["vy"] += random.uniform(-0.2, 0.2)
                b["vx"] = max(-3.0, min(3.0, b["vx"]))
                b["vy"] = max(-2.5, min(2.5, b["vy"]))
                b["x"] += b["vx"]; b["y"] += b["vy"]
                if b["x"] < 0: b["x"] = 0; b["vx"] = abs(b["vx"])
                elif b["x"] >= cols: b["x"] = cols - 1; b["vx"] = -abs(b["vx"])
                if b["y"] < 0: b["y"] = 0; b["vy"] = abs(b["vy"])
                elif b["y"] >= rows: b["y"] = rows - 1; b["vy"] = -abs(b["vy"])
                b["age"] += 1
                if b["age"] < b["life"]: alive.append(b)
            bees = alive

            grid = [[" " for _ in range(cols)] for _ in range(rows)]
            cgrid = [[None for _ in range(cols)] for _ in range(rows)]

            for s in stars:
                if 0 <= s["x"] < cols and 0 <= s["y"] < rows:
                    grid[s["y"]][s["x"]] = "·"
                    cgrid[s["y"]][s["x"]] = s["bright"]

            for b in bees:
                bx, by = int(b["x"]), int(b["y"])
                if 0 <= bx < cols and 0 <= by < rows:
                    grid[by][bx] = b["char"]
                    cgrid[by][bx] = b["color"]

            # ─── JARVIS (belirli beat'ten sonra görünür) ─
            show_jarvis = beat.current_beat >= 8  # 4s sonra
            if show_jarvis:
                j_y_base = cy - art_rows // 2 - 2
                j_x_base = cx - art_cols // 2
                for (ry, rx), st in drop_state.items():
                    if not st["settled"]:
                        st["y"] += st["vy"]
                        st["vy"] += 0.12
                        if st["y"] >= ry:
                            st["y"] = ry
                            st["settled"] = True
                    gy = j_y_base + int(st["y"])
                    gx = j_x_base + rx
                    if 0 <= gx < cols and 0 <= gy < rows:
                        grid[gy][gx] = JARVIS_ART[ry][rx]
                        if st["settled"]:
                            rv = random.random()
                            if rv < 0.4: cgrid[gy][gx] = GOLD_BRIGHT + BOLD
                            elif rv < 0.75: cgrid[gy][gx] = GOLD + BOLD
                            else: cgrid[gy][gx] = AMBER + BOLD
                        else:
                            cgrid[gy][gx] = DIM + AMBER
                            for tr in range(1, 5):
                                ty = gy - tr
                                if 0 <= ty < rows and grid[ty][gx] == " ":
                                    grid[ty][gx] = "│"
                                    cgrid[ty][gx] = DIM + DEEP_GOLD

            # ─── OG (belirli beat'ten sonra) ──────────────
            show_og = beat.current_beat >= 20  # 10s sonra
            if show_og:
                og_y_base = cy + art_rows // 2 - 1
                og_x_base = cx - og_cols // 2
                for (ry, rx), st in og_drop_state.items():
                    if not st["settled"]:
                        st["y"] += st["vy"]
                        st["vy"] += 0.25
                        if st["y"] >= ry:
                            st["y"] = ry
                            st["settled"] = True
                    gy = og_y_base + int(st["y"])
                    gx = og_x_base + rx
                    if 0 <= gx < cols and 0 <= gy < rows:
                        grid[gy][gx] = OG_ART[ry][rx]
                        cgrid[gy][gx] = GOLD_BRIGHT + BOLD

            # ─── EFEKT UYGULAMA (beat-driven) ─────────────
            if active:

                # 1) FLASH
                if effect == "flash":
                    alpha = 1.0 - (eage / beat.effect_duration)
                    if alpha > 0.3:
                        for y in range(rows):
                            for x in range(cols):
                                if grid[y][x] != " " or random.random() < alpha:
                                    grid[y][x] = "█"
                                    cgrid[y][x] = WHITE + BOLD

                # 2) ZOOM PUNCH
                elif effect == "zoom":
                    zoom = 1.0 - (eage / beat.effect_duration)
                    if zoom > 0.3:
                        j_y_base = cy - art_rows // 2 - 2
                        j_x_base = cx - art_cols // 2
                        if show_jarvis:
                            for (ry, rx) in drop_state:
                                gy = j_y_base + ry
                                gx = j_x_base + rx
                                if 0 <= gx < cols and 0 <= gy < rows:
                                    for dy in (-1, 0, 1):
                                        for dx in (-1, 0, 1):
                                            ny, nx = gy + dy, gx + dx
                                            if 0 <= ny < rows and 0 <= nx < cols:
                                                grid[ny][nx] = JARVIS_ART[ry][rx]
                                                cgrid[ny][nx] = GOLD_BRIGHT + BOLD

                # 3) RGB SPLIT
                elif effect == "rgb":
                    for y in range(0, rows, 2):
                        offset = random.randint(-6, 6)
                        if offset == 0: continue
                        row_copy = grid[y][:]
                        col_copy = cgrid[y][:]
                        for x in range(cols):
                            src_x = (x + offset) % cols
                            grid[y][x] = row_copy[src_x]
                            cgrid[y][x] = col_copy[src_x]
                    for _ in range(30):
                        gx = random.randint(0, cols - 1)
                        gy = random.randint(0, rows - 1)
                        if grid[gy][gx] != " ":
                            grid[gy][gx] = random.choice(STATIC_CH)
                            cgrid[gy][gx] = random.choice([RED, CYAN, MAGENTA]) + BOLD

                # 4) SHAKE
                elif effect == "shake":
                    inten = 5 * (1 - (eage / beat.effect_duration))
                    shake_x = int(random.uniform(-inten, inten))
                    shake_y = int(random.uniform(-inten, inten) * 0.6)

                # 5) MATRIX
                elif effect == "matrix":
                    density = 0.05 * (1.0 - eage / beat.effect_duration + 0.3)
                    for y in range(rows):
                        for x in range(cols):
                            if grid[y][x] == " " and random.random() < density:
                                grid[y][x] = random.choice(MATRIX)
                                cgrid[y][x] = random.choice([DEEP_GOLD, AMBER, GOLD])

                # 6) GLITCH
                elif effect == "glitch":
                    for _ in range(50):
                        gx = random.randint(0, cols - 1)
                        gy = random.randint(0, rows - 1)
                        grid[gy][gx] = random.choice(STATIC_CH)
                        cgrid[gy][gx] = random.choice([WHITE, RED, CYAN]) + BOLD
                    for y in range(0, rows, 5):
                        offset = random.randint(-8, 8)
                        for x in range(cols):
                            src_x = (x + offset) % cols
                            grid[y][x] = grid[y][src_x]
                            cgrid[y][x] = cgrid[y][src_x]

                # 7) DROP JARVIS (özellikle harfler düşerken)
                elif effect == "drop_jarvis":
                    # Zaten normal akışta düşüyor, sadece altın vurgu ekle
                    pass

                # 8) WAVE
                elif effect == "wave":
                    if show_jarvis:
                        j_y_base = cy - art_rows // 2 - 2
                        j_x_base = cx - art_cols // 2
                        for (ry, rx) in drop_state:
                            wave = int(math.sin(eage * 30 + rx * 0.5) * 2)
                            gy = j_y_base + ry + wave
                            gx = j_x_base + rx
                            if 0 <= gx < cols and 0 <= gy < rows:
                                grid[gy][gx] = JARVIS_ART[ry][rx]
                                cgrid[gy][gx] = GOLD_BRIGHT + BOLD

                # 9) COLOR PULSE
                elif effect == "color_pulse":
                    palette = [GOLD_BRIGHT, AMBER, ORANGE, RED_GOLD, MAGENTA, CYAN, GOLD]
                    idx = int(eage * 30) % len(palette)
                    if show_jarvis:
                        j_y_base = cy - art_rows // 2 - 2
                        j_x_base = cx - art_cols // 2
                        for (ry, rx) in drop_state:
                            gy = j_y_base + ry
                            gx = j_x_base + rx
                            if 0 <= gx < cols and 0 <= gy < rows:
                                grid[gy][gx] = JARVIS_ART[ry][rx]
                                cgrid[gy][gx] = palette[idx] + BOLD

                # 10) INVERT
                elif effect == "invert":
                    for y in range(rows):
                        for x in range(cols):
                            if grid[y][x] != " ":
                                cgrid[y][x] = WHITE + BOLD
                            elif random.random() < 0.4:
                                grid[y][x] = "█"
                                cgrid[y][x] = DIM + GOLD

                # 11) CRT
                elif effect == "crt":
                    for y in range(rows):
                        for x in range(cols):
                            if random.random() < 0.4:
                                grid[y][x] = random.choice(STATIC_CH)
                                cgrid[y][x] = random.choice([DIM + GOLD, DIM + AMBER, WHITE])

                # 12) FREEZE
                elif effect == "freeze":
                    if show_jarvis:
                        j_y_base = cy - art_rows // 2 - 2
                        j_x_base = cx - art_cols // 2
                        for (ry, rx) in drop_state:
                            gy = j_y_base + ry
                            gx = j_x_base + rx
                            if 0 <= gx < cols and 0 <= gy < rows:
                                grid[gy][gx] = JARVIS_ART[ry][rx]
                                cgrid[gy][gx] = GOLD_BRIGHT + BOLD

                # 13) GHOST
                elif effect == "ghost":
                    if show_jarvis:
                        j_y_base = cy - art_rows // 2 - 2
                        j_x_base = cx - art_cols // 2
                        offsets = [(-2, 0, DIM + RED), (0, 0, GOLD_BRIGHT + BOLD), (2, 0, DIM + CYAN)]
                        for off_x, off_y, color in offsets:
                            for (ry, rx) in drop_state:
                                gy = j_y_base + ry + off_y
                                gx = j_x_base + rx + off_x
                                if 0 <= gx < cols and 0 <= gy < rows:
                                    if off_x == 0:
                                        grid[gy][gx] = JARVIS_ART[ry][rx]
                                        cgrid[gy][gx] = color
                                    elif grid[gy][gx] == " ":
                                        grid[gy][gx] = JARVIS_ART[ry][rx]
                                        cgrid[gy][gx] = color

                # 14) DROP OG
                elif effect == "drop_og":
                    pass

                # 15) SWEEP
                elif effect == "sweep":
                    progress = eage / beat.effect_duration
                    sweep_y = int(progress * rows)
                    for x in range(cols):
                        if 0 <= sweep_y < rows:
                            grid[sweep_y][x] = "━"
                            cgrid[sweep_y][x] = GOLD_BRIGHT + BOLD
                    if sweep_y + 1 < rows:
                        for x in range(cols):
                            grid[sweep_y + 1][x] = "·"
                            cgrid[sweep_y + 1][x] = DIM + AMBER

                # 16) WHIP PAN (büyük blur offset)
                elif effect == "whip":
                    inten = 15 * (1 - (eage / beat.effect_duration))
                    for y in range(rows):
                        offset = int(random.uniform(-inten, inten))
                        for x in range(cols):
                            src_x = (x + offset) % cols
                            grid[y][x] = grid[y][src_x]
                            cgrid[y][x] = cgrid[y][src_x]

                # 17) BASS DROP — büyük flash + ring + glitch aynı anda
                elif effect == "bass_drop":
                    progress = eage / beat.effect_duration
                    if progress < 0.15:
                        for y in range(rows):
                            for x in range(cols):
                                grid[y][x] = "█"
                                cgrid[y][x] = WHITE + BOLD
                    else:
                        radius = progress * max(cols, rows) * 1.5
                        r2 = radius * radius
                        r_in2 = max(0.0, radius - 12.0) ** 2
                        for y in range(rows):
                            for x in range(cols):
                                dx = x - cx
                                dy = (y * 2.2) - (cy * 2.2)
                                d2 = dx * dx + dy * dy
                                if r_in2 < d2 < r2:
                                    grid[y][x] = "█"
                                    rv = random.random()
                                    if rv < 0.3: cgrid[y][x] = WHITE + BOLD
                                    elif rv < 0.7: cgrid[y][x] = GOLD_BRIGHT + BOLD
                                    else: cgrid[y][x] = ORANGE + BOLD
                                elif d2 <= r_in2:
                                    grid[y][x] = " "
                                    cgrid[y][x] = None
                        # glitch
                        for _ in range(40):
                            gx = random.randint(0, cols - 1)
                            gy = random.randint(0, rows - 1)
                            if grid[gy][gx] != " ":
                                grid[gy][gx] = random.choice(STATIC_CH)
                                cgrid[gy][gx] = random.choice([RED, CYAN]) + BOLD

                # 18) SHATTER
                elif effect == "shatter":
                    if show_jarvis:
                        j_y_base = cy - art_rows // 2 - 2
                        j_x_base = cx - art_cols // 2
                        for (ry, rx) in drop_state:
                            gy = j_y_base + ry
                            gx = j_x_base + rx
                            if 0 <= gx < cols and 0 <= gy < rows:
                                offset_x = int(eage * 30 * (rx - art_cols // 2))
                                offset_y = int(eage * 25 * (ry - art_rows // 2))
                                ngx = gx + offset_x
                                ngy = gy + offset_y
                                if 0 <= ngx < cols and 0 <= ngy < rows:
                                    grid[ngy][ngx] = JARVIS_ART[ry][rx]
                                    cgrid[ngy][ngx] = random.choice([GOLD, AMBER, ORANGE, RED_GOLD]) + BOLD

                # 19) JITTER (küçük rastgele sarsıntı)
                elif effect == "jitter":
                    for _ in range(80):
                        gx = random.randint(0, cols - 1)
                        gy = random.randint(0, rows - 1)
                        if grid[gy][gx] != " ":
                            dx = random.randint(-1, 1)
                            dy = random.randint(-1, 1)
                            ngx = max(0, min(cols - 1, gx + dx))
                            ngy = max(0, min(rows - 1, gy + dy))
                            grid[ngy][ngx] = grid[gy][gx]
                            cgrid[ngy][ngx] = cgrid[gy][gx]
                            grid[gy][gx] = " "
                            cgrid[gy][gx] = None

                # 20) SLIDE (satırlar yatay kayar)
                elif effect == "slide":
                    progress = eage / beat.effect_duration
                    for y in range(rows):
                        offset = int(progress * 30 * math.sin(y * 0.5))
                        row_copy = grid[y][:]
                        col_copy = cgrid[y][:]
                        for x in range(cols):
                            src_x = (x + offset) % cols
                            grid[y][x] = row_copy[src_x]
                            cgrid[y][x] = col_copy[src_x]

                # 21) SPIN (döndürme benzeri)
                elif effect == "spin":
                    progress = eage / beat.effect_duration
                    angle = progress * math.pi * 2
                    for y in range(rows):
                        for x in range(cols):
                            if grid[y][x] != " ":
                                dx = x - cx
                                dy = y - cy
                                r = math.sqrt(dx * dx + dy * dy)
                                a = math.atan2(dy, dx) + angle * (1 - r / max(cols, rows))
                                nx = int(cx + r * math.cos(a))
                                ny = int(cy + r * math.sin(a))
                                if 0 <= nx < cols and 0 <= ny < rows and nx != x:
                                    ch = grid[y][x]
                                    clr = cgrid[y][x]
                                    grid[ny][nx] = ch
                                    cgrid[ny][nx] = clr

                # 22) MIRROR (sol yarı sağa yansır)
                elif effect == "mirror":
                    for y in range(rows):
                        for x in range(cx):
                            src_x = cx - 1 - x
                            grid[y][cx + x] = grid[y][src_x]
                            cgrid[y][cx + x] = cgrid[y][src_x]

                # 23) TILT (satır satır hafif kayma, eğim)
                elif effect == "tilt":
                    for y in range(rows):
                        offset = int((y - cy) * 0.3)
                        row_copy = grid[y][:]
                        col_copy = cgrid[y][:]
                        for x in range(cols):
                            src_x = (x + offset) % cols
                            grid[y][x] = row_copy[src_x]
                            cgrid[y][x] = col_copy[src_x]

                # 24) CHROMATIC (RGB split hafif)
                elif effect == "chromatic":
                    for y in range(rows):
                        for x in range(cols):
                            if grid[y][x] != " ":
                                if random.random() < 0.4:
                                    # sol kırmızı, sağ mavi
                                    nx = x - 1
                                    if 0 <= nx < cols and grid[y][nx] == " ":
                                        grid[y][nx] = grid[y][x]
                                        cgrid[y][nx] = RED + BOLD
                                    nx = x + 1
                                    if 0 <= nx < cols and grid[y][nx] == " ":
                                        grid[y][nx] = grid[y][x]
                                        cgrid[y][nx] = CYAN + BOLD

                # 25) FINAL (patlama)
                elif effect == "final":
                    radius = eage * 80.0
                    r2 = radius * radius
                    r_in2 = max(0.0, radius - 12.0) ** 2
                    for y in range(rows):
                        for x in range(cols):
                            dx = x - cx
                            dy = (y * 2.2) - (cy * 2.2)
                            d2 = dx * dx + dy * dy
                            if r_in2 < d2 < r2:
                                grid[y][x] = "█"
                                rv = random.random()
                                if rv < 0.3: cgrid[y][x] = WHITE + BOLD
                                elif rv < 0.7: cgrid[y][x] = GOLD_BRIGHT + BOLD
                                else: cgrid[y][x] = ORANGE + BOLD
                            elif d2 <= r_in2:
                                grid[y][x] = " "
                                cgrid[y][x] = None

            # ─── EDITION yazısı (12s sonra) ──────────────
            if elapsed > 12.0 and show_og:
                ed_y = cy + art_rows // 2 + og_rows
                ed_x = cx - len(EDITION) // 2
                reveal = min(len(EDITION), int((elapsed - 12.0) * len(EDITION) / 2.0))
                for i, ch in enumerate(EDITION):
                    if ch == " " or i > reveal: continue
                    gx = ed_x + i
                    if 0 <= gx < cols and 0 <= ed_y < rows:
                        grid[ed_y][gx] = ch
                        cgrid[ed_y][gx] = GOLD + BOLD

            # ─── SCANLINE + FILM GRAIN (her zaman) ────────
            for y in range(0, rows, 4):
                if random.random() < 0.3:
                    for x in range(cols):
                        if grid[y][x] == " ":
                            grid[y][x] = "─"
                            cgrid[y][x] = DIM + GOLD

            for _ in range(30):
                gx = random.randint(0, cols - 1)
                gy = random.randint(0, rows - 1)
                if grid[gy][gx] == " " and random.random() < 0.3:
                    grid[gy][gx] = "·"
                    cgrid[gy][gx] = DIM + AMBER

            # ─── LETTERBOX (üst/alt siyah bar) ────────────
            bar_h = 2
            for y in range(bar_h):
                for x in range(cols):
                    grid[y][x] = " "
                    cgrid[y][x] = None
                    grid[rows - 1 - y][x] = " "
                    cgrid[rows - 1 - y][x] = None

            # ─── RENDER ──────────────────────────────────
            sys.stdout.write(move_home)
            out = []
            for y in range(rows):
                row_str = []
                for x in range(cols):
                    sx = x + shake_x
                    sy = y + shake_y
                    if 0 <= sx < cols and 0 <= sy < rows:
                        ch = grid[sy][sx]
                        color = cgrid[sy][sx]
                    else:
                        ch = " "
                        color = None
                    if color and ch != " ":
                        row_str.append(color + ch + RESET)
                    else:
                        row_str.append(ch)
                out.append("".join(row_str))

            sys.stdout.write("\n".join(out))
            sys.stdout.flush()
            time.sleep(0.016)  # 60 FPS

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(show_cursor + RESET)
        sys.stdout.flush()

    os.system("cls" if os.name == "nt" else "clear")
    print(f"\n{GOLD_BRIGHT}{BOLD}  🏛️  OG EDITION — Launching JARVIS...{RESET}\n")
    subprocess.Popen([sys.executable, jarvis2_path])
    sys.exit(0)


if __name__ == "__main__":
    jarvis_og_tiktok()