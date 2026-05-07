# Incident: GitLab Database Deletion — 300GB of Production Data Lost
# Date: 2017-01-31
# Severity: P0
# Service: gitlab-production-db

> **Source:** [GitLab Postmortem (public)](https://about.gitlab.com/blog/2017/02/01/gitlab-dot-com-database-incident/)
> An engineer ran `rm -rf` on a production database directory during a late-night maintenance window. 300GB of data was lost. Recovery took 18 hours.

## What Happened

During an incident involving database replication lag, a GitLab engineer
attempted to fix the issue by deleting the PostgreSQL data directory on
what they believed was a staging server. It was production.

The backup systems had multiple failures:
- LVM snapshots were never configured
- Regular pg_dump backups hadn't been tested — and were partially broken
- Azure disk snapshots were enabled but ~6 hours old

GitLab lost approximately 6 hours of production data and was down for 18 hours.

## Root Cause

1. Late-night manual operations on production infrastructure.
2. No safeguard against destructive commands on production.
3. Backup verification was never automated.
4. Exhausted engineer working past midnight.

## What Graveyard Would Have Caught

```graveyard
# Never deploy or run maintenance after business hours
- type: deploy_window
  block_days: monday, tuesday, wednesday, thursday, friday
  block_after: "20:00"

# Never deploy on weekends (tired engineers make mistakes)
- type: deploy_window
  block_days: saturday, sunday

# Verify database is healthy and reachable before any deploy
- type: dependency
  url: https://db-primary.internal:5432/health
  name: Production PostgreSQL

# Verify backup service is operational
- type: dependency
  url: https://backup-service.internal/status
  name: Backup Verification Service
```
