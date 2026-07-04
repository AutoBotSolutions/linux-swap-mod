# Configuration Guide

## Configuration File Location

The main configuration file is located at:
```
/etc/swap-optimizer/config.json
```

## Configuration Structure

```json
{
  "swappiness": 10,
  "vfs_cache_pressure": 75,
  "page_cluster": 0,
  "min_free_kbytes": 65536,
  "watermark_scale_factor": 200,
  "cpu_threshold": 80,
  "memory_threshold": 85,
  "ai_processes": [
    "python", "jupyter", "ollama", "llama", "tensor", "torch"
  ],
  "ide_processes": [
    "code", "cursor", "idea", "pycharm", "webstorm", "phpstorm",
    "clion", "rider", "datagrip", "rubymine", "appcode",
    "goland", "android-studio", "vscode", "atom", "sublime",
    "emacs", "vim", "nvim", "neovim", "nano", "gedit",
    "kate", "kwrite", "geany", "code-insiders", "codium"
  ],
  "interactive_processes": [
    "firefox", "chrome", "chromium", "brave", "opera",
    "thunderbird", "evolution", "discord", "slack", "telegram",
    "zoom", "teams", "skype", "vlc", "mpv", "mplayer"
  ],
  "background_processes": [
    "systemd", "cron", "anacron", "atd", "rsyslog",
    "dbus", "NetworkManager", "bluetooth", "cups", "avahi"
  ],
  "optimize_all_apps": true,
  "check_interval": 5,
  "aggressive_mode": false,
  "log_level": "INFO"
}
```

## Parameter Reference

### Swap Parameters

#### swappiness
- **Type**: Integer
- **Range**: 0-100
- **Default**: 10
- **Description**: Controls the kernel's tendency to swap out memory
- **Lower values**: Less swapping, more RAM usage
- **Higher values**: More swapping, less RAM usage
- **Recommendations**:
  - Low-end systems (< 4GB RAM): 5-10
  - Mid-range systems (4-8GB RAM): 10-15
  - High-end systems (> 8GB RAM): 15-20

#### vfs_cache_pressure
- **Type**: Integer
- **Range**: 0-100
- **Default**: 75
- **Description**: Controls the kernel's preference for reclaiming memory vs caching
- **Lower values**: More aggressive caching
- **Higher values**: More aggressive memory reclaim
- **Recommendations**:
  - File-heavy workloads: 50-75
  - Memory-heavy workloads: 75-100

#### page_cluster
- **Type**: Integer
- **Range**: 0-3
- **Default**: 0
- **Description**: Number of pages to swap together (2^n pages)
- **0**: 1 page (no clustering)
- **1**: 2 pages
- **2**: 4 pages
- **3**: 8 pages
- **Recommendations**:
  - Low-latency needs: 0
  - High-throughput needs: 2-3

#### min_free_kbytes
- **Type**: Integer
- **Range**: 0-∞
- **Default**: 65536 (64MB)
- **Description**: Minimum free memory in kilobytes
- **Purpose**: Prevents out-of-memory situations
- **Recommendations**:
  - < 4GB RAM: 131072 (128MB)
  - 4-8GB RAM: 65536 (64MB)
  - > 8GB RAM: 32768 (32MB)

#### watermark_scale_factor
- **Type**: Integer
- **Range**: 10-1000
- **Default**: 200
- **Description**: Scale factor for memory watermarks
- **Higher values**: More aggressive memory management
- **Recommendations**:
  - Conservative: 100-150
  - Balanced: 200
  - Aggressive: 300-400

### Threshold Parameters

#### cpu_threshold
- **Type**: Integer
- **Range**: 0-100
- **Default**: 80
- **Description**: CPU usage percentage that triggers adaptive mode
- **Effect**: When CPU exceeds this, swappiness increases
- **Recommendations**:
  - CPU-bound systems: 70-80
  - I/O-bound systems: 85-95

#### memory_threshold
- **Type**: Integer
- **Range**: 0-100
- **Default**: 85
- **Description**: Memory usage percentage that triggers adaptive mode
- **Effect**: When memory exceeds this, swappiness increases
- **Recommendations**:
  - Low-memory systems: 75-85
  - High-memory systems: 90-95

### Process Detection

#### ai_processes
- **Type**: Array of strings
- **Default**: ["python", "jupyter", "ollama", "llama", "tensor", "torch"]
- **Description**: AI/ML process names to identify and prioritize (highest priority)
- **Matching**: Case-insensitive substring match
- **Examples**:
  ```json
  "ai_processes": [
    "python",      # Matches python, python3, etc.
    "jupyter",     # Matches Jupyter notebooks
    "ollama",      # Matches Ollama LLM
    "my-ai-app"    # Custom AI application
  ]
  ```

#### ide_processes
- **Type**: Array of strings
- **Default**: ["code", "cursor", "idea", "pycharm", "webstorm", "phpstorm", "clion", "rider", "datagrip", "rubymine", "appcode", "goland", "android-studio", "vscode", "atom", "sublime", "emacs", "vim", "nvim", "neovim", "nano", "gedit", "kate", "kwrite", "geany", "code-insiders", "codium"]
- **Description**: IDE process names to identify and prioritize (high priority)
- **Matching**: Case-insensitive substring match
- **Examples**:
  ```json
  "ide_processes": [
    "code",        # Matches VS Code
    "idea",        # Matches IntelliJ IDEA
    "pycharm",     # Matches PyCharm
    "vim",         # Matches Vim/Neovim
    "my-editor"    # Custom editor
  ]
  ```

#### interactive_processes
- **Type**: Array of strings
- **Default**: ["firefox", "chrome", "chromium", "brave", "opera", "thunderbird", "evolution", "discord", "slack", "telegram", "zoom", "teams", "skype", "vlc", "mpv", "mplayer"]
- **Description**: Interactive application names to identify and prioritize (medium priority)
- **Matching**: Case-insensitive substring match
- **Examples**:
  ```json
  "interactive_processes": [
    "firefox",     # Matches Firefox browser
    "chrome",      # Matches Chrome browser
    "discord",     # Matches Discord
    "vlc",         # Matches VLC media player
    "my-app"       # Custom interactive app
  ]
  ```

#### background_processes
- **Type**: Array of strings
- **Default**: ["systemd", "cron", "anacron", "atd", "rsyslog", "dbus", "NetworkManager", "bluetooth", "cups", "avahi"]
- **Description**: Background process names to identify and deprioritize (low priority)
- **Matching**: Case-insensitive substring match
- **Examples**:
  ```json
  "background_processes": [
    "systemd",     # Matches systemd services
    "cron",        # Matches cron jobs
    "rsyslog",     # Matches logging daemon
    "my-service"   # Custom background service
  ]
  ```

### Operational Parameters

#### check_interval
- **Type**: Integer
- **Range**: 1-60
- **Default**: 5
- **Description**: Monitoring interval in seconds
- **Lower values**: More responsive, higher CPU usage
- **Higher values**: Less responsive, lower CPU usage
- **Recommendations**:
  - Real-time needs: 1-3
  - Normal operation: 5-10
  - Background operation: 15-30

#### aggressive_mode
- **Type**: Boolean
- **Default**: false
- **Description**: If true, disables swap when RAM is sufficient
- **Condition**: Disables swap when memory < 70%
- **Warning**: Use only on systems with adequate RAM
- **Recommendations**:
  - < 4GB RAM: false
  - 4-8GB RAM: false
  - > 8GB RAM: true

#### optimize_all_apps
- **Type**: Boolean
- **Default**: true
- **Description**: If true, optimizes all running applications across all categories
- **Effect**: Enables general application optimization mode
- **Legacy mode**: When false, only optimizes AI and IDE processes
- **Recommendations**:
  - General desktop usage: true
  - Dedicated AI/IDE workstation: false
  - Server environment: false

#### log_level
- **Type**: String
- **Values**: "DEBUG", "INFO", "WARNING", "ERROR"
- **Default**: "INFO"
- **Description**: Logging verbosity level
- **Recommendations**:
  - Troubleshooting: "DEBUG"
  - Normal operation: "INFO"
  - Production: "WARNING"

## Configuration Profiles

### Low-End System Profile (< 4GB RAM)

```json
{
  "swappiness": 5,
  "vfs_cache_pressure": 50,
  "page_cluster": 0,
  "min_free_kbytes": 131072,
  "watermark_scale_factor": 300,
  "cpu_threshold": 70,
  "memory_threshold": 75,
  "check_interval": 3,
  "aggressive_mode": false,
  "log_level": "INFO"
}
```

### Mid-Range System Profile (4-8GB RAM)

```json
{
  "swappiness": 10,
  "vfs_cache_pressure": 75,
  "page_cluster": 0,
  "min_free_kbytes": 65536,
  "watermark_scale_factor": 200,
  "cpu_threshold": 80,
  "memory_threshold": 85,
  "check_interval": 5,
  "aggressive_mode": false,
  "log_level": "INFO"
}
```

### High-End System Profile (> 8GB RAM)

```json
{
  "swappiness": 15,
  "vfs_cache_pressure": 100,
  "page_cluster": 1,
  "min_free_kbytes": 32768,
  "watermark_scale_factor": 150,
  "cpu_threshold": 85,
  "memory_threshold": 90,
  "check_interval": 10,
  "aggressive_mode": true,
  "log_level": "WARNING"
}
```

### AI Development Profile

```json
{
  "swappiness": 8,
  "vfs_cache_pressure": 60,
  "page_cluster": 0,
  "min_free_kbytes": 98304,
  "watermark_scale_factor": 250,
  "cpu_threshold": 75,
  "memory_threshold": 80,
  "ai_processes": [
    "python", "jupyter", "tensor", "pytorch",
    "code", "cursor", "idea", "pycharm"
  ],
  "check_interval": 3,
  "aggressive_mode": false,
  "log_level": "INFO"
}
```

### Web Development Profile

```json
{
  "swappiness": 12,
  "vfs_cache_pressure": 80,
  "page_cluster": 1,
  "min_free_kbytes": 65536,
  "watermark_scale_factor": 180,
  "cpu_threshold": 85,
  "memory_threshold": 85,
  "ai_processes": [
    "node", "npm", "code", "cursor",
    "chrome", "firefox", "docker"
  ],
  "check_interval": 5,
  "aggressive_mode": false,
  "log_level": "INFO"
}
```

## Applying Configuration Changes

### Method 1: Direct Edit

```bash
sudo nano /etc/swap-optimizer/config.json
# Make changes
sudo systemctl restart swap-optimizer
```

### Method 2: Profile Switch

```bash
# Backup current config
sudo cp /etc/swap-optimizer/config.json /etc/swap-optimizer/config.json.backup

# Copy new profile
sudo cp low-end-profile.json /etc/swap-optimizer/config.json

# Restart service
sudo systemctl restart swap-optimizer
```

### Method 3: Command Line Override

```bash
# Use custom config temporarily
sudo python3 /opt/swap-optimizer/swap_optimizer.py \
  --monitor \
  --config /path/to/custom-config.json
```

## Validation

### Check Current Configuration

```bash
sudo python3 /opt/swap-optimizer/swap_optimizer.py --status
```

### Verify Applied Settings

```bash
# Check swap parameters
sudo sysctl vm.swappiness
sudo sysctl vm.vfs_cache_pressure
sudo sysctl vm.page-cluster

# Check service status
sudo systemctl status swap-optimizer
```

### Test Configuration

```bash
# Apply configuration
sudo python3 /opt/swap-optimizer/swap_optimizer.py --optimize

# Monitor for issues
sudo journalctl -u swap-optimizer -f

# If issues occur, restore
sudo python3 /opt/swap-optimizer/swap_optimizer.py --restore
```

## Common Configuration Mistakes

### 1. Aggressive Mode on Low RAM
**Problem**: Setting `aggressive_mode: true` on systems with < 4GB RAM
**Solution**: Keep `aggressive_mode: false` for low-memory systems

### 2. Too Low Swappiness
**Problem**: Setting `swappiness: 0` can cause OOM
**Solution**: Minimum recommended value is 5

### 3. Insufficient min_free_kbytes
**Problem**: Too low `min_free_kbytes` can cause system freeze
**Solution**: Use at least 64MB (65536) for most systems

### 4. Too Frequent Checking
**Problem**: `check_interval: 1` causes high CPU usage
**Solution**: Use 3-5 seconds for most cases

### 5. Missing Process Names
**Problem**: AI processes not being prioritized
**Solution**: Add process names to `ai_processes` array

## Advanced Configuration

### Per-User Configuration

Create user-specific configs:
```bash
mkdir -p ~/.config/swap-optimizer
cp /etc/swap-optimizer/config.json ~/.config/swap-optimizer/
# Edit user config
python3 /opt/swap-optimizer/swap_optimizer.py \
  --config ~/.config/swap-optimizer/config.json
```

### Conditional Configuration

Use environment variables:
```bash
export SWAP_OPTIMIZER_MODE="development"
sudo -E python3 /opt/swap-optimizer/swap_optimizer.py --monitor
```

### Dynamic Configuration

Create a script that generates config based on system:
```bash
#!/bin/bash
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
if [ $RAM_GB -lt 4 ]; then
    cp low-end-profile.json /etc/swap-optimizer/config.json
elif [ $RAM_GB -lt 8 ]; then
    cp mid-range-profile.json /etc/swap-optimizer/config.json
else
    cp high-end-profile.json /etc/swap-optimizer/config.json
fi
systemctl restart swap-optimizer
```

## Configuration Migration

### From Old Version

If upgrading from an older version:
```bash
# Backup old config
sudo cp /etc/swap-optimizer/config.json /etc/swap-optimizer/config.json.old

# Merge new defaults
# (Manual process - compare old config with new default)
```

### To New System

```bash
# Export config
sudo cat /etc/swap-optimizer/config.json > backup-config.json

# Import on new system
sudo cp backup-config.json /etc/swap-optimizer/config.json
sudo systemctl restart swap-optimizer
```

---

**Last Updated**: 2026-07-03
**Version**: 2.0.0
