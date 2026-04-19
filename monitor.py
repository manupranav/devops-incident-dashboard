#!/usr/bin/env python3
"""
monitor.py — System Health Monitor
Checks CPU, memory, and disk usage against configured thresholds.
Sends alerts if thresholds are breached.

TODO: Add network I/O monitoring
TODO: Add support for multiple hosts (not just localhost)
TODO: Hook this into alert.sh properly
"""

import os
import sys
import time
import yaml
import logging
import random  # TODO: Remove this — used for fake data simulation only
from datetime import datetime

# --- Logging setup ---
LOG_FILE = "logs/monitor.log"
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

CONFIG_PATH = "config/thresholds.yaml"


def load_config(path: str) -> dict:
    """Load threshold configuration from YAML file."""
    if not os.path.exists(path):
        logger.error(f"Config file not found: {path}")
        sys.exit(1)
    with open(path, "r") as f:
        return yaml.safe_load(f)


def get_cpu_usage() -> float:
    """
    Simulated CPU usage.
    TODO: Replace with psutil.cpu_percent(interval=1) in production.
    """
    return round(random.uniform(10.0, 95.0), 2)


def get_memory_usage() -> float:
    """
    Simulated memory usage percentage.
    TODO: Replace with psutil.virtual_memory().percent in production.
    """
    return round(random.uniform(20.0, 90.0), 2)


def get_disk_usage(path: str = "/") -> float:
    """
    Simulated disk usage percentage.
    TODO: Replace with psutil.disk_usage(path).percent in production.
    """
    return round(random.uniform(30.0, 85.0), 2)

def get_network_io() -> dict:
    """
    Simulated network I/O stats.
    TODO: Replace with psutil.net_io_counters() in production.
    """
    return {
        "bytes_sent": random.randint(1000, 50000),
        "bytes_recv": random.randint(5000, 100000),
    }

def check_thresholds(metrics: dict, thresholds: dict) -> list:
    """Compare metrics against thresholds and return list of alerts."""
    alerts = []

    cpu = metrics.get("cpu")
    mem = metrics.get("memory")
    disk = metrics.get("disk")

    if cpu is not None and cpu > thresholds.get("cpu_critical", 90):
        alerts.append({"level": "CRITICAL", "metric": "CPU", "value": cpu, "threshold": thresholds["cpu_critical"]})
    elif cpu is not None and cpu > thresholds.get("cpu_warning", 75):
        alerts.append({"level": "WARNING", "metric": "CPU", "value": cpu, "threshold": thresholds["cpu_warning"]})

    if mem is not None and mem > thresholds.get("memory_critical", 90):
        alerts.append({"level": "CRITICAL", "metric": "Memory", "value": mem, "threshold": thresholds["memory_critical"]})
    elif mem is not None and mem > thresholds.get("memory_warning", 80):
        alerts.append({"level": "WARNING", "metric": "Memory", "value": mem, "threshold": thresholds["memory_warning"]})

    if disk is not None and disk > thresholds.get("disk_critical", 90):
        alerts.append({"level": "CRITICAL", "metric": "Disk", "value": disk, "threshold": thresholds["disk_critical"]})
    elif disk is not None and disk > thresholds.get("disk_warning", 75):
        alerts.append({"level": "WARNING", "metric": "Disk", "value": disk, "threshold": thresholds["disk_warning"]})

    return alerts


def run_monitor(interval: int = 10):
    """Main monitoring loop."""
    config = load_config(CONFIG_PATH)
    thresholds = config.get("thresholds", {})
    logger.info("Monitor started. Polling every %d seconds.", interval)

    while True:
        metrics = {
            "cpu": get_cpu_usage(),
            "memory": get_memory_usage(),
            "disk": get_disk_usage(),
        }

        logger.info("Metrics — CPU: %.1f%%  Memory: %.1f%%  Disk: %.1f%%",
                    metrics["cpu"], metrics["memory"], metrics["disk"])

        alerts = check_thresholds(metrics, thresholds)

        if alerts:
            for alert in alerts:
                logger.warning(
                    "[%s] %s at %.1f%% (threshold: %.1f%%)",
                    alert["level"], alert["metric"], alert["value"], alert["threshold"]
                )
            # TODO: Pipe alerts to alert.sh instead of just logging
        else:
            logger.info("All systems nominal.")

        time.sleep(interval)


if __name__ == "__main__":
    # Default polling interval: 10 seconds
    # TODO: Make this configurable via CLI arg (argparse)
    run_monitor(interval=10)
