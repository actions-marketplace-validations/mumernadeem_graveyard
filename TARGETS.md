# Graveyard — Build Targets (OSS)

> **Tagline:** "Turn your past incidents into unbreakable deploy gates."

## Targets

### ✅ Target 1: Core CLI skeleton (`graveyard check`)
- Argparse-based CLI with subcommands
- Colored terminal output with pass/fail/skip/warn statuses
- JSON output mode (`--output json`)

### ✅ Target 2: Configuration file (`.graveyard.yml`)
- Zero-dependency YAML parser
- Deep-merge with defaults
- Per-check enable/disable and thresholds

### ✅ Target 3: Test Results Check (JUnit XML)
- Parse JUnit XML files
- Enforce configurable pass-rate threshold

### ✅ Target 4: Security Scan Check (Trivy)
- Shell out to Trivy binary
- Parse JSON output, enforce severity thresholds

### ✅ Target 5: K8s Manifest Validation
- Regex-based deployment YAML validation
- Check resource limits, probes, replica counts, image tags

### ✅ Target 6: Dependency Health Check
- HTTP ping configured URLs with latency measurement
- Configurable timeout and warn thresholds

### ✅ Target 7: Cost Estimation Check
- Parse K8s resource requests
- Calculate monthly costs using provider presets (AWS/GCP/Azure/Hetzner/DO/Linode)
- Support user-provided per-node pricing

### ✅ Target 8: Incident-Trained Deploy Gates
- Parse postmortem markdown files from `incidents/`
- Extract deploy rules from fenced `graveyard` code blocks
- Enforce deploy windows, dependency requirements, pass rate overrides
- Override baseline config with incident-learned policies

### ✅ Target 9: Deploy Decision Records (DDR)
- Generate immutable Markdown audit trail per deploy attempt
- Capture git commit, branch, user, all check results
- List all incident-trained policies enforced

### ✅ Target 10: `graveyard demo` command
- Single command that demonstrates the full pipeline
- Uses built-in sample data, zero setup required

### ✅ Target 11: `graveyard init` command
- Detects project structure (Python, Node, K8s, CI)
- Generates starter `.graveyard.yml`
- Creates `incidents/` directory with postmortem template

### ✅ Target 12: `graveyard validate` command
- Lints `.graveyard.yml` for errors
- Validates incident files for unknown rule types and typos

### ✅ Target 13: Famous Incidents Library
- 6 reconstructed real-world public postmortems with Deploy Rules
- Knight Capital, GitLab, Cloudflare, AWS S3, Facebook, Atlassian

### ✅ Target 14: Pytest Suite
- 30+ tests covering parser, rule enforcement, DDR, config
- CI-ready with GitHub Actions workflow

### ✅ Target 15: Community & Launch Assets
- CONTRIBUTING.md, CODE_OF_CONDUCT.md, ISSUE_TEMPLATEs
- README comparison table vs competitors
- Docker image, GitHub Action
