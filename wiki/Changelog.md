# Changelog

All notable changes to the Linux Swap Optimizer project will be documented in this file.

## [2.0.0] - 2026-07-03

### Added
- **General Application Optimization**: System now optimizes all running applications, not just AI/IDE processes
- **Process Categorization**: Implemented 5-tier priority system (AI, IDE, Interactive, Normal, Background)
- **OS-Level Kernel Optimizations**: Added dirty page ratio tuning and scheduler granularity settings
- **Interactive Process Detection**: Added detection for web browsers, communication apps, and media players
- **Background Process Detection**: Added detection for system services and background tasks
- **Dry-Run Mode**: Added `--dry-run` flag for safe testing without making changes
- **Enhanced Status Reporting**: Status command now shows process categories and optimization mode
- **Process Priority Tiers Documentation**: Comprehensive documentation for the new priority system

### Changed
- **Configuration Structure**: Split `ai_processes` into separate `ai_processes`, `ide_processes`, `interactive_processes`, and `background_processes` arrays
- **Priority Management**: Enhanced to support category-based priority tiers with different CPU and I/O priorities
- **Adaptive Management**: Updated to support general optimization mode with user process detection
- **Error Handling**: Improved kernel parameter handling with graceful degradation for unavailable parameters
- **Default Behavior**: `optimize_all_apps` now defaults to `true` for general desktop optimization

### Fixed
- **Kernel Compatibility**: Scheduler granularity parameters now handled gracefully when not available on certain kernels
- **Restore Function**: Enhanced to use system defaults when no original settings are saved
- **Logging**: Improved log level handling from configuration file

### Technical Details
- **Priority Settings**:
  - AI: nice=-10, ionice class 1 level 4
  - IDE: nice=-5, ionice class 1 level 4
  - Interactive: nice=-2, ionice class 2 level 4
  - Normal: nice=0, ionice class 2 level 7
  - Background: nice=5, ionice class 3 level 0

- **New Kernel Parameters**:
  - `vm.dirty_ratio=10`
  - `vm.dirty_background_ratio=5`
  - `kernel.sched_min_granularity_ns=1000000` (when available)
  - `kernel.sched_wakeup_granularity_ns=1000000` (when available)

### Migration Notes
- Existing configurations will automatically use defaults for new parameters
- Set `optimize_all_apps=false` in config to maintain legacy AI/IDE-only behavior
- Process lists can be customized in `/etc/swap-optimizer/config.json`

## [1.0.0] - 2026-07-03

### Added
- **Initial Release**: AI-aware swap management system
- **Process Prioritization**: Automatic prioritization of AI/IDE processes
- **Adaptive Monitoring**: Real-time adjustment based on system load
- **Configuration System**: JSON-based configuration with multiple parameters
- **Systemd Integration**: Service for continuous monitoring
- **Installation Script**: Automated setup and deployment
- **Comprehensive Documentation**: Wiki with architecture, configuration, and troubleshooting guides

### Features
- Swap parameter optimization (swappiness, vfs_cache_pressure, page_cluster, etc.)
- AI/IDE process detection and prioritization
- CPU and memory threshold-based adaptive management
- Automatic backup and restore of original settings
- Status reporting with system metrics

---

## Version History

### Version 2.0.0 (Current)
- General application optimization for all processes
- 5-tier priority categorization system
- OS-level kernel optimizations
- Enhanced documentation and debugging capabilities

### Version 1.0.0
- Initial AI/IDE-focused optimization
- Basic process prioritization
- Adaptive monitoring
- Core swap management features

## Future Plans

### Version 2.1.0 (Planned)
- Machine learning-based workload prediction
- Per-process memory cgroups integration
- GPU memory optimization coordination
- Automatic workload detection and profiling

### Version 3.0.0 (Future)
- Distributed system support
- Real-time performance dashboard
- Advanced analytics and reporting
- Integration with container orchestration systems

---

**Last Updated**: 2026-07-03
**Current Version**: 2.0.0
