# Contributing to Graveyard

Thank you for your interest in contributing! Graveyard is an open-source project and we welcome contributions of all kinds.

## Quick Start

```bash
git clone https://github.com/mumernadeem/graveyard.git
cd graveyard

# Run the CLI directly (zero dependencies)
python3 src/cli/graveyard.py demo

# Run the test suite
pip install pytest
pytest tests/unit/ -v
```

## How to Contribute

### 🐛 Bug Reports
Open an issue using the Bug Report template. Include:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your Python version (`python3 --version`)

### 💡 Feature Requests
Open an issue using the Feature Request template. We especially welcome:
- New incident rule types
- Support for new CI/CD platforms
- Postmortem format improvements

### 📝 New Incident Reconstructions
We love contributions to `examples/famous-incidents/`. If you know of a public postmortem that would make a great Graveyard example:
1. Create a new `.md` file following the existing format
2. Link to the original public postmortem
3. Write the `## Deploy Rules` section with rules that would have caught it

### 🔧 Code Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest tests/unit/ -v`)
5. Submit a Pull Request

## Code Style
- Python 3.9+ compatible
- Standard library only in `src/cli/` (zero production dependencies)
- `pytest` is the only dev dependency
- Use docstrings on all public functions

## Architecture
```
src/cli/
├── graveyard.py      # CLI entrypoint, argparse, display logic
├── config.py         # .graveyard.yml loader
├── ddr_writer.py     # Deploy Decision Record generator
└── checks/           # Each check is a standalone module
    ├── incident_check.py    # The differentiator
    ├── test_check.py        # JUnit XML parsing
    ├── security_check.py    # Trivy integration
    ├── k8s_check.py         # K8s manifest validation
    ├── dependency_check.py  # HTTP health pings
    └── cost_check.py        # Cloud cost estimation
```

Each check module exports a `run_*_check()` function that returns:
```python
{"status": "PASS|FAIL|WARN|SKIP", "message": "Human-readable details"}
```
