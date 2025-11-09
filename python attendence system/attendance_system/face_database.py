import face_recognition
import pickle
import os
import cv2
from config import FACE_DB_PATH, TRAINED_MODEL_PATH

def train_faces_improved():
    """Train face recognition model with better face detection"""
    known_encodings = []
    known_names = []
    
    print("🔍 Training face recognition model (improved)...")
    
    if not os.path.exists(FACE_DB_PATH):
        print("❌ Face database folder not found!")
        return
    
    total_images = 0
    faces_found = 0
    
    for person_name in os.listdir(FACE_DB_PATH):
        person_path = os.path.join(FACE_DB_PATH, person_name)
        
        if os.path.isdir(person_path):
            print(f"\n👤 Processing: {person_name}")
            
            for image_file in os.listdir(person_path):
                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    total_images += 1
                    image_path = os.path.join(person_path, image_file)
                    
                    try:
                        # Load image
                        image = face_recognition.load_image_file(image_path)
                        
                        # Try multiple face detection methods
                        # Method 1: Default
                        face_locations = face_recognition.face_locations(image)
                        
                        if not face_locations:
                            # Method 2: Use CNN model (more accurate but slower)
                            face_locations = face_recognition.face_locations(image, model="cnn")
                        
                        if face_locations:
                            # Get encodings for the first face found
                            face_encodings = face_recognition.face_encodings(image, face_locations)
                            
                            if face_encodings:
                                known_encodings.append(face_encodings[0])
                                known_names.append(person_name)
                                faces_found += 1
                                print(f"  ✅ Face found in: {image_file}")
                            else:
                                print(f"  ⚠️  Face detected but no encoding: {image_file}")
                        else:
                            print(f"  ❌ No face detected in: {image_file}")
                            
                    except Exception as e:
                        print(f"  ❌ Error with {image_file}: {e}")
    
    # Save trained model
    if known_encodings:
        model_data = {
            "encodings": known_encodings,
            "names": known_names
        }
        
        os.makedirs(os.path.dirname(TRAINED_MODEL_PATH), exist_ok=True)
        
        with open(TRAINED_MODEL_PATH, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"\n🎉 Training Summary:")
        print(f"📁 Total images processed: {total_images}")
        print(f"👤 Faces successfully trained: {faces_found}")
        print(f"💾 Model saved to: {TRAINED_MODEL_PATH}")
    else:
        print("\n❌ No faces were trained! Check your images.")

if __name__ == "__main__":
    train_faces_improved()