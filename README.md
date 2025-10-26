# Blog API - Microservice Architecture

FastAPI-based blog application with users, articles, and comments functionality.

## Features

- ✅ User registration and authentication (JWT)
- ✅ Article management (CRUD operations)
- ✅ Comments system
- ✅ PostgreSQL database
- ✅ Docker containerization
- ✅ Health checks
- ✅ API documentation

## Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <your-repo-url>
cd MSA
```

2. Create .env file:
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/msa_db
JWT_SECRET=jwt-key
ACCESS_TOKEN_EXPIRE_MINUTES=3000

3. Start services:
```bash
docker-compose up -d
```

4. Access the application:

API: http://localhost:8000

Documentation: http://localhost:8000/docs

# Manual Development Setup
1. Install dependencies:

```bash
pip install -r requirements.txt
```
Set up PostgreSQL and update DATABASE_URL in .env

Run the application:

```bash
python run.py
```

# API Endpoints
## Authentication
POST /api/users - Register new user

POST /api/users/login - User login

GET /api/user - Get current user

PUT /api/user - Update current user

## Articles
GET /api/articles - List all articles

POST /api/articles - Create article (authenticated)

GET /api/articles/{slug} - Get article by slug

PUT /api/articles/{slug} - Update article (author only)

DELETE /api/articles/{slug} - Delete article (author only)

## Comments
GET /api/articles/{slug}/comments - Get article comments

POST /api/articles/{slug}/comments - Add comment (authenticated)

DELETE /api/articles/{slug}/comments/{comment_id} - Delete comment (author only)


