# Training Data Reference

This document provides comprehensive reference information about the training data available for the Linux Swap Optimizer. The training data includes configuration templates, performance baselines, process mappings, and kernel parameter presets.

## Training Data Overview

The training data is located in the `/tranning/` directory and contains:

- **Configuration Templates** - Pre-configured settings for different system types
- **Performance Baselines** - Reference performance data and optimization targets
- **Process Priority Mappings** - Default process categorization and priority settings
- **Kernel Parameter Presets** - Pre-configured kernel parameter sets
- **Documentation** - Comprehensive usage and customization guides

## Configuration Templates

### Available Templates

1. **AI Workload Configuration** (`ai-workload-config.json`)
   - Target: AI/ML development workstations
   - Hardware: 32GB RAM, 16 CPU cores, 16GB swap
   - Optimization: Aggressive AI process prioritization

2. **Low-End System Configuration** (`low-end-system-config.json`)
   - Target: Resource-constrained systems
   - Hardware: 4GB RAM, 2 CPU cores, 8GB swap
   - Optimization: Conservative memory management

3. **Gaming Configuration** (`gaming-config.json`)
   - Target: Gaming systems
   - Hardware: 16GB RAM, 8 CPU cores, 16GB swap
   - Optimization: Low latency and responsiveness

4. **Server Configuration** (`server-config.json`)
   - Target: Production servers
   - Hardware: 64GB RAM, 32 CPU cores, 32GB swap
   - Optimization: Stability and throughput

## Performance Baselines

### System Type Profiles

**AI Workstation:**
- RAM: 32GB, CPU: 16 cores, Swap: 16GB
- Memory target: 75%, CPU target: 80%, Swap target: 20%
- Expected: 60% CPU reduction, 40% memory efficiency

**Low-End System:**
- RAM: 4GB, CPU: 2 cores, Swap: 8GB
- Memory target: 85%, CPU target: 90%, Swap target: 60%
- Expected: 30% CPU reduction, 25% memory efficiency

**Gaming System:**
- RAM: 16GB, CPU: 8 cores, Swap: 16GB
- Memory target: 70%, CPU target: 85%, Swap target: 10%
- Expected: 45% CPU reduction, 35% memory efficiency

**Server System:**
- RAM: 64GB, CPU: 32 cores, Swap: 32GB
- Memory target: 80%, CPU target: 75%, Swap target: 30%
- Expected: 35% CPU reduction, 30% memory efficiency

## Process Priority Mappings

### Priority Tier Structure

**AI Tier (nice -10):** Python AI/ML, TensorFlow, PyTorch, Keras, Jupyter, CUDA
**IDE Tier (nice -5):** VSCode, JetBrains IDEs, Vim, Emacs, Nano
**Interactive Tier (nice 0):** Firefox, Chrome, Terminal, Audio services
**Normal Tier (nice 10):** Systemd, D-Bus, Network, Cron
**Background Tier (nice 19):** Updatedb, Backup, Indexing, Logrotate

## Kernel Parameter Presets

**Conservative:** Swappiness 1, minimize swap, sufficient RAM systems
**Balanced:** Swappiness 10, balanced swap, general purpose systems
**Aggressive:** Swappiness 60, maximize swap, limited RAM systems
**Performance:** Swappiness 5, low latency, gaming/real-time systems
**Server:** Swappiness 20, moderate swap, production servers

## Using Training Data

### Applying Configuration Templates

```bash
cp tranning/ai-workload-config.json config.json
sudo systemctl restart swap-optimizer
python3 swap_optimizer.py --status
```

### Customizing Process Mappings

Edit `tranning/process-priority-mappings.json` to add custom process patterns.

### Selecting Kernel Presets

Choose from available presets in `tranning/kernel-parameter-presets.json`.

## Additional Resources

- **Use Cases:** [Use-Cases.md](Use-Cases.md)
- **Configuration Templates:** [Configuration-Templates.md](Configuration-Templates.md)
- **Configuration Guide:** [Configuration-Guide.md](Configuration-Guide.md)
- **Process Priority Tiers:** [Process-Priority-Tiers.md](Process-Priority-Tiers.md)
- **Performance Tuning:** [Performance-Tuning.md](Performance-Tuning.md)
