# IOC Extraction Workflow

**Quick malware triage using Indicators of Compromise.**

## Overview

Extract network indicators and suspicious APIs without full deobfuscation. Perfect for:
- Incident response
- Malware triage
- Quick threat assessment

## Prerequisites

```bash
npm i @babel/parser @babel/traverse
```

## Workflow Steps

### Step 1: Static IOC Sweep (2-5 minutes)

```bash
# Quick check
node examples/tools/extract_iocs.mjs sample.js

# Review results
cat iocs.json | jq '.'
```

### Step 2: Behavioral Assessment (2-3 minutes)

```bash
# Count indicators
jq '.indicators | keys | length' iocs.json

# Check threat level
jq '.threat_level' iocs.json
```

### Step 3: Generate Blocking Rules (2-5 minutes)

```bash
# Extract domains
jq -r '.indicators.domains[]' iocs.json > domains.txt

# Generate iptables rules
while read domain; do
  echo "iptables -A OUTPUT -d $domain -j DROP"
done < domains.txt > firewall_rules.txt
```

## Time Estimate: 5-15 minutes

## Deliverables

- iocs.json - Structured IOCs
- threat_assessment.txt - Threat level
- firewall_rules.txt - Blocking rules

## References

- [IOC Standards](../references/ioc-standards.md)
- [MITRE ATT&CK](https://attack.mitre.org/)
