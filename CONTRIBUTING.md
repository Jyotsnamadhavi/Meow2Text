# Contributing to Meow2Text

Thank you for your interest in contributing to Meow2Text! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/your-username/meow2text.git`
3. **Create a virtual environment**: `python -m venv venv && source venv/bin/activate`
4. **Install dependencies**: `pip install -e ".[dev]"`
5. **Set up pre-commit**: `pre-commit install`
6. **Create a branch**: `git checkout -b feature/your-feature-name`

## 📋 Development Setup

### Prerequisites
- Python 3.8+
- Node.js 14+ (for frontend development)
- Git

### Backend Development
```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
isort src/

# Type checking
mypy src/

# Linting
flake8 src/
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

## 🎯 Areas for Contribution

### High Priority
- **Audio Classification**: Improve meow classification accuracy
- **Translation Quality**: Enhance LangChain prompts and responses
- **Error Handling**: Better error messages and recovery
- **Testing**: Add comprehensive test coverage

### Medium Priority
- **New Personalities**: Add more cat personality types
- **Audio Processing**: Better audio preprocessing and feature extraction
- **API Documentation**: Improve OpenAPI documentation
- **Performance**: Optimize audio processing and API responses

### Low Priority
- **UI/UX**: Frontend improvements and new features
- **Deployment**: Docker configuration and deployment scripts
- **Monitoring**: Add logging and monitoring capabilities
- **Internationalization**: Support for multiple languages

## 📝 Code Style

### Python
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions small and focused on a single responsibility

### TypeScript/React
- Use functional components with hooks
- Follow ESLint and Prettier configurations
- Use TypeScript for all new code
- Write meaningful component and function names

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_audio_service.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Writing Tests
- Write tests for all new functionality
- Aim for at least 80% code coverage
- Use descriptive test names
- Test both success and error cases

## 📦 Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the code style guidelines
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Run the test suite** and ensure all tests pass
6. **Submit a pull request** with a clear description

### Pull Request Template
```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added tests for new functionality
- [ ] All existing tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**: OS, Python version, package versions
2. **Steps to reproduce**: Clear, step-by-step instructions
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Error messages**: Full error traceback if applicable
6. **Sample data**: Audio files or other relevant data (if possible)

## 💡 Feature Requests

When requesting features, please include:

1. **Use case**: Why this feature would be useful
2. **Proposed implementation**: How you think it should work
3. **Alternatives considered**: Other approaches you've thought about
4. **Mockups or examples**: Visual or code examples if applicable

## 📄 License

By contributing to Meow2Text, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) for details.

## 📞 Getting Help

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub discussions for questions and general chat
- **Email**: Contact the maintainers directly for sensitive issues

## 🎉 Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing to Meow2Text! 🐱✨ 