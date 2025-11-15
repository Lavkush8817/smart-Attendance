from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
from PIL import Image
import numpy as np
import json, io, os, cv2
from datetime import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS_FILE = "backend/users.json"
ATTENDANCE_FILE = "backend/attendance.json"

os.makedirs("backend", exist_ok=True)
if not os.path.exists(USERS_FILE): json.dump([], open(USERS_FILE, "w"))
if not os.path.exists(ATTENDANCE_FILE): json.dump([], open(ATTENDANCE_FILE, "w"))

def load_json(file): return json.load(open(file))
def save_json(file, data): json.dump(data, open(file, "w"), indent=2)

@app.get("/")
def root():
    return {"message": "Face Attendance API running"}

@app.post("/register")
async def register_user(name: str = Form(...), student_id: str = Form(...), photo: UploadFile = None):
    image = Image.open(io.BytesIO(await photo.read()))
    np_img = np.array(image)
    embedding = DeepFace.represent(np_img, model_name="Facenet512", enforce_detection=False)[0]['embedding']

    users = load_json(USERS_FILE)
    users.append({"name": name, "student_id": student_id, "embedding": embedding})
    save_json(USERS_FILE, users)
    return {"message": f"User {name} registered successfully"}

@app.post("/mark-attendance")
async def mark_attendance(photo: UploadFile):
    image = Image.open(io.BytesIO(await photo.read()))
    np_img = np.array(image)

    users = load_json(USERS_FILE)
    if not users:
        return {"error": "No users registered"}

    try:
        # Get embedding for the captured face
        captured_embedding = DeepFace.represent(np_img, model_name="Facenet512", enforce_detection=False)[0]['embedding']
        
        # Find the best match by comparing embeddings
        best_match = None
        min_distance = float('inf')
        
        for user in users:
            # Calculate cosine distance between embeddings
            distance = np.linalg.norm(np.array(captured_embedding) - np.array(user['embedding']))
            if distance < min_distance:
                min_distance = distance
                best_match = user
        
        # Threshold for face recognition (adjust as needed)
        if min_distance > 10:  # If distance is too large, face not recognized
            return {"error": "Face not recognized"}
        
        name = best_match['name']
        student_id = best_match['student_id']
    except Exception as e:
        return {"error": f"Face not recognized: {str(e)}"}

    attendance = load_json(ATTENDANCE_FILE)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attendance.append({"name": name, "student_id": student_id, "time": now})
    save_json(ATTENDANCE_FILE, attendance)
    return {"message": f"Attendance marked for {name} at {now}"}

@app.get("/users")
def get_users():
    return load_json(USERS_FILE)

@app.get("/attendance")
def get_attendance():
    return load_json(ATTENDANCE_FILE)

@app.get("/attendance/export")
def export_excel():
    import openpyxl
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Student ID", "Time"])

    for record in load_json(ATTENDANCE_FILE):
        ws.append([record["name"], record["student_id"], record["time"]])

    file_path = "backend/attendance.xlsx"
    wb.save(file_path)
    return FileResponse(file_path, filename="attendance.xlsx")
