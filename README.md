# Real Estate Website

A modern and responsive real estate website built with Flask, featuring property listings, user authentication, and advanced search functionality.

## Features

- **Property Listings**
  - Browse properties with detailed information
  - Advanced search and filtering options
  - Property favorites and saved searches
  - Image galleries with lazy loading

- **User Features**
  - User registration and authentication
  - User profiles with saved properties
  - Contact agents and schedule viewings
  - Email notifications

- **Admin Features**
  - Property management dashboard
  - User management
  - Analytics and reporting
  - Content management

- **Modern UI/UX**
  - Responsive design for all devices
  - Smooth animations and transitions
  - Intuitive navigation
  - Dark/light mode support

## Tech Stack

- **Backend**
  - Python 3.8+
  - Flask 2.0+
  - SQLAlchemy
  - Flask-Login
  - Flask-WTF
  - Flask-Mail

- **Frontend**
  - HTML5
  - CSS3 (with custom properties)
  - JavaScript (ES6+)
  - Bootstrap 5
  - Font Awesome

- **Database**
  - PostgreSQL
  - Redis (for caching)

- **Development Tools**
  - Git
  - Docker
  - pytest
  - Black (code formatting)
  - Flake8 (linting)

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Redis 6 or higher
- Node.js 14 or higher (for frontend assets)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/real-estate.git
   cd real-estate
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   flask seed-db
   ```

6. Run the development server:
   ```bash
   flask run
   ```

## Development

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Format code:
   ```bash
   black .
   ```

4. Lint code:
   ```bash
   flake8
   ```

## Docker Setup

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Run the containers:
   ```bash
   docker-compose up
   ```

## Project Structure

```
real-estate/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   └── utils/
├── migrations/
├── tests/
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

## Contributing

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

## Testing

- Write unit tests for all new features
- Maintain test coverage above 80%
- Run tests before submitting PRs
- Include integration tests for critical paths

## Deployment

1. Set up production environment variables
2. Configure production database
3. Set up SSL certificates
4. Configure web server (Nginx/Apache)
5. Set up CI/CD pipeline

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)

## Support

For support, email support@realestate.com or open an issue in the repository. 