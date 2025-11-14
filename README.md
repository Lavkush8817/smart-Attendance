# Smart Attendance System

AI-powered face recognition attendance system using FastAPI and DeepFace.

## Features

- 🎯 Face Recognition using Facenet512
- 📝 User Registration
- ✅ Automatic Attendance Marking
- 📊 Excel Export
- 🎨 Modern UI with Real-time Camera Feed

## Tech Stack

**Backend:**
- FastAPI
- DeepFace (Facenet512)
- Python 3.x

**Frontend:**
- HTML5
- CSS3
- JavaScript (ES6+)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Lavkush8817/smart-Attendance.git
cd smart-Attendance
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the backend server:
```bash
python3 -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

2. Open the frontend:
```bash
open frontend/index.html
```

## API Endpoints

- `GET /` - Health check
- `POST /register` - Register new user
- `POST /mark-attendance` - Mark attendance
- `GET /users` - Get all users
- `GET /attendance` - Get attendance records
- `GET /attendance/export` - Export to Excel

## License

MIT
