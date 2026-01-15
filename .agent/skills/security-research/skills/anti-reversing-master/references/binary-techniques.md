# Binary Reverse Engineering Techniques

## Overview

Traditional reverse engineering techniques for compiled binaries.

## Topics

### Anti-Debugging
- API-based detection (IsDebuggerPresent, CheckRemoteDebuggerPresent)
- PEB-based detection (BeingDebugged, NtGlobalFlag)
- Timing-based detection (RDTSC, QueryPerformanceCounter)
- Exception-based detection (SEH, VEH)

### Anti-VM Detection
- CPUID-based detection (hypervisor bit)
- Hardware fingerprinting
- Timing anomalies
- Registry/file detection

### Code Obfuscation
- Control flow flattening
- Opaque predicates
- Dead code insertion
- Instruction substitution

### Packing/Unpacking
- Common packers (UPX, Themida, VMProtect)
- Unpacking methodology
- OEP finding techniques
- Import table reconstruction

## References

See: [anti-reversing-techniques skill](../anti-reversing-techniques/SKILL.md)

## Usage

Navigate to the anti-reversing-techniques skill for complete documentation.
