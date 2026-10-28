#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

home = Path.home()
palette_file = home / ".cache/noctalia-rgb-palette.json"
output_file = home / ".config/kitty/noctalia-colors.conf"

if not palette_file.exists():
    raise SystemExit(f"No Noctalia palette found: {palette_file}")

palette = json.loads(palette_file.read_text())

mapping = {
    "foreground": "terminal_foreground",
    "background": "terminal_background",
    "cursor": "terminal_cursor",
    "selection_foreground": "terminal_selection_fg",
    "selection_background": "terminal_selection_bg",
    "color0": "terminal_normal_black",
    "color1": "terminal_normal_red",
    "color2": "terminal_normal_green",
    "color3": "terminal_normal_yellow",
    "color4": "terminal_normal_blue",
    "color5": "terminal_normal_magenta",
    "color6": "terminal_normal_cyan",
    "color7": "terminal_normal_white",
    "color8": "terminal_bright_black",
    "color9": "terminal_bright_red",
    "color10": "terminal_bright_green",
    "color11": "terminal_bright_yellow",
    "color12": "terminal_bright_blue",
    "color13": "terminal_bright_magenta",
    "color14": "terminal_bright_cyan",
    "color15": "terminal_bright_white",
}

missing = [source for source in mapping.values() if source not in palette]
if missing:
    raise SystemExit("Missing palette keys: " + ", ".join(missing))

output_file.write_text(
    "# Generated from the Noctalia wallpaper palette. Do not edit manually.\n"
    + "".join(f"{target} {palette[source]}\n"
              for target, source in mapping.items())
)

print(f"Generated {output_file}")

result = subprocess.run([
    "kitty", "@", "set-colors", "--all", str(output_file)
])

if result.returncode != 0:
    print("Colors file created, but live update failed.")
    print("Check that Kitty is running with remote control enabled.")
