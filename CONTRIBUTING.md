# Contributing to MentorAgents 🤝

Thank you for your interest in contributing to MentorAgents! We welcome contributions from developers, AI researchers, UX designers, and anyone passionate about making AI mentorship accessible to everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Types of Contributions](#types-of-contributions)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Review Process](#code-review-process)
- [Community](#community)

## 📜 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be respectful**: Treat everyone with respect and consideration
- **Be inclusive**: Welcome newcomers and diverse perspectives
- **Be collaborative**: Work together and help each other learn
- **Be constructive**: Focus on what's best for the community and project
- **Be patient**: Remember that everyone has different experience levels

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.11+** installed
- **Node.js 16+** for frontend development
- **Git** for version control
- **MongoDB** instance (local or cloud)
- **API Keys**: Groq, OpenAI (for development)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mentoragents.git
   cd mentoragents
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/mentoragents.git
   ```

## 🛠 Development Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies using uv** (preferred):
   ```bash
   uv install
   ```
   
   Or using pip:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Environment configuration**:
   ```bash
   cp .env.example .env
   ```
   
   Fill in your environment variables:
   ```env
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   MONGO_URI=mongodb://localhost:27017/mentoragents_dev
   COMET_API_KEY=your_comet_api_key  # Optional for experiments
   ```

5. **Run the development server**:
   ```bash
   python -m mentoragents.main
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

### Database Setup

1. **Start MongoDB** locally or use MongoDB Atlas
2. **Run database migrations** (if any):
   ```bash
   python -m mentoragents.db.migrations
   ```

## 🏗 Project Structure

Understanding the codebase structure:

```
backend/src/mentoragents/
├── api/                    # FastAPI routes and endpoints
├── core/                   # Core configuration and utilities
├── db/                     # Database connections and operations
├── models/                 # Data models and AI model definitions
├── rag/                    # RAG system components
│   ├── data/              # Data extraction and processing
│   ├── embeddings.py      # Text embedding utilities
│   └── memory/            # Memory management systems
├── tools/                  # CLI tools and utilities
├── utils/                  # Helper functions and constants
└── workflow/              # LangGraph workflow definitions
    ├── chains.py          # AI chains and sequences
    ├── nodes.py           # Workflow nodes
    └── state.py           # State management
```

## 🎯 Types of Contributions

We welcome various types of contributions:

### 🐛 Bug Fixes
- Fix existing issues
- Improve error handling
- Performance optimizations

### ✨ Features
- New mentor personalities
- Enhanced memory systems
- UI/UX improvements
- API endpoints

### 📚 Documentation
- Code documentation
- API documentation
- Tutorials and guides
- README improvements

### 🧪 Testing
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests

### 🎨 Design & UX
- UI components
- User experience improvements
- Accessibility enhancements

### 🤖 AI/ML Improvements
- Model performance
- RAG system enhancements
- Memory management
- Prompt engineering

## 📝 Development Guidelines

### Code Style

#### Python (Backend)
- Follow **PEP 8** style guidelines
- Use **Black** for code formatting
- Use **isort** for import organization
- Use **type hints** for all functions
- Maximum line length: **88 characters**

```bash
# Format code
black .
isort .

# Check linting
flake8 .
mypy .
```

#### JavaScript/React (Frontend)
- Use **ESLint** and **Prettier**
- Follow **React best practices**
- Use **TypeScript** when possible
- Prefer **functional components** with hooks

```bash
# Format code
npm run format

# Check linting
npm run lint
```

### Naming Conventions

- **Files**: Use snake_case for Python, kebab-case for JavaScript
- **Classes**: PascalCase
- **Functions/Variables**: snake_case (Python), camelCase (JavaScript)
- **Constants**: UPPER_SNAKE_CASE
- **Components**: PascalCase

### Documentation Standards

- **Docstrings**: Use Google-style docstrings for Python
- **Comments**: Explain the "why", not the "what"
- **README**: Update relevant documentation for new features
- **API Docs**: Use FastAPI automatic documentation

Example Python docstring:
```python
def create_mentor_agent(mentor_name: str, config: Dict[str, Any]) -> MentorAgent:
    """Create a new mentor agent with specified configuration.
    
    Args:
        mentor_name: The name of the mentor personality
        config: Configuration dictionary containing model settings
        
    Returns:
        Initialized mentor agent instance
        
    Raises:
        ValueError: If mentor_name is not supported
        ConfigurationError: If config is invalid
    """
```

### Commit Messages

Follow **Conventional Commits** specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(rag): add long-term memory retrieval system

fix(api): resolve authentication token validation issue

docs(readme): update installation instructions

test(models): add unit tests for mentor factory
```

## 🧪 Testing

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# All tests with coverage
pytest --cov=mentoragents --cov-report=html
```

### Test Structure

#### Backend Testing
- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test API endpoints and database operations
- **AI/ML tests**: Test model outputs and RAG system

```python
# Example test structure
def test_mentor_agent_creation():
    """Test mentor agent initialization."""
    config = {"model": "gpt-3.5-turbo", "temperature": 0.7}
    agent = create_mentor_agent("naval", config)
    
    assert agent.name == "naval"
    assert agent.model == "gpt-3.5-turbo"
```

#### Frontend Testing
- **Component tests**: React component rendering and behavior
- **Integration tests**: User workflows and API integration
- **E2E tests**: Complete user journeys

### Test Coverage Requirements

- **Minimum coverage**: 80% for new code
- **Critical paths**: 95% coverage for core functionality
- **AI components**: Test with mock data and expected outputs

## 📤 Submitting Changes

### Before Submitting

1. **Sync with upstream**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** following the guidelines above

4. **Test thoroughly**:
   ```bash
   # Run all tests
   pytest
   npm test
   
   # Check code quality
   black --check .
   flake8 .
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat(scope): your descriptive commit message"
   ```

### Pull Request Process

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub with:
   - **Clear title** following conventional commits
   - **Detailed description** of changes
   - **Screenshots/demos** for UI changes
   - **Testing instructions**
   - **Breaking changes** (if any)

3. **PR Template**:
   ```markdown
   ## Description
   Brief description of what this PR does
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed
   
   ## Screenshots (if applicable)
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] Tests added/updated
   ```

## 👀 Code Review Process

### Review Criteria

Reviewers will check for:
- **Functionality**: Does the code work as intended?
- **Code Quality**: Follows style guidelines and best practices
- **Testing**: Adequate test coverage and quality
- **Documentation**: Clear and up-to-date documentation
- **Performance**: No performance regressions
- **Security**: No security vulnerabilities introduced

### Review Timeline

- **Initial review**: Within 2-3 business days
- **Follow-up reviews**: Within 1-2 business days
- **Approval**: Requires at least 1 approval from maintainers
- **Merge**: After all checks pass and approval received

### Addressing Review Comments

1. **Respond to all comments** - even if just acknowledging
2. **Make requested changes** in separate commits
3. **Test changes** after addressing comments
4. **Re-request review** when ready
5. **Be patient and collaborative** - reviews improve code quality

## 🎯 Specific Guidelines for AI/ML Components

### Mentor Development

When adding new mentors:

1. **Research thoroughly**: Study the mentor's background, philosophy, and communication style
2. **Create comprehensive profiles**: Include biographical data, key principles, and example responses
3. **Test personality consistency**: Ensure responses align with the mentor's known views
4. **Provide diverse examples**: Include various topics and question types

### RAG System Improvements

- **Benchmark performance**: Compare retrieval accuracy before/after changes
- **Test with diverse queries**: Ensure improvements work across different question types
- **Document embedding strategies**: Explain chunking and embedding approaches
- **Validate memory systems**: Test both short-term and long-term memory functionality

### Model Integration

- **Environment variables**: Use configuration for model parameters
- **Error handling**: Robust handling of API failures and timeouts
- **Rate limiting**: Respect API rate limits and implement backoff
- **Cost optimization**: Monitor and optimize API usage costs

## 🌟 Recognition

Contributors will be recognized through:

- **Contributors section** in README
- **Release notes** mentions for significant contributions
- **GitHub achievements** and contributor statistics
- **Community shoutouts** in Discord/discussions

## 💬 Community

### Getting Help

- **GitHub Discussions**: For questions and general discussion
- **Discord Server**: Real-time chat with maintainers and contributors
- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Comprehensive guides and API references

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas, showcase
- **Discord**: Real-time collaboration and community chat
- **Email**: security@mentoragents.ai for security issues

## 🚀 Development Workflow

### Typical Contribution Workflow

1. **Find or create an issue** to work on
2. **Comment on the issue** to claim it
3. **Fork and clone** the repository
4. **Create a feature branch** from main
5. **Make your changes** following guidelines
6. **Write/update tests** for your changes
7. **Run the full test suite** locally
8. **Update documentation** as needed
9. **Submit a pull request** with clear description
10. **Respond to review feedback** promptly
11. **Celebrate** when your PR is merged! 🎉

### Release Process

- **Semantic versioning**: MAJOR.MINOR.PATCH
- **Release branches**: Created from main for releases
- **Changelog**: Maintained for all releases
- **Migration guides**: For breaking changes

## 🏷 Labels and Issues

### Issue Labels

- `good-first-issue`: Perfect for newcomers
- `help-wanted`: Community help needed
- `bug`: Something isn't working
- `enhancement`: New feature request
- `documentation`: Documentation improvements
- `ai/ml`: AI/ML related issues
- `frontend`: Frontend/UI related
- `backend`: Backend/API related
- `priority-high`: Urgent issues

### Issue Templates

We provide templates for:
- **Bug reports**: Detailed bug information
- **Feature requests**: New feature proposals
- **Documentation**: Documentation improvements
- **AI/ML**: AI/ML specific enhancements

---

## 🙏 Thank You

Your contributions make MentorAgents better for everyone! Whether you're fixing a typo, adding a new mentor, or architecting major features, every contribution matters.

**Happy coding!** 🚀

---

*For questions about contributing, reach out to us through any of our community channels. We're here to help!* 