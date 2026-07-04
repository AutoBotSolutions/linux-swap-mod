#!/usr/bin/env python3
"""
Linux Swap Optimizer for AI Workloads
Optimizes swap behavior to reduce CPU and system load during AI development
"""

import os
import sys
import time
import psutil
import logging
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import json

class SwapOptimizer:
    """
    Advanced swap management system with AI-aware heuristics
    """
    
    def __init__(self, config_path: str = "/etc/swap-optimizer/config.json", dry_run: bool = False):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = self._setup_logging()
        self.original_swap_settings = {}
        self.monitoring = False
        self.dry_run = dry_run
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('swap_optimizer')
        
        # Get log level from config
        log_level_str = self.config.get('log_level', 'INFO').upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        logger.setLevel(log_level)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _load_config(self) -> Dict:
        """Load configuration from file or use defaults"""
        default_config = {
            "swappiness": 10,
            "vfs_cache_pressure": 75,
            "page_cluster": 0,
            "min_free_kbytes": 65536,
            "watermark_scale_factor": 200,
            "cpu_threshold": 80,
            "memory_threshold": 85,
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
                "dbus", " NetworkManager", "bluetooth", "cups", "avahi"
            ],
            "optimize_all_apps": True,
            "check_interval": 5,
            "aggressive_mode": False
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
        except Exception as e:
            print(f"Warning: Could not load config, using defaults: {e}")
        
        return default_config
    
    def _save_original_settings(self):
        """Save original swap settings before modification"""
        swap_settings = {
            'vm.swappiness': self._read_sysctl('vm.swappiness'),
            'vm.vfs_cache_pressure': self._read_sysctl('vm.vfs_cache_pressure'),
            'vm.page-cluster': self._read_sysctl('vm.page-cluster'),
            'vm.min_free_kbytes': self._read_sysctl('vm.min_free_kbytes'),
            'vm.watermark_scale_factor': self._read_sysctl('vm.watermark_scale_factor')
        }
        self.original_swap_settings = swap_settings
        self.logger.info(f"Saved original settings: {swap_settings}")
    
    def _read_sysctl(self, key: str) -> int:
        """Read sysctl value"""
        try:
            result = subprocess.run(['sysctl', '-n', key], 
                                  capture_output=True, text=True)
            return int(result.stdout.strip())
        except Exception:
            return 0
    
    def _write_sysctl(self, key: str, value: int):
        """Write sysctl value"""
        if self.dry_run:
            self.logger.info(f"[DRY RUN] Would set {key}={value}")
            return True
        
        try:
            result = subprocess.run(['sysctl', '-w', f'{key}={value}'], 
                                  check=True, capture_output=True, text=True)
            self.logger.info(f"Set {key}={value}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to set {key}={value}: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to set {key}={value}: {e}")
            return False
    
    def _get_ai_processes(self) -> List[psutil.Process]:
        """Identify AI related processes"""
        ai_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name']:
                    proc_name = proc.info['name'].lower()
                    for ai_proc in self.config['ai_processes']:
                        if ai_proc in proc_name:
                            ai_processes.append(proc)
                            break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return ai_processes
    
    def _get_ide_processes(self) -> List[psutil.Process]:
        """Identify IDE related processes"""
        ide_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name']:
                    proc_name = proc.info['name'].lower()
                    for ide_proc in self.config.get('ide_processes', []):
                        if ide_proc in proc_name:
                            ide_processes.append(proc)
                            break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return ide_processes
    
    def _has_ide_running(self) -> bool:
        """Check if any IDE process is currently running"""
        ide_processes = self._get_ide_processes()
        return len(ide_processes) > 0
    
    def _get_interactive_processes(self) -> List[psutil.Process]:
        """Identify interactive user applications"""
        interactive_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name']:
                    proc_name = proc.info['name'].lower()
                    for app in self.config.get('interactive_processes', []):
                        if app in proc_name:
                            interactive_processes.append(proc)
                            break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return interactive_processes
    
    def _get_background_processes(self) -> List[psutil.Process]:
        """Identify background system processes"""
        background_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name']:
                    proc_name = proc.info['name'].lower()
                    for bg_proc in self.config.get('background_processes', []):
                        if bg_proc in proc_name:
                            background_processes.append(proc)
                            break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return background_processes
    
    def _categorize_process(self, proc: psutil.Process) -> str:
        """Categorize a process into priority tiers"""
        proc_name = proc.info['name'].lower() if proc.info['name'] else ""
        
        # Check AI processes (highest priority)
        for ai_proc in self.config['ai_processes']:
            if ai_proc in proc_name:
                return 'ai'
        
        # Check IDE processes (high priority)
        for ide_proc in self.config['ide_processes']:
            if ide_proc in proc_name:
                return 'ide'
        
        # Check interactive processes (medium priority)
        for app in self.config.get('interactive_processes', []):
            if app in proc_name:
                return 'interactive'
        
        # Check background processes (low priority)
        for bg_proc in self.config.get('background_processes', []):
            if bg_proc in proc_name:
                return 'background'
        
        # Default to normal priority
        return 'normal'
    
    def _get_all_user_processes(self) -> Dict[str, List[psutil.Process]]:
        """Get all user processes categorized by type"""
        categories = {
            'ai': [],
            'ide': [],
            'interactive': [],
            'normal': [],
            'background': []
        }
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                category = self._categorize_process(proc)
                categories[category].append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return categories
    
    def _get_system_load(self) -> Dict[str, float]:
        """Get current system load metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        load_avg = os.getloadavg()
        
        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'load_1min': load_avg[0],
            'load_5min': load_avg[1],
            'load_15min': load_avg[2]
        }
    
    def optimize_swap_settings(self):
        """Apply optimized swap settings for general system optimization"""
        self.logger.info("Applying optimized swap settings...")
        
        # Save original settings
        self._save_original_settings()
        
        # Apply optimized settings
        self._write_sysctl('vm.swappiness', self.config['swappiness'])
        self._write_sysctl('vm.vfs_cache_pressure', self.config['vfs_cache_pressure'])
        self._write_sysctl('vm.page-cluster', self.config['page_cluster'])
        self._write_sysctl('vm.min_free_kbytes', self.config['min_free_kbytes'])
        self._write_sysctl('vm.watermark_scale_factor', self.config['watermark_scale_factor'])
        
        # Additional OS-level optimizations
        self._apply_os_optimizations()
        
        # Disable swap if in aggressive mode and enough RAM available
        if self.config['aggressive_mode']:
            memory = psutil.virtual_memory()
            if memory.percent < 70:
                self.logger.info("Aggressive mode: Disabling swap")
                try:
                    subprocess.run(['swapoff', '-a'], check=True)
                except Exception as e:
                    self.logger.error(f"Failed to disable swap: {e}")
        
        self.logger.info("Swap optimization applied successfully")
    
    def _apply_os_optimizations(self):
        """Apply additional OS-level optimizations"""
        # Optimize dirty page ratios for better responsiveness
        try:
            self._write_sysctl('vm.dirty_ratio', 10)
            self._write_sysctl('vm.dirty_background_ratio', 5)
        except Exception as e:
            self.logger.warning(f"Could not set dirty ratios: {e}")
        
        # Optimize vfs cache pressure for better file performance
        try:
            self._write_sysctl('vm.vfs_cache_pressure', self.config['vfs_cache_pressure'])
        except Exception as e:
            self.logger.warning(f"Could not set vfs cache pressure: {e}")
        
        # Optimize for desktop responsiveness (only if available)
        # These parameters may not be available on all kernels
        try:
            self._write_sysctl('kernel.sched_min_granularity_ns', 1000000)
        except Exception as e:
            self.logger.debug(f"Scheduler min granularity not available: {e}")
        
        try:
            self._write_sysctl('kernel.sched_wakeup_granularity_ns', 1000000)
        except Exception as e:
            self.logger.debug(f"Scheduler wakeup granularity not available: {e}")
    
    def restore_original_settings(self):
        """Restore original swap settings"""
        self.logger.info("Restoring original swap settings...")
        
        if not self.original_swap_settings:
            self.logger.warning("No original settings saved, restoring to system defaults")
            # Restore to common system defaults
            default_settings = {
                'vm.swappiness': 60,
                'vm.vfs_cache_pressure': 100,
                'vm.page-cluster': 3,
                'vm.min_free_kbytes': 67584,
                'vm.watermark_scale_factor': 10
            }
            for key, value in default_settings.items():
                self._write_sysctl(key, value)
        else:
            for key, value in self.original_swap_settings.items():
                success = self._write_sysctl(key, value)
                if not success:
                    self.logger.error(f"Failed to restore {key}")
        
        # Re-enable swap if it was disabled
        try:
            subprocess.run(['swapon', '-a'], check=True, capture_output=True)
        except Exception as e:
            self.logger.error(f"Failed to re-enable swap: {e}")
        
        self.logger.info("Settings restored")
    
    def set_process_priorities(self):
        """Set nice and ionice priorities for all processes based on category"""
        if not self.config.get('optimize_all_apps', False):
            # Only optimize AI and IDE processes if optimize_all_apps is disabled
            self._set_priority_for_specific_processes()
            return
        
        if self.dry_run:
            categories = self._get_all_user_processes()
            total = sum(len(procs) for procs in categories.values())
            self.logger.info(f"[DRY RUN] Would set priorities for {total} processes across all categories")
            for category, procs in categories.items():
                if procs:
                    self.logger.info(f"[DRY RUN] {category.capitalize()}: {len(procs)} processes")
                    for proc in procs[:2]:
                        self.logger.info(f"[DRY RUN]   - {proc.info['name']} (PID: {proc.pid})")
            return
        
        categories = self._get_all_user_processes()
        
        # Priority settings for each category
        priority_settings = {
            'ai': {'nice': -10, 'ionice_class': 1, 'ionice_level': 4},
            'ide': {'nice': -5, 'ionice_class': 1, 'ionice_level': 4},
            'interactive': {'nice': -2, 'ionice_class': 2, 'ionice_level': 4},
            'normal': {'nice': 0, 'ionice_class': 2, 'ionice_level': 7},
            'background': {'nice': 5, 'ionice_class': 3, 'ionice_level': 0}
        }
        
        for category, processes in categories.items():
            settings = priority_settings.get(category, priority_settings['normal'])
            
            for proc in processes:
                try:
                    # Set CPU priority (nice value)
                    try:
                        proc.nice(settings['nice'])
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        pass
                    
                    # Set I/O priority
                    try:
                        subprocess.run(['ionice', '-c', str(settings['ionice_class']), 
                                      '-n', str(settings['ionice_level']), '-p', str(proc.pid)],
                                      check=True, capture_output=True)
                    except Exception:
                        pass
                    
                    self.logger.debug(f"Set {category} priority for {proc.info['name']} (PID: {proc.pid})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        
        # Log summary
        total_optimized = sum(len(procs) for procs in categories.values())
        self.logger.info(f"Optimized priorities for {total_optimized} processes across all categories")
    
    def _set_priority_for_specific_processes(self):
        """Set priorities only for AI and IDE processes (legacy mode)"""
        if self.dry_run:
            ai_processes = self._get_ai_processes()
            ide_processes = self._get_ide_processes()
            total_processes = len(ai_processes) + len(ide_processes)
            self.logger.info(f"[DRY RUN] Would set priorities for {total_processes} processes ({len(ai_processes)} AI, {len(ide_processes)} IDE)")
            for proc in ai_processes[:3]:
                self.logger.info(f"[DRY RUN] Would set priority for AI process {proc.info['name']} (PID: {proc.pid})")
            for proc in ide_processes[:3]:
                self.logger.info(f"[DRY RUN] Would set priority for IDE process {proc.info['name']} (PID: {proc.pid})")
            return
        
        # Combine AI and IDE processes
        ai_processes = self._get_ai_processes()
        ide_processes = self._get_ide_processes()
        all_processes = list(set(ai_processes + ide_processes))
        
        for proc in all_processes:
            try:
                proc.nice(-5)
                try:
                    subprocess.run(['ionice', '-c', '1', '-n', '4', '-p', str(proc.pid)],
                                  check=True, capture_output=True)
                except Exception:
                    pass
                self.logger.info(f"Set priority for {proc.info['name']} (PID: {proc.pid})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    def adaptive_swap_management(self):
        """Dynamically adjust swap behavior based on system load and all running processes"""
        if not self.monitoring:
            return
        
        load = self._get_system_load()
        
        if self.config.get('optimize_all_apps', False):
            # General optimization mode - always maintain optimal settings
            categories = self._get_all_user_processes()
            has_user_processes = sum(len(procs) for procs in categories.values()) > 0
            
            if has_user_processes:
                current_swappiness = self._read_sysctl('vm.swappiness')
                target_swappiness = self.config['swappiness']
                
                if current_swappiness != target_swappiness:
                    self._write_sysctl('vm.swappiness', target_swappiness)
                    self.logger.info(f"User processes detected, adjusted swappiness to {target_swappiness}")
        else:
            # Legacy mode - only optimize for AI/IDE
            has_ide = self._has_ide_running()
            has_ai = len(self._get_ai_processes()) > 0
            
            if has_ide or has_ai:
                current_swappiness = self._read_sysctl('vm.swappiness')
                target_swappiness = self.config['swappiness']
                
                if current_swappiness != target_swappiness:
                    self._write_sysctl('vm.swappiness', target_swappiness)
                    self.logger.info(f"IDE/AI detected, adjusted swappiness to {target_swappiness}")
        
        # Increase swappiness under heavy load to prevent OOM
        if load['cpu_percent'] > self.config['cpu_threshold'] or \
           load['memory_percent'] > self.config['memory_threshold']:
            
            current_swappiness = self._read_sysctl('vm.swappiness')
            if current_swappiness < 30:
                new_swappiness = min(current_swappiness + 10, 30)
                self._write_sysctl('vm.swappiness', new_swappiness)
                self.logger.info(f"High load detected, increased swappiness to {new_swappiness}")
        
        # Decrease swappiness under normal load
        else:
            current_swappiness = self._read_sysctl('vm.swappiness')
            if current_swappiness > self.config['swappiness']:
                new_swappiness = max(current_swappiness - 5, self.config['swappiness'])
                self._write_sysctl('vm.swappiness', new_swappiness)
                self.logger.info(f"Normal load, decreased swappiness to {new_swappiness}")
    
    def start_monitoring(self):
        """Start continuous monitoring and adaptive management"""
        self.monitoring = True
        self.logger.info("Starting adaptive swap monitoring...")
        
        try:
            while self.monitoring:
                self.adaptive_swap_management()
                self.set_process_priorities()
                time.sleep(self.config['check_interval'])
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
            self.monitoring = False
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        self.logger.info("Stopping monitoring...")
    
    def get_status(self) -> Dict:
        """Get current system status and settings"""
        load = self._get_system_load()
        swap_info = psutil.swap_memory()
        categories = self._get_all_user_processes()
        
        return {
            'system_load': load,
            'swap_usage': {
                'total': swap_info.total,
                'used': swap_info.used,
                'free': swap_info.free,
                'percent': swap_info.percent
            },
            'current_settings': {
                'swappiness': self._read_sysctl('vm.swappiness'),
                'vfs_cache_pressure': self._read_sysctl('vm.vfs_cache_pressure'),
                'page_cluster': self._read_sysctl('vm.page-cluster')
            },
            'process_categories': {
                'ai': len(categories['ai']),
                'ide': len(categories['ide']),
                'interactive': len(categories['interactive']),
                'normal': len(categories['normal']),
                'background': len(categories['background'])
            },
            'optimize_all_apps': self.config.get('optimize_all_apps', False),
            'total_processes': sum(len(procs) for procs in categories.values())
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Linux Swap Optimizer for AI Workloads')
    parser.add_argument('--optimize', action='store_true', help='Apply optimized swap settings')
    parser.add_argument('--restore', action='store_true', help='Restore original settings')
    parser.add_argument('--monitor', action='store_true', help='Start adaptive monitoring')
    parser.add_argument('--status', action='store_true', help='Show current status')
    parser.add_argument('--config', default='/etc/swap-optimizer/config.json', 
                       help='Path to config file')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    optimizer = SwapOptimizer(config_path=args.config, dry_run=args.dry_run)
    
    if args.optimize:
        optimizer.optimize_swap_settings()
        optimizer.set_process_priorities()
    
    elif args.restore:
        optimizer.restore_original_settings()
    
    elif args.monitor:
        optimizer.optimize_swap_settings()
        optimizer.start_monitoring()
    
    elif args.status:
        status = optimizer.get_status()
        print(json.dumps(status, indent=2))
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
