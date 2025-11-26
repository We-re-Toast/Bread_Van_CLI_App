# Flask MVC Template - Replit Setup

## Project Overview
This is a Flask MVC (Model-View-Controller) template application with user authentication, database integration, and admin functionality. The application has been successfully configured to run in the Replit environment.

## Architecture
- **Backend**: Flask framework with Python 3.11
- **Database**: SQLite (development) with SQLAlchemy ORM
- **Frontend**: HTML templates with Jinja2, Bootstrap styling
- **Authentication**: Flask-JWT-Extended with cookie-based auth
- **File uploads**: Flask-Reuploaded for handling file uploads
- **Admin panel**: Flask-Admin for administration interface

## Current Configuration

### Development Environment
- **Host**: 0.0.0.0 (configured for Replit proxy)
- **Port**: 5000 
- **Database**: SQLite (temp-database.db)
- **Debug Mode**: Enabled in development
- **Workflow**: Flask development server configured and running

### Deployment Configuration
- **Target**: Autoscale deployment
- **Production Server**: Gunicorn with reuse-port
- **Command**: `gunicorn --bind=0.0.0.0:5000 --reuse-port wsgi:app`

## Key Features
- User authentication and registration
- JWT-based session management
- Database migrations with Flask-Migrate
- File upload capabilities
- Admin dashboard
- CORS enabled for cross-origin requests
- CLI commands for database management

## Available Commands
- `flask init` - Initialize database
- `flask run --host 0.0.0.0 --port 5000` - Start development server
- `flask user create <username> <password>` - Create user
- `flask user list` - List users
- `flask test user` - Run tests

## Project Structure
- `App/` - Main application package
  - `controllers/` - Business logic controllers
  - `models/` - Database models
  - `views/` - Route definitions
  - `templates/` - HTML templates
  - `static/` - CSS, JS, and static files
- `wsgi.py` - WSGI application entry point
- `requirements.txt` - Python dependencies

## Status
✅ All dependencies installed
✅ Database initialized
✅ Flask configured for Replit environment
✅ Workflow running on port 5000
✅ Deployment configuration set
✅ Application tested and functional

## Recent Changes (September 25, 2025)
- Installed Python 3.11 and all required dependencies
- Configured Flask to run on 0.0.0.0:5000 for Replit proxy compatibility
- Set up development workflow with proper host binding
- Initialized SQLite database
- Configured autoscale deployment with Gunicorn
- Verified application functionality and accessibility

## User Preferences
- Development environment configured for immediate use
- Production-ready deployment configuration available
- All original project structure and functionality preserved