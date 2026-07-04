# Architecture and Design

## System Overview

The Linux Swap Optimizer is a comprehensive system designed to reduce CPU and system load during AI development and general application usage on low-end systems. It achieves this through intelligent swap management, process prioritization across multiple categories, adaptive monitoring, and OS-level optimizations.

## Core Components

### 1. SwapOptimizer Class

The main orchestrator that coordinates all optimization activities.

**Responsibilities:**
- Configuration management
- System monitoring
- Swap parameter optimization
- Process priority management across 5 categories
- OS-level kernel optimization
- Adaptive decision making

### 2. Swap Management Module

Handles all Linux kernel swap parameter modifications.

**Key Parameters:**
- `vm.swappiness` - Controls kernel's tendency to swap
- `vm.vfs_cache_pressure` - Balances cache vs memory reclaim
- `vm.page_cluster` - Controls page clustering during swap
- `vm.min_free_kbytes` - Ensures minimum free memory
- `vm.watermark_scale_factor` - Improves watermark calculations
- `vm.dirty_ratio` - Dirty page ratio for responsiveness
- `vm.dirty_background_ratio` - Background dirty page handling
- `kernel.sched_min_granularity_ns` - Scheduler granularity (kernel-dependent)
- `kernel.sched_wakeup_granularity_ns` - Wakeup granularity (kernel-dependent)

**Note**: Some kernel parameters may not be available on all Linux distributions. The system gracefully handles unavailable parameters by logging them at debug level and continuing with available optimizations.

### 3. System Monitor

Continuously tracks system metrics for adaptive decisions.

**Monitored Metrics:**
- CPU usage percentage
- Memory usage percentage
- System load averages (1, 5, 15 min)
- Swap usage statistics
- Process categories (AI, IDE, interactive, normal, background)

### 4. Process Manager

Identifies and prioritizes processes across 5 categories.

**Process Categories:**
- AI processes (highest priority)
- IDE processes (high priority)
- Interactive applications (medium priority)
- Normal processes (default priority)
- Background processes (low priority)

**Detection Methods:**
- Process name matching against configurable lists
- Command line analysis
- Real-time process tracking
- Automatic categorization algorithm

**Priority Settings:**
- CPU priority (nice values): -10 to +5
- I/O priority (ionice classes): 1-3 with levels 0-7

**Priority Adjustments:**
- Nice value adjustment (CPU priority)
- I/O nice value adjustment (I/O priority)
- Real-time scheduling for critical processes
- Category-based priority tiers

### 5. Adaptive Controller

Makes dynamic decisions based on system state.

**Decision Logic:**
```
IF (optimize_all_apps enabled AND user processes detected):
    Maintain optimal swap settings
ELSE IF (AI/IDE processes detected):
    Maintain optimal swap settings
ELSE IF (CPU > threshold OR Memory > threshold):
    Increase swappiness to prevent OOM
ELSE:
    Decrease swappiness to reduce swap activity
```

## Data Flow

```
┌─────────────────┐
│  Configuration  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SwapOptimizer   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────────┐
│ Monitor │ │ Process    │
│         │ │ Manager    │
└────┬────┘ └─────┬──────┘
     │             │
     └──────┬──────┘
            ▼
     ┌──────────────┐
     │ Adaptive     │
     │ Controller   │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ Swap Manager │
     └──────────────┘
```

## Design Principles

### 1. Safety First

- Original settings always backed up before modification
- Conservative default values
- Graceful degradation on errors
- One-command rollback capability

### 2. AI-Aware

- Specifically tuned for AI/IDE workloads
- Process detection for common AI tools
- Priority management for AI applications
- Memory optimization for ML frameworks

### 3. Adaptive

- Real-time monitoring
- Dynamic parameter adjustment
- Load-based decision making
- Self-tuning behavior

### 4. Low-End Optimized

- Minimal CPU overhead
- Efficient memory usage
- Fast I/O operations
- Reduced system calls

## Technical Details

### Swap Parameter Optimization

#### vm.swappiness
- **Default**: 10 (vs system default 60)
- **Purpose**: Reduces aggressive swapping
- **Effect**: Keeps more data in RAM, reduces disk I/O

#### vm.vfs_cache_pressure
- **Default**: 75 (vs system default 100)
- **Purpose**: Better cache retention
- **Effect**: Improves file system performance

#### vm.page-cluster
- **Default**: 0 (vs system default 3)
- **Purpose**: Disables page clustering
- **Effect**: Faster individual page swaps, less burst I/O

#### vm.min_free_kbytes
- **Default**: 65536 (64MB)
- **Purpose**: Ensures memory for critical operations
- **Effect**: Prevents OOM situations

#### vm.watermark_scale_factor
- **Default**: 200 (vs system default 10)
- **Purpose**: Improves memory watermark calculations
- **Effect**: Better memory pressure handling

### Process Priority System

#### CPU Priority (nice)
- **Range**: -20 (highest) to 19 (lowest)
- **AI Processes**: Set to -5 (elevated priority)
- **Effect**: Better CPU time allocation

#### I/O Priority (ionice)
- **Classes**: 1 (realtime), 2 (best-effort), 3 (idle)
- **AI Processes**: Class 1, level 4
- **Effect**: Reduced I/O latency

### Adaptive Algorithm

```
while monitoring:
    load = get_system_load()
    
    if load.cpu > cpu_threshold or load.memory > memory_threshold:
        current = read_sysctl('vm.swappiness')
        if current < 30:
            new = min(current + 10, 30)
            write_sysctl('vm.swappiness', new)
    else:
        current = read_sysctl('vm.swappiness')
        if current > config.swappiness:
            new = max(current - 5, config.swappiness)
            write_sysctl('vm.swappiness', new)
    
    set_process_priorities()
    sleep(check_interval)
```

## Performance Characteristics

### CPU Overhead
- **Monitoring**: < 1% CPU
- **Optimization**: < 0.5% CPU
- **Total**: < 2% CPU overhead

### Memory Usage
- **Base**: ~20MB RSS
- **Per process**: ~1KB
- **Total**: < 50MB typical

### I/O Impact
- **Read**: Minimal (config files)
- **Write**: Periodic sysctl updates
- **Network**: None

## Security Considerations

### Privilege Requirements
- **Root access**: Required for sysctl modifications
- **Process priority**: Requires appropriate permissions
- **Service**: Runs as root user

### Security Measures
- No network connections
- No external dependencies beyond psutil
- Configuration file validation
- Safe parameter ranges enforced

## Extensibility

### Adding New Process Types
Edit `ai_processes` in config.json:
```json
"ai_processes": [
  "python", "node", "code", "cursor",
  "your_new_process"
]
```

### Custom Monitoring Metrics
Extend `_get_system_load()` method:
```python
def _get_system_load(self) -> Dict[str, float]:
    # Add custom metrics here
    custom_metric = get_custom_metric()
    return {
        'cpu_percent': cpu_percent,
        'custom_metric': custom_metric
    }
```

### Additional Swap Parameters
Add to `_save_original_settings()` and `optimize_swap_settings()`:
```python
self._write_sysctl('vm.new_parameter', value)
```

## Limitations

1. **Linux Only**: Designed specifically for Linux kernel
2. **Root Required**: Cannot run without root privileges
3. **Kernel Version**: Requires kernel 3.10+
4. **Process Detection**: Limited to name-based matching
5. **Swap Device**: Does not manage swap device creation

## Future Enhancements

### Planned Features
- Machine learning-based prediction
- Per-process memory cgroups
- Swap device management
- GPU memory optimization
- Network-aware swap (for distributed systems)

### Research Areas
- AI workload pattern recognition
- Predictive pre-fetching
- Dynamic swap partition sizing
- Cross-node swap coordination

---

**Last Updated**: 2026-07-03
**Version**: 2.0.0
