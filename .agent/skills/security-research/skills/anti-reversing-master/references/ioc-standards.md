# IOC Standards & Formats

## Overview

Learn how to format, share, and use Indicators of Compromise (IOCs) in standard formats for threat intelligence sharing and automated blocking.

## Standard IOC Formats

### 1. STIX 2.1 (Structured Threat Information Expression)

**Use case**: Structured threat intelligence sharing between platforms

**Example - Malware IOCs**:
```json
{
  "type": "malware",
  "spec_version": "2.1",
  "id": "malware--f0fcd9a2-5f2f-4070-b0e9-0b8e6b5e8c2d",
  "created": "2026-01-12T00:00:00Z",
  "modified": "2026-01-12T00:00:00Z",
  "name": "JSBackdoor.Trojan",
  "description": "JavaScript-based backdoor with C2 communication",
  "pattern": "[file:name = '*.js' AND (file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e' OR file:hashes.SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')]",
  "labels": ["trojan", "backdoor"],
  "pattern_type": "stix",
  "valid_from": "2026-01-12T00:00:00Z"
}
```

**Example - Network IOCs**:
```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--a6f2e3b4-5c6d-7e8f-9a0b-1c2d3e4f5678",
  "created": "2026-01-12T00:00:00Z",
  "modified": "2026-01-12T00:00:00Z",
  "name": "Malicious C2 Domain",
  "description": "C2 communication endpoint for JSBackdoor",
  "pattern": "[domain-name:value = 'evil-c2.com']",
  "labels": ["malicious-activity", "c2"],
  "valid_from": "2026-01-12T00:00:00Z"
}
```

**Example - Complete IOC Package**:
```json
{
  "type": "bundle",
  "id": "bundle--a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "spec_version": "2.1",
  "objects": [
    {
      "type": "malware",
      "id": "malware--f0fcd9a2-5f2f-4070-b0e9-0b8e6b5e8c2d",
      "name": "JSBackdoor.Trojan",
      "labels": ["trojan"]
    },
    {
      "type": "indicator",
      "id": "indicator--a6f2e3b4-5c6d-7e8f-9a0b-1c2d3e4f5678",
      "pattern": "[domain-name:value = 'evil-c2.com']",
      "labels": ["malicious-activity"]
    }
  ]
}
```

**Benefits**:
- Interoperable across platforms (MISP, OpenCTI, ThreatConnect)
- Rich metadata and context
- Temporal validity (valid_from, valid_until)
- Relationship mapping (malware → indicators → observables)

**Tools for STIX**:
- Python: `stix2` library
- JavaScript: `stix2` library
- Online: STIX-shifter, OpenCTI

---

### 2. YARA (Signature-based Detection)

**Use case**: Endpoint detection, file scanning, malware families

**Example - JavaScript Obfuscation**:
```yara
rule Obfuscated_JavaScript_Malware {
    meta:
        description = "Detects obfuscated JavaScript malware"
        author = "Your Name"
        date = "2026-01-12"
        hash1 = "d41d8cd98f00b204e9800998ecf8427e"

    strings:
        $hex_array = { 5A ?? ?? ?? ?? ?? ?? ?? ?? 2C }
        $eval_func = "eval("
        $jsfuck_pattern = /\[\]\(!\[\]\+\[\]\)\[\+\[\]\]/
        $suspicious_domains = /https?:\/\/[a-z0-9.-]+\.(tk|ml|cf|ga)/

    condition:
        uint16(0) == 0x6A21 and (
            $hex_array and $eval_func
        ) or (
            #jsfuck_pattern > 10 and $suspicious_domains
        )
}
```

**Example - C2 Communication**:
```yara
rule JSBackdoor_C2_Communication {
    meta:
        description = "Detects JavaScript backdoor C2 communication"
        author = "Your Name"

    strings:
        $beacon = "navigator.sendBeacon"
        $post_data = "XMLHttpRequest"
        $domain1 = "evil-c2.com"
        $domain2 = "backup-c2.net"

    condition:
        any of them
}
```

**Benefits**:
- Fast signature-based matching
- Widely supported (YARA-L for Lima, Enterprise products)
- Flexible pattern matching
- Good for file-based detection

**Tools**:
- YARA command-line tool
- Virustotal Intelligence
- Enterprise EDR platforms

---

### 3. OpenIOC (Open Indicators of Compromise)

**Use case**: XML format for incident response and SIEM integration

**Example**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<OpenIOC id="a1b2c3d4-e5f6-7890-abcd-ef1234567890" last-modified="2026-01-12T00:00:00Z">
    <metadata>
        <short_description>JSBackdoor.Trojan</short_description>
        <description>JavaScript-based backdoor malware</description>
        <authored_by>Your Name</authored_by>
        <authored_date>2026-01-12</authored_date>
    </metadata>

    <criteria>
        <Indicator operator="OR">
            <IndicatorItem condition="is">
                <Content type="string">d41d8cd98f00b204e9800998ecf8427e</Content>
                <SearchKey>FileItem/Md5sum</SearchKey>
            </IndicatorItem>

            <IndicatorItem condition="contains">
                <Content type="string">eval(</Content>
                <SearchKey>FileItem/RecordSection/Record/Field[@name="content"]</SearchKey>
            </IndicatorItem>

            <IndicatorItem condition="is">
                <Content type="string">evil-c2.com</Content>
                <SearchKey>Network/DNSEntryItem/RecordName</SearchKey>
            </IndicatorItem>
        </Indicator>
    </criteria>
</OpenIOC>
```

**Benefits**:
- XML format (human-readable)
- Widely supported in incident response tools
- Flexible criteria structure

---

### 4. Plain JSON (Simple & Automation-Friendly)

**Use case**: Quick sharing, script integration, simple automation

**Example**:
```json
{
  "metadata": {
    "tool": "js-malware-triage-iocs",
    "timestamp": "2026-01-12T00:00:00Z",
    "source": "suspicious-sample.js"
  },
  "indicators": {
    "domains": [
      "evil-c2.com",
      "backup-c2.net"
    ],
    "urls": [
      "https://evil-c2.com/beacon",
      "http://backup-c2.net/data"
    ],
    "ipv4_addresses": [
      "192.0.2.1",
      "198.51.100.2"
    ],
    "file_hashes": {
      "md5": "d41d8cd98f00b204e9800998ecf8427e",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    "suspicious_apis": [
      "network: fetch",
      "crypto: crypto.subtle",
      "storage: localStorage"
    ]
  },
  "threat_level": "HIGH",
  "confidence": "HIGH",
  "tags": ["trojan", "backdoor", "c2"]
}
```

**Benefits**:
- Simple to parse
- Easy to generate
- Good for scripts and automation
- No special tooling required

---

## Format Selection Guide

| Format | Best For | Pros | Cons |
|--------|----------|------|------|
| **STIX 2.1** | Threat intel sharing, enterprise | Rich metadata, interoperable | Complex, requires tooling |
| **YARA** | Endpoint detection, file scanning | Fast, widely supported | File-focused, limited network |
| **OpenIOC** | Incident response, SIEM | XML, flexible | Verbose, less common now |
| **Plain JSON** | Automation, quick sharing | Simple, flexible | No standardization |

## Blocking Rules Generation

### Firewall Rules

**iptables**:
```bash
# Block domains
iptables -A OUTPUT -d evil-c2.com -j DROP
iptables -A OUTPUT -d backup-c2.net -j DROP

# Block IPs
iptables -A OUTPUT -d 192.0.2.1 -j DROP
iptables -A OUTPUT -d 198.51.100.2 -j DROP
```

**Windows Firewall**:
```powershell
# Block domain
New-NetFirewallRule -DisplayName "Block Evil C2" -Direction Outbound -Action Block -RemoteAddress evil-c2.com

# Block IP
New-NetFirewallRule -DisplayName "Block IP 192.0.2.1" -Direction Outbound -Action Block -RemoteAddress 192.0.2.1
```

### WAF Rules

**Cloudflare**:
```javascript
// Block specific URLs
if (http.request.uri.path contains "/beacon") {
  block("Malicious C2 beacon")
}

// Block domains
if (http.request.host contains "evil-c2.com") {
  block("Known malicious domain")
}
```

**ModSecurity**:
```apache
SecRule REQUEST_HEADERS:Host "@contains evil-c2.com" \
    "id:1001,\
    phase:1,\
    deny,\
    msg:'Blocked malicious domain'"
```

## Sharing IOCs

### Automated Sharing

**MISP (Malware Information Sharing Platform)**:
```python
import pymisp

misp = pymisp.PyMISP('https://misp.example.com', 'API_KEY', False)

# Create event
event = misp.new_event(
    info='JSBackdoor.Trojan IOCs',
    threat_level_id=2,  # High
    analysis=1  # Ongoing analysis
)

# Add attributes
misp.add_attribute(event, {
    'category': 'Network activity',
    'type': 'domain',
    'value': 'evil-c2.com'
})

misp.add_attribute(event, {
    'category': 'Artifacts dropped',
    'type': 'md5',
    'value': 'd41d8cd98f00b204e9800998ecf8427e'
})
```

**ThreatConnect**:
```python
import threatconnect as tc

tc_api = tc.ThreatConnect(app_id='YOUR_APP_ID',
                          access_id='YOUR_ACCESS_ID',
                          secret_key='YOUR_SECRET_KEY')

# Create group
indicators = tc_api.indicators()

# Add domain
indicator = indicators.add('evil-c1.com', tc.OwnerEnum.CUSTOM)
indicator.add_tag('malicious')
indicator.upload()
```

### Manual Sharing

**Cybersecurity Infrastructure Security Agency (CISA)**:
- Submit via: https://www.us-cert.gov/forms/report
- Use STIX 2.1 format
- Include context and attribution

**VirusTotal Intelligence**:
- Upload IOCs as collections
- Share with community
- Tag for easy discovery

**AlienVault OTX**:
- Create pulse with IOCs
- Subscribe to relevant pulses
- Exchange with community

## IOC Lifecycle Management

### 1. Discovery
- Extract from malware analysis
- Validate in sandbox
- Tag with confidence level

### 2. Sharing
- Choose appropriate format
- Add context and metadata
- Share with relevant communities

### 3. Maintenance
- Monitor for validity
- Update confidence levels
- Remove outdated IOCs

### 4. Validation
- Test in detection tools
- Monitor false positive rates
- Gather feedback from community

## Best Practices

### Do's
✅ **Add context**: Include malware family, attribution, TTPs
✅ **Validate before sharing**: Test in sandbox, check false positives
✅ **Use standard formats**: STIX 2.1 for sharing, YARA for detection
✅ **Include timestamps**: When discovered, valid from/until
✅ **Tag appropriately**: Malware family, attack type, confidence

### Don'ts
❌ **Don't overshare**: Protect sensitive details, follow need-to-know
❌ **Don't share without validation**: Test to reduce false positives
❌ **Don't forget updates**: Keep IOCs current, remove invalid ones
❌ **Don't ignore attribution**: Credit original discoverer
❌ **Don't share private data**: No customer PII, internal details

## References

- **STIX 2.1 Specification**: https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html
- **YARA Documentation**: https://virustotal.github.io/yara/
- **OpenIOC Format**: https://openioc.org/
- **MISP Project**: https://www.misp-project.org/
- **ThreatConnect**: https://threatconnect.com/
- **AlienVault OTX**: https://otx.alienvault.com/
