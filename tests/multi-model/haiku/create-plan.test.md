# Test: create-plan - Haiku Tier

## Test Case 1: Simple Plan Creation
**Input**: `/sys-builder:create-plan "Build a basic Python CLI tool"`
**Expected Output**: Plan files created in `.cattoolkit/plan/python-cli-tool/`
**Success Criteria**:
- [ ] BRIEF.md created with project definition
- [ ] ROADMAP.md created with phase structure
- [ ] Phase plan files created in phases/ directory
- [ ] Files follow naming conventions
- [ ] Status codes are [ ] (pending)
- [ ] No errors in creation

## Test Case 2: React App Plan
**Input**: `/sys-builder:create-plan "Create a React app with authentication"`
**Expected Output**: React-specific plan structure
**Success Criteria**:
- [ ] BRIEF.md mentions React and authentication
- [ ] ROADMAP.md has 3-4 phases (Foundation, Auth, Core, Polish)
- [ ] Phase plans include React-specific tasks
- [ ] Dependencies properly set
- [ ] Templates sourced from managing-project-plans

## Test Case 3: Microservice Plan
**Input**: `/sys-builder:create-plan "Build a Go microservice with Docker"`
**Expected Output**: Microservice architecture plan
**Success Criteria**:
- [ ] BRIEF.md defines microservice scope
- [ ] ROADMAP.md includes service + deployment phases
- [ ] Phase plans include Go and Docker tasks
- [ ] Containerization tasks present
- [ ] Testing strategy defined

## Test Case 4: Empty Codebase
**Input**: `/sys-builder:create-plan "Build a new web application"`
**Expected Output**: Greenfield project plan
**Success Criteria**:
- [ ] Discovery finds no existing code
- [ ] Plan assumes new project structure
- [ ] Foundation phase includes setup tasks
- [ ] No brownfield migration tasks
- [ ] Technology stack clearly defined

## Test Case 5: Plan in Existing Project
**Input**: `/sys-builder:create-plan "Add payment processing"`
**Expected Output**: Brownfield integration plan
**Success Criteria**:
- [ ] Discovery scans existing codebase
- [ ] BRIEF.md mentions existing project
- [ ] Plan includes integration tasks
- [ ] No setup tasks (project exists)
- [ ] Migration strategy defined if needed
