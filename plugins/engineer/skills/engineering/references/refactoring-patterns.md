# Refactoring Patterns

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