# Performance Tuning Guide

## Overview

This guide provides advanced tuning strategies for optimizing the Linux Swap Optimizer for specific workloads and hardware configurations.

## System Assessment

### Baseline Performance Measurement

Before tuning, establish a baseline:

```bash
# Record current swap settings
sudo sysctl -a | grep -E "swappiness|vfs_cache|page-cluster|min_free|watermark" > baseline-sysctl.txt

# Record system performance
free -h > baseline-memory.txt
swapon --show > baseline-swap.txt
iostat -x 1 5 > baseline-io.txt
vmstat 1 5 > baseline-vmstat.txt
```

### Workload Identification

Identify your primary workload type:

**AI/ML Development**
- Python processes (TensorFlow, PyTorch)
- Jupyter notebooks
- Large model training/inference
- GPU memory pressure

**Web Development**
- Node.js processes
- Build tools (webpack, vite)
- Multiple browser tabs
- Docker containers

**General Development**
- IDE processes (VS Code, IntelliJ)
- Compilation/linking
- Database operations
- Testing frameworks

## Hardware-Specific Tuning

### Low-End Systems (< 4GB RAM)

#### Characteristics
- Limited memory capacity
- Slower storage (HDD)
- Fewer CPU cores
- I/O bound workloads

#### Recommended Configuration

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

#### Additional Optimizations

**1. Reduce Background Services**
```bash
# Disable unnecessary services
sudo systemctl disable bluetooth
sudo systemctl disable cups
```

**2. Use ZRAM (Compressed RAM Swap)**
```bash
# Install zram
sudo apt-get install zram-config

# Configure zram size (50% of RAM)
echo "zram" | sudo tee -a /etc/modules-load.d/zram.conf
```

**3. Prefer SSD Over HDD**
- If possible, use SSD for swap partition
- If using HDD, consider USB 3.0 external SSD

### Mid-Range Systems (4-8GB RAM)

#### Characteristics
- Adequate memory for most tasks
- SSD storage common
- Multi-core CPU
- Balanced workloads

#### Recommended Configuration

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

#### Additional Optimizations

**1. Enable Swap Prefetch**
```bash
# Add to /etc/sysctl.conf
vm.page-cluster = 3
```

**2. Optimize I/O Scheduler**
```bash
# For SSDs
echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler

# For HDDs
echo cfq | sudo tee /sys/block/sda/queue/scheduler
```

**3. Use Swap File Instead of Partition**
```bash
# Create swap file
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### High-End Systems (> 8GB RAM)

#### Characteristics
- Abundant memory
- Fast NVMe storage
- Many CPU cores
- CPU-bound workloads

#### Recommended Configuration

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

#### Additional Optimizations

**1. Enable Transparent Huge Pages**
```bash
# Add to /etc/sysctl.conf
vm.transparent_hugepage = always
```

**2. Optimize NUMA (if applicable)**
```bash
# Check NUMA topology
numactl --hardware

# Bind processes to local memory
numactl --interleave=all python3 script.py
```

**3. Use Multiple Swap Devices**
```bash
# Create multiple swap files
sudo fallocate -l 2G /swapfile1
sudo fallocate -l 2G /swapfile2
sudo mkswap /swapfile1
sudo mkswap /swapfile2
sudo swapon /swapfile1
sudo swapon /swapfile2

# Set equal priorities
sudo swapon --show
```

## Workload-Specific Tuning

### AI/ML Development

#### Configuration
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

#### Additional Optimizations

**1. GPU Memory Management**
```bash
# Monitor GPU memory
nvidia-smi

# Set GPU memory growth (TensorFlow)
export TF_FORCE_GPU_ALLOW_GROWTH=true
```

**2. Batch Size Tuning**
- Start with small batches (8-16)
- Increase until memory pressure is acceptable
- Monitor swap activity during training

**3. Data Loading Optimization**
```python
# Use prefetching
dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)

# Use caching
dataset = dataset.cache()
```

### Web Development

#### Configuration
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

#### Additional Optimizations

**1. Node.js Memory Limit**
```bash
# Increase Node.js heap size
export NODE_OPTIONS="--max-old-space-size=4096"
```

**2. Build Tool Optimization**
```bash
# Use parallel builds
npm install --parallel

# Increase file watchers
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
```

**3. Browser Tab Management**
- Use tab suspension extensions
- Limit active tabs to < 20
- Enable hardware acceleration

### Database Development

#### Configuration
```json
{
  "swappiness": 10,
  "vfs_cache_pressure": 50,
  "page_cluster": 0,
  "min_free_kbytes": 131072,
  "watermark_scale_factor": 200,
  "cpu_threshold": 80,
  "memory_threshold": 85,
  "ai_processes": [
    "postgres", "mysql", "mongodb", "redis",
    "code", "cursor", "idea"
  ],
  "check_interval": 5,
  "aggressive_mode": false,
  "log_level": "INFO"
}
```

#### Additional Optimizations

**1. Database Memory Configuration**
```sql
-- PostgreSQL
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
```

**2. Connection Pooling**
- Use connection pools
- Limit concurrent connections
- Implement connection timeouts

**3. Query Optimization**
- Use EXPLAIN ANALYZE
- Add appropriate indexes
- Optimize JOIN operations

## Advanced Tuning Techniques

### Custom Monitoring Scripts

Create custom monitoring for specific metrics:

```bash
#!/bin/bash
# custom-monitor.sh

while true; do
    # Monitor specific process
    python3_mem=$(ps aux | grep python | awk '{sum+=$4} END {print sum}')
    
    # Monitor swap activity
    swap_in=$(vmstat 1 2 | tail -1 | awk '{print $7}')
    swap_out=$(vmstat 1 2 | tail -1 | awk '{print $8}')
    
    # Log if thresholds exceeded
    if [ "$python3_mem" -gt 50 ]; then
        echo "High Python memory: $python3_mem%" >> /var/log/swap-monitor.log
    fi
    
    sleep 5
done
```

### Dynamic Configuration Adjustment

Create a script that adjusts config based on time of day:

```bash
#!/bin/bash
# time-based-config.sh

HOUR=$(date +%H)

if [ $HOUR -ge 9 ] && [ $HOUR -lt 17 ]; then
    # Work hours - more aggressive
    cp work-hours-config.json /etc/swap-optimizer/config.json
else
    # Off hours - conservative
    cp off-hours-config.json /etc/swap-optimizer/config.json
fi

systemctl restart swap-optimizer
```

### Load-Based Configuration

Adjust configuration based on system load:

```python
#!/usr/bin/env python3
import psutil
import json

def get_load_profile():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    
    if cpu > 80 or memory > 85:
        return "high-load"
    elif cpu > 60 or memory > 70:
        return "medium-load"
    else:
        return "low-load"

# Load appropriate config
profile = get_load_profile()
with open(f"{profile}-config.json") as f:
    config = json.load(f)

# Apply config
with open("/etc/swap-optimizer/config.json", "w") as f:
    json.dump(config, f)
```

## Performance Benchmarking

### Benchmark Script

```bash
#!/bin/bash
# benchmark.sh

echo "=== Swap Optimizer Benchmark ==="

# Test 1: Swap operations
echo "Testing swap operations..."
time dd if=/dev/zero of=/tmp/swap-test bs=1M count=1000
sync
time dd if=/tmp/swap-test of=/dev/null bs=1M
rm /tmp/swap-test

# Test 2: Memory allocation
echo "Testing memory allocation..."
python3 -c "
import time
import psutil
start = time.time()
data = [bytearray(1024*1024) for _ in range(100)]
end = time.time()
print(f'Memory allocation time: {end-start:.2f}s')
print(f'Memory used: {psutil.virtual_memory().percent}%')
"

# Test 3: Process spawning
echo "Testing process spawning..."
time python3 -c "
import subprocess
for i in range(10):
    subprocess.run(['sleep', '0.1'])
"
```

### Comparative Testing

Test with and without optimization:

```bash
# Baseline (no optimization)
sudo python3 /opt/swap-optimizer/swap_optimizer.py --restore
./benchmark.sh > baseline-results.txt

# With optimization
sudo python3 /opt/swap-optimizer/swap_optimizer.py --optimize
./benchmark.sh > optimized-results.txt

# Compare
diff baseline-results.txt optimized-results.txt
```

## Monitoring and Analysis

### Real-Time Monitoring

```bash
# Monitor swap activity
watch -n 1 'cat /proc/vmstat | grep -E "pswpin|pswpout"'

# Monitor memory pressure
watch -n 1 'cat /proc/pressure/memory'

# Monitor CPU pressure
watch -n 1 'cat /proc/pressure/cpu'
```

### Long-Term Analysis

```bash
# Collect data over time
#!/bin/bash
for i in {1..144}; do  # 24 hours at 10-minute intervals
    date >> performance-log.txt
    free -h >> performance-log.txt
    iostat -x 1 2 >> performance-log.txt
    vmstat 1 2 >> performance-log.txt
    sleep 600
done
```

### Performance Graphing

Use collected data to create graphs:

```python
#!/usr/bin/env python3
import matplotlib.pyplot as plt

# Parse log file and create graphs
# (Implementation depends on log format)
```

## Troubleshooting Performance Issues

### Swap Thrashing

**Symptoms**: High I/O wait, system slowdown

**Solutions**:
1. Reduce swappiness
2. Increase min_free_kbytes
3. Add more RAM
4. Use faster storage

### Memory Fragmentation

**Symptoms**: Out-of-memory despite free memory

**Solutions**:
1. Enable transparent huge pages
2. Increase watermark_scale_factor
3. Restart memory-intensive applications

### High CPU Usage by Optimizer

**Symptoms**: swap-optimizer process using significant CPU

**Solutions**:
1. Increase check_interval
2. Reduce ai_processes list
3. Disable debug logging

## Best Practices

1. **Test Changes Gradually**: Change one parameter at a time
2. **Monitor After Changes**: Watch system behavior for at least 24 hours
3. **Keep Backups**: Always backup working configurations
4. **Document Changes**: Note what you changed and why
5. **Use Profiles**: Maintain different configs for different workloads
6. **Regular Review**: Reassess tuning as workload changes

## Safety Guidelines

1. **Never set swappiness to 0** - Can cause OOM
2. **Don't enable aggressive_mode on low RAM** - Can cause system freeze
3. **Keep min_free_kbytes reasonable** - Too high wastes memory
4. **Test in safe environment** - Before production deployment
5. **Have rollback plan** - Know how to restore quickly
