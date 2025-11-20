#!/bin/bash

# MarThaba Pro Installer
# Author: archa212
# Version: 1.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Installation directories
INSTALL_DIR="/opt/marthaba"
BIN_DIR="/usr/local/bin"
DESKTOP_APP_DIR="/usr/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║         MarThaba Pro Installer         ║"
echo "║           Ultimate Focus System        ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root: sudo ./install_marthaba.sh${NC}"
    exit 1
fi

# Function to print status
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 is not installed. Installing..."
    apt update
    apt install -y python3 python3-tk
fi

# Create installation directory
print_status "Creating installation directory..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_APP_DIR"
mkdir -p "$AUTOSTART_DIR"

# Download or copy the application
print_status "Installing MarThaba Pro..."
if [ -f "marthaba.py" ]; then
    cp marthaba.py "$INSTALL_DIR/"
else
    # Download from GitHub release
    wget -O "$INSTALL_DIR/marthaba.py" "https://github.com/archa212/Mar-Thaba/releases/latest/download/marthaba.py"
fi

# Make executable
chmod +x "$INSTALL_DIR/marthaba.py"

# Create launcher script
print_status "Creating launcher script..."
cat > "$BIN_DIR/marthaba" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
python3 marthaba.py
EOF

chmod +x "$BIN_DIR/marthaba"

# Create desktop entry
print_status "Creating desktop application entry..."
cat > "$DESKTOP_APP_DIR/marthaba-pro.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MarThaba Pro
Comment=Ultimate Focus System
Exec=$BIN_DIR/marthaba
Icon=system-run
Categories=Utility;Productivity;
Terminal=false
StartupNotify=true
EOF

# Ask for autostart
print_status "Would you like to enable auto-start on boot? (y/n)"
read -r enable_autostart

if [ "$enable_autostart" = "y" ] || [ "$enable_autostart" = "Y" ]; then
    cp "$DESKTOP_APP_DIR/marthaba-pro.desktop" "$AUTOSTART_DIR/"
    print_success "Auto-start enabled!"
fi

# Create uninstaller
print_status "Creating uninstaller..."
cat > "$INSTALL_DIR/uninstall_marthaba.sh" << EOF
#!/bin/bash

# MarThaba Pro Uninstaller

set -e

echo "Uninstalling MarThaba Pro..."

# Remove files
rm -f "$BIN_DIR/marthaba"
rm -f "$DESKTOP_APP_DIR/marthaba-pro.desktop"
rm -f "$AUTOSTART_DIR/marthaba-pro.desktop"

# Remove installation directory
rm -rf "$INSTALL_DIR"

# Remove config files
rm -f "$HOME/.marthaba_config.json"
rm -f "$HOME/.marthaba_history.json"

echo "MarThaba Pro has been completely uninstalled!"
echo "Please restart your browser to clear any remaining blocks."
EOF

chmod +x "$INSTALL_DIR/uninstall_marthaba.sh"

# Create symbolic link for easy uninstall
ln -sf "$INSTALL_DIR/uninstall_marthaba.sh" "$BIN_DIR/uninstall-marthaba"

print_success "MarThaba Pro installed successfully!"
echo ""
echo -e "${GREEN}Installation Details:${NC}"
echo "• Application: $INSTALL_DIR/marthaba.py"
echo "• Launcher: $BIN_DIR/marthaba"
echo "• Desktop Entry: $DESKTOP_APP_DIR/marthaba-pro.desktop"
echo "• Uninstaller: $BIN_DIR/uninstall-marthaba"
echo ""
echo -e "${GREEN}Usage:${NC}"
echo "• Run from terminal: marthaba"
echo "• Run from application menu: Search 'MarThaba Pro'"
echo "• Uninstall: sudo uninstall-marthaba"
echo ""
print_success "Installation completed! You can now run 'marthaba' from terminal or find it in your applications menu."
