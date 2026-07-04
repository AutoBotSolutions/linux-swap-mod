#!/bin/bash
# Uninstallation script for Linux Swap Optimizer

set -e

echo "Uninstalling Linux Swap Optimizer..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Stop and disable service
echo "Stopping and disabling service..."
systemctl stop swap-optimizer 2>/dev/null || true
systemctl disable swap-optimizer 2>/dev/null || true

# Remove systemd service
echo "Removing systemd service..."
rm -f /etc/systemd/system/swap-optimizer.service
systemctl daemon-reload

# Restore original settings
echo "Restoring original swap settings..."
if [ -f "/opt/swap-optimizer/swap_optimizer.py" ]; then
    python3 /opt/swap-optimizer/swap_optimizer.py --restore 2>/dev/null || true
fi

# Remove installation directory
echo "Removing installation directory..."
rm -rf /opt/swap-optimizer

# Remove config directory (optional, preserves user config)
read -p "Remove configuration directory /etc/swap-optimizer? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf /etc/swap-optimizer
    echo "Configuration directory removed"
else
    echo "Configuration directory preserved"
fi

echo "Uninstallation complete!"
echo "Note: Python dependencies (psutil) were not removed."
