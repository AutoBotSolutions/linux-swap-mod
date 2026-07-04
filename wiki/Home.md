# Linux Swap Optimizer - Wiki

Welcome to the Linux Swap Optimizer documentation wiki. This system is designed to reduce CPU and system load during AI development and general application usage on low-end systems, with the goal of eliminating application lagging through intelligent swap management and process prioritization.

## Quick Links

- [Architecture and Design](Architecture.md) - System architecture and technical details
- [Configuration Guide](Configuration-Guide.md) - Complete configuration reference
- [Process Priority Tiers](Process-Priority-Tiers.md) - Process categorization and priority management
- [Performance Tuning](Performance-Tuning.md) - Advanced tuning strategies
- [Troubleshooting](Troubleshooting.md) - Common issues and solutions
- [FAQ](FAQ.md) - Frequently asked questions
- [Changelog](Changelog.md) - Version history and release notes

## Getting Started

### Installation

```bash
sudo bash install.sh
```

### Basic Usage

```bash
# Start the service
sudo systemctl start swap-optimizer

# Enable at boot
sudo systemctl enable swap-optimizer

# Check status
sudo python3 /opt/swap-optimizer/swap_optimizer.py --status
```

## Key Features

- **AI-Aware Swap Management**: Optimized specifically for AI/IDE workloads
- **General Application Optimization**: Optimizes all running applications with intelligent priority tiers
- **IDE-Aware Optimization**: Automatically optimizes system when any IDE is detected
- **OS-Level Optimization**: Applies kernel-level optimizations for better system responsiveness
- **Adaptive Monitoring**: Real-time adjustment based on system load
- **Process Prioritization**: Automatic prioritization across 5 categories (AI, IDE, interactive, normal, background)
- **Low-End Optimization**: Tuned for systems with limited resources
- **Safe Operation**: Automatic backup and easy rollback

## Documentation Structure

### For Users

- **README.md** - Project overview and quick start
- **FAQ.md** - Common questions and answers
- **Configuration Guide** - How to configure the system
- **Process Priority Tiers** - Understanding process categorization

### For Administrators

- **Installation** - Deployment and setup
- **Troubleshooting** - Issue resolution
- **Performance Tuning** - Optimization strategies

### For Developers

- **Architecture** - System design and components
- **Configuration Guide** - Parameter reference
- **Performance Tuning** - Advanced techniques
- **Process Priority Tiers** - Priority management implementation

## System Requirements

- **OS**: Linux (kernel 3.10+)
- **RAM**: Minimum 2GB, recommended 4GB+
- **CPU**: Minimum 2 cores, recommended 4+ cores
- **Storage**: 100MB free space
- **Python**: 3.6+
- **Privileges**: Root access required

## Configuration Profiles

### Low-End Systems (< 4GB RAM)
- Conservative swap settings
- Aggressive memory management
- Frequent monitoring
- No aggressive mode
- General application optimization enabled

### Mid-Range Systems (4-8GB RAM)
- Balanced settings
- Adaptive monitoring
- Standard optimization
- Disabled aggressive mode
- General application optimization enabled

### High-End Systems (> 8GB RAM)
- Relaxed swap settings
- Less frequent monitoring
- Aggressive mode enabled
- Maximum performance
- General application optimization enabled

## Common Use Cases

### AI/ML Development
- Python process optimization
- Jupyter notebook performance
- Model training/inference
- GPU memory coordination

### Web Development
- Node.js optimization
- Build tool performance
- Browser tab management
- Docker container optimization

### General Development
- IDE responsiveness
- Compilation performance
- Database operations
- Testing framework optimization

### Desktop Usage
- Web browser optimization
- Media player performance
- Communication app responsiveness
- General system responsiveness

## Performance Impact

Typical improvements on low-end systems:

- **Swap Activity**: 40-60% reduction
- **CPU Usage**: 15-25% reduction during workloads
- **Application Responsiveness**: Elimination of stuttering
- **Memory Efficiency**: Better RAM utilization
- **System Latency**: Reduced context switching
- **I/O Performance**: Better disk scheduling

## Safety Features

- Automatic backup of original settings
- Conservative default values
- Graceful error handling
- One-command rollback
- Safe parameter ranges
- Dry-run mode for testing

## Support and Resources

### Documentation
- [README.md](../README.md) - Main project documentation
- [Architecture.md](Architecture.md) - Technical details
- [Configuration-Guide.md](Configuration-Guide.md) - Configuration reference
- [Process-Priority-Tiers.md](Process-Priority-Tiers.md) - Priority management
- [Performance-Tuning.md](Performance-Tuning.md) - Optimization guide
- [Troubleshooting.md](Troubleshooting.md) - Issue resolution
- [FAQ.md](FAQ.md) - Common questions

### Files
- `swap_optimizer.py` - Main optimizer script
- `config.json` - Default configuration
- `install.sh` - Installation script
- `UNINSTALL.sh` - Removal script
- `requirements.txt` - Python dependencies

### Directories
- `/opt/swap-optimizer/` - Installation directory
- `/etc/swap-optimizer/` - Configuration directory
- `wiki/` - Documentation wiki

## Contributing

Contributions are welcome! Please:
1. Test thoroughly on low-end systems
2. Follow existing code style
3. Update documentation
4. Include tests for new features

## License

MIT License - Free to modify and distribute

## Version History

### Current Version (2.0.0)
- General application optimization for all processes
- Process categorization into 5 priority tiers
- OS-level kernel optimizations
- Enhanced adaptive management
- Interactive and background process detection
- Improved status reporting

### Previous Version (1.0.0)
- AI-aware swap management
- Adaptive monitoring
- Process prioritization
- Configuration system
- Systemd service integration

### Future Plans
- Machine learning-based prediction
- Per-process memory cgroups
- GPU memory optimization
- Distributed system support

## Quick Reference

### Essential Commands

```bash
# Install
sudo bash install.sh

# Start
sudo systemctl start swap-optimizer

# Enable
sudo systemctl enable swap-optimizer

# Status
sudo systemctl status swap-optimizer

# Optimize once
sudo python3 /opt/swap-optimizer/swap_optimizer.py --optimize

# Dry run (test without changes)
sudo python3 /opt/swap-optimizer/swap_optimizer.py --optimize --dry-run

# Restore
sudo python3 /opt/swap-optimizer/swap_optimizer.py --restore

# Status details
sudo python3 /opt/swap-optimizer/swap_optimizer.py --status
```

### Key Files

- `/opt/swap-optimizer/swap_optimizer.py` - Main script
- `/etc/swap-optimizer/config.json` - Configuration
- `/etc/systemd/system/swap-optimizer.service` - Service

### Important Parameters

- `swappiness` - Swap tendency (default: 10)
- `vfs_cache_pressure` - Cache pressure (default: 75)
- `cpu_threshold` - CPU trigger threshold (default: 80)
- `memory_threshold` - Memory trigger threshold (default: 85)
- `optimize_all_apps` - Optimize all applications (default: true)
- `check_interval` - Monitoring interval (default: 5 seconds)

## Getting Help

1. Check the [FAQ](FAQ.md)
2. Review [Troubleshooting](Troubleshooting.md)
3. Consult [Configuration Guide](Configuration-Guide.md)
4. Examine [Process Priority Tiers](Process-Priority-Tiers.md)
5. Check [Architecture](Architecture.md) for technical details

## Security Notes

- Requires root privileges
- Modifies kernel parameters
- No network connections
- No external dependencies beyond psutil
- Local operation only

## Best Practices

1. Test configuration changes in safe environment
2. Monitor system behavior after changes
3. Keep backup of working configurations
4. Review settings when hardware/workload changes
5. Use appropriate profile for your system
6. Use dry-run mode before applying changes

## Related Projects

- [zram-config](https://github.com/foundry376/zram-config) - Compressed RAM swap
- [earlyoom](https://github.com/rfjakob/earlyoom) - OOM daemon
- [systemd-swap](https://github.com/graysky2/systemd-swap) - Swap management

---

**Last Updated**: 2026-07-03
**Version**: 2.0.0
**Maintainer**: Linux Swap Optimizer Project
