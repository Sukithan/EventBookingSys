# Backend Quick Start

## Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Setup environment:
```bash
cp .env.example .env
```

## Running

```bash
python main.py
```

API available at: http://localhost:8000
Docs available at: http://localhost:8000/docs

## API Endpoints

- `GET /` - API info
- `GET /api/health` - Health check
- `GET /api/items` - List all items
- `POST /api/items` - Create item
- `PUT /api/items/{id}` - Update item
- `DELETE /api/items/{id}` - Delete item
