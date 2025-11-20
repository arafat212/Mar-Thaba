#!/bin/bash

echo "
MarThaba Pro Uninstaller
"

echo "[INFO] Removing MarThaba Pro files..."
sudo rm -rf /opt/marthaba

echo "[INFO] Removing desktop shortcut..."
rm -f ~/Desktop/MarThaba.desktop

echo "[INFO] Uninstalling Python packages..."
pip3 uninstall -y Pillow pycaw screen-brightness-control

echo "[SUCCESS] MarThaba Pro completely uninstalled!"
