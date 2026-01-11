#!/bin/bash
# SessionStart Hook Example - Project Context Detection
# Detects project type and loads relevant environment variables
# Output is written to $CLAUDE_ENV_FILE for persistence across the session

set -euo pipefail

# Ensure we're in the project directory
cd "$CLAUDE_PROJECT_DIR" || {
  echo "Failed to navigate to project directory" >&2
  exit 1
}

echo "🔍 Loading project context..."

# Detect project type and set environment variables
# These are written to $CLAUDE_ENV_FILE which persists for the session

if [ -f "package.json" ]; then
  echo "📦 Node.js project detected"
  echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"

  # Detect TypeScript usage
  if [ -f "tsconfig.json" ]; then
    echo "  → TypeScript configuration found"
    echo "export USES_TYPESCRIPT=true" >> "$CLAUDE_ENV_FILE"
  fi

  # Detect framework
  if grep -q "react" package.json 2>/dev/null; then
    echo "  → React framework detected"
    echo "export FRAMEWORK=react" >> "$CLAUDE_ENV_FILE"
  elif grep -q "vue" package.json 2>/dev/null; then
    echo "  → Vue.js framework detected"
    echo "export FRAMEWORK=vue" >> "$CLAUDE_ENV_FILE"
  fi

  # Detect testing framework
  if [ -d "node_modules/.bin" ]; then
    if [ -f "node_modules/.bin/jest" ] || grep -q '"jest"' package.json 2>/dev/null; then
      echo "  → Jest testing framework detected"
      echo "export TEST_FRAMEWORK=jest" >> "$CLAUDE_ENV_FILE"
    elif [ -f "node_modules/.bin/vitest" ] || grep -q '"vitest"' package.json 2>/dev/null; then
      echo "  → Vitest testing framework detected"
      echo "export TEST_FRAMEWORK=vitest" >> "$CLAUDE_ENV_FILE"
    fi
  fi

elif [ -f "Cargo.toml" ]; then
  echo "🦀 Rust project detected"
  echo "export PROJECT_TYPE=rust" >> "$CLAUDE_ENV_FILE"

  # Check for common Rust tools
  if [ -f "Cargo.lock" ]; then
    echo "  → Dependencies locked"
  fi

elif [ -f "go.mod" ]; then
  echo "🐹 Go project detected"
  echo "export PROJECT_TYPE=go" >> "$CLAUDE_ENV_FILE"

  # Extract Go version if available
  if command -v go >/dev/null 2>&1; then
    go_version=$(go version 2>/dev/null | awk '{print $3}' || echo "unknown")
    echo "  → Go version: $go_version"
    echo "export GO_VERSION=$go_version" >> "$CLAUDE_ENV_FILE"
  fi

elif [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
  echo "🐍 Python project detected"
  echo "export PROJECT_TYPE=python" >> "$CLAUDE_ENV_FILE"

  # Detect Python testing framework
  if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ] && grep -q "\[tool.pytest" pyproject.toml 2>/dev/null; then
    echo "  → Pytest framework detected"
    echo "export TEST_FRAMEWORK=pytest" >> "$CLAUDE_ENV_FILE"
  fi

  # Detect virtual environment
  if [ -n "${VIRTUAL_ENV:-}" ]; then
    echo "  → Virtual environment active: $VIRTUAL_ENV"
    echo "export VENV_ACTIVE=true" >> "$CLAUDE_ENV_FILE"
  fi

elif [ -f "pom.xml" ]; then
  echo "☕ Java (Maven) project detected"
  echo "export PROJECT_TYPE=java" >> "$CLAUDE_ENV_FILE"
  echo "export BUILD_SYSTEM=maven" >> "$CLAUDE_ENV_FILE"

elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
  echo "☕ Java/Kotlin (Gradle) project detected"
  echo "export PROJECT_TYPE=java" >> "$CLAUDE_ENV_FILE"
  echo "export BUILD_SYSTEM=gradle" >> "$CLAUDE_ENV_FILE"

elif [ -f "composer.json" ]; then
  echo "🎼 PHP (Composer) project detected"
  echo "export PROJECT_TYPE=php" >> "$CLAUDE_ENV_FILE"

else
  echo "❓ Unknown project type"
  echo "export PROJECT_TYPE=unknown" >> "$CLAUDE_ENV_FILE"
fi

# Detect CI/CD configuration
if [ -f ".github/workflows" ] && [ -d ".github/workflows" ]; then
  echo "🔄 GitHub Actions detected"
  echo "export HAS_CI=true" >> "$CLAUDE_ENV_FILE"
  echo "export CI_SYSTEM=github" >> "$CLAUDE_ENV_FILE"
elif [ -f ".gitlab-ci.yml" ] || [ -f ".gitlab-ci.yaml" ]; then
  echo "🔄 GitLab CI detected"
  echo "export HAS_CI=true" >> "$CLAUDE_ENV_FILE"
  echo "export CI_SYSTEM=gitlab" >> "$CLAUDE_ENV_FILE"
elif [ -f ".circleci/config.yml" ]; then
  echo "🔄 CircleCI detected"
  echo "export HAS_CI=true" >> "$CLAUDE_ENV_FILE"
  echo "export CI_SYSTEM=circleci" >> "$CLAUDE_ENV_FILE"
fi

# Detect database configuration
if [ -f ".env" ] && grep -q "DATABASE_URL" .env 2>/dev/null; then
  echo "🗄️ Database configuration detected"
  echo "export HAS_DATABASE=true" >> "$CLAUDE_ENV_FILE"
fi

# Detect Docker usage
if [ -f "Dockerfile" ] || [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
  echo "🐳 Docker detected"
  echo "export HAS_DOCKER=true" >> "$CLAUDE_ENV_FILE"
fi

# Check for common configuration files
if [ -f ".editorconfig" ]; then
  echo "✏️ EditorConfig detected"
  echo "export HAS_EDITORCONFIG=true" >> "$CLAUDE_ENV_FILE"
fi

if [ -f ".gitignore" ]; then
  echo "📋 .gitignore detected"
  echo "export HAS_GITIGNORE=true" >> "$CLAUDE_ENV_FILE"
fi

# Set timestamp for when context was loaded
echo "export CONTEXT_LOADED_AT=$(date -Iseconds)" >> "$CLAUDE_ENV_FILE"

echo "✅ Project context loaded successfully"

exit 0
