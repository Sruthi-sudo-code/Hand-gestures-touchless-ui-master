"""
System Test Script
This script tests if all dependencies are installed correctly
and if the webcam is accessible.
"""

import sys

def test_imports():
    """Test if all required packages are installed"""
    print("\n" + "="*60)
    print("TESTING DEPENDENCIES")
    print("="*60 + "\n")
    
    modules = {
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe',
        'numpy': 'numpy',
        'pyautogui': 'pyautogui'
    }
    
    failed = []
    
    for module, package in modules.items():
        try:
            __import__(module)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            failed.append(package)
    
    if failed:
        print("\n" + "="*60)
        print("INSTALLATION REQUIRED")
        print("="*60)
        print("\nMissing packages:", ", ".join(failed))
        print("\nTo install, run:")
        print("  pip install " + " ".join(failed))
        print("\nOr install all dependencies:")
        print("  pip install -r requirements.txt")
        print("="*60 + "\n")
        return False
    
    print("\n✓ All dependencies installed successfully!")
    return True


def test_webcam():
    """Test if webcam is accessible"""
    print("\n" + "="*60)
    print("TESTING WEBCAM")
    print("="*60 + "\n")
    
    try:
        import cv2
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Webcam could not be opened")
            print("\nTroubleshooting:")
            print("  1. Check if webcam is connected")
            print("  2. Close other apps using webcam")
            print("  3. Try different USB port")
            print("  4. Check camera permissions in system settings")
            cap.release()
            return False
        
        # Try to read a frame
        ret, frame = cap.read()
        
        if not ret or frame is None:
            print("✗ Could not capture frame from webcam")
            cap.release()
            return False
        
        print(f"✓ Webcam is working!")
        print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
        
        # Show a test frame
        print("\nDisplaying test frame for 3 seconds...")
        print("(Close the window with 'Q' or wait)")
        
        cv2.putText(frame, "Webcam Test - Press Q to close", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Webcam Test', frame)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        
        cap.release()
        print("✓ Webcam test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error testing webcam: {e}")
        return False


def test_mediapipe():
    """Test if MediaPipe hand detection works"""
    print("\n" + "="*60)
    print("TESTING MEDIAPIPE HAND DETECTION")
    print("="*60 + "\n")
    
    try:
        import cv2
        import mediapipe as mp
        
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        
        print("✓ MediaPipe initialized successfully!")
        print("\nTesting hand detection...")
        print("Show your hand to the camera (10 seconds)")
        print("Press 'Q' to skip")
        
        cap = cv2.VideoCapture(0)
        mp_drawing = mp.solutions.drawing_utils
        
        hand_detected = False
        start_time = cv2.getTickCount()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                hand_detected = True
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, "HAND DETECTED!", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Show your hand", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.putText(frame, "Press Q to continue", (10, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow('MediaPipe Test', frame)
            
            elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
            
            if cv2.waitKey(1) & 0xFF == ord('q') or elapsed > 10:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        
        if hand_detected:
            print("✓ Hand detection working perfectly!")
        else:
            print("⚠ No hand detected (this is OK if you didn't show your hand)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing MediaPipe: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_gesture_data():
    """Check if gesture data exists"""
    print("\n" + "="*60)
    print("CHECKING GESTURE DATA")
    print("="*60 + "\n")
    
    import os
    
    if not os.path.exists('gesture_data'):
        print("✗ gesture_data directory not found")
        print("\nNext step:")
        print("  Run: python collect_gestures.py")
        print("  This will create gesture training data")
        return False
    
    gestures = ['palm', 'fist', 'peace', 'thumbs_up']
    found = []
    missing = []
    
    for gesture in gestures:
        path = f'gesture_data/{gesture}.txt'
        if os.path.exists(path):
            with open(path, 'r') as f:
                lines = len(f.readlines())
            print(f"✓ {gesture}.txt found ({lines} samples)")
            found.append(gesture)
        else:
            print(f"✗ {gesture}.txt not found")
            missing.append(gesture)
    
    if missing:
        print(f"\n⚠ Missing gesture data: {missing}")
        print("\nNext step:")
        print("  Run: python collect_gestures.py")
        print("  Collect data for all gestures")
        return False
    
    print("\n✓ All gesture data files found!")
    return True


def main():
    print("\n" + "="*60)
    print("TOUCHLESS UI SYSTEM TEST")
    print("="*60)
    print("\nThis script will test if everything is set up correctly.")
    
    results = {
        'Dependencies': test_imports(),
        'Webcam': False,
        'MediaPipe': False,
        'Gesture Data': False
    }
    
    if results['Dependencies']:
        results['Webcam'] = test_webcam()
        
        if results['Webcam']:
            results['MediaPipe'] = test_mediapipe()
        
        results['Gesture Data'] = check_gesture_data()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60 + "\n")
    
    for test, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test}")
    
    print("\n" + "="*60)
    
    all_passed = all(results.values())
    
    if all_passed:
        print("SUCCESS! System is ready to use!")
        print("="*60)
        print("\nNext step:")
        print("  Run: python main.py")
        print("\nEnjoy your touchless UI experience! 🎉")
    else:
        print("SETUP INCOMPLETE")
        print("="*60)
        print("\nPlease fix the failed tests above.")
        
        if not results['Dependencies']:
            print("\n1. Install dependencies:")
            print("   pip install -r requirements.txt")
        
        if not results['Gesture Data']:
            print("\n2. Collect gesture data:")
            print("   python collect_gestures.py")
        
        if not results['Webcam']:
            print("\n3. Fix webcam issues (see troubleshooting above)")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
