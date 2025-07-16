# Contributing to Think AI

Thank you for your interest in contributing to Think AI! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Contributions](#making-contributions)
- [Testing Requirements](#testing-requirements)
- [Style Guidelines](#style-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

- Be welcoming and inclusive
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/think_ai.git
   cd think_ai
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/champi-dev/think_ai.git
   ```
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Rust 1.70 or higher
- Node.js 18 or higher
- Git
- SQLite3
- Optional: Docker for containerized development

### Initial Setup

1. **Install dependencies**:
   ```bash
   npm run install:all
   ```

2. **Run tests to verify setup**:
   ```bash
   npm test
   ```

3. **Start development servers**:
   ```bash
   npm run dev
   ```

### Development Tools

- **VSCode**: Recommended with Rust Analyzer and ESLint extensions
- **Pre-commit hooks**: Automatically installed via Husky
- **Formatting**: Rust fmt and Prettier are configured

## Making Contributions

### Types of Contributions

1. **Bug Fixes**: Fix issues reported in GitHub Issues
2. **Features**: Add new functionality (discuss in issue first)
3. **Documentation**: Improve or add documentation
4. **Tests**: Add missing tests or improve test coverage
5. **Performance**: Optimize code for better performance
6. **Refactoring**: Improve code quality and maintainability

### Development Workflow

1. **Sync with upstream**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make changes**:
   - Write code following our style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Test thoroughly**:
   ```bash
   npm test
   npm run lint
   npm run typecheck
   ```

5. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: Add new feature"
   ```

## Testing Requirements

All contributions must maintain or improve test coverage. Our target is 100% coverage.

### Running Tests

```bash
# Run all tests
npm test

# Run specific test suites
npm run test:backend      # Rust tests
npm run test:frontend     # React tests
npm run test:e2e         # End-to-end tests

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run coverage
```

### Writing Tests

1. **Unit Tests**: Test individual functions/components
2. **Integration Tests**: Test component interactions
3. **E2E Tests**: Test complete user workflows

Example test structure:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_feature() {
        // Arrange
        let input = "test";
        
        // Act
        let result = process(input);
        
        // Assert
        assert_eq!(result, "expected");
    }
}
```

```jsx
test('component renders correctly', async () => {
  // Arrange
  const user = userEvent.setup();
  
  // Act
  render(<Component />);
  
  // Assert
  expect(screen.getByText('Expected Text')).toBeInTheDocument();
});
```

## Style Guidelines

### Rust Code Style

- Follow standard Rust conventions
- Use `cargo fmt` for formatting
- Use `cargo clippy` for linting
- Keep functions small and focused
- Document public APIs with doc comments

```rust
/// Processes the input and returns a result.
///
/// # Arguments
///
/// * `input` - The input string to process
///
/// # Examples
///
/// ```
/// let result = process("hello");
/// assert_eq!(result, "HELLO");
/// ```
pub fn process(input: &str) -> String {
    input.to_uppercase()
}
```

### JavaScript/TypeScript Style

- Use ESLint configuration
- Prefer functional components with hooks
- Use TypeScript for new code
- Keep components small and reusable

```jsx
/**
 * Button component with loading state
 * @param {Object} props - Component props
 * @param {string} props.label - Button label
 * @param {boolean} props.loading - Loading state
 * @param {Function} props.onClick - Click handler
 */
export function Button({ label, loading, onClick }) {
  return (
    <button 
      onClick={onClick} 
      disabled={loading}
      className="btn"
    >
      {loading ? 'Loading...' : label}
    </button>
  );
}
```

## Commit Guidelines

We follow Conventional Commits specification:

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Examples

```bash
feat(frontend): Add dark mode toggle

Implemented a toggle switch in the header that allows users
to switch between light and dark themes. Theme preference
is saved to localStorage.

Closes #123
```

```bash
fix(backend): Resolve memory leak in session handler

The session cleanup routine was not properly releasing
memory for expired sessions. Added proper cleanup logic
that runs every 5 minutes.

Fixes #456
```

## Pull Request Process

1. **Update your branch**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature
   ```

3. **Create Pull Request**:
   - Go to GitHub and create a PR from your fork
   - Fill out the PR template completely
   - Link related issues

4. **PR Requirements**:
   - All tests must pass
   - Code coverage must not decrease
   - No merge conflicts
   - At least one approval from maintainers
   - PR description clearly explains changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No console errors/warnings
```

## Release Process

Releases follow semantic versioning (SemVer):

- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features (backward compatible)
- **Patch** (0.0.X): Bug fixes

### Release Steps

1. Update version numbers
2. Update CHANGELOG.md
3. Create release PR
4. After merge, tag release
5. Deploy to production

## Getting Help

- **Discord**: Join our community server
- **Issues**: Check existing issues or create new ones
- **Discussions**: Use GitHub Discussions for questions
- **Email**: contact@thinkai.lat

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Annual contributor spotlight

Thank you for contributing to Think AI! 🧠✨