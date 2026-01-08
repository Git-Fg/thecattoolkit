# Workflow: Quick Scan

## Required Reading
None.

## Process

### Step 1: File System Overview
Execute the following commands to get the lay of the land:
```bash
# List root files to identify project type
ls -F

# List structure excluding common noise
find . -maxdepth 2 -not -path '*/.*' -not -path './node_modules*' -not -path './venv*'
```

### Step 2: Read Entry Points
Based on the file list, identify and read the key entry/configuration files:
- **Node/JS**: `package.json` (scripts, dependencies)
- **Python**: `pyproject.toml`, `requirements.txt`, or `setup.py`
- **Go**: `go.mod`
- **Rust**: `Cargo.toml`
- **General**: `README.md` (first 50 lines), `Dockerfile`, `docker-compose.yml`

### Step 3: Synthesis
Generate a summary in the following format:

```markdown
# Project: [Name]

## Overview
[1-2 sentence description based on README/Context]

## Tech Stack
- **Language**: [e.g., TypeScript]
- **Framework**: [e.g., Next.js 14]
- **Database**: [e.g., PostgreSQL (inferred from docker-compose or deps)]
- **Key Libs**: [e.g., Prisma, Tailwind, React Query]

## Key Directories
- `src/` or `app/`: [Purpose]
- `lib/` or `utils/`: [Purpose]
- `tests/`: [Test runner used]

## Workflow
- **Build**: [Command]
- **Dev**: [Command]
- **Test**: [Command]
```

## Success Criteria
- [ ] Tech stack identified
- [ ] Entry points located
- [ ] Build/Run commands verified