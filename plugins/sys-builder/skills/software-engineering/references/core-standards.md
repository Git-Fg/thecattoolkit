# Core Engineering Standards

## Universal Standards

### Security (OWASP Top 10)
- **Injection Prevention**: All user inputs validated/sanitized
- **Authentication**: Auth checks on sensitive endpoints
- **Access Control**: Authorization on every protected resource
- **Cryptography**: No hardcoded passwords or keys
- **Input Validation**: All entry points validated
- **Error Handling**: Errors don't expose sensitive information
- **Dependencies**: No vulnerable/outdated components

### Testing
- No code without tests
- Edge cases covered
- Test quality and assertions correct

### State Persistence
- Persist decisions to `.cattoolkit/context/scratchpad.md`
