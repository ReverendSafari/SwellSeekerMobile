# SwellSeeker Mobile

A surf reporting mobile app backend built with FastAPI and PostgreSQL.

## Features

- **Surf Data API**: Real-time wind, wave, tide, and temperature data
- **Beach Management**: Database of surf spots with coordinates
- **Caching System**: 12-hour TTL caching for weather data
- **Surf Grading**: Automatic surf quality assessment (green/yellow/red)
- **API Key Authentication**: Secure access control
- **PostgreSQL Database**: Reliable data storage with SQLAlchemy ORM

## Tech Stack

- **Backend**: FastAPI with Uvicorn
- **Database**: PostgreSQL with SQLAlchemy
- **Caching**: Custom TTL-based caching system
- **Authentication**: API key-based authentication
- **Weather APIs**: Open-Meteo, NOAA, and tide services

## Project Structure

```
SwellSeekerMobile/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   ├── core/           # Configuration
│   │   │   ├── db/             # Database setup
│   │   │   ├── models/         # SQLAlchemy models
│   │   │   ├── schemas/        # Pydantic schemas
│   │   │   └── services/       # Business logic
│   │   ├── scripts/            # Database utilities
│   │   └── venv/               # Python virtual environment
│   ├── beaches.json            # Beach data import file
│   ├── api_keys.txt           # API keys (gitignored)
│   └── README.md              # This file
```

## Quick Start

1. **Setup Database**:
   ```bash
   cd backend
   source venv/bin/activate
   python scripts/init_db.py
   ```

2. **Import Beaches**:
   ```bash
   python scripts/import_beaches.py
   ```

3. **Generate API Key**:
   ```bash
   python scripts/generate_api_key.py
   ```

4. **Run Server**:
   ```bash
   uvicorn app.main:app --reload --port 8002
   ```

## API Endpoints

- `GET /api/v1/beaches/` - List all beaches
- `GET /api/v1/beaches/{beach_name}` - Get specific beach
- `GET /api/v1/surf-data/{beach_name}` - Get surf data with grading

## Environment Variables

Copy `env.example` to `.env` and configure:
- Database connection
- API keys for weather services
- CORS settings

## License

MIT License - see LICENSE file for details. 
