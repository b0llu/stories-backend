# Stories Backend

A FastAPI-based backend service for the Stories application.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Virtual environment (recommended)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stories-backend.git
cd stories-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your database:
   - Create a PostgreSQL database
   - Update the database URL in `alembic.ini` if necessary

5. Run database migrations:
```bash
# Initialize alembic if not already initialized
alembic init alembic

# Generate a new migration
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# To downgrade one version
alembic downgrade -1

# To get migration history
alembic history

# To get current version
alembic current
```

## Running the Application

Start the development server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
stories-backend/
├── alembic/            # Database migrations
├── app/                # Application source code
├── venv/              # Virtual environment
├── alembic.ini        # Alembic configuration
├── requirements.txt    # Project dependencies
└── run.py             # Application entry point
```

## Development

To add new dependencies:
1. Install the package: `pip install package-name`
2. Update requirements.txt: `pip freeze > requirements.txt`

## Database Migrations

When making changes to database models:

1. Make your changes to the SQLAlchemy models
2. Generate a new migration:
```bash
alembic revision --autogenerate -m "describe your changes"
```
3. Review the generated migration in `alembic/versions/`
4. Apply the migration:
```bash
alembic upgrade head
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

[Add your license information here] 