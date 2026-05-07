# Incident: Facebook BGP Misconfiguration — 6 Hours of Total Outage
# Date: 2021-10-04
# Severity: P0
# Service: facebook-backbone

> **Source:** [Facebook Engineering Blog](https://engineering.fb.com/2021/10/04/networking-traffic/outage-details/)
> A routine BGP configuration change disconnected Facebook's data centers from the internet. Facebook, Instagram, WhatsApp, and Messenger were completely unreachable for approximately 6 hours. Engineers couldn't even access the data centers remotely because internal tools also relied on the failed DNS infrastructure.

## What Happened

During a routine maintenance operation on the backbone network, a command
was issued to assess the capacity of Facebook's global backbone. This
command unintentionally took down all connections in the backbone network,
disconnecting Facebook's data centers globally.

The DNS servers, being unable to reach the backbone, withdrew their BGP
route announcements. This made Facebook's DNS unreachable, which made
every Facebook property unreachable.

Engineers had to physically travel to data centers to fix the issue because
remote access tools were also affected by the outage.

## Root Cause

1. Configuration change tool did not verify the impact before execution.
2. The audit tool that should have caught the bad config had a bug.
3. No staged rollout — change went global immediately.
4. No out-of-band access path existed for recovery.

## What Graveyard Would Have Caught

```graveyard
# Never deploy network changes on Monday (start-of-week = max blast radius)
- type: deploy_window
  block_days: monday

# Verify all core dependencies before config changes
- type: dependency
  url: https://dns-primary.internal/health
  name: Primary DNS Infrastructure

- type: dependency
  url: https://backbone-monitor.internal/status
  name: Backbone Network Monitor

# Enforce minimum replicas for rollback capability
- type: min_replicas
  value: 3

# Block unscanned changes
- type: security_scan
  required: true
  block_on: CRITICAL
```
