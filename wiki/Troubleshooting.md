# Troubleshooting Guide

## Common Issues and Solutions

### Service Won't Start

#### Symptom
```bash
$ sudo systemctl start swap-optimizer
Job for swap-optimizer.service failed.
```

#### Diagnosis
```bash
# Check service status
sudo systemctl status swap-optimizer

# View detailed logs
sudo journalctl -u swap-optimizer -n 50
```

#### Common Causes

**1. Missing Python Dependencies**
```
Error: ModuleNotFoundError: No module named 'psutil'
```
**Solution**:
```bash
sudo pip3 install psutil
```

**2. Permission Issues**
```
Error: Permission denied when writing to /proc/sys
```
**Solution**:
```bash
# Ensure running as root
sudo systemctl start swap-optimizer

# Check file permissions
ls -la /opt/swap-optimizer/
sudo chmod +x /opt/swap-optimizer/swap_optimizer.py
```

**3. Invalid Configuration**
```
Error: JSON decode error in config file
```
**Solution**:
```bash
# Validate JSON
python3 -m json.tool /etc/swap-optimizer/config.json

# Restore default config
sudo cp config.json /etc/swap-optimizer/config.json
```

**4. Missing Config File**
```
Error: Config file not found
```
**Solution**:
```bash
sudo mkdir -p /etc/swap-optimizer
sudo cp config.json /etc/swap-optimizer/
```

### Settings Not Applying

#### Symptom
Running `--optimize` but sysctl values don't change

#### Diagnosis
```bash
# Check current values
sudo sysctl vm.swappiness
sudo sysctl vm.vfs_cache_pressure

# Try manual set
sudo sysctl -w vm.swappiness=10
```

#### Solutions

**1. Sysctl Not Available**
```bash
# Install procps
sudo apt-get install procps  # Debian/Ubuntu
sudo yum install procps-ng   # RHEL/CentOS
```

**2. SELinux Blocking**
```bash
# Check SELinux status
sestatus

# Temporarily disable for testing
sudo setenforce 0

# Create proper SELinux policy
# (Advanced - see SELinux documentation)
```

**3. Read-Only Filesystem**
```bash
# Check filesystem mount
mount | grep "proc/sys"

# Remount if necessary
sudo mount -o remount,rw /proc/sys
```

### High CPU Usage

#### Symptom
System CPU usage increases after starting swap-optimizer

#### Diagnosis
```bash
# Check process CPU
top -p $(pgrep -f swap_optimizer)

# Monitor over time
sudo journalctl -u swap-optimizer -f
```

#### Solutions

**1. Check Interval Too Low**
```json
// In /etc/swap-optimizer/config.json
{
  "check_interval": 1  // Too frequent
}
```
**Fix**: Increase to 5-10 seconds
```json
{
  "check_interval": 5
}
```

**2. Process List Too Large**
```json
{
  "ai_processes": ["very", "long", "list", "..."]
}
```
**Fix**: Reduce to essential processes only

**3. Infinite Loop Bug**
```bash
# Check for rapid log entries
sudo journalctl -u swap-optimizer --since "1 minute ago"
```
**Fix**: Report bug and restart service

### System Becomes Unresponsive

#### Symptom
System freezes or becomes very slow after optimization

#### Immediate Action
```bash
# Restore original settings immediately
sudo python3 /opt/swap-optimizer/swap_optimizer.py --restore

# Or reboot if unresponsive
sudo reboot
```

#### Investigation

**1. Aggressive Mode on Low RAM**
```json
{
  "aggressive_mode": true  // Dangerous on low RAM
}
```
**Fix**: Set to false
```json
{
  "aggressive_mode": false
}
```

**2. Swappiness Too Low**
```json
{
  "swappiness": 0  // Can cause OOM
}
```
**Fix**: Set to at least 5
```json
{
  "swappiness": 10
}
```

**3. min_free_kbytes Too High**
```json
{
  "min_free_kbytes": 1048576  // 1GB - too high
}
```
**Fix**: Reduce to appropriate value
```json
{
  "min_free_kbytes": 65536
}
```

### Process Priorities Not Changing

#### Symptom
AI processes still have default priorities

#### Diagnosis
```bash
# Check process priority
ps -eo pid,ni,comm | grep python

# Check ionice availability
which ionice
```

#### Solutions

**1. ionice Not Installed**
```bash
# Install ionice
sudo apt-get install util-linux  # Debian/Ubuntu
sudo yum install util-linux       # RHEL/CentOS
sudo pacman -S util-linux         # Arch
```

**2. Permission Denied**
```bash
# Check if running as root
sudo systemctl status swap-optimizer

# Test manually
sudo ionice -c 1 -n 4 -p $(pgrep python)
```

**3. Process Not Detected**
```bash
# Check process name
ps aux | grep python

# Add to config
sudo nano /etc/swap-optimizer/config.json
# Add "python" to ai_processes array
```

### Swap Not Disabled in Aggressive Mode

#### Symptom
`aggressive_mode: true` but swap remains enabled

#### Diagnosis
```bash
# Check memory usage
free -h

# Check swap status
swapon --show
```

#### Solutions

**1. Memory Threshold Not Met**
```bash
# Aggressive mode only disables swap when memory < 70%
# Check current usage
free -h | grep Mem
```
**Fix**: Either free memory or disable aggressive mode

**2. swapoff Command Failing**
```bash
# Test manually
sudo swapoff -a

# Check for errors
# Common issue: swap cannot be disabled if in use
```

**3. Permission Issues**
```bash
# Ensure service runs as root
sudo systemctl cat swap-optimizer
# Look for "User=root"
```

### Configuration Changes Not Taking Effect

#### Symptom
Modified config but behavior unchanged

#### Diagnosis
```bash
# Check if service restarted
sudo systemctl status swap-optimizer

# Verify config location
sudo systemctl cat swap-optimizer | grep config
```

#### Solutions

**1. Service Not Restarted**
```bash
sudo systemctl restart swap-optimizer
```

**2. Wrong Config File**
```bash
# Check which config is being used
sudo systemctl cat swap-optimizer

# Edit correct config
sudo nano /etc/swap-optimizer/config.json
```

**3. Config Syntax Error**
```bash
# Validate JSON
python3 -m json.tool /etc/swap-optimizer/config.json
```

### Log Files Too Large

#### Symptom
Disk space filling with log files

#### Diagnosis
```bash
# Check log size
sudo journalctl --disk-usage

# Check swap-optimizer log size
sudo journalctl -u swap-optimizer --since "1 week ago" | wc -l
```

#### Solutions

**1. Reduce Log Level**
```json
{
  "log_level": "WARNING"  // Instead of "DEBUG"
}
```

**2. Configure Journal Rotation**
```bash
# Edit journald config
sudo nano /etc/systemd/journald.conf

# Add/modify:
SystemMaxUse=50M
SystemMaxFiles=5
```

**3. Manual Log Cleanup**
```bash
# Rotate logs
sudo journalctl --rotate

# Vacuum old logs
sudo journalctl --vacuum-time=7d
```

## Performance Issues

### System Slower After Optimization

#### Diagnosis
```bash
# Check swap usage before/after
swapon --show
free -h

# Check I/O wait
iostat -x 1
```

#### Solutions

**1. Swap Thrashing**
```bash
# Increase swappiness slightly
# In config.json:
"swappiness": 15  // Was 10
```

**2. Cache Pressure Too Low**
```bash
# Increase vfs_cache_pressure
"vfs_cache_pressure": 90  // Was 75
```

**3. Page Cluster Disabled**
```bash
# Enable page clustering for better throughput
"page_cluster": 2  // Was 0
```

### High I/O Wait

#### Diagnosis
```bash
# Check I/O statistics
iostat -x 5

# Check swap activity
vmstat 1
```

#### Solutions

**1. Reduce Swap Activity**
```bash
# Lower swappiness
"swappiness": 5
```

**2. Enable Page Clustering**
```bash
"page_cluster": 3
```

**3. Check Disk Health**
```bash
sudo smartctl -a /dev/sda
```

## Installation Issues

### Installation Script Fails

#### Symptom
```bash
$ sudo bash install.sh
Error: ...
```

#### Common Solutions

**1. Python Not Found**
```bash
# Install Python 3
sudo apt-get install python3  # Debian/Ubuntu
sudo yum install python3       # RHEL/CentOS
```

**2. pip Not Available**
```bash
# Install pip
sudo apt-get install python3-pip  # Debian/Ubuntu
sudo yum install python3-pip       # RHEL/CentOS
```

**3. Directory Permissions**
```bash
# Create directories manually
sudo mkdir -p /opt/swap-optimizer
sudo mkdir -p /etc/swap-optimizer
```

### Uninstallation Issues

#### Symptom
Files or service remain after uninstall

#### Solutions

**1. Service Still Running**
```bash
sudo systemctl stop swap-optimizer
sudo systemctl disable swap-optimizer
```

**2. Files Remain**
```bash
sudo rm -rf /opt/swap-optimizer
sudo rm -rf /etc/swap-optimizer
```

**3. systemd Cache**
```bash
sudo systemctl daemon-reload
sudo systemctl reset-failed
```

## Getting Help

### Collect Diagnostic Information

```bash
# System info
uname -a
free -h
swapon --show

# Service status
sudo systemctl status swap-optimizer

# Recent logs
sudo journalctl -u swap-optimizer -n 100

# Current config
sudo cat /etc/swap-optimizer/config.json

# Current sysctl values
sudo sysctl -a | grep -E "swappiness|vfs_cache|page-cluster|min_free|watermark"
```

### Debug Mode

```bash
# Enable debug logging
# In config.json:
{
  "log_level": "DEBUG"
}

# Restart service
sudo systemctl restart swap-optimizer

# Watch logs
sudo journalctl -u swap-optimizer -f
```

### Manual Testing

```bash
# Test optimization manually
sudo python3 /opt/swap-optimizer/swap_optimizer.py --optimize

# Check status
sudo python3 /opt/swap-optimizer/swap_optimizer.py --status

# Test restore
sudo python3 /opt/swap-optimizer/swap_optimizer.py --restore
```

## Known Limitations

1. **Cannot modify swap device size** - Only manages swap behavior
2. **Requires root access** - Cannot run in user space
3. **Linux only** - Not compatible with other OSes
4. **Process name matching only** - Cannot identify processes by behavior
5. **No GPU memory management** - Only handles system RAM

## When to Report Bugs

Report a bug if:
- The service crashes repeatedly
- Settings don't apply despite correct configuration
- System becomes unstable after optimization
- Unexpected error messages in logs
- Performance degrades significantly

Include in bug report:
- OS distribution and version
- Kernel version (`uname -r`)
- Python version (`python3 --version`)
- Configuration file
- Relevant log excerpts
- Steps to reproduce
