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

#### Schema Overview
The problem schema has been updated with the following new fields:

1. **Steps with Details and Acceptance Criteria**: Each step now includes:
   - A `details` array containing strings with additional information
   - An `acceptanceCriteria` array containing strings defining the criteria for that step
2. **Git Repository**: The `metadata` object now includes a `gitRepo` field with the repository URL.
3. **Downloadable Items**: A list of strings describing items that can be downloaded.
4. **Preparation Steps**: A list of strings describing steps to prepare for the problem.

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
        "steps": [
            {
                "step": "number",
                "description": "string",
                "details": ["string"],
                "acceptanceCriteria": ["string"]
            }
        ],
        "resources": [],
        "metadata": {
            "created": "string",
            "author": "string",
            "lastUpdated": "string",
            "gitRepo": "string"
        },
        "downloadableItems": ["string"],
        "preparationSteps": ["string"]
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
    "steps": [
        {
            "step": "number",
            "description": "string",
            "details": ["string"],
            "acceptanceCriteria": ["string"]
        }
    ],
    "resources": [],
    "metadata": {
        "created": "string",
        "author": "string",
        "lastUpdated": "string",
        "gitRepo": "string"
    },
    "downloadableItems": ["string"],
    "preparationSteps": ["string"]
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
            "description": "string",
            "details": ["string"],
            "acceptanceCriteria": ["string"]
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
        "lastUpdated": "string",
        "gitRepo": "string"
    },
    "downloadableItems": ["string"],
    "preparationSteps": ["string"]
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
    "requirements": {},
    "steps": [
        {
            "step": "number",
            "description": "string",
            "details": ["string"],
            "acceptanceCriteria": ["string"]
        }
    ],
    "metadata": {
        "gitRepo": "string"
    },
    "downloadableItems": ["string"],
    "preparationSteps": ["string"]
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


# Audio Transcription API

This API provides functionality to transcribe audio files to text.

## API Endpoint

- **URL**: `/api/v1/transcribe`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| audio | File | Yes | Audio file to transcribe (WAV format) |
| language | String | No | Language code (default: "en-US") |

## Response Format

### Success Response (200 OK)

```json
{
  "success": true,
  "data": {
    "transcription": "The transcribed text content",
    "confidence": 0.95,
    "processingTime": 1234.56,
    "wordCount": 42,
    "language": "en-US",
    "timestamp": "2023-05-01T12:34:56.789"
  }
}
```

### Error Response (4xx/5xx)

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly error message",
    "details": "Technical details (if available)"
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| MISSING_FILE | No audio file was provided in the request |
| INVALID_FILE | The provided file is invalid (wrong format, too large, etc.) |
| TRANSCRIPTION_FAILED | The transcription process failed |
| SERVER_ERROR | An unexpected server error occurred |

## Testing the API

### Using the Test Script

The repository includes a test script that can record audio from your microphone and send it to the API for transcription.

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure the Flask server is running:
   ```bash
   python src/app.py
   ```

3. Run the test script:
   ```bash
   python test_transcription.py [recording_duration]
   ```

   Where `[recording_duration]` is an optional parameter specifying how many seconds to record (default: 5 seconds).

4. Follow the prompts to record your voice, and the script will automatically send the recording to the API and display the transcription results.

### Using Postman or cURL

You can also test the API using tools like Postman or cURL:

```bash
curl -X POST -F "audio=@path/to/your/audio.wav" -F "language=en-US" http://localhost:5000/api/v1/transcribe
```

## Implementation Details

The API uses the following technologies:
- Flask for the web server
- SpeechRecognition library with Google's Speech Recognition API for transcription
  - Uses Google's free Speech-to-Text service for accurate transcription
  - Handles audio conversion using pydub instead of requiring FLAC utility
- PyAudio for audio recording in the test script

## Security Considerations

- The API currently limits file sizes to 10MB
- Only WAV format is supported
- For production use, consider adding authentication, rate limiting, and HTTPS


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

### Example Problem with New Schema

Here's an example of a complete problem with all the new schema fields:

```json
{
  "problem_num": "P005",
  "title": "Build a Recommendation System",
  "description": "Create a content-based recommendation system for an e-commerce platform",
  "longDescription": "Develop a recommendation engine that analyzes user behavior and product attributes to suggest relevant items to users.",
  "difficulty": "intermediate",
  "category": "data-science",
  "requirements": {
    "time": "3 weeks",
    "skills": ["Python", "Machine Learning", "Data Analysis"],
    "prerequisites": ["Basic ML knowledge", "Data processing"]
  },
  "tags": ["recommendation-system", "machine-learning", "e-commerce"],
  "steps": [
    {
      "step": 1,
      "description": "Data collection and preprocessing",
      "details": [
        "Gather user interaction data (clicks, purchases, ratings)",
        "Clean and normalize the dataset",
        "Split into training and testing sets"
      ],
      "acceptanceCriteria": [
        "Dataset contains at least 10,000 user interactions",
        "Data is properly normalized and cleaned",
        "Training/testing split follows 80/20 ratio"
      ]
    },
    {
      "step": 2,
      "description": "Feature engineering",
      "details": [
        "Extract relevant features from product metadata",
        "Create user profiles based on historical interactions"
      ],
      "acceptanceCriteria": [
        "Feature extraction is documented and justified",
        "User profiles accurately reflect browsing and purchase history"
      ]
    }
  ],
  "resources": [
    {
      "type": "article",
      "url": "https://example.com/recommendation-systems",
      "description": "Introduction to recommendation systems"
    }
  ],
  "metadata": {
    "created": "2024-04-05",
    "author": "Alex Johnson",
    "lastUpdated": "2024-04-05",
    "gitRepo": "https://github.com/example/recommendation-system"
  },
  "downloadableItems": [
    "Sample dataset (CSV)",
    "System architecture diagram (PDF)"
  ],
  "preparationSteps": [
    "Install Python 3.8+ and required libraries",
    "Set up a virtual environment for the project"
  ]
}
```


# Problem Instance API Documentation

This API provides endpoints for managing problem instances and subtasks.

## GET Endpoints

### Get Problem Instance

- **Endpoint:** `GET /api/problem-instances/:problemNum/:userId`
- **Description:** Retrieves the specific instance of a user working on a problem
- **URL Parameters:**
  - `problemNum`: The problem number
  - `userId`: The user ID
- **Response:**
```json
{
  "problemNum": "P001",
  "owner": {
    "userId": "user123",
    "username": "johndoe",
    "email": "john@example.com"
  },
  "collaborationMode": "solo",
  "collaborators": [],
  "status": "in-progress",
  "startedAt": "2023-05-01T12:34:56.789",
  "lastUpdatedAt": "2023-05-01T12:34:56.789",
  "completedAt": null,
  "_id": "60a1b2c3d4e5f6g7h8i9j0k1"
}
```

### Get Subtask Instances

- **Endpoint:** `GET /api/problem-instances/:instanceId/subtasks`
- **Description:** Gets all subtask instances for a specific problem instance
- **URL Parameters:**
  - `instanceId`: The problem instance ID
- **Response:**
```json
[
  {
    "problemInstanceId": "60a1b2c3d4e5f6g7h8i9j0k1",
    "stepNum": 1,
    "assignee": {
      "userId": "user123",
      "username": "johndoe"
    },
    "reporter": {
      "userId": "user456",
      "username": "janedoe"
    },
    "status": "in-progress",
    "branchCreated": true,
    "prCreated": false,
    "deliverables": "Implemented data collection module",
    "acceptanceCriteria": [
      {
        "criteriaText": "Data is properly normalized",
        "completed": true
      },
      {
        "criteriaText": "Test coverage is at least 80%",
        "completed": false
      }
    ],
    "prFeedback": [],
    "startedAt": "2023-05-01T12:34:56.789",
    "completedAt": null,
    "_id": "60a1b2c3d4e5f6g7h8i9j0k2"
  }
]
```

### Get Single Subtask Instance

- **Endpoint:** `GET /api/subtask-instances/:subtaskId`
- **Description:** Gets a specific subtask instance by ID
- **URL Parameters:**
  - `subtaskId`: The subtask instance ID
- **Response:**
```json
{
  "problemInstanceId": "60a1b2c3d4e5f6g7h8i9j0k1",
  "stepNum": 1,
  "assignee": {
    "userId": "user123",
    "username": "johndoe"
  },
  "reporter": {
    "userId": "user456",
    "username": "janedoe"
  },
  "status": "in-progress",
  "branchCreated": true,
  "prCreated": false,
  "deliverables": "Implemented data collection module",
  "acceptanceCriteria": [
    {
      "criteriaText": "Data is properly normalized",
      "completed": true
    },
    {
      "criteriaText": "Test coverage is at least 80%",
      "completed": false
    }
  ],
  "prFeedback": [],
  "startedAt": "2023-05-01T12:34:56.789",
  "completedAt": null,
  "_id": "60a1b2c3d4e5f6g7h8i9j0k2"
}
```

### Get Collaborators

- **Endpoint:** `GET /api/problem-instances/:instanceId/collaborators`
- **Description:** Gets all collaborators for a problem instance
- **URL Parameters:**
  - `instanceId`: The problem instance ID
- **Response:**
```json
[
  {
    "userId": "user456",
    "username": "janedoe",
    "email": "jane@example.com",
    "invitedAt": "2023-05-01T12:34:56.789",
    "joinedAt": "2023-05-01T13:45:56.789",
    "status": "active"
  }
]
```

## POST Endpoints

### Create Problem Instance

- **Endpoint:** `POST /api/problem-instances`
- **Description:** Creates a new instance when a user starts working on a problem
- **Request Body:**
```json
{
  "problemNum": "P001",
  "owner": {
    "userId": "user123",
    "username": "johndoe",
    "email": "john@example.com"
  },
  "collaborationMode": "solo"
}
```
- **Response:**
```json
{
  "message": "Problem instance created successfully",
  "instanceId": "60a1b2c3d4e5f6g7h8i9j0k1"
}
```

### Add Collaborator

- **Endpoint:** `POST /api/problem-instances/:instanceId/collaborators`
- **Description:** Adds a collaborator to a problem instance
- **URL Parameters:**
  - `instanceId`: The problem instance ID
- **Request Body:**
```json
{
  "userId": "user456",
  "username": "janedoe",
  "email": "jane@example.com"
}
```
- **Response:**
```json
{
  "message": "Collaborator added successfully"
}
```

### Create Subtask Instance

- **Endpoint:** `POST /api/problem-instances/:instanceId/subtasks`
- **Description:** Creates a subtask instance
- **URL Parameters:**
  - `instanceId`: The problem instance ID
- **Request Body:**
```json
{
  "stepNum": 1,
  "assignee": {
    "userId": "user123",
    "username": "johndoe"
  },
  "reporter": {
    "userId": "user456",
    "username": "janedoe"
  },
  "status": "not-started"
}
```
- **Response:**
```json
{
  "message": "Subtask instance created successfully",
  "subtaskId": "60a1b2c3d4e5f6g7h8i9j0k2"
}
```

## PATCH Endpoints

### Update Problem Instance Status

- **Endpoint:** `PATCH /api/problem-instances/:instanceId`
- **Description:** Updates the status of a problem instance
- **URL Parameters:**
  - `instanceId`: The problem instance ID
- **Request Body:**
```json
{
  "status": "completed",
  "completedAt": "2023-05-10T15:30:45.123"
}
```
- **Response:**
```json
{
  "message": "Problem instance status updated successfully"
}
```

### Update Subtask Instance

- **Endpoint:** `PATCH /api/problem-instances/:instanceId/subtasks/:subtaskId`
- **Description:** Updates a subtask instance
- **URL Parameters:**
  - `instanceId`: The problem instance ID
  - `subtaskId`: The subtask instance ID
- **Request Body:**
```json
{
  "assignee": {
    "userId": "user789",
    "username": "bobsmith"
  },
  "status": "in-progress",
  "branchCreated": true,
  "prCreated": false,
  "deliverables": "Implemented the data collection module"
}
```
- **Response:**
```json
{
  "message": "Subtask instance updated successfully"
}
```

### Update Acceptance Criteria Status

- **Endpoint:** `PATCH /api/problem-instances/:instanceId/subtasks/:subtaskId/criteria/:criteriaId`
- **Description:** Updates the status of a specific acceptance criterion
- **URL Parameters:**
  - `instanceId`: The problem instance ID
  - `subtaskId`: The subtask instance ID
  - `criteriaId`: The ID or index of the criterion
- **Request Body:**
```json
{
  "completed": true
}
```
- **Response:**
```json
{
  "message": "Acceptance criterion updated successfully"
}
```

## Error Responses

### Not Found (404)
```json
{
  "error": "Problem instance not found"
}
```

### Server Error (500)
```json
{
  "error": "Error message details"
}
```



## Development

- Python 3.x
- Flask 2.0.1
- MongoDB 4.x
- Additional requirements listed in `requirements.txt`









# Pangea Context API

chmod +x run.sh 
./run.sh