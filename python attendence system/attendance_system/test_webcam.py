import cv2
import os
from config import FACE_DB_PATH

def capture_faces_better():
    print("🎯 Starting Face Capture System...")
    
    # Get person's name
    name = input("Enter person's name: ").strip()
    if not name:
        print("❌ Please enter a valid name!")
        return
    
    # Create person's folder
    person_path = os.path.join(FACE_DB_PATH, name)
    os.makedirs(person_path, exist_ok=True)
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not access webcam!")
        return
    
    print("\n📸 INSTRUCTIONS:")
    print("• Press 'C' to CAPTURE a photo")
    print("• Press 'Q' to QUIT")
    print("• Capture 10-15 photos from different angles")
    print("• Make sure your face is clearly visible")
    print("\nStarting capture in 3 seconds...")
    
    cv2.waitKey(3000)  # Wait 3 seconds
    
    count = 0
    while True:
        # Read frame from camera
        ret, frame = cap.read()
        if not ret:
            print("❌ Error reading from camera!")
            break
        
        # Display instruction on frame
        display_frame = frame.copy()
        cv2.putText(display_frame, f"Photos captured: {count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, "Press 'C' to CAPTURE, 'Q' to QUIT", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show the frame
        cv2.imshow('Face Capture - Press C to Capture, Q to Quit', display_frame)
        
        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('c') or key == ord('C'):
            # Capture and save image
            filename = f"{name}_{count}.jpg"
            filepath = os.path.join(person_path, filename)
            
            # Save the image
            success = cv2.imwrite(filepath, frame)
            
            if success:
                count += 1
                print(f"✅ Captured photo {count}: {filename}")
                
                # Show confirmation on screen
                confirmation_frame = frame.copy()
                cv2.putText(confirmation_frame, "PHOTO CAPTURED!", (50, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                cv2.imshow('Face Capture - Press C to Capture, Q to Quit', confirmation_frame)
                cv2.waitKey(500)  # Show confirmation for 0.5 seconds
            else:
                print(f"❌ Failed to save photo {count}")
                
        elif key == ord('q') or key == ord('Q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n🎉 Capture session completed!")
    print(f"📁 Saved {count} photos in: {person_path}")
    
    # Verify files were saved
    if os.path.exists(person_path):
        saved_files = [f for f in os.listdir(person_path) if f.endswith('.jpg')]
        print(f"📊 Verified {len(saved_files)} files in folder")

if __name__ == "__main__":
    capture_faces_better()