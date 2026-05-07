# Famous Incidents — Reconstructions with Deploy Rules

This directory contains reconstructions of well-known public software incidents, each accompanied by the Graveyard Deploy Rules that *would have prevented them*.

These exist for three reasons:
1. **Inspiration** — see how to write Deploy Rules that capture the lessons of an incident
2. **Onboarding** — drop one into your `incidents/` directory to see Graveyard in action immediately
3. **Education** — every entry links to the original public postmortem so you can read the full story

---

## Index

| Incident | Year | Cost / Impact | What Graveyard Catches |
|---|---|---|---|
| [Knight Capital — $460M in 45 minutes](./famous-incidents/knight-capital-2012.md) | 2012 | $460M loss, company acquired | Replica consistency, dead-code flag detection |
| [GitLab — `rm -rf` on production DB](./famous-incidents/gitlab-db-deletion-2017.md) | 2017 | 6 hrs of data lost, 18 hr outage | After-hours deploy block, backup-service health |
| [AWS S3 — A typo took down half the internet](./famous-incidents/aws-s3-outage-2017.md) | 2017 | 4 hrs of S3 us-east-1 down | Min-replica enforcement, dependency health |
| [Cloudflare — Regex CPU exhaustion](./famous-incidents/cloudflare-regex-2019.md) | 2019 | 27 min global outage | Test pass rate, security review gate |
| [Facebook — BGP misconfiguration](./famous-incidents/facebook-bgp-2021.md) | 2021 | 6 hrs of FB/IG/WhatsApp down | Deploy-window block, DNS dependency check |
| [Atlassian — 14-day outage](./famous-incidents/atlassian-outage-2022.md) | 2022 | 400 customers locked out for up to 14 days | Friday deploy block, backup verification |

---

## How to use these

```bash
# Try one out — copy it into your incidents/ directory
cp examples/famous-incidents/gitlab-db-deletion-2017.md incidents/

# See the rules light up
graveyard validate
graveyard check --tests ./test-results/
```

---

## Contributing a new incident

We love contributions. If you know of a public postmortem that would make a great Graveyard example:

1. Add a new `.md` file to `famous-incidents/` following the existing format
2. Always link to the original public postmortem source
3. Include a `## What Graveyard Would Have Caught` section with a fenced ` ```graveyard ` block
4. Submit a PR — see [../CONTRIBUTING.md](../CONTRIBUTING.md)

The best incident reconstructions teach a transferable lesson, not just a one-off failure.
