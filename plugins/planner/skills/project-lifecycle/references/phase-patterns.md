# Phase Patterns by Project Type

## Web Service

**Typical phases:**

1. **01-foundation** - Setup, structure, config
2. **02-core** - Main features and functionality
3. **03-enhancement** - Testing, docs, deployment

**Example phase breakdown:**

```
01-foundation
├── Task 1: Initialize project with TypeScript
├── Task 2: Set up Express server
└── Task 3: Configure database connection

02-authentication
├── Task 1: Create User model
├── Task 2: Build login endpoint
└── Task 3: Add auth middleware

03-api-endpoints
├── Task 1: Create CRUD endpoints
├── Task 2: Add input validation
└── Task 3: Implement error handling

04-polish
├── Task 1: Add integration tests
├── Task 2: Write API documentation
└── Task 3: Set up deployment
```

## CLI Tool

**Typical phases:**

1. **01-framework** - Argument parsing, CLI structure
2. **02-commands** - Implement commands
3. **03-polish** - Help text, completion, packaging

**Example phase breakdown:**

```
01-framework
├── Task 1: Set up commander.js or yargs
├── Task 2: Create basic CLI structure
└── Task 3: Add configuration file support

02-commands
├── Task 1: Implement init command
├── Task 2: Implement build command
└── Task 3: Implement deploy command

03-polish
├── Task 1: Add help text and examples
├── Task 2: Add shell completion
└── Task 3: Package for npm
```

## Library

**Typical phases:**

1. **01-core-api** - Interfaces and types
2. **02-implementation** - Core logic
3. **03-examples** - Documentation, examples, tests

**Example phase breakdown:**

```
01-core-api
├── Task 1: Define TypeScript interfaces
├── Task 2: Create type definitions
└── Task 3: Document API surface

02-implementation
├── Task 1: Implement core functions
├── Task 2: Add error handling
└── Task 3: Add input validation

03-examples
├── Task 1: Write usage examples
├── Task 2: Create README documentation
└── Task 3: Add integration tests
```

## Frontend Application

**Typical phases:**

1. **01-setup** - Framework, routing, state
2. **02-components** - Core UI components
3. **03-integration** - API integration, features
4. **04-polish** - Styling, testing, build

**Example phase breakdown:**

```
01-setup
├── Task 1: Initialize React/Next.js project
├── Task 2: Set up routing
└── Task 3: Configure state management

02-components
├── Task 1: Create layout components
├── Task 2: Build form components
└── Task 3: Add data display components

03-integration
├── Task 1: Connect to API endpoints
├── Task 2: Implement authentication flow
└── Task 3: Add data fetching logic

04-polish
├── Task 1: Add responsive styles
├── Task 2: Write component tests
└── Task 3: Configure production build
```

## Customizing Patterns

**Adjust based on:**

- **Project complexity** - More phases for complex projects
- **Team size** - More phases for team coordination
- **Timeline** - Fewer phases for rapid prototyping

**Key principle:** Keep phases focused on cohesive sets of tasks.
