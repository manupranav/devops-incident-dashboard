# devops-incident-dashboard

A lightweight DevOps incident monitoring and alerting toolkit for on-call engineers.

> **Status:** Active development — not production-ready yet. See TODOs throughout.

---

## What This Does

This toolkit monitors system health metrics (CPU, memory, disk) against configurable thresholds and dispatches alerts via log files and simulated Slack/PagerDuty notifications.

```
monitor.py  →  checks metrics  →  breaches threshold?
                                        ↓ yes
                              alert.sh  →  logs/alerts.log
                                        →  Slack #ops-alerts
                                        →  PagerDuty (CRITICAL only)
```

---

## Project Structure

```
devops-incident-dashboard/
├── monitor.py              # Main health monitoring script
├── alert.sh                # Alert dispatcher (Slack + PagerDuty simulation)
├── config/
│   └── thresholds.yaml     # Configurable alert thresholds
├── docs/
│   └── runbook.md          # Incident response runbook
├── logs/                   # Runtime logs (git-ignored)
│   ├── monitor.log
│   └── alerts.log
├── .gitignore
├── README.md
├── TASKS.md                # Git learning tasks (hands-on exercises)
└── NOTES.md                # Git reference notes for DevOps interviews
```

---

## Quick Start

### Prerequisites
- Python 3.8+
- `pyyaml` installed: `pip install pyyaml`
- Bash (Git Bash on Windows, or WSL)

### Run the Monitor

```bash
# Clone the repo
git clone https://github.com/YOURUSERNAME/devops-incident-dashboard.git
cd devops-incident-dashboard

# Install dependencies
pip install pyyaml

# Start monitoring (polls every 10 seconds)
python3 monitor.py
```

### Test Alert Dispatch

```bash
# Make script executable
chmod +x alert.sh

# Test a WARNING alert
./alert.sh WARNING CPU 82.5 75

# Test a CRITICAL alert
./alert.sh CRITICAL Memory 93.1 90
```

---

## Configuration

Edit `config/thresholds.yaml` to adjust alert thresholds:

```yaml
thresholds:
  cpu_warning: 75
  cpu_critical: 90
  memory_warning: 80
  memory_critical: 90
  disk_warning: 75
  disk_critical: 90
```

---

## Logs

All logs are written to the `logs/` directory (excluded from Git via `.gitignore`):

| File | Contents |
|------|----------|
| `logs/monitor.log` | Timestamped metric readings |
| `logs/alerts.log` | All dispatched alerts |

---

## Roadmap

- [ ] Replace simulated metrics with real `psutil` calls
- [ ] Add real Slack webhook integration
- [ ] Add PagerDuty Events API v2 integration
- [ ] Add network I/O monitoring
- [ ] Add per-host threshold overrides
- [ ] Set up as systemd service
- [ ] Add alert deduplication (cooldown window)
- [ ] Add Grafana dashboard export

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## License

MIT — see LICENSE (TODO: add LICENSE file)
