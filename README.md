# psybot-service

![Tests](https://github.com/maxterdize/psybot-service/workflows/Automated%20Tests/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Django](https://img.shields.io/badge/django-5.2-green)
![MongoDB](https://img.shields.io/badge/database-mongodb-brightgreen)

Python Backend Service for PsyBot App - A Django REST API with MongoDB integration.

**✅ Automated Testing Enabled** - All pushes to main/develop are automatically tested with GitHub Actions.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) (usually comes with Docker Desktop)

## Quick Start with Docker

### 1. Clone the Repository
```bash
git clone <repository-url>
cd psybot-service
```

### 2. Set Up Environment Variables
Copy the example environment file and update it with your settings:
```bash
cp .env.example .env
```

**Important:** Edit the `.env` file and update the following variables:
- `SECRET_KEY`: Generate a new Django secret key
- `JWT_SECRET_KEY`: Generate a JWT secret key
- `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`: If using email features
- Any API keys you need (OpenAI, etc.)

### 3. Run with Docker Compose
Navigate to the `psybot` directory and start the services:
```bash
cd psybot
docker-compose up --build
```

This will start:
- **Django Backend**: http://localhost:8000
- **MongoDB Database**: localhost:27017

### 4. Access the Application
- **API Root**: http://localhost:8000/api/
- **User API**: http://localhost:8000/api/users/
- **Django Admin**: http://localhost:8000/admin/ (if configured)

## 🛠️ Development Commands

### Start the Application
```bash
cd psybot
docker-compose up
```

### Start in Background (Detached Mode)
```bash
docker-compose up -d
```

### Stop the Application
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs mongo
```

### Rebuild Containers (after code changes)
```bash
docker-compose up --build
```

### Execute Commands in Running Containers
```bash
# Access Django shell
docker-compose exec backend python manage.py shell

# Run Django migrations (if needed)
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access MongoDB shell
docker-compose exec mongo mongosh
```

## 📁 Project Structure

```
psybot-service/
├── accounts/              # User management app
├── psybot/               # Main Django project
│   ├── Dockerfile        # Docker configuration
│   ├── docker-compose.yml # Docker Compose configuration
│   └── settings.py       # Django settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## 🔧 Environment Variables

The application uses the following environment variables (see `.env.example`):

- `SECRET_KEY`: Django secret key
- `DEBUG`: Enable/disable debug mode
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `MONGO_DB_NAME`: MongoDB database name
- `MONGO_HOST`: MongoDB connection string
- `CORS_ALLOWED_ORIGINS`: Allowed CORS origins (optional - for frontend integration)
- `JWT_SECRET_KEY`: JWT token secret
- Email configuration variables (if using email features)

## Troubleshooting

### Port Already in Use
If you get port conflicts, you can either:
1. Stop the conflicting service
2. Change ports in `docker-compose.yml`

### Container Build Issues
```bash
# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Database Connection Issues
Ensure MongoDB container is running:
```bash
docker-compose ps
```

### View Container Status
```bash
docker-compose ps
```

## 📝 API Documentation

Once the application is running, you can explore the API using:
- **Django REST Framework Browsable API**: http://localhost:8000/api/
- **API Endpoints**:
  - `GET /api/users/` - List users
  - `POST /api/users/` - Create user
  - `GET /api/users/{id}/` - Get specific user
  - `PUT /api/users/{id}/` - Update user
  - `DELETE /api/users/{id}/` - Delete user

## 🧪 Automated Testing

### Running Tests Locally
```bash
# Make sure Docker is running first
cd psybot && docker-compose up -d && cd ..

# Run automated tests
python run_tests.py
```

### Test Coverage
The project includes automated tests for:
- ✅ **Patient Creation** - Validates patient model and database operations
- ✅ **PHQ-9 Assessments** - Tests assessment creation and validation
- ✅ **AI Analysis** - Mocked Gemini AI integration testing
- ✅ **Trend Analysis** - Multi-assessment trend detection

### Continuous Integration
GitHub Actions automatically runs all tests on:
- Push to `main`, `develop`, or `Reto6` branches
- Pull requests to `main` or `develop`

Tests include MongoDB integration and mocked external services.

## Contributing

1. Make sure Docker is running
2. Follow the Quick Start guide
3. Make your changes
4. Run tests locally: `python run_tests.py`
5. Test with `docker-compose up --build`
6. Submit your pull request

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the logs with `docker-compose logs`
3. Ensure all environment variables are properly set
4. Contact the development team

---

**Note**: This is a development setup. For production deployment, additional security and performance configurations are required.
