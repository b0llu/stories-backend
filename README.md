# Stories Backend

A FastAPI-based backend for the Stories application, handling user authentication and story management.

## Features

- User authentication with JWT
- Story creation and management
- Media upload support via Cloudinary
- PostgreSQL database integration
- CORS support for frontend integration

## Prerequisites

- Python 3.8+
- PostgreSQL
- Cloudinary account

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd stories-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

- Format code: `black .`
- Lint code: `ruff .`
- Type check: `mypy .`

## License

MIT 