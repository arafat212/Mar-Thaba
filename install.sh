#!/bin/bash

echo "
╔═══════════════════════════════════════╗
║        MarThaba Pro QUICK INSTALLER   ║
║        (User Space Installation)      ║
╚═══════════════════════════════════════╝
"

echo "👤 Developer: Arafat Rahman"
echo "🔧 Installation Type: Quick User Install"
echo "📍 Location: ~/.local/share/marthaba/"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ This is QUICK INSTALLER - don't run as root/sudo."
    echo "💡 For system-wide installation, use: sudo ./install_marthaba.sh"
    exit 1
fi

echo "[1/7] Checking dependencies..."
python3 --version || { 
    echo "❌ Python3 not installed. Installing..."
    sudo apt update && sudo apt install python3 python3-pip python3-tk -y 
}

echo "[2/7] Installing Python packages..."
pip3 install --user Pillow pycaw screen-brightness-control || {
    echo "⚠️  Trying without --user flag..."
    pip3 install Pillow pycaw screen-brightness-control
}

echo "[3/7] Creating application directories..."
mkdir -p ~/.local/share/marthaba
mkdir -p ~/.local/bin

echo "[4/7] Copying application files..."
# Check if marthaba.py exists in current directory
if [ -f "marthaba.py" ]; then
    cp marthaba.py ~/.local/share/marthaba/
    cp marthaba.py ~/.local/bin/marthaba.py
    echo "✅ Using local marthaba.py file"
else
    echo "📥 Downloading from GitHub..."
    wget -q -O ~/.local/share/marthaba/marthaba.py https://raw.githubusercontent.com/arafat212/Mar-Thaba/main/marthaba.py
    cp ~/.local/share/marthaba/marthaba.py ~/.local/bin/marthaba.py
    echo "✅ Downloaded marthaba.py from GitHub"
fi

chmod +x ~/.local/share/marthaba/marthaba.py
chmod +x ~/.local/bin/marthaba.py

echo "[5/7] Creating application menu entry..."
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/marthaba.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MarThaba Pro (Quick)
Comment=Ultimate Focus System - Quick Install
Exec=python3 ~/.local/share/marthaba/marthaba.py
Icon=system-lock-screen
Terminal=false
StartupNotify=true
Categories=Utility;Productivity;
Keywords=productivity;focus;block;timer;
EOF

echo "[6/7] Creating desktop shortcut..."
cat > ~/Desktop/MarThaba-Quick.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MarThaba Pro (Quick)
Comment=Ultimate Focus System - Quick Install
Exec=python3 ~/.local/share/marthaba/marthaba.py
Icon=system-lock-screen
Terminal=false
StartupNotify=true
Categories=Utility;
EOF

chmod +x ~/Desktop/MarThaba-Quick.desktop
chmod +x ~/.local/share/applications/marthaba.desktop

echo "[7/7] Creating uninstall script..."
cat > ~/.local/share/marthaba/uninstall.sh << 'EOF'
#!/bin/bash
echo "╔═══════════════════════════════════════╗"
echo "║      MarThaba Pro QUICK UNINSTALLER   ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "Removing MarThaba Pro Quick Install..."
rm -rf ~/.local/share/marthaba
rm -f ~/.local/bin/marthaba.py
rm -f ~/.local/share/applications/marthaba.desktop
rm -f ~/Desktop/MarThaba-Quick.desktop
echo ""
echo "✅ MarThaba Pro Quick Install completely removed!"
echo "💡 Note: Python packages are still installed system-wide."
echo "   To remove them, run: pip3 uninstall Pillow pycaw screen-brightness-control"
EOF

chmod +x ~/.local/share/marthaba/uninstall.sh

echo "
╔═══════════════════════════════════════╗
║         QUICK INSTALLATION COMPLETE!  ║
╚═══════════════════════════════════════╝

🎉 MarThaba Pro Quick Install successful!

📱 Launch from: 
   • Applications Menu > 'MarThaba Pro (Quick)'
   • Desktop Shortcut: 'MarThaba Pro (Quick)'
   • Terminal: python3 ~/.local/share/marthaba/marthaba.py

🛠️  Uninstall: ~/.local/share/marthaba/uninstall.sh

💡 ABOUT THIS INSTALL:
   ✅ User-space installation (no sudo required)
   ✅ Easy to remove
   ✅ Perfect for testing
   ✅ Does not affect system files

🔧 Developer: Arafat Rahman
🚀 Focus on your productivity!

📌 For permanent system-wide installation, use:
   sudo ./install_marthaba.sh
"
