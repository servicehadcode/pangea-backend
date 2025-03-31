# Pangea Backend API Documentation

Backend service for Pangea platform providing APIs for problem management and contact functionality.

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and update the values
4. Start MongoDB service
5. Run the application:
```bash
python src/app.py
```

## API Endpoints

### Problems API

#### 1. Get All Problems
- **Endpoint:** `GET /api/problems`
- **Query Parameters:** 
  - `category` (optional): Filter problems by category
- **Response:**
```json
[
    {
        "problem_num": "string",
        "title": "string",
        "description": "string",
        "longDescription": "string",
        "difficulty": "string",
        "category": "string",
        "requirements": {},
        "tags": [],
        "steps": [],
        "resources": [],
        "metadata": {}
    }
]
```

#### 2. Get Single Problem
- **Endpoint:** `GET /api/problem/{problem_num}`
- **Response:**
```json
{
    "problem_num": "string",
    "title": "string",
    "description": "string",
    "longDescription": "string",
    "difficulty": "string",
    "category": "string",
    "requirements": {},
    "tags": [],
    "steps": [],
    "resources": [],
    "metadata": {}
}
```

#### 3. Add New Problem
- **Endpoint:** `POST /api/addProblem`
- **Headers:** `Content-Type: application/json`
- **Request Body:**
```json
{
    "problem_num": "string",
    "title": "string",
    "description": "string",
    "longDescription": "string",
    "difficulty": "string",
    "category": "string",
    "requirements": {
        "time": "string",
        "skills": ["string"],
        "prerequisites": ["string"]
    },
    "tags": ["string"],
    "steps": [
        {
            "step": "number",
            "description": "string"
        }
    ],
    "resources": [
        {
            "type": "string",
            "url": "string",
            "description": "string"
        }
    ],
    "metadata": {
        "created": "string",
        "author": "string",
        "lastUpdated": "string"
    }
}
```
- **Response:**
```json
{
    "message": "Problem added successfully"
}
```

#### 4. Update Problem
- **Endpoint:** `PUT /api/updateProblem/{problem_num}`
- **Headers:** `Content-Type: application/json`
- **Request Body:** 
```json
{
    "title": "string",
    "difficulty": "string",
    "requirements": {}
    // Any other fields that need to be updated
}
```
- **Response:**
```json
{
    "message": "Problem updated successfully"
}
```

#### 5. Delete Problem
- **Endpoint:** `DELETE /api/deleteProblem/{problem_num}`
- **Response:**
```json
{
    "message": "Problem deleted successfully"
}
```

### Contact API

#### 1. Send Contact Message
- **Endpoint:** `POST /api/contact`
- **Headers:** `Content-Type: application/json`
- **Request Body:**
```json
{
    "name": "string",
    "email": "string",
    "subject": "string",
    "message": "string"
}
```
- **Response:**
```json
{
    "message": "Email sent successfully"
}
```

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `201`: Created successfully
- `400`: Bad request
- `404`: Resource not found
- `500`: Server error

Error response format:
```json
{
    "error": "Error message description"
}
```

## Environment Variables

Required environment variables in `.env`:

```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=pangea
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=True
SMTP_USE_SSL=False
SENDER_EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
FOUNDERS_EMAIL=email1@example.com,email2@example.com
```

## Testing

Use the provided Postman collection for testing the APIs. Import the collection from `problems_api_collection.json`.

## Development

- Python 3.x
- Flask 2.0.1
- MongoDB 4.x
- Additional requirements listed in `requirements.txt`