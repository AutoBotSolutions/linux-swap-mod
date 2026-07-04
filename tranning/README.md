# Linux Swap Optimizer - Training Data

This directory contains training data and configuration templates for the Linux Swap Optimizer system. These files provide pre-configured settings and reference data for different system types and use cases.

## Directory Contents

### Configuration Templates
- **ai-workload-config.json** - Configuration for AI/ML development workstations
- **low-end-system-config.json** - Configuration for low-end systems with limited resources
- **gaming-config.json** - Configuration for gaming systems with low latency focus
- **server-config.json** - Configuration for production servers with stability focus

### Reference Data
- **performance-baselines.json** - Performance targets and optimization results for different system types
- **process-priority-mappings.json** - Default process categorization and priority settings
- **kernel-parameter-presets.json** - Pre-configured kernel parameter sets for different scenarios

## Usage

### Applying Configuration Templates

1. Copy the appropriate configuration template to your system:
```bash
cp tranning/ai-workload-config.json config.json
```

2. Modify the configuration as needed for your specific requirements

3. Restart the swap optimizer service:
```bash
sudo systemctl restart swap-optimizer
```

### Customizing Process Priority Mappings

Edit the `process-priority-mappings.json` file to add custom process patterns:

```json
{
  "custom_mappings": {
    "mappings": [
      {
        "name": "my-application",
        "patterns": ["myapp", "my-process"],
        "tier": "ai",
        "nice_value": -10
      }
    ]
  }
}
```

### Selecting Kernel Parameter Presets

Choose from the available presets in `kernel-parameter-presets.json`:
- **conservative** - Minimize swap usage, prioritize RAM
- **balanced** - Balance between RAM and swap usage
- **aggressive** - Maximize swap usage for better RAM utilization
- **performance** - Minimize latency, prioritize responsiveness
- **server** - Prioritize stability and throughput

## System Types

### AI Workstation
- **Hardware**: 32GB RAM, 16 CPU cores, 16GB swap
- **Optimization**: Aggressive AI process prioritization
- **Expected Results**: 60% CPU reduction, 40% memory efficiency

### Low-End System
- **Hardware**: 4GB RAM, 2 CPU cores, 8GB swap
- **Optimization**: Conservative memory management
- **Expected Results**: 30% CPU reduction, 25% memory efficiency

### Gaming System
- **Hardware**: 16GB RAM, 8 CPU cores, 16GB swap
- **Optimization**: Low latency and responsiveness
- **Expected Results**: 45% CPU reduction, 35% memory efficiency

### Server System
- **Hardware**: 64GB RAM, 32 CPU cores, 32GB swap
- **Optimization**: Stability and throughput
- **Expected Results**: 35% CPU reduction, 30% memory efficiency

## Performance Monitoring

Use the performance baselines to compare your system's performance against expected results:

```bash
# Check current system performance
python3 swap_optimizer.py --status

# Compare with baseline
python3 swap_optimizer.py --benchmark
```

## Customization Guidelines

### Memory Management
- Systems with sufficient RAM: Use conservative preset
- Systems with limited RAM: Use aggressive preset
- Balanced approach: Use balanced preset

### Process Prioritization
- AI/ML workloads: Prioritize AI tier processes
- Development work: Prioritize IDE tier processes
- Gaming: Prioritize interactive tier processes
- Server: Prioritize normal tier processes

### Kernel Parameters
- Always test kernel parameter changes in a safe environment
- Monitor system performance after applying changes
- Revert to default settings if issues occur

## Training and Learning

### Understanding Priority Tiers
1. **AI Tier** (-10 nice): Highest priority for AI/ML processes
2. **IDE Tier** (-5 nice): High priority for development tools
3. **Interactive Tier** (0 nice): Normal priority for user applications
4. **Normal Tier** (10 nice): Lower priority for system services
5. **Background Tier** (19 nice): Lowest priority for maintenance tasks

### Kernel Parameter Tuning
- Start with conservative settings
- Gradually adjust based on system performance
- Monitor swap usage and memory pressure
- Adjust swappiness based on available RAM

### Process Pattern Matching
- Use regex patterns for flexible process matching
- Test patterns before deployment
- Consider process name variations
- Account for different Linux distributions

## Troubleshooting

### Configuration Issues
- Verify JSON syntax is correct
- Check file permissions
- Ensure configuration file path is correct
- Review system logs for errors

### Performance Issues
- Compare against performance baselines
- Check system resource usage
- Verify process priority assignments
- Review kernel parameter settings

### Compatibility Issues
- Ensure Linux kernel version compatibility
- Check systemd service status
- Verify Python version requirements
- Review system dependencies

## Contributing

When adding new configurations or data:
1. Follow the existing JSON structure
2. Include descriptive comments
3. Test configurations before submission
4. Document expected performance results
5. Update this README with new information

## Support

For additional support:
- Check the main project README
- Review the documentation in the wiki
- Open an issue on GitHub
- Consult the performance reports

## Version Information

- **Training Data Version**: 1.0.0
- **Compatible with**: Linux Swap Optimizer v2.0.0
- **Last Updated**: 2026-07-04
