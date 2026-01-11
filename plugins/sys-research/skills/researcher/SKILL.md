---
name: researcher
description: "USE when answering technical questions requiring external verification, documentation lookup, or library/repo research. Automatically determines the optimal research tool based on query type and available information."
allowed-tools:
  - mcp__plugin_sys-research_context7__resolve-library-id
  - mcp__plugin_sys-research_context7__query-docs
  - mcp__plugin_sys-research_deepwiki__ask_question
  - mcp__plugin_sys-research_deepwiki__read_wiki_structure
  - mcp__plugin_sys-research_duckduckgo__search
  - mcp__plugin_sys-research_duckduckgo__fetch_content
---

# Technical Research Skill

Use this skill when the user asks technical questions requiring external verification or research. This skill automatically selects the optimal research tool based on your query.

## Trigger Conditions

Automatically invoke this skill when you encounter:
- **"How do I..."** questions about libraries/frameworks
- **Error messages** requiring external documentation
- **"What is..."** queries about specific technologies
- **Library comparisons** or feature lookups
- **API documentation** requests
- **Implementation examples** for specific tools

## Tool Selection Logic

### Step 1: Unknown Terms? Use DuckDuckGo (Scout)
If you're unfamiliar with a term, library name, or need to find the correct repository:

**Tool:** `mcp__plugin_sys-research_duckduckgo__search`

**Goal:** Find:
- Exact official library name
- Primary GitHub repository `owner/repo`
- Official documentation URL

**Example:** User asks about "that new Python async library everyone is using"
→ Search to identify the specific library name and repository

### Step 2: Standard Libraries? Use Context7 (Librarian)
For established frameworks, SDKs, and well-documented libraries:

**Tool Sequence:**
1. `mcp__plugin_sys-research_context7__resolve-library-id` with the library name
2. **CRITICAL**: Use the exact `libraryId` from step 1 in step 2
3. `mcp__plugin_sys-research_context7__query-docs` with the resolved ID

**Best For:**
- React, Next.js, Vue.js, Angular
- Python: pandas, numpy, requests, flask, django
- AWS SDK, Azure SDK, GCP SDK
- Node.js: express, mongoose, graphql
- Java: spring, hibernate, junit
- Go: gin, gorm, cobra
- Rust: serde, tokio, actix

**Example:** User asks "How do I implement authentication in React?"
→ Resolve library ID for "react" then query for authentication patterns

### Step 3: Specific Repos? Use DeepWiki (Code Expert)
For GitHub repositories, specific branches, or niche tools:

**Tool:** `mcp__plugin_sys-research_deepwiki__ask_question` or `mcp__plugin_sys-research_deepwiki__read_wiki_structure`

**Best For:**
- GitHub repositories (e.g., "owner/repo-name")
- Specific branches or commits
- Open source project internals
- Niche or experimental libraries
- Understanding specific file structures

**Example:** User asks "How does the dev branch of vercel/next.js implement edge runtime?"
→ Use DeepWiki with repoName "vercel/next.js" and branch "dev"

## Decision Tree

```
Query Type
├── Contains library name I recognize?
│   ├── YES → Is it a standard framework/library?
│   │   ├── YES → Context7 (resolve → query)
│   │   └── NO → DuckDuckGo (identify) → DeepWiki
│   └── NO → DuckDuckGo (identify)
├── Mentions specific GitHub repo?
│   └── YES → DeepWiki (ask_question)
└── Asking for general understanding?
    └── YES → DeepWiki (read_wiki_structure)
```

## Failure Handling

### Context7 Resolution Fails
**Fallback:** Use `mcp__plugin_sys-research_duckduckgo__search` to find:
1. Correct library naming convention
2. Official documentation URL
3. Alternative names or aliases

Then retry Context7 with the correct name.

### Insufficient Documentation Data
**Fallback:** Use `mcp__plugin_sys-research_duckduckgo__fetch_content` on:
1. Official docs URL found via search
2. GitHub README or wiki pages
3. Community tutorials or guides

### DeepWiki Returns Limited Info
**Fallback:** Use `mcp__plugin_sys-research_duckduckgo__search` to find:
1. Additional resources about the repository
2. Community discussions or issues
3. Related projects or alternatives

## Response Format

Structure your answer as:

```
## Research Summary

**Query:** [Restate the user's question]

**Tools Used:** [List the MCP tools invoked]

**Key Findings:**
- [Bullet point 1 with citation]
- [Bullet point 2 with citation]

**Solution/Code Example:**
```[language]
[Complete, working code example]
```

**Explanation:**
[Why this solution works based on the retrieved documentation/repo structure]
```

## Examples

### Example 1: Standard Library Query
**User:** "How do I read a CSV file in Python?"

**Action:**
1. Recognize "pandas" as standard library
2. Call `resolve-library-id` for "pandas"
3. Call `query-docs` with resolved ID for CSV reading
4. Provide code example and explanation

### Example 2: Unknown Library
**User:** "What's the best way to do state management in Svelte?"

**Action:**
1. Not immediately familiar with Svelte state libraries
2. Call `duckduckgo__search` for "Svelte state management libraries"
3. Identify "svelte/store" as the official solution
4. If needed, use Context7 or DeepWiki for deeper dive
5. Provide comprehensive answer

### Example 3: GitHub Repository
**User:** "How does authentication work in the Auth.js NextAuth repo?"

**Action:**
1. Recognize this as GitHub repo-specific question
2. Call `deepwiki__ask_question` with repoName "next-auth/next-auth.js"
3. Ask specific question about authentication implementation
4. Provide detailed answer with file references

## Best Practices

1. **Always verify** the library name before using Context7
2. **Use the exact libraryId** returned from resolve-library-id
3. **Cite sources** in your response (documentation paths, file locations)
4. **Provide complete, working code examples**
5. **Explain the "why"** not just the "how"
6. **Chain tools intelligently** when one tool's output informs the next
7. **Document your research process** so the user understands the methodology
