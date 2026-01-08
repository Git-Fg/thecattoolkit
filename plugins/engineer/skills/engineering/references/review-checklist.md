# Code Review Checklist

## 1. Correctness
- [ ] Does the logic handle edge cases (null, 0, empty array)?
- [ ] Are error states handled (try/catch, promises)?

## 2. Security
- [ ] No hardcoded secrets?
- [ ] Inputs validated/sanitized?
- [ ] Auth checks on sensitive endpoints?

## 3. Performance
- [ ] No DB queries inside loops?
- [ ] Large datasets paginated?
- [ ] Heavy computations cached?

## 4. Maintainability
- [ ] Variables named for intent (`userList` vs `data`)?
- [ ] Functions do one thing?
- [ ] No magic numbers?