# Incident: Atlassian 14-Day Outage — 400 Companies Locked Out
# Date: 2022-04-05
# Severity: P0
# Service: atlassian-cloud

> **Source:** [Atlassian Incident Post](https://www.atlassian.com/engineering/april-2022-outage-update)
> A maintenance script intended to deactivate a legacy app accidentally deleted the entire cloud sites of approximately 400 Atlassian customers. Full restoration took 14 days due to the complexity of the multi-tenant architecture.

## What Happened

Atlassian was decommissioning a standalone legacy app ("Insight Asset
Management") that had been integrated into Jira Service Management.
A script was written to deactivate the legacy app instances.

Due to a communication gap between teams, the script was provided with
the wrong list of IDs — site IDs instead of app IDs. The script then
deleted 883 entire Atlassian cloud sites (Jira, Confluence, OpsGenie,
Statuspage) belonging to approximately 400 customers.

Restoration required rebuilding each site individually from backups.
Some customers were offline for up to 14 days.

## Root Cause

1. The deletion script accepted raw IDs without type validation.
2. No dry-run or preview step before execution.
3. No blast radius check ("this will delete 883 items" should have raised alarms).
4. Cross-team handoff of IDs had no verification step.

## What Graveyard Would Have Caught

```graveyard
# Block deploys/scripts on Fridays and after hours
- type: deploy_window
  block_days: friday
  block_after: "15:00"

# Enforce 100% test pass rate for destructive operations
- type: min_pass_rate
  value: 100

# Verify backup service is healthy before destructive ops
- type: dependency
  url: https://backup-restore.internal/health
  name: Backup & Restore Service

# Verify the target service is in expected state
- type: dependency
  url: https://site-registry.internal/count
  name: Site Registry Service
```
