#!/bin/bash

echo "
MarThaba Pro Installer
Ultimate Focus System
"

echo "[INFO] Checking Python installation..."
python3 --version || { echo "[ERROR] Python3 not installed"; exit 1; }

echo "[INFO] Creating installation directory..."
sudo mkdir -p /opt/marthaba

echo "[INFO] Downloading MarThaba Pro..."
sudo wget -O /opt/marthaba/marthaba.py https://raw.githubusercontent.com/arafat212/Mar-Thaba/main/marthaba.py

echo "[INFO] Downloading requirements file..."
sudo wget -O /opt/marthaba/requirements.txt https://raw.githubusercontent.com/arafat212/Mar-Thaba/main/requirements.txt

echo "[INFO] Installing Python packages..."
pip3 install -r /opt/marthaba/requirements.txt

echo "[INFO] Creating desktop shortcut..."
cat > ~/Desktop/MarThaba.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MarThaba Pro
Comment=Ultimate Focus System
Exec=python3 /opt/marthaba/marthaba.py
Icon=/opt/marthaba/icon.png
Terminal=false
StartupNotify=true
Categories=Utility;
EOF

chmod +x ~/Desktop/MarThaba.desktop

echo "[SUCCESS] MarThaba Pro installed successfully!"
echo "Location: /opt/marthaba/marthaba.py"
echo "Desktop shortcut created!"
