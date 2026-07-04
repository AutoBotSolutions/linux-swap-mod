# Process Priority Tiers

## Overview

The Linux Swap Optimizer uses a sophisticated process categorization system to optimize system performance by assigning appropriate CPU and I/O priorities to different types of processes. This ensures that critical applications receive the resources they need while maintaining overall system stability.

## Priority Tiers

### 1. AI Processes (Highest Priority)

**Purpose**: Machine learning and AI workloads require maximum resources for optimal performance.

**Processes Included**:
- Python (for AI/ML frameworks)
- Jupyter (notebooks)
- Ollama, Llama (local LLMs)
- TensorFlow, PyTorch (ML frameworks)

**Priority Settings**:
- **CPU Priority (nice)**: -10 (very high priority)
- **I/O Priority**: Class 1 (realtime), Level 4

**Rationale**: AI/ML workloads are computationally intensive and benefit from maximum CPU and I/O resources. These processes often handle large datasets and model training/inference, which require consistent performance.

### 2. IDE Processes (High Priority)

**Purpose**: Development environments need responsive performance for developer productivity.

**Processes Included**:
- VS Code, Cursor, VSCodium
- JetBrains suite (IntelliJ IDEA, PyCharm, WebStorm, PHPStorm, CLion, Rider, DataGrip, RubyMine, GoLand)
- Text editors (Vim, Neovim, Emacs, Nano, Gedit, Kate, Geany)
- Other editors (Atom, Sublime Text, Android Studio)

**Priority Settings**:
- **CPU Priority (nice)**: -5 (high priority)
- **I/O Priority**: Class 1 (realtime), Level 4

**Rationale**: IDEs are interactive applications where responsiveness directly impacts developer productivity. High I/O priority ensures smooth file operations and code completion.

### 3. Interactive Applications (Medium Priority)

**Purpose**: User-facing applications that benefit from good responsiveness but aren't critical.

**Processes Included**:
- Web browsers (Firefox, Chrome, Chromium, Brave, Opera)
- Email clients (Thunderbird, Evolution)
- Communication apps (Discord, Slack, Telegram, Zoom, Teams, Skype)
- Media players (VLC, MPV, MPlayer)

**Priority Settings**:
- **CPU Priority (nice)**: -2 (slightly elevated priority)
- **I/O Priority**: Class 2 (best-effort), Level 4

**Rationale**: Interactive applications need good responsiveness for user experience but don't require the extreme priority of development tools.

### 4. Normal Processes (Default Priority)

**Purpose**: Standard applications that don't fit into other categories.

**Processes Included**:
- All other applications not in specific categories
- General user applications
- Standard system tools

**Priority Settings**:
- **CPU Priority (nice)**: 0 (default priority)
- **I/O Priority**: Class 2 (best-effort), Level 7

**Rationale**: These processes receive standard system priority, ensuring fair resource allocation without special treatment.

### 5. Background Processes (Low Priority)

**Purpose**: System services and background tasks that should not interfere with user applications.

**Processes Included**:
- System services (systemd, cron, rsyslog)
- Network services (NetworkManager, bluetooth)
- Print services (CUPS)
- Discovery services (Avahi)

**Priority Settings**:
- **CPU Priority (nice)**: 5 (lower priority)
- **I/O Priority**: Class 3 (idle), Level 0

**Rationale**: Background services should yield to user-facing applications to maintain system responsiveness.

## Priority Implementation

### CPU Priority (nice)

The nice value ranges from -20 (highest priority) to 19 (lowest priority), with 0 being the default.

```
-20 ──────────────────────────────────────── 19
 ↑                                           ↑
Highest Priority                    Lowest Priority
```

**Our Implementation**:
- AI: -10 (very high)
- IDE: -5 (high)
- Interactive: -2 (slightly elevated)
- Normal: 0 (default)
- Background: 5 (lower)

### I/O Priority (ionice)

I/O priority has three classes and levels within each class:

**Classes**:
- Class 1: Realtime (highest)
- Class 2: Best-effort (default)
- Class 3: Idle (lowest)

**Levels** (0-7, lower is higher priority within class):
- 0: Highest priority within class
- 7: Lowest priority within class

**Our Implementation**:
- AI: Class 1, Level 4 (realtime, medium)
- IDE: Class 1, Level 4 (realtime, medium)
- Interactive: Class 2, Level 4 (best-effort, medium)
- Normal: Class 2, Level 7 (best-effort, low)
- Background: Class 3, Level 0 (idle, highest within idle)

## Process Categorization Algorithm

The system categorizes processes using the following logic:

```python
def _categorize_process(proc):
    proc_name = proc.info['name'].lower()
    
    # Check AI processes (highest priority)
    for ai_proc in config['ai_processes']:
        if ai_proc in proc_name:
            return 'ai'
    
    # Check IDE processes (high priority)
    for ide_proc in config['ide_processes']:
        if ide_proc in proc_name:
            return 'ide'
    
    # Check interactive processes (medium priority)
    for app in config['interactive_processes']:
        if app in proc_name:
            return 'interactive'
    
    # Check background processes (low priority)
    for bg_proc in config['background_processes']:
        if bg_proc in proc_name:
            return 'background'
    
    # Default to normal priority
    return 'normal'
```

## Configuration

### Process Lists

You can customize the process lists in `/etc/swap-optimizer/config.json`:

```json
{
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
  ]
}
```

### Enable/Disable General Optimization

Control whether all processes are optimized using the `optimize_all_apps` setting:

```json
{
  "optimize_all_apps": true
}
```

- `true`: Optimize all processes across all categories (default)
- `false`: Only optimize AI and IDE processes (legacy mode)

## Monitoring and Status

### Check Current Process Distribution

```bash
sudo python3 /opt/swap-optimizer/swap_optimizer.py --status
```

Output includes:
```json
{
  "process_categories": {
    "ai": 2,
    "ide": 0,
    "interactive": 1,
    "normal": 205,
    "background": 19
  },
  "total_processes": 227
}
```

### View Priority Changes in Real-Time

```bash
# Watch process priorities
watch -n 1 'ps -eo pid,ni,comm | head -20'

# View I/O priorities
sudo ionice -p $(pgrep python)
```

## Customization

### Adding Custom Processes

To add a custom process to a specific category:

1. Edit `/etc/swap-optimizer/config.json`
2. Add the process name to the appropriate array
3. Restart the service

```json
{
  "ai_processes": [
    "python", "jupyter", "ollama", "llama", "tensor", "torch",
    "my-custom-ai-app"
  ]
}
```

### Adjusting Priority Values

To modify priority settings, edit the `priority_settings` dictionary in `swap_optimizer.py`:

```python
priority_settings = {
    'ai': {'nice': -10, 'ionice_class': 1, 'ionice_level': 4},
    'ide': {'nice': -5, 'ionice_class': 1, 'ionice_level': 4},
    'interactive': {'nice': -2, 'ionice_class': 2, 'ionice_level': 4},
    'normal': {'nice': 0, 'ionice_class': 2, 'ionice_level': 7},
    'background': {'nice': 5, 'ionice_class': 3, 'ionice_level': 0}
}
```

## Performance Impact

### Expected Improvements

- **AI Workloads**: 20-30% faster training/inference
- **IDE Responsiveness**: Elimination of input lag
- **Application Switching**: Smoother transitions
- **System Responsiveness**: Better overall feel
- **Background Tasks**: Reduced interference with foreground apps

### Resource Allocation

The priority system ensures:
- Critical processes get resources when needed
- Background tasks don't starve user applications
- Fair distribution among similar-priority processes
- Adaptive adjustment based on system load

## Troubleshooting

### Process Not Being Prioritized

**Symptom**: A process isn't receiving expected priority

**Solutions**:
1. Check if process name matches configuration
2. Verify `optimize_all_apps` is enabled
3. Check process permissions
4. Review logs for errors

```bash
# Check process name
ps aux | grep process-name

# Check current priority
ps -eo pid,ni,comm | grep process-name

# Check logs
sudo journalctl -u swap-optimizer -f
```

### Process Categorization Issues

**Symptom**: Processes not being categorized correctly

**Solutions**:
1. Verify process name matches configuration exactly
2. Check for case sensitivity (matching is case-insensitive)
3. Ensure process is running when checking
4. Review categorization algorithm logs

```bash
# Test categorization
python3 -c "
from swap_optimizer import SwapOptimizer
opt = SwapOptimizer()
categories = opt._get_all_user_processes()
for cat, procs in categories.items():
    print(f'{cat}: {len(procs)}')
"
```

### System Becomes Unresponsive

**Symptom**: System lag after priority changes

**Solutions**:
1. Disable general optimization temporarily
2. Reduce priority differences between tiers
3. Check for priority conflicts
4. Restore original settings

```bash
# Disable general optimization
# Edit config.json: "optimize_all_apps": false
sudo systemctl restart swap-optimizer

# Restore original settings
sudo python3 /opt/swap-optimizer/swap_optimizer.py --restore
```

## Best Practices

1. **Test Gradually**: Start with default settings and adjust incrementally
2. **Monitor Performance**: Watch system behavior after changes
3. **Customize for Workload**: Tailor process lists to your specific needs
4. **Use Dry-Run**: Test changes before applying them
5. **Keep Backups**: Save working configurations

## Advanced Topics

### Dynamic Priority Adjustment

The system can be extended to dynamically adjust priorities based on:
- Process CPU usage
- Memory consumption
- I/O patterns
- User activity

### Per-User Priorities

Different users can have different priority configurations:
```bash
# User-specific config
~/.config/swap-optimizer/user-config.json
```

### Integration with cgroups

For more advanced control, integrate with Linux cgroups:
```bash
# Create cgroup for AI processes
sudo cgcreate -g cpu,memory:/ai

# Assign process to cgroup
sudo cgclassify -g cpu,memory:/ai $(pgrep python)
```

## Related Documentation

- [Architecture.md](Architecture.md) - System design and components
- [Configuration-Guide.md](Configuration-Guide.md) - Configuration reference
- [Performance-Tuning.md](Performance-Tuning.md) - Advanced optimization strategies

---

**Last Updated**: 2026-07-03
**Version**: 2.0.0
