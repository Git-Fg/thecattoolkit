# Refactoring Patterns

## When to Refactor
- Code smells present (duplication, long methods, large classes)
- Before adding new features
- After tests are passing
- When fixing bugs

## Common Refactoring Techniques

### Composing Methods
- **Extract Method**: Break down complex methods
- **Inline Method**: Replace method calls with method body
- **Replace Temp with Query**: Use method instead of temporary variable
- **Introduce Parameter Object**: Group related parameters

### Moving Features Between Objects
- **Move Method**: Move method to more appropriate class
- **Move Field**: Move field to more appropriate class
- **Extract Class**: Split class with multiple responsibilities
- **Inline Class**: Merge class with single responsibility

### Organizing Data
- **Replace Data Value with Object**: Wrap primitives in objects
- **Change Value to Reference**: Use objects for identity-based data
- **Replace Array with Object**: Use objects instead of arrays
- **Encapsulate Collection**: Return copies, not direct references

### Simplifying Conditional Expressions
- **Decompose Conditional**: Extract methods from complex conditions
- **Consolidate Conditional Expression**: Merge similar conditions
- **Replace Conditional with Polymorphism**: Use polymorphism for type-based logic

## Code Smells
- **Feature Envy**: A method accesses data of another object more than its own. -> *Move Method*
- **Long Parameter List**: >3 arguments. -> *Introduce Parameter Object*
- **Shotgun Surgery**: Making many small changes to many classes for one feature. -> *Move Field/Method*

## SOLID Principles
- **S**ingle Responsibility
- **O**pen/Closed
- **L**iskov Substitution
- **I**nterface Segregation
- **D**ependency Inversion

## Refactoring Safety
1. **Always have tests** before refactoring
2. **Make changes small and incremental**
3. **Run tests frequently**
4. **Don't change behavior** while refactoring
5. **Leave code better than you found it**
