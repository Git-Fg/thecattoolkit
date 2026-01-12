---
name: statistical-analysis
description: "Statistical analysis toolkit for hypothesis testing, regression, correlation, Bayesian statistics, power analysis, and APA reporting. USE when conducting academic research, analyzing experimental data, testing hypotheses with t-tests or ANOVA, performing regression analyses, calculating effect sizes, checking statistical assumptions, or generating publication-ready statistical reports."
allowed-tools: [Read, Write, Edit, Bash]
---

# Statistical Analysis

## Overview

Statistical analysis is a systematic process for testing hypotheses and quantifying relationships. Conduct hypothesis tests (t-tests, ANOVA, chi-square), regression, correlation, and Bayesian analyses with assumption checks and APA reporting. Apply this skill for academic research.

## When to Use This Skill

This skill should be used when:
- Conducting statistical hypothesis tests (t-tests, ANOVA, chi-square)
- Performing regression or correlation analyses
- Running Bayesian statistical analyses
- Checking statistical assumptions and diagnostics
- Calculating effect sizes and conducting power analyses
- Reporting statistical results in APA format
- Analyzing experimental or observational data for research

---

## Core Capabilities

- **Test Selection and Planning**: Choose appropriate tests and compute power. See [references/test_selection_guide.md](references/test_selection_guide.md).
- **Assumption Checking**: Verify normality, homogeneity, etc. See [references/assumptions_and_diagnostics.md](references/assumptions_and_diagnostics.md).
- **Statistical Testing**: hypothesis testing, regression, correlation, Bayesian. See [references/analysis-examples.md](references/analysis-examples.md).
- **Effect Sizes**: Calculate and interpret. See [references/effect_sizes_and_power.md](references/effect_sizes_and_power.md).
- **Reporting**: APA-style reports. See [references/reporting_standards.md](references/reporting_standards.md).

---

## Workflow Decision Tree

Use this decision tree to determine your analysis path:

```
START
│
├─ Need to SELECT a statistical test?
│  └─ YES → See [references/test_selection_guide.md](references/test_selection_guide.md)
│  └─ NO → Continue
│
├─ Ready to check ASSUMPTIONS?
│  └─ YES → See [references/assumptions_and_diagnostics.md](references/assumptions_and_diagnostics.md)
│  └─ NO → Continue
│
├─ Ready to run ANALYSIS?
│  └─ YES → See [references/analysis-examples.md](references/analysis-examples.md)
│  └─ NO → Continue
│
└─ Need to REPORT results?
   └─ YES → See [references/report-templates.md](references/report-templates.md)
```

---

## Resources

- **[references/test_selection_guide.md](references/test_selection_guide.md)**: Decision tree for choosing tests.
- **[references/assumptions_and_diagnostics.md](references/assumptions_and_diagnostics.md)**: Guidance on assumption checks.
- **[references/effect_sizes_and_power.md](references/effect_sizes_and_power.md)**: Effect sizes and power analysis.
- **[references/bayesian_statistics.md](references/bayesian_statistics.md)**: Bayesian methods.
- **[references/reporting_standards.md](references/reporting_standards.md)**: APA-style reporting.
- **[references/analysis-examples.md](references/analysis-examples.md)**: Code examples for tests.
- **[references/report-templates.md](references/report-templates.md)**: Report templates.

### Scripts

- **[scripts/assumption_checks.py](scripts/assumption_checks.py)**: Automated assumption checking tools.

