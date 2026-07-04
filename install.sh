#!/bin/bash
# Installation script for Linux Swap Optimizer

set -e

echo "Installing Linux Swap Optimizer for AI Workloads..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Create installation directory
INSTALL_DIR="/opt/swap-optimizer"
mkdir -p $INSTALL_DIR

# Copy files
echo "Copying files to $INSTALL_DIR..."
cp swap_optimizer.py $INSTALL_DIR/
chmod +x $INSTALL_DIR/swap_optimizer.py

# Create config directory
CONFIG_DIR="/etc/swap-optimizer"
mkdir -p $CONFIG_DIR

# Copy config file
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    cp config.json $CONFIG_DIR/
    echo "Config file installed to $CONFIG_DIR/config.json"
else
    echo "Config file already exists, skipping..."
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create systemd service
echo "Creating systemd service..."
cat > /etc/systemd/system/swap-optimizer.service << EOF
[Unit]
Description=Linux Swap Optimizer for AI Workloads
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $INSTALL_DIR/swap_optimizer.py --monitor --config $CONFIG_DIR/config.json
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload

echo "Installation complete!"
echo ""
echo "To enable the service at boot:"
echo "  sudo systemctl enable swap-optimizer"
echo ""
echo "To start the service now:"
echo "  sudo systemctl start swap-optimizer"
echo ""
echo "To check status:"
echo "  sudo systemctl status swap-optimizer"
echo ""
echo "To run once (without service):"
echo "  sudo python3 $INSTALL_DIR/swap_optimizer.py --optimize"
