# Example: Solo Developer Tone

**Use for:** Personal projects, indie development, one-person teams, internal documentation

## Characteristics

- **Direct communication** - Skip corporate formalities
- **Practical focus** - Emphasize what works
- **Efficient** - Optimize for developer productivity
- **Opinionated** - Share what actually works
- **Honest** - Acknowledge trade-offs and limitations

## Voice & Style

### Language Patterns

**Direct instructions:**
- ✅ "Configure the database"
- ❌ "You may want to configure the database"
- ✅ "This will fail if port 5432 is in use"
- ❌ "There's a possibility this could fail if the port is unavailable"

**Practical examples:**
- ✅ "I use this pattern in production"
- ❌ "According to best practices..."
- ✅ "This breaks with node 18.17"
- ❌ "There appears to be an issue with version compatibility"

**Trade-off awareness:**
- ✅ "Simple but not scalable"
- ❌ "Not optimal for enterprise use"
- ✅ "Fast to implement, hard to maintain"
- ❌ "This approach has some limitations"

### Tone Characteristics

| Element | Style | Avoid |
|---------|-------|-------|
| **Voice** | "You" (direct) | "One might consider" |
| **Certainty** | Confident | Hedging ("might", "could", "perhaps") |
| **Complexity** | Explain simply | Jargon without context |
| **Errors** | Direct statement | Apologetic tone |
| **Success** | Matter-of-fact | Celebratory |

## Communication Pattern Examples

### Project Setup
```markdown
# Quick Start
1. Clone and install: `npm install`
2. Configure `.env` from `.env.example`
3. Start services: `docker-compose up -d`
4. Migrate: `npm run migrate`
5. Dev: `npm run dev`
```

### Explaining Architecture
```markdown
## Why This Design
I went with a simple 3-layer architecture. Overkill for a solo project.
- **Pro**: One deploy, simple debugging, less overhead.
- **Con**: Harder to scale horizontally.
For 10K users, this is the right trade-off.
```

### Key Phrases

**Instead of "This ensures high availability":**
- "This won't crash if one server dies"
- "Your app keeps running even if something breaks"

**Instead of "Following industry standards":**
- "This is what works in production"
- "I've tested this approach"

**Instead of "It is recommended to":**
- "You should"
- "Do this"
- "Skip this and you'll regret it"
