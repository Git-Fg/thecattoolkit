# Advanced Workflows: UV and Ruff

## Monorepo Management

### Workspace Structure

```
monorepo/
├── pyproject.toml          # Workspace root
├── uv.lock                 # Shared lockfile
├── packages/
│   ├── core/
│   │   └── pyproject.toml
│   └── api/
│       └── pyproject.toml
└── apps/
    └── web/
        └── pyproject.toml
```

### Root Configuration

```toml
[tool.uv.workspace]
members = ["packages/*", "apps/*"]

[tool.uv]
dev-dependencies = ["pytest>=7.0.0", "ruff>=0.1.0"]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B"]
```

### Package Dependencies

```toml
# packages/api/pyproject.toml
[project]
name = "myproject-api"
dependencies = ["fastapi>=0.100.0", "myproject-core"]

[tool.uv.sources]
myproject-core = { workspace = true }
```

### Workspace Commands

```bash
uv sync                                   # All packages
uv run --package myproject-api pytest     # Specific package
uv add --package myproject-api requests   # Add to package
```

## Docker Integration

### Multi-Stage Build

```dockerfile
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-cache

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "myapp"]
```

### Development Container

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache
COPY . .
CMD ["uv", "run", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
```

### Docker Compose

```yaml
services:
  app:
    build: .
    volumes:
      - .:/app
      - uv-cache:/root/.cache/uv
    ports:
      - "8000:8000"
    command: uv run uvicorn main:app --reload --host 0.0.0.0

volumes:
  uv-cache:
```

### Production Optimizations

```dockerfile
# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Cache mount for faster builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
```

## CI/CD Pipelines

### GitHub Actions

```yaml
name: CI
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync --frozen

      - name: Lint
        run: |
          uv run ruff check .
          uv run ruff format --check .

      - name: Test
        run: uv run pytest --cov=src

  test-matrix:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - run: uv python install ${{ matrix.python }}
      - run: uv sync --frozen
      - run: uv run pytest
```

### GitLab CI

```yaml
variables:
  UV_CACHE_DIR: ${CI_PROJECT_DIR}/.cache/uv

cache:
  paths:
    - .cache/uv
    - .venv

before_script:
  - curl -LsSf https://astral.sh/uv/install.sh | sh
  - export PATH="$HOME/.local/bin:$PATH"
  - uv sync --frozen

lint:
  script:
    - uv run ruff check .
    - uv run ruff format --check .

test:
  script: uv run pytest
```

### Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.8
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

```bash
uv add --dev pre-commit
uv run pre-commit install
```

## Development Workflow

### VS Code Settings

```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

### Task Runner (justfile)

```justfile
install:
    uv sync

dev:
    uv run uvicorn main:app --reload

lint:
    uv run ruff check --fix .
    uv run ruff format .

test:
    uv run pytest -v

test-cov:
    uv run pytest --cov=src --cov-report=html

update:
    uv lock --upgrade
    uv sync

clean:
    uv cache clean
    ruff clean
    find . -type d -name __pycache__ -exec rm -rf {} +

check: lint test
```

## Production Deployments

### AWS Lambda

```dockerfile
FROM public.ecr.aws/lambda/python:3.12
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
COPY src ${LAMBDA_TASK_ROOT}/src
RUN uv sync --frozen --no-dev --no-cache
CMD ["src.handler.lambda_handler"]
```

### Google Cloud Run

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-cache
COPY . .
ENV PORT=8080
CMD exec uv run uvicorn main:app --host 0.0.0.0 --port ${PORT}
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
```

## Performance Tips

### Caching in CI

```yaml
- name: Cache UV
  uses: actions/cache@v3
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}
```

### Build Optimization

```bash
UV_COMPILE_BYTECODE=1      # Compile .pyc
UV_SYSTEM_PYTHON=1         # Use system Python
UV_NO_CACHE=1              # Skip cache (CI)
```

### Offline Mode

```bash
uv sync --offline          # Use only cached packages
```

## Team Collaboration

### Contributing Guide

```markdown
## Setup

1. Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Clone and install: `git clone ... && cd repo && uv sync`
3. Run tests: `uv run pytest`

## Before Committing

- `uv run ruff check --fix .`
- `uv run ruff format .`
- `uv run pytest`

## Adding Dependencies

```bash
uv add package-name        # Production
uv add --dev package-name  # Development
```
```

### Code Review Checklist

- [ ] `uv run ruff check --fix .`
- [ ] `uv run ruff format .`
- [ ] `uv run pytest`
- [ ] Updated `uv.lock` if deps changed
- [ ] CI passes
