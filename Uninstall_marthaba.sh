#!/bin/bash

echo "
╔═══════════════════════════════════════╗
║         MarThaba Pro Uninstaller      ║
╚═══════════════════════════════════════╝
"

echo "[1/4] Removing application files..."
sudo rm -rf /opt/marthaba

echo "[2/4] Removing menu entry..."
sudo rm -f /usr/share/applications/marthaba.desktop

echo "[3/4] Removing desktop shortcut..."
rm -f ~/Desktop/MarThaba.desktop

echo "[4/4] Cleaning up packages..."
pip3 uninstall -y Pillow pycaw screen-brightness-control 2>/dev/null

echo "
╔═══════════════════════════════════════╗
║         UNINSTALLATION COMPLETE!      ║
╚═══════════════════════════════════════╝

🗑️  MarThaba Pro completely removed from system.
"
