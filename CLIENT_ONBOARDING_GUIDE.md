# 🚀 Graveyard — Complete Onboarding & Deployment Guide

Welcome! This guide walks you through implementing **Incident-Trained Deploy Gates** in your team's CI/CD pipeline using Graveyard.

Graveyard runs as the final gate before a deploy reaches production. It reads your incident postmortems, evaluates your test results, scans your K8s manifests, estimates cloud cost impact, and decides: **GO**, **CAUTION**, or **BLOCK**.

---

## 🗺️ The 4-Phase Roadmap

1. **[Phase 1](#-phase-1-configuration--incident-writing)** — Configure Graveyard and write your first postmortem rules
2. **[Phase 2](#-phase-2-running--testing-locally)** — Test locally before pipeline integration
3. **[Phase 3](#-phase-3-deploying-into-your-cicd-pipeline)** — Wire it into GitHub Actions or GitLab CI
4. **[Phase 4](#-phase-4-reviewing-the-audit-trail-ddr)** — Review the Deploy Decision Record audit trail

---

## 🟢 Phase 1: Configuration & Incident Writing

### 1.1 Initialize the project (recommended)

The fastest way to get started is `graveyard init` — it auto-detects your stack and writes a sensible `.graveyard.yml`:

```bash
graveyard init
```

You'll see something like:

```
🪦 Graveyard Init

  ✓ Detected: Python project (pytest)
  ✓ Detected: K8s manifests in ./k8s/
  ✓ Detected: GitHub Actions
  ✓ Detected: Dockerfile
  ✓ Wrote .graveyard.yml
  ✓ Created incidents/ with postmortem template
  ✓ Created deploy-records/ (audit trail)
```

### 1.2 Customize `.graveyard.yml`

Open the generated file and tune the thresholds:

```yaml
project: "my-production-app"
environment: "production"

checks:
  tests:
    enabled: true
    min_pass_rate: 90        # Block deploys if <90% of tests pass

  security:
    enabled: true
    block_on: CRITICAL       # Block on any CRITICAL CVE
    max_high: 5              # Allow up to 5 HIGH-severity findings

  k8s:
    enabled: true
    namespace: "production"
    require_limits: true
    require_probes: true
    min_replicas: 3

  cost:
    enabled: true
    warn_threshold: 200      # Warn if estimated +$200/mo
    provider: aws            # aws | gcp | azure | hetzner | digitalocean | linode
```

### 1.3 Write your first postmortem with Deploy Rules

Graveyard's superpower is learning from past incidents. Create a markdown file in `incidents/` after every real incident, and end it with a fenced ` ```graveyard ` block:

````markdown
# Incident: Friday Cache Stampede
# Date: 2025-06-20
# Severity: P1
# Service: user-api

## What Happened
We deployed user-api at 5pm Friday. The new cache key format invalidated all
existing sessions, causing 50K concurrent DB queries and a cascading outage.

## Root Cause
Cache migration was not backward-compatible.

## What We Should Have Checked
- Never deploy after 16:00 UTC on Fridays
- Redis must be reachable before any deploy of user-api

## Deploy Rules

```graveyard
- type: deploy_window
  block_days: friday
  block_after: "16:00"

- type: dependency
  url: https://redis-health.internal/ping
  name: Redis Cache Health
```
````

> **Important:** rules must live in a fenced ` ```graveyard ` code block. This is what makes them machine-readable. The rest of the postmortem is for humans.

### 1.4 Validate your incident files

Before running checks, lint everything:

```bash
graveyard validate
```

This catches typos, unknown rule types, and malformed values *before* they silently break a deploy gate.

---

## 🐳 Phase 2: Running & Testing Locally

### Option A — Run the script directly

```bash
graveyard check \
  --config .graveyard.yml \
  --tests ./test-results/ \
  --k8s-dir ./k8s/ \
  --image my-app:dev
```

### Option B — Run via Docker

```bash
docker run --rm \
  -v $(pwd):/project \
  -w /project \
  ghcr.io/mumernadeem/graveyard:latest check \
  --config /project/.graveyard.yml \
  --tests /project/test-results/ \
  --k8s-dir /project/k8s/
```

### What you'll see

- If today is **Friday after 4pm** and you have the cache-stampede incident above, Graveyard will **BLOCK** the deploy citing that exact rule and incident as the source.
- If your K8s manifest is missing CPU limits, it will **BLOCK**.
- If everything is fine, you'll see **✅ GO FOR DEPLOYMENT**.

### Try the built-in demo

Want to see all this without configuring anything?

```bash
graveyard demo
```

Loads sample incidents and a deliberately bad K8s manifest, runs the full pipeline, and shows the BLOCK decision in 30 seconds.

---

## ⚙️ Phase 3: Deploying into your CI/CD Pipeline

Graveyard runs as a **gate** — after your tests + container build, but before your `kubectl apply` / `helm upgrade` step.

### GitHub Actions

```yaml
deploy-check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    # ... your test + build steps that produce JUnit XML in ./test-results/ ...

    - name: Run Graveyard Deploy Gates
      uses: mumernadeem/graveyard@main
      with:
        config: .graveyard.yml
        tests: test-results/
        k8s-dir: k8s/
        image: my-app:${{ github.sha }}
```

The action automatically uploads `deploy-records/` as an artifact (`name: deploy-records`) for 90 days — your auditors will love it.

### GitLab CI

```yaml
include:
  - remote: 'https://raw.githubusercontent.com/mumernadeem/graveyard/main/gitlab-ci-template.yml'

graveyard_deploy_check:
  inputs:
    tests: test-results/
    k8s_dir: k8s/
    image: my-app:$CI_COMMIT_SHA
```

DDR artifacts are saved automatically with a 90-day retention.

### Anywhere else (raw script)

```bash
curl -sSL https://raw.githubusercontent.com/mumernadeem/graveyard/main/src/cli/graveyard.py -o graveyard.py
python3 graveyard.py check --tests ./results --k8s-dir ./k8s --output json
```

`--output json` is machine-readable. Exit code is non-zero on BLOCK so any pipeline halts automatically.

---

## 📜 Phase 4: Reviewing the Audit Trail (DDR)

Every `graveyard check` writes a **Deploy Decision Record** to `deploy-records/`.

```markdown
# Deploy Decision Record: my-production-app → production

## 📝 Metadata
- **Date:** 2026-05-01T14:00:00Z
- **Decision:** `BLOCK`
- **Triggered By:** ci-runner@github
- **Commit:** `8f2a1b9` (Branch: `main`)

## 🛡️ Checks Executed
| Check | Status | Details |
|---|---|---|
| Tests | ✅ PASS | 412/412 passed (100% — threshold: 90%) |
| Security | ✅ PASS | 0 Critical, 1 Medium |
| K8s Config | ❌ FAIL | Missing resource limits in user-api |

## 🧠 Incident-Trained Policies Enforced
| Policy | Source | Severity | Result |
|---|---|---|---|
| Check dependency: Redis Cache Health | Friday Cache Stampede | P2 | ❌ |
```

These are immutable plain Markdown — commit them to git, upload as CI artifacts, or pipe them into your SOC 2 / ISO 27001 evidence pipeline.

---

## 🆘 Troubleshooting

| Problem | Fix |
|---|---|
| `graveyard validate` says "no Deploy Rules found" | Make sure your rules are inside a fenced ` ```graveyard ` block, not just a `## Deploy Rules` heading |
| Trivy security check skips | Install Trivy on the runner: `curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \| sh -s -- -b /usr/local/bin` |
| Deploy-window rule doesn't trigger | Check timezone — Graveyard uses the runner's local timezone unless you specify `timezone: UTC` in the rule |
| Pipeline fails but I want to know why | Check the DDR file in `deploy-records/` — it lists every rule that fired and the exact incident source |

---

## 📚 Further Reading

- [README](README.md) — overview, install, comparison vs OPA/Checkov/Trivy
- [Examples: Famous Incidents](examples/) — real-world postmortems with Deploy Rules
- [Contributing](CONTRIBUTING.md) — add new rule types, fix bugs, contribute incidents
