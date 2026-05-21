import os
import time
import sys
import random
import subprocess
import shutil
from colorama import Fore, Style, init

init(autoreset=True)

# JARVIS ASCII sanatı
JARVIS_ART = [
    "      ██  █████  ██████  ██    ██ ██ ███████ ",
    "      ██ ██   ██ ██   ██ ██    ██ ██ ██      ",
    "      ██ ███████ ██████  ██    ██ ██ ███████ ",
    "  ██  ██ ██   ██ ██   ██  ██  ██  ██      ██ ",
    "   ████  ██   ██ ██   ██   ████   ██ ███████ "
]

def jarvis_ghost_animation():
    # Terminal boyutunu otomatik al
    terminal = shutil.get_terminal_size(fallback=(120, 35))
    cols = terminal.columns
    rows = terminal.lines

    # Windows CMD'yi tam ekrana al ve boyutu senkronize et
    if os.name == 'nt':
        os.system(f'mode con: cols={cols} lines={rows}')

    duration = 15.0
    art_rows = len(JARVIS_ART)
    art_cols = len(JARVIS_ART[0])
    j_y = (rows - art_rows) // 2
    j_y_end = j_y + art_rows
    j_x = (cols - art_cols) // 2
    j_x_end = j_x + art_cols
    cx, cy = cols // 2, rows // 2

    chars = ["0", "1", "X", "θ", "λ", "§", "#", "Δ", "8", "Z"]

    CYAN_BRIGHT = Fore.CYAN + Style.BRIGHT
    BLUE_DIM    = Fore.BLUE + Style.DIM
    BLACK_      = Fore.BLACK
    GREEN_DIM   = Fore.GREEN + Style.DIM
    WHITE_BLOCK = Fore.WHITE + "█"

    rand = random.random
    rand_ch = lambda: random.choice(chars)

    move_home = "\033[H"
    hide_cursor = "\033[?25l"
    show_cursor = "\033[?25h"

    # İmleci gizle
    sys.stdout.write(hide_cursor)
    sys.stdout.flush()

    start_time = time.time()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    jarvis2_path = os.path.join(script_dir, "JARVIS_2.py")

    try:
        while True:
            elapsed = time.time() - start_time
            if elapsed > duration:
                break

            # Her frame'de terminal boyutunu yeniden kontrol et
            terminal = shutil.get_terminal_size(fallback=(cols, rows))
            cols = terminal.columns
            rows = terminal.lines
            cx, cy = cols // 2, rows // 2
            j_y = (rows - art_rows) // 2
            j_y_end = j_y + art_rows
            j_x = (cols - art_cols) // 2
            j_x_end = j_x + art_cols

            sys.stdout.write(move_home)

            ghost_intensity = min(1.0, elapsed / 10.0)
            ghost_sq = ghost_intensity * ghost_intensity
            show_bg_noise = elapsed < 12.0

            if elapsed > 12.0:
                radius = (elapsed - 12.0) * 40.0
                radius_sq = radius * radius
                r_inner_sq = (radius - 3.0) * (radius - 3.0)
                explosion_active = True
            else:
                explosion_active = False

            out_lines = []
            for y in range(rows):
                in_art_y = j_y <= y < j_y_end
                if in_art_y:
                    art_row = JARVIS_ART[y - j_y]
                row_chars = []
                for x in range(cols):
                    if in_art_y and j_x <= x < j_x_end:
                        target_char = art_row[x - j_x]
                        if target_char != " ":
                            rv = rand()
                            if rv < ghost_sq:
                                row_chars.append(CYAN_BRIGHT + target_char)
                            elif rv < ghost_intensity:
                                row_chars.append(BLUE_DIM + rand_ch())
                            else:
                                row_chars.append(" " if rand() > 0.2 else BLACK_ + rand_ch())
                        else:
                            row_chars.append(" ")
                    else:
                        if show_bg_noise and rand() > 0.990:
                            row_chars.append(GREEN_DIM + rand_ch())
                        else:
                            row_chars.append(" ")

                    if explosion_active:
                        dx = x - cx
                        dy = (y * 2.2) - (cy * 2.2)
                        dist_sq = dx*dx + dy*dy
                        if r_inner_sq < dist_sq < radius_sq:
                            row_chars[-1] = WHITE_BLOCK
                        elif dist_sq < r_inner_sq:
                            row_chars[-1] = " "

                out_lines.append("".join(row_chars))

            sys.stdout.write("\n".join(out_lines))
            sys.stdout.flush()
            time.sleep(0.04)

    except KeyboardInterrupt:
        pass
    finally:
        # İmleci geri getir
        sys.stdout.write(show_cursor)
        sys.stdout.flush()

    # ── ANİMASYON BİTTİ → JARVIS_2.PY'Yİ BAŞLAT, KENDİNİ KAPAT ──
    os.system('cls' if os.name == 'nt' else 'clear')
    subprocess.Popen([sys.executable, jarvis2_path])
    sys.exit(0)

if __name__ == "__main__":
    jarvis_ghost_animation()
