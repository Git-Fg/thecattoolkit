# Prompt Taxonomy

A detailed guide to the three core categories of prompt artifacts.

## 1. Single Prompts
**Focus**: direct execution of a standalone task.
**Storage**: `.cattoolkit/prompts/`
**Pattern**: Pure Markdown (0 XML tags).

### Common Types:
| Type | Purpose | Example |
|:---|:---|:---|
| **Analysis** | Examine and interpret info | Code review, data analysis |
| **Generation** | Create new content | Write code, documentation |
| **Review** | Evaluate and check quality | Security audit, compliance check |
| **Transformation** | Convert/restructure formats | JSON to CSV, translation |
| **Q&A** | Answer specific questions | Technical support, troubleshooting |
| **Creative** | Generate ideas/development | Brainstorming, feature design |

---

## 2. Prompt Chains
**Focus**: multi-step sequential workflows.
**Storage**: `.cattoolkit/chains/{number}-{topic}/`
**Pattern**: Hybrid XML (3-5 tags).

### The Standard Chain Pattern:
1. **Research**: Gather information and analyze requirements.
2. **Plan**: Design the solution and strategy.
3. **Execute**: Perform the primary task.
4. **Refine**: Polishing and final validation.

### Chain Artifacts:
- **SUMMARY.md**: Overview of the chain's purpose and state.
- **step-{n}-{name}.md**: The individual prompts for each phase.
- **outputs/**: Directory for storing intermediate and final results.

---

## 3. Meta-Prompts
**Focus**: Prompts that act on other prompts.
**Storage**: `.cattoolkit/generators/`
**Pattern**: Hybrid XML (3-5 tags).

### Common Meta-Prompts:
- **Prompt Generator**: Creates a new prompt from a user description.
- **Prompt Optimizer**: Refines an existing prompt for better performance.
- **Prompt Auditor**: Evaluates a prompt against the `quality.md` criteria.

---

## Choosing the Right Category

- **Is it a one-time standalone task?** → Single Prompt.
- **Does it require research or planning before execution?** → Prompt Chain.
- **Are you trying to automate prompt creation itself?** → Meta-Prompt.
