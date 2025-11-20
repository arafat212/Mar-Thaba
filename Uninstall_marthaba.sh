#!/bin/bash

# MarThaba Pro Uninstaller

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${RED}"
echo "╔════════════════════════════════════════╗"
echo "║         MarThaba Pro Uninstaller       ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root: sudo uninstall-marthaba${NC}"
    exit 1
fi

INSTALL_DIR="/opt/marthaba"
BIN_DIR="/usr/local/bin"
DESKTOP_APP_DIR="/usr/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "This will completely remove MarThaba Pro from your system."
echo "Are you sure you want to continue? (y/n)"
read -r confirmation

if [ "$confirmation" != "y" ] && [ "$confirmation" != "Y" ]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo "Removing MarThaba Pro..."

# Remove launcher
if [ -f "$BIN_DIR/marthaba" ]; then
    rm -f "$BIN_DIR/marthaba"
    echo "✓ Removed launcher"
fi

# Remove desktop entry
if [ -f "$DESKTOP_APP_DIR/marthaba-pro.desktop" ]; then
    rm -f "$DESKTOP_APP_DIR/marthaba-pro.desktop"
    echo "✓ Removed desktop entry"
fi

# Remove autostart entry
if [ -f "$AUTOSTART_DIR/marthaba-pro.desktop" ]; then
    rm -f "$AUTOSTART_DIR/marthaba-pro.desktop"
    echo "✓ Removed autostart entry"
fi

# Remove uninstaller link
if [ -f "$BIN_DIR/uninstall-marthaba" ]; then
    rm -f "$BIN_DIR/uninstall-marthaba"
    echo "✓ Removed uninstaller link"
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ Removed installation directory"
fi

# Remove config files
if [ -f "$HOME/.marthaba_config.json" ]; then
    rm -f "$HOME/.marthaba_config.json"
    echo "✓ Removed config file"
fi

if [ -f "$HOME/.marthaba_history.json" ]; then
    rm -f "$HOME/.marthaba_history.json"
    echo "✓ Removed history file"
fi

# Clean hosts file (remove any MarThaba blocks)
echo "Cleaning hosts file..."
sed -i '/# MarThaba Focus/d' /etc/hosts

echo ""
echo -e "${GREEN}MarThaba Pro has been completely uninstalled!${NC}"
echo "Please restart your browser to clear any remaining blocks."
