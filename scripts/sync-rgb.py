#!/usr/bin/env python3

import json
import colorsys
from pathlib import Path

from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

from ak820 import AK820


from pathlib import Path

STATE = Path.home() / ".cache" / "rgb_enabled"

if not STATE.exists():
    print("RGB is disabled.")
    raise SystemExit


# ============================================================
# Settings
# ============================================================

# Brightness (0.0 - 1.0)
# 1.0 = 100%
# 0.5 = 50%
# 0.35 = 35%
BRIGHTNESS = 0.1
SATURATION = 2

# ============================================================
# Load Noctalia-generated colors
# ============================================================

theme = json.loads(
    Path.home().joinpath(
        ".cache/noctalia-rgb-palette.json"
    ).read_text()
)

palette = [
    theme["primary"],
    theme["secondary"],
    theme["tertiary"],
    theme["primary_fixed_dim"],
    theme["secondary_fixed_dim"],
    theme["tertiary_fixed_dim"],
]


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    # RGB -> HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # Increase/decrease saturation
    s = min(1.0, s * SATURATION)

    # Apply brightness
    v *= BRIGHTNESS
    v = min(1.0, v)

    # HSV -> RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    return RGBColor(
        int(r * 255),
        int(g * 255),
        int(b * 255),
    )

def brighten(color, factor):
    """
    Increase brightness of an RGBColor.
    factor = 1.0 -> unchanged
    factor = 2.0 -> twice as bright (clamped)
    """

    return RGBColor(
        min(255, int(color.red * factor)),
        min(255, int(color.green * factor)),
        min(255, int(color.blue * factor)),
    )

palette = [hex_to_rgb(c) for c in palette]

# Pick the most saturated color from the palette
keyboard_color = brighten(
    max(
        palette,
        key=lambda c: colorsys.rgb_to_hsv(
            c.red / 255,
            c.green / 255,
            c.blue / 255,
        )[1]
    ),
    2.5,   # Try 1.5–2.5
)

# ============================================================
# Connect to OpenRGB
# ============================================================

client = OpenRGBClient()

print(f"Connected to {len(client.devices)} devices\n")

# ============================================================
# Apply gradient
# ============================================================

for device in client.devices:
    print(f"Syncing: {device.name}")

    leds = len(device.leds)
    colors = []

    for i in range(leds):
        index = int(i * len(palette) / leds)
        index = min(index, len(palette) - 1)
        colors.append(palette[index])

    device.set_colors(colors)

print("\nRGB synchronization complete!")
# ============================================================
# Sync AK820 keyboard
# ============================================================

kb = AK820()

kb.static(
    keyboard_color.red,
    keyboard_color.green,
    keyboard_color.blue,
)

kb.close()

print(
    f"Keyboard synchronized! "
    f"({keyboard_color.red}, "
    f"{keyboard_color.green}, "
    f"{keyboard_color.blue})"
)