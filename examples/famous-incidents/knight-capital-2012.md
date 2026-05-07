# Incident: Knight Capital — $460M Loss in 45 Minutes
# Date: 2012-08-01
# Severity: P0
# Service: trading-platform

> **Source:** [SEC Filing](https://www.sec.gov/litigation/admin/2013/34-70694.pdf)
> Knight Capital deployed untested code that reactivated a defunct trading strategy, executing 4 million trades in 45 minutes. The company lost $460 million and was acquired within days.

## What Happened

On August 1, 2012, Knight Capital deployed new software to its production
trading servers to support a NYSE Retail Liquidity Provider (RLP) program.
A technician failed to deploy the new code to one of eight servers. That
server still had old code referencing a repurposed flag, which inadvertently
activated a defunct high-frequency trading function called "Power Peg."

The rogue algorithm bought high and sold low across 154 stocks for 45
minutes before it was identified and killed. Total loss: $460 million —
enough to bankrupt the company.

## Root Cause

1. Deployment was manual — no automated verification that all servers got the same version.
2. A dead code flag was reused instead of removed.
3. No pre-deploy smoke test verified the trading behavior was expected.
4. No kill switch or circuit breaker existed.

## What Graveyard Would Have Caught

```graveyard
# Require 100% test pass rate for financial services
- type: min_pass_rate
  value: 100

# Block deploys without security scan (dead code = attack surface)
- type: security_scan
  required: true
  block_on: CRITICAL

# Ensure all replicas are consistent (the 1-of-8 problem)
- type: min_replicas
  value: 8

# Block :latest tag to prevent version drift
- type: image_tag
  block_latest: true
```
