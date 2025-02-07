# Book Reviews API

## Project Overview
This is a RESTful API built with Django Rest Framework that allows users to manage books, reviews, and comments. Users can publish books, write reviews for books (except their own), and leave comments. The API includes user authentication using JWT tokens and comprehensive API documentation using Swagger/ReDoc.

Key Features:
- User registration and authentication with JWT tokens
- CRUD operations for books, reviews, and comments
- Pagination support for all list endpoints
- Permission-based access control
- API documentation with Swagger and ReDoc
- Secure endpoints requiring authentication

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/Elsaeed97/books_reviews.git
cd books_reviews
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
python manage.py makemigrations
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

## API Documentation

The API documentation is available at:
- Swagger: http://localhost:8000/api/v1/swagger/
- ReDoc: http://localhost:8000/api/v1/redoc/
- Postman Collection: https://documenter.getpostman.com/view/10101685/2sAYX8JgH4

