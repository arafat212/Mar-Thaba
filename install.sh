#!/bin/bash
echo "🚀 Installing MarThaba Productivity Guard..."
echo "Developer: Arafat Rahman"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run as root/sudo"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt update
sudo apt install python3 python3-tk -y

# Create directories
echo "📁 Setting up directories..."
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications

# Copy main application
echo "🔧 Installing MarThaba..."
cp marthaba.py ~/.local/bin/marthaba.py
chmod +x ~/.local/bin/marthaba.py

# Create desktop entry
echo "🎯 Creating desktop shortcut..."
cat > ~/.local/share/applications/marthaba.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MarThaba
Comment=Productivity Guard by Arafat Rahman
Exec=python3 ~/.local/bin/marthaba.py
Icon=system-lock-screen
Terminal=false
Categories=Utility;Productivity;
Keywords=productivity;block;focus;
EOF

# Make desktop entry executable
chmod +x ~/.local/share/applications/marthaba.desktop

echo "✅ Installation completed!"
echo "🎉 MarThaba is now installed!"
echo "📝 You can find it in your applications menu or run: python3 ~/.local/bin/marthaba.py"
echo "🔧 Developer: Arafat Rahman"
