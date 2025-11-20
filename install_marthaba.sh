#!/bin/bash

# MarThaba Pro Installer
# Ultimate Focus System

set -e

echo ""
echo "MarThaba Pro Installer"
echo "Ultimate Focus System"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 is not installed. Please install Python3 first."
    exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2)
print_info "Python version: $python_version"

# Create installation directory
install_dir="/opt/marthaba"
print_info "Creating installation directory..."
sudo mkdir -p "$install_dir"

# Download MarThaba Pro
print_info "Installing MarThaba Pro..."
cd "$install_dir"

# Download the main marthaba.py file using raw GitHub URL
sudo wget -O marthaba.py https://raw.githubusercontent.com/arafat212/Mar-Thaba/main/marthaba.py

# Download requirements.txt if exists
sudo wget -O requirements.txt https://raw.githubusercontent.com/arafat212/Mar-Thaba/main/requirements.txt

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    print_info "Installing Python dependencies..."
    sudo pip3 install -r requirements.txt
else
    print_warn "requirements.txt not found, skipping dependency installation"
fi

# Create desktop entry
print_info "Creating desktop entry..."
cat > /tmp/marthaba.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MarThaba Pro
Comment=Ultimate Focus System
Exec=python3 $install_dir/marthaba.py
Icon=
Terminal=false
StartupNotify=false
Categories=Utility;
EOF

sudo mv /tmp/marthaba.desktop /usr/share/applications/marthaba.desktop

# Make the script executable
sudo chmod +x marthaba.py

print_info "MarThaba Pro installation completed successfully!"
print_info "Installation directory: $install_dir"
print_info "You can find MarThaba Pro in your application menu or run with: python3 $install_dir/marthaba.py"

# Check if running in GUI environment
if [ -n "$DISPLAY" ]; then
    print_info "Would you like to launch MarThaba Pro now? (y/N)"
    read -r response
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        print_info "Launching MarThaba Pro..."
        python3 "$install_dir/marthaba.py" &
    fi
fi
