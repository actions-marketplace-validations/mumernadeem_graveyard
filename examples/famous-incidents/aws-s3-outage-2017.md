# Incident: AWS S3 Outage — A Typo Took Down Half the Internet
# Date: 2017-02-28
# Severity: P0
# Service: aws-s3-us-east-1

> **Source:** [AWS Post-Event Summary](https://aws.amazon.com/message/41926/)
> An authorized S3 team member executed a command to remove a small number of servers during a debugging exercise. The command was entered incorrectly, removing a larger set of servers than intended. This took down S3 in us-east-1 for ~4 hours, cascading to hundreds of major websites and services.

## What Happened

During routine debugging of the S3 billing system, an engineer ran a
playbook command to take a small number of servers offline. A typo in
the command input caused a much larger set of servers to be removed,
including the S3 index and placement subsystems.

The cascading failure took 4+ hours to resolve because the S3 subsystems
hadn't been fully restarted in years and the restart process itself was
slow due to the massive scale.

Affected services: Slack, Trello, Quora, IFTTT, Business Insider,
Docker Registry, and thousands of others hosted on or backed by S3.

## Root Cause

1. Manual command execution without guardrails.
2. No input validation on the blast radius of the command.
3. Subsystem restart procedures were untested at scale.
4. No canary/staged approach to infrastructure changes.

## What Graveyard Would Have Caught

```graveyard
# Enforce minimum replicas — single-server changes are high risk
- type: min_replicas
  value: 5

# Block deploys without passing all tests
- type: min_pass_rate
  value: 100

# Verify core dependencies before making changes
- type: dependency
  url: https://s3-index.internal/health
  name: S3 Index Subsystem

- type: dependency
  url: https://s3-placement.internal/health
  name: S3 Placement Subsystem
```
