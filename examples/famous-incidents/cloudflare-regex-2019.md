# Incident: Cloudflare Regex Outage — 30 Minutes of Global Downtime
# Date: 2019-07-02
# Severity: P0
# Service: cloudflare-waf

> **Source:** [Cloudflare Blog Post](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)
> A single poorly-written regular expression in a WAF rule update caused CPU exhaustion across every Cloudflare edge server worldwide. Global outage lasted 27 minutes.

## What Happened

A routine WAF rule deployment included a regular expression with
catastrophic backtracking: `(?:(?:\"|'|\]|\}|\\|\d|(?:nan|infinity|true|false|null|undefined|symbol|math)|\`|\-|\+)+[)]*;?((?:\s|-|~|!|{}|\|\||\+)*.*(?:.*=.*)))`.

When this rule was deployed globally, every Cloudflare edge server's
CPU spiked to 100%. HTTP/HTTPS proxy, CDN, and DDoS protection for
millions of websites went offline simultaneously.

## Root Cause

1. WAF rules were deployed globally without canary testing.
2. No CPU usage gate existed for rule validation.
3. No staged rollout (deploy to 1% → 10% → 100% of edge).
4. The regex was not tested against a corpus of real traffic.

## What Graveyard Would Have Caught

```graveyard
# Test pass rate must be 100% for infrastructure-level changes
- type: min_pass_rate
  value: 100

# Block deploys without thorough security review
- type: security_scan
  required: true
  block_on: CRITICAL
  max_high: 0

# Minimum replicas to ensure canary capability
- type: min_replicas
  value: 3
```
