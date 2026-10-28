# Wallpaper Color Sync

Automatically synchronize Kitty terminal colors and OpenRGB lighting
with the current KDE Plasma wallpaper using Noctalia's color generation.

## Features

- Detects KDE Plasma wallpaper changes through D-Bus.
- Generates a color palette using the Noctalia CLI.
- Updates Kitty terminal colors.
- Synchronizes supported OpenRGB devices.

## Requirements

- Linux with KDE Plasma
- Python 3
- Noctalia CLI
- Kitty terminal
- OpenRGB and the dependencies required by the RGB sync script
- qdbus6, dbus-monitor, and systemd user services

## How it works

1. KDE Plasma emits a wallpaper-change event.
2. The watcher retrieves the current wallpaper.
3. Noctalia generates a palette.
4. The Kitty sync script updates terminal colors.
5. The RGB sync script updates connected devices.

## Installation

Installation instructions will be added after the install script
and configuration requirements are finalized.

## Notes

Review the scripts and device-specific settings before running them.
The RGB synchronization script may require customization for your
hardware and OpenRGB configuration.
