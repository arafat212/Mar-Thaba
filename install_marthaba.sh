#!/bin/bash

echo "
╔═══════════════════════════════════════╗
║          MarThaba Pro Installer       ║  
║          Ultimate Focus System        ║
╚═══════════════════════════════════════╝
"

# Check if already installed
if [ -d "/opt/marthaba" ]; then
    echo "[INFO] MarThaba Pro is already installed!"
    echo "[INFO] Would you like to reinstall? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        echo "[INFO] Installation cancelled."
        exit 0
    fi
    echo "[INFO] Removing old installation..."
    sudo rm -rf /opt/marthaba
fi

echo "[1/7] Checking dependencies..."
python3 --version || { 
    echo "[ERROR] Python3 not installed. Installing..."
    sudo apt update && sudo apt install python3 python3-pip python3-tk -y 
}

echo "[2/7] Creating installation directory..."
sudo mkdir -p /opt/marthaba

echo "[3/7] Downloading application files..."
sudo wget -q -O /opt/marthaba/marthaba.py https://raw.githubusercontent.com/arafat212/Mar-Thaba/main/marthaba.py
sudo wget -q -O /opt/marthaba/requirements.txt https://raw.githubusercontent.com/arafat212/Mar-Thaba/main/requirements.txt

echo "[4/7] Installing Python packages..."
sudo pip3 install -q Pillow pycaw screen-brightness-control

echo "[5/7] Creating system command..."
sudo tee /usr/local/bin/marthaba-pro > /dev/null << 'EOF'
#!/bin/bash
python3 /opt/marthaba/marthaba.py
EOF
sudo chmod +x /usr/local/bin/marthaba-pro

echo "[6/7] Creating application menu entry..."
sudo tee /usr/share/applications/marthaba-pro.desktop > /dev/null << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MarThaba Pro
Comment=Ultimate Focus System - Shield Your Time
Exec=python3 /opt/marthaba/marthaba.py
Icon=system-lock-screen
Terminal=false
StartupNotify=true
Categories=Utility;Productivity;
Keywords=focus;productivity;timer;shield;block;
EOF

echo "[7/7] Creating desktop shortcut..."
tee ~/Desktop/MarThaba-Pro.desktop > /dev/null << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MarThaba Pro
Comment=Ultimate Focus System
Exec=python3 /opt/marthaba/marthaba.py
Icon=system-lock-screen
Terminal=false
StartupNotify=true
Categories=Utility;
EOF

chmod +x ~/Desktop/MarThaba-Pro.desktop

echo "
╔═══════════════════════════════════════╗
║         INSTALLATION COMPLETE!        ║
╚═══════════════════════════════════════╝

🎉 MarThaba Pro successfully installed!

📱 Launch Methods:
   • Applications Menu > MarThaba Pro
   • Desktop Shortcut: MarThaba Pro
   • Terminal Command: marthaba-pro
   • Direct: python3 /opt/marthaba/marthaba.py

🛡️  Features:
   • Focus Timer with Shield Protection
   • Website Blocking
   • Multiple Themes
   • Focus History Tracking

🔧 Developer: Arafat Rahman
💡 Shield your time, boost your productivity!

To uninstall: sudo /opt/marthaba/uninstall.sh
"
