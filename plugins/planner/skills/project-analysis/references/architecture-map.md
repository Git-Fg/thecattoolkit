# Workflow: Architecture Map

## Required Reading
- `references/tech-stack-signatures.md`

## Process

### Step 1: Identify Key Components
Scan the `src` or `app` directories to identify architectural archetypes. Look for:
- **API/Routes**: `routes/`, `controllers/`, `pages/api/`
- **Business Logic**: `services/`, `use_cases/`, `handlers/`
- **Data Access**: `models/`, `repositories/`, `db/`, `schema/`
- **UI Components**: `components/`, `views/`

```bash
# Search for these patterns
find src -maxdepth 3 -type d
```

### Step 2: Trace Data Flow
Pick one core feature (e.g., "User Login" or "Create Item") and trace it from entry point to database.
1. Find the route/entry point.
2. Read the handler/controller.
3. Identify what service/function it calls.
4. Identify how data is persisted.

### Step 3: Analyze Patterns
Determine the high-level architecture:
- **Monolith vs Microservices** (Docker compose, multiple package.json?)
- **MVC vs Clean Architecture** (Folder structure)
- **Client-Side vs Server-Side Rendering** (Framework analysis)

### Step 4: Output Map
Generate an ASCII diagram and explanation:

```markdown
# Architecture Map

## Pattern: [e.g., Layered Monolith]

## Data Flow (Example: [Feature])
[Request] -> [Controller/Route] -> [Service Layer] -> [ORM/DAO] -> [Database]

## Key Components
1. **[Component A]**: Handles [responsibility]
2. **[Component B]**: Handles [responsibility]

## Constraints & Conventions
- [e.g., All logic must reside in services]
- [e.g., Uses DTOs for API responses]
```

## Success Criteria
- [ ] Architecture pattern identified
- [ ] Data flow traced for at least one feature
- [ ] Key directories mapped to responsibilities