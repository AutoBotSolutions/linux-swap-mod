# Use Cases

This document describes the various use cases and system configurations supported by the Linux Swap Optimizer. Each use case is optimized for specific hardware profiles and workload requirements.

## Available Use Cases

### AI Workstation Optimization

**Target System:** AI/ML Development Workstations
**Hardware Profile:** 32GB RAM, 16 CPU cores, 16GB swap

**Description:**
Optimized for AI/ML workloads with GPU training and inference operations. This configuration provides aggressive prioritization for AI processes while maintaining system responsiveness for development tools.

**Key Features:**
- AI processes receive highest priority (nice -10)
- IDE processes get high priority (nice -5)
- Aggressive CPU and I/O optimization
- Real-time monitoring with 3-second intervals
- Memory threshold at 90%

**Performance Targets:**
- Memory usage: 75%
- CPU usage: 80%
- Swap usage: 20%
- Response time: 100ms

**Expected Results:**
- 60% CPU reduction
- 40% memory efficiency improvement
- 50% latency reduction

**Process Patterns:**
- Python training/inference processes
- TensorFlow, PyTorch, Keras frameworks
- Jupyter notebooks
- CUDA/GPU processes
- Development IDEs

**Configuration File:** `tranning/ai-workload-config.json`

---

### Low-End System Optimization

**Target System:** Low-End Desktops and Laptops
**Hardware Profile:** 4GB RAM, 2 CPU cores, 8GB swap

**Description:**
Designed for resource-constrained systems with limited RAM and CPU. This configuration uses conservative memory management with aggressive swap usage to maximize available resources.

**Key Features:**
- Conservative memory management (swappiness: 1)
- Aggressive swap utilization
- Reduced monitoring frequency (5-second intervals)
- Lower memory threshold (85%)
- Powersave CPU affinity for background processes

**Performance Targets:**
- Memory usage: 85%
- CPU usage: 90%
- Swap usage: 60%
- Response time: 500ms

**Expected Results:**
- 30% CPU reduction
- 25% memory efficiency improvement
- 35% latency reduction

**Process Patterns:**
- Lightweight AI processes
- Basic development tools
- Essential system services
- Background maintenance tasks

**Configuration File:** `tranning/low-end-system-config.json`

---

### Gaming System Optimization

**Target System:** Gaming Desktops and Laptops
**Hardware Profile:** 16GB RAM, 8 CPU cores, 16GB swap

**Description:**
Optimized for gaming systems with focus on low latency and high responsiveness. This configuration prioritizes game processes and audio services while maintaining system stability.

**Key Features:**
- Game processes receive highest priority
- Low-latency audio prioritization
- Performance-focused kernel parameters
- Fast monitoring (2-second intervals)
- High thresholds for memory (95%) and CPU (98%)

**Performance Targets:**
- Memory usage: 70%
- CPU usage: 85%
- Swap usage: 10%
- Response time: 50ms

**Expected Results:**
- 45% CPU reduction
- 35% memory efficiency improvement
- 60% latency reduction

**Process Patterns:**
- Steam, game executables
- Wine/Proton compatibility layers
- Discord and overlay applications
- Audio services (PulseAudio, PipeWire)

**Configuration File:** `tranning/gaming-config.json`

---

### Server System Optimization

**Target System:** Production Servers
**Hardware Profile:** 64GB RAM, 32 CPU cores, 32GB swap

**Description:**
Configured for production servers with emphasis on stability, throughput, and reliability. This configuration balances performance with system stability for continuous operation.

**Key Features:**
- Balanced memory management (swappiness: 20)
- Server-optimized kernel parameters
- Longer monitoring intervals (10 seconds)
- Conservative thresholds
- Strict memory overcommit policies

**Performance Targets:**
- Memory usage: 80%
- CPU usage: 75%
- Swap usage: 30%
- Response time: 200ms

**Expected Results:**
- 35% CPU reduction
- 30% memory efficiency improvement
- 40% latency reduction

**Process Patterns:**
- Web servers (Nginx, Apache)
- Databases (MySQL, PostgreSQL, Redis, MongoDB)
- SSH and administrative services
- System maintenance tasks

**Configuration File:** `tranning/server-config.json`

---

## Selecting the Right Use Case

### Hardware Considerations

**RAM Capacity:**
- **4GB or less:** Use Low-End System configuration
- **8-16GB:** Use Gaming or AI Workstation configuration
- **32GB or more:** Use AI Workstation or Server configuration

**CPU Cores:**
- **2-4 cores:** Use Low-End System configuration
- **8-16 cores:** Use Gaming or AI Workstation configuration
- **32+ cores:** Use Server configuration

**Primary Workload:**
- **AI/ML Development:** Use AI Workstation configuration
- **Gaming:** Use Gaming configuration
- **Web/Database Services:** Use Server configuration
- **General Desktop:** Use Low-End System configuration

### Performance Requirements

**Low Latency (gaming, real-time):**
- Use Gaming configuration
- Minimize swap usage
- Prioritize interactive processes

**High Throughput (servers):**
- Use Server configuration
- Balance memory and swap
- Optimize for sustained performance

**Resource Constrained:**
- Use Low-End System configuration
- Aggressive swap management
- Conservative memory usage

## Customizing Use Cases

### Modifying Configuration Templates

1. Copy the appropriate template:
```bash
cp tranning/ai-workload-config.json config.json
```

2. Edit the configuration to match your system:
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

3. Apply the configuration:
```bash
sudo systemctl restart swap-optimizer
```

### Creating Custom Use Cases

1. Start with the closest existing template
2. Adjust hardware profile settings
3. Modify priority tier assignments
4. Tune kernel parameters for your needs
5. Test and monitor performance
6. Save as custom configuration

## Performance Monitoring

### Comparing Against Baselines

Use the performance baselines to track your system's performance:

```bash
# Check current performance
python3 swap_optimizer.py --status

# Run benchmark comparison
python3 swap_optimizer.py --benchmark

# View detailed metrics
python3 swap_optimizer.py --metrics
```

### Expected vs Actual Performance

Compare your system's actual performance against the expected results for your use case:

- **CPU Reduction:** Compare actual vs expected CPU usage reduction
- **Memory Efficiency:** Monitor memory usage patterns
- **Latency:** Measure response times
- **Swap Usage:** Track swap utilization

## Troubleshooting Use Cases

### Performance Not Meeting Expectations

1. Verify hardware matches use case profile
2. Check configuration is applied correctly
3. Monitor system resources during workload
4. Adjust kernel parameters if needed
5. Consider hybrid configuration approach

### System Instability

1. Revert to conservative settings
2. Check for conflicting configurations
3. Review system logs for errors
4. Verify kernel parameter compatibility
5. Test with default configuration

### Resource Exhaustion

1. Lower monitoring thresholds
2. Increase swap priority
3. Adjust nice values for less aggressive prioritization
4. Consider hardware upgrade
5. Use more conservative use case

## Best Practices

### Before Applying Use Cases

1. Backup current configuration
2. Document system baseline performance
3. Test in safe environment first
4. Monitor system during initial deployment
5. Have rollback plan ready

### During Operation

1. Monitor performance metrics regularly
2. Adjust based on actual workload patterns
3. Keep system updated
4. Review logs for optimization patterns
5. Document custom modifications

### Maintenance

1. Review configuration quarterly
2. Update process patterns as needed
3. Adjust for hardware changes
4. Compare against latest baselines
5. Contribute improvements back to project

## Additional Resources

- **Configuration Guide:** [Configuration-Guide.md](Configuration-Guide.md)
- **Process Priority Tiers:** [Process-Priority-Tiers.md](Process-Priority-Tiers.md)
- **Performance Tuning:** [Performance-Tuning.md](Performance-Tuning.md)
- **Training Data:** See `/tranning/` directory for configuration templates

## Support

For use case-specific issues:
- Check the FAQ for common problems
- Review troubleshooting documentation
- Open GitHub issue with system details
- Consult performance reports for guidance
