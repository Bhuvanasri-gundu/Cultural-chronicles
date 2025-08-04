# Contributing to Cultural Chronicles

Thank you for your interest in contributing to Cultural Chronicles! This project aims to preserve and promote India's diverse cultural heritage through digital storytelling.

## How to Contribute

### Reporting Bugs
1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include steps to reproduce the issue
4. Provide system information and screenshots if relevant

### Suggesting Features
1. Check existing feature requests
2. Use the feature request template
3. Explain the cultural or technical value of your suggestion
4. Consider the impact on performance and user experience

### Contributing Code
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Follow our coding standards (see below)
4. Write tests for new functionality
5. Update documentation as needed
6. Submit a pull request with a clear description

## Development Setup

### Prerequisites
- Python 3.11 or higher
- PostgreSQL (optional, SQLite fallback available)
- Git

### Installation
```bash
git clone https://github.com/your-username/cultural-chronicles.git
cd cultural-chronicles
pip install -r requirements.txt
```

### Running the Application
```bash
streamlit run app.py --server.port 5000
```

## Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Keep functions focused and modular

### File Organization
- `app.py` - Main application entry point
- `pages/` - Individual page components
- `utils/` - Utility functions and helpers
- `models/` - Data models and database schemas
- `data/` - Static data files

### Database Guidelines
- Use SQLAlchemy ORM for database operations
- Never write raw SQL unless absolutely necessary
- Include proper error handling for database operations
- Test with both PostgreSQL and SQLite

### UI/UX Guidelines
- Maintain cultural sensitivity in all content
- Ensure accessibility compliance
- Test responsive design on different screen sizes
- Follow the established orange gradient theme

## Cultural Sensitivity

This project deals with India's cultural heritage. Please ensure:
- Respectful representation of all communities
- Accurate cultural information
- Inclusive language and imagery
- Consultation with cultural experts when needed

## Testing

### Running Tests
```bash
python -m pytest tests/
```

### Test Coverage
- Aim for 80%+ test coverage
- Include unit tests for utility functions
- Add integration tests for database operations
- Test UI components where possible

## Documentation

- Update `README.md` for user-facing changes
- Update `replit.md` for architectural changes
- Include docstrings for all new functions
- Update this file for process changes

## Review Process

1. All contributions require review
2. Maintainers will provide constructive feedback
3. Address review comments promptly
4. Squash commits before merging

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and provide helpful guidance
- Focus on constructive criticism
- Respect cultural differences and perspectives

## Getting Help

- Check the documentation first
- Search existing issues
- Ask questions in discussions
- Contact maintainers for guidance

## Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- Special recognition for significant contributions

Thank you for helping preserve and share India's cultural heritage!