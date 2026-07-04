# Configuration Templates

This document provides detailed information about the configuration templates available in the Linux Swap Optimizer training data. These templates are pre-configured for different system types and use cases.

## Available Templates

### AI Workload Configuration

**File:** `tranning/ai-workload-config.json`

**System Type:** AI/ML Development Workstations
**Hardware:** 32GB RAM, 16 CPU cores, 16GB swap
**Optimization Level:** Aggressive

#### Priority Tier Settings

**AI Tier (nice -10):**
- Ionice class: 1 (Real-time)
- Ionice priority: 0 (Highest)
- Memory priority: High
- CPU affinity: Performance
- Process patterns: python.*train, python.*infer, tensor, torch, keras, tensorflow, jupyter, cuda, nvidia-smi

**IDE Tier (nice -5):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 0 (Highest)
- Memory priority: Medium
- CPU affinity: Balanced
- Process patterns: code, idea, pycharm, vscode, vim, emacs, nano

**Interactive Tier (nice 0):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 4
- Memory priority: Normal
- CPU affinity: Balanced
- Process patterns: firefox, chrome, chromium, browser, terminal, bash, zsh

**Normal Tier (nice 10):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 7 (Lowest)
- Memory priority: Low
- CPU affinity: Powersave
- Process patterns: systemd, dbus, network

**Background Tier (nice 19):**
- Ionice class: 3 (Idle)
- Ionice priority: 7 (Lowest)
- Memory priority: Minimal
- CPU affinity: Powersave
- Process patterns: updatedb, backup, rsync, cron

#### Kernel Parameters

- `vm.swappiness`: 10 (Low swap tendency)
- `vm.vfs_cache_pressure`: 50 (Balanced cache pressure)
- `vm.dirty_ratio`: 15 (15% RAM before writeback)
- `vm.dirty_background_ratio`: 5 (5% RAM for background writeback)
- `vm.min_free_kbytes`: 65536 (64MB minimum free memory)

#### Swap Settings

- Enable swap: Yes
- Swap priority: AI processes first
- Swap threshold: 85%
- Aggressive swap: No

#### Monitoring

- Check interval: 3 seconds
- Memory threshold: 90%
- CPU threshold: 95%
- Swap threshold: 80%
- Auto-adjust: Yes

---

### Low-End System Configuration

**File:** `tranning/low-end-system-config.json`

**System Type:** Low-End Desktops and Laptops
**Hardware:** 4GB RAM, 2 CPU cores, 8GB swap
**Optimization Level:** Conservative

#### Priority Tier Settings

**AI Tier (nice -5):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 0 (Highest)
- Memory priority: High
- CPU affinity: Balanced
- Process patterns: python, tensor, torch

**IDE Tier (nice -3):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 0 (Highest)
- Memory priority: Medium
- CPU affinity: Balanced
- Process patterns: code, vim, nano

**Interactive Tier (nice 0):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 4
- Memory priority: Normal
- CPU affinity: Balanced
- Process patterns: firefox, chrome, terminal

**Normal Tier (nice 15):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 7 (Lowest)
- Memory priority: Low
- CPU affinity: Powersave
- Process patterns: systemd, dbus

**Background Tier (nice 19):**
- Ionice class: 3 (Idle)
- Ionice priority: 7 (Lowest)
- Memory priority: Minimal
- CPU affinity: Powersave
- Process patterns: updatedb, backup

#### Kernel Parameters

- `vm.swappiness`: 1 (Very low swap tendency)
- `vm.vfs_cache_pressure`: 75 (High cache pressure)
- `vm.dirty_ratio`: 5 (5% RAM before writeback)
- `vm.dirty_background_ratio`: 2 (2% RAM for background writeback)
- `vm.min_free_kbytes`: 131072 (128MB minimum free memory)

#### Swap Settings

- Enable swap: Yes
- Swap priority: Memory first
- Swap threshold: 70%
- Aggressive swap: Yes

#### Monitoring

- Check interval: 5 seconds
- Memory threshold: 85%
- CPU threshold: 90%
- Swap threshold: 60%
- Auto-adjust: Yes

---

### Gaming Configuration

**File:** `tranning/gaming-config.json`

**System Type:** Gaming Desktops and Laptops
**Hardware:** 16GB RAM, 8 CPU cores, 16GB swap
**Optimization Level:** Performance

#### Priority Tier Settings

**AI Tier (nice -8):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 0 (Highest)
- Memory priority: High
- CPU affinity: Performance
- Process patterns: steam, game, wine, proton

**IDE Tier (nice -3):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 0 (Highest)
- Memory priority: Medium
- CPU affinity: Balanced
- Process patterns: discord, overlay

**Interactive Tier (nice 0):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 4
- Memory priority: Normal
- CPU affinity: Balanced
- Process patterns: pulseaudio, pipewire

**Normal Tier (nice 10):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 7 (Lowest)
- Memory priority: Low
- CPU affinity: Powersave
- Process patterns: systemd, network

**Background Tier (nice 19):**
- Ionice class: 3 (Idle)
- Ionice priority: 7 (Lowest)
- Memory priority: Minimal
- CPU affinity: Powersave
- Process patterns: updatedb, backup

#### Kernel Parameters

- `vm.swappiness`: 5 (Very low swap tendency)
- `vm.vfs_cache_pressure`: 50 (Balanced cache pressure)
- `vm.dirty_ratio`: 10 (10% RAM before writeback)
- `vm.dirty_background_ratio`: 3 (3% RAM for background writeback)
- `vm.min_free_kbytes`: 98304 (96MB minimum free memory)

#### Swap Settings

- Enable swap: Yes
- Swap priority: Performance first
- Swap threshold: 90%
- Aggressive swap: No

#### Monitoring

- Check interval: 2 seconds
- Memory threshold: 95%
- CPU threshold: 98%
- Swap threshold: 85%
- Auto-adjust: Yes

---

### Server Configuration

**File:** `tranning/server-config.json`

**System Type:** Production Servers
**Hardware:** 64GB RAM, 32 CPU cores, 32GB swap
**Optimization Level:** Balanced

#### Priority Tier Settings

**AI Tier (nice -7):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 0 (Highest)
- Memory priority: High
- CPU affinity: Balanced
- Process patterns: nginx, apache, mysql, postgres, redis, mongodb

**IDE Tier (nice -2):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 0 (Highest)
- Memory priority: Medium
- CPU affinity: Balanced
- Process patterns: ssh, sshd

**Interactive Tier (nice 0):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 4
- Memory priority: Normal
- CPU affinity: Balanced
- Process patterns: bash, zsh

**Normal Tier (nice 5):**
- Ionice class: 2 (Best-effort)
- Ionice priority: 7 (Lowest)
- Memory priority: Low
- CPU affinity: Balanced
- Process patterns: systemd, dbus, cron

**Background Tier (nice 15):**
- Ionice class: 3 (Idle)
- Ionice priority: 7 (Lowest)
- Memory priority: Minimal
- CPU affinity: Powersave
- Process patterns: logrotate, updatedb

#### Kernel Parameters

- `vm.swappiness`: 20 (Moderate swap tendency)
- `vm.vfs_cache_pressure`: 75 (High cache pressure)
- `vm.dirty_ratio`: 20 (20% RAM before writeback)
- `vm.dirty_background_ratio`: 10 (10% RAM for background writeback)
- `vm.min_free_kbytes`: 65536 (64MB minimum free memory)

#### Swap Settings

- Enable swap: Yes
- Swap priority: Balanced
- Swap threshold: 75%
- Aggressive swap: No

#### Monitoring

- Check interval: 10 seconds
- Memory threshold: 90%
- CPU threshold: 85%
- Swap threshold: 70%
- Auto-adjust: Yes

---

## Using Configuration Templates

### Applying a Template

1. Copy the template to your configuration:
```bash
cp tranning/ai-workload-config.json config.json
```

2. Restart the service:
```bash
sudo systemctl restart swap-optimizer
```

3. Verify the configuration:
```bash
python3 swap_optimizer.py --status
```

### Customizing Templates

Edit the copied configuration file to match your specific needs:

```json
{
  "priority_tiers": {
    "ai": {
      "nice_value": -10,
      "process_patterns": ["your-custom-patterns"]
    }
  }
}
```

### Creating Custom Templates

1. Copy the closest matching template
2. Modify hardware profile settings
3. Adjust priority tier assignments
4. Tune kernel parameters
5. Save as custom configuration
6. Test thoroughly before deployment

## Template Parameters

### Priority Tier Parameters

**nice_value:** Process priority (-20 to 19, lower = higher priority)
- AI tier: -10 to -8
- IDE tier: -5 to -2
- Interactive tier: 0
- Normal tier: 5 to 15
- Background tier: 15 to 19

**ionice_class:** I/O scheduling class
- 1: Real-time (highest priority)
- 2: Best-effort (normal priority)
- 3: Idle (lowest priority)

**ionice_priority:** I/O priority within class (0-7, lower = higher priority)

**memory_priority:** Memory allocation priority
- high: Prefer RAM allocation
- medium: Balanced memory allocation
- normal: Standard memory allocation
- low: Minimal memory allocation
- minimal: Background memory allocation

**cpu_affinity:** CPU scheduling preference
- performance: Prefer performance cores
- balanced: Balanced CPU usage
- powersave: Prefer power-saving

### Kernel Parameter Parameters

**vm.swappiness:** Swap tendency (0-100)
- 1-5: Conservative (minimize swap)
- 10-20: Balanced
- 60+: Aggressive (maximize swap)

**vm.vfs_cache_pressure:** Cache reclaim tendency (0-100)
- 50: Balanced
- 75+: Aggressive cache reclaim
- Lower: Preserve cache

**vm.dirty_ratio:** Dirty memory percentage before writeback
- 5-10: Conservative
- 15-20: Balanced
- Higher: Delay writeback

**vm.dirty_background_ratio:** Background writeback percentage
- Typically 1/3 to 1/2 of dirty_ratio

**vm.min_free_kbytes:** Minimum free memory in kilobytes
- 32768: 32MB (aggressive)
- 65536: 64MB (balanced)
- 98304: 96MB (performance)
- 131072: 128MB (conservative)

### Monitoring Parameters

**check_interval:** Seconds between system checks
- 2-3 seconds: Real-time monitoring
- 5 seconds: Standard monitoring
- 10 seconds: Server monitoring

**thresholds:** Resource usage percentages
- Memory: 85-95%
- CPU: 85-98%
- Swap: 60-85%

**auto_adjust:** Enable automatic parameter adjustment
- true: Automatically tune based on conditions
- false: Manual adjustment only

## Best Practices

### Template Selection

1. Match hardware profile as closely as possible
2. Consider primary workload type
3. Evaluate performance requirements
4. Test in safe environment first
5. Monitor after deployment

### Customization Guidelines

1. Start with appropriate template
2. Make incremental changes
3. Document modifications
4. Test each change
5. Roll back if issues occur

### Performance Monitoring

1. Compare against baseline performance
2. Monitor key metrics regularly
3. Adjust based on actual workload
4. Keep historical performance data
5. Update templates based on experience

## Troubleshooting

### Template Not Working

1. Verify JSON syntax is correct
2. Check file permissions
3. Ensure service is running
4. Review system logs
5. Test with default configuration

### Performance Issues

1. Verify hardware matches template
2. Check resource utilization
3. Review process priorities
4. Adjust kernel parameters
5. Consider hybrid approach

### Compatibility Issues

1. Check Linux kernel version
2. Verify systemd compatibility
3. Review Python version requirements
4. Test kernel parameter compatibility
5. Check system dependencies

## Additional Resources

- **Use Cases:** [Use-Cases.md](Use-Cases.md)
- **Configuration Guide:** [Configuration-Guide.md](Configuration-Guide.md)
- **Process Priority Tiers:** [Process-Priority-Tiers.md](Process-Priority-Tiers.md)
- **Performance Tuning:** [Performance-Tuning.md](Performance-Tuning.md)
- **Training Data:** See `/tranning/` directory
