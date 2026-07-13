# Tender Search AI - Backend

AI-powered tender search and recommendation system built with FastAPI, MongoDB, and Ollama.

## Features

- Search tenders by keyword and location
- AI-powered tender recommendations
- Chat interface for general queries
- Web scraping for tender data collection

## Prerequisites

- Python 3.8+
- MongoDB (running locally or remote URI)
- Ollama with Llama 3.2 model

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tender-search-ai-backend.git
cd tender-search-ai-backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

5. Copy `.env.example` to `.env` and configure:
```bash
copy .env.example .env
```

6. Start MongoDB:
```bash
mongod
```

7. Start Ollama:
```bash
ollama serve
```

8. Run the application:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status |
| POST | `/tenders` | Add new tender |
| GET | `/tenders` | List all tenders |
| GET | `/tenders/{id}` | Get tender by ID |
| PUT | `/tenders/{id}` | Update tender |
| DELETE | `/tenders/{id}` | Delete tender |
| POST | `/search` | Search tenders with AI |
| POST | `/chat` | Chat with AI |

## Scraping Tenders

Run the scraper to collect tenders:
```bash
python scraper.py
```
Solve the CAPTCHA manually when prompted.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `MONGO_DB` | Database name | `tender_ai` |
| `OLLAMA_URL` | Ollama API URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | AI model name | `llama3.2` |

## License

MIT
