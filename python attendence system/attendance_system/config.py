import os

# Path configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACE_DB_PATH = os.path.join(BASE_DIR, "face_database")
TRAINED_MODEL_PATH = os.path.join(BASE_DIR, "trained_model", "face_encodings.pkl")
ATTENDANCE_PATH = os.path.join(BASE_DIR, "attendance_records")

# Create directories if they don't exist
os.makedirs(FACE_DB_PATH, exist_ok=True)
os.makedirs(os.path.dirname(TRAINED_MODEL_PATH), exist_ok=True)
os.makedirs(ATTENDANCE_PATH, exist_ok=True)

print("✅ Project directories created successfully!")