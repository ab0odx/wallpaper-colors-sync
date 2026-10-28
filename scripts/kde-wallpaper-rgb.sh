
#!/usr/bin/env bash

set -u

PALETTE="$HOME/.cache/noctalia-rgb-palette.json"
RGB_SCRIPT="$HOME/.config/rgb-sync/sync.py"

process_wallpaper() {
    local image_url wall

    image_url=$(qdbus6 org.kde.plasmashell /PlasmaShell \
        org.kde.PlasmaShell.wallpaper 0 2>/dev/null |
        sed -n 's/^Image: file:\/\///p')

    [[ -n "$image_url" ]] || return

    wall="$image_url"

    if [[ ! -f "$wall" ]]; then
        echo "Wallpaper not found: $wall"
        return
    fi

    echo "Generating Noctalia palette from: $wall"

    if noctalia theme "$wall" --scheme vibrant --dark -o "$PALETTE"; then
        echo "Palette generated successfully."

        # Update Kitty colors from the new Noctalia palette
        if python "$HOME/.local/bin/sync-kitty-colors.py"; then
            echo "Kitty synchronization complete."
        else
            echo "Kitty synchronization failed."
        fi

        # Synchronize RGB devices
        if python "$RGB_SCRIPT"; then
            echo "RGB synchronization complete."
        else
            echo "RGB synchronization failed."
        fi
    else
        echo "Noctalia palette generation failed."
    fi
}

# Synchronize the current wallpaper at startup.
process_wallpaper

# Listen for KDE wallpaper-change events; no polling.
dbus-monitor --session \
    "type='signal',interface='org.kde.PlasmaShell',member='wallpaperChanged'" |
while IFS= read -r line; do
    if [[ "$line" == *"member=wallpaperChanged"* ]]; then
        sleep 0.3
        process_wallpaper
    fi
done
