# Workflow: Testing Strategy

## Purpose
Create a robust test suite following the Testing Pyramid.

## Process

### Step 1: Unit Tests (70%)
Focus on pure functions and business logic.
- Mock all external dependencies (DB, Network).
- Cover Happy Path + 2 Edge Cases + 1 Error State.

### Step 2: Integration Tests (20%)
Test the interaction between modules (e.g., API -> DB).
- Use real database (test instance).
- Mock only 3rd party APIs (Stripe, Twilio).

### Step 3: E2E Tests (10%)
Critical user journeys only.
- Login -> Checkout -> Payment.

## Success Criteria
- [ ] Tests are deterministic (no flake).
- [ ] Tests run fast (unit tests < 5ms).
- [ ] Failure messages are descriptive.