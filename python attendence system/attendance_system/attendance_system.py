import face_recognition
import cv2
import numpy as np
import pickle
import pandas as pd
from datetime import datetime, date
import os
from config import TRAINED_MODEL_PATH, ATTENDANCE_PATH

class AttendanceSystem:
    def __init__(self):
        self.load_trained_model()
        self.attended_today = set()
        self.load_today_attendance()
        
    def load_trained_model(self):
        """Load pre-trained face encodings"""
        try:
            with open(TRAINED_MODEL_PATH, 'rb') as f:
                data = pickle.load(f)
                self.known_encodings = data["encodings"]
                self.known_names = data["names"]
            print("✅ Model loaded successfully!")
            print(f"✅ Loaded {len(self.known_names)} trained faces")
        except FileNotFoundError:
            print("❌ No trained model found. Please run improved_face_trainer.py first.")
            self.known_encodings = []
            self.known_names = []
    
    def load_today_attendance(self):
        """Load today's attendance records"""
        today_file = os.path.join(ATTENDANCE_PATH, f"attendance_{date.today()}.xlsx")
        if os.path.exists(today_file):
            try:
                df = pd.read_excel(today_file)
                self.attended_today = set(df['Name'].tolist())
                print(f"✅ Loaded today's attendance: {len(self.attended_today)} people")
            except:
                self.attended_today = set()
    
    def mark_attendance(self, name):
        """Mark attendance in Excel file"""
        if name in self.attended_today:
            return False
            
        today_file = os.path.join(ATTENDANCE_PATH, f"attendance_{date.today()}.xlsx")
        
        # Create new record
        new_record = {
            'Name': [name],
            'Time': [datetime.now().strftime("%H:%M:%S")],
            'Date': [date.today().strftime("%Y-%m-%d")]
        }
        
        df_new = pd.DataFrame(new_record)
        
        if os.path.exists(today_file):
            # Append to existing file
            df_existing = pd.read_excel(today_file)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_excel(today_file, index=False)
        else:
            # Create new file
            df_new.to_excel(today_file, index=False)
        
        self.attended_today.add(name)
        return True
    
    def run_attendance(self):
        """Main attendance system loop"""
        if not self.known_encodings:
            print("❌ No trained faces found.")
            return
        
        video_capture = cv2.VideoCapture(0)
        
        print("🚀 Starting attendance system...")
        print("📷 Look at the camera to mark attendance")
        print("⏹️  Press 'q' to quit")
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            
            # Find faces in the frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            for face_encoding, face_location in zip(face_encodings, face_locations):
                # Compare with known faces
                matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
                name = "Unknown"
                
                face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_names[best_match_index]
                        if self.mark_attendance(name):
                            print(f"✅ Attendance marked for: {name}")
                
                # Draw box and name
                top, right, bottom, left = face_location
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            cv2.imshow('🎯 Attendance System - Press Q to quit', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        video_capture.release()
        cv2.destroyAllWindows()
        print("📊 Attendance system stopped.")

if __name__ == "__main__":
    system = AttendanceSystem()
    system.run_attendance()
