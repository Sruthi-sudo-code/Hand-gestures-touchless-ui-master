"""
Gesture Diagnostic Tool
This helps identify why gestures might not be working.
"""

import cv2
import mediapipe as mp
import numpy as np
import os

def check_gesture_data():
    """Check if gesture data is present and valid"""
    print("\n" + "="*60)
    print("CHECKING GESTURE DATA FILES")
    print("="*60)
    
    gestures = ['palm', 'fist', 'peace', 'thumbs_up']
    data_dir = 'gesture_data'
    
    all_ok = True
    for gesture in gestures:
        file_path = os.path.join(data_dir, f'{gesture}.txt')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                valid_lines = [l for l in lines if l.strip()]
                
                if len(valid_lines) > 0:
                    first_line = valid_lines[0].strip()
                    values = first_line.split(',')
                    
                    print(f"✓ {gesture}.txt")
                    print(f"  - Samples: {len(valid_lines)}")
                    print(f"  - Values per sample: {len(values)}")
                    
                    if len(values) != 42:
                        print(f"  ⚠ WARNING: Should have 42 values, has {len(values)}")
                        all_ok = False
                    if len(valid_lines) < 10:
                        print(f"  ⚠ WARNING: Only {len(valid_lines)} samples (recommend 20+)")
                else:
                    print(f"✗ {gesture}.txt is EMPTY!")
                    all_ok = False
        else:
            print(f"✗ {gesture}.txt NOT FOUND!")
            all_ok = False
    
    return all_ok


def test_hand_detection():
    """Test if hand can be detected from webcam"""
    print("\n" + "="*60)
    print("TESTING HAND DETECTION")
    print("="*60)
    print("\nShow your hand to the camera...")
    print("We'll check if MediaPipe can detect it.")
    print("Press 'Q' to continue\n")
    
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("✗ ERROR: Cannot access webcam!")
        return False
    
    detection_count = 0
    total_frames = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        total_frames += 1
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            detection_count += 1
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
            
            cv2.putText(frame, "HAND DETECTED!", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Detection rate: {detection_count}/{total_frames}", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "NO HAND DETECTED", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, "Show your hand clearly!", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        
        cv2.putText(frame, "Press Q to continue", (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.imshow('Hand Detection Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    
    detection_rate = (detection_count / total_frames * 100) if total_frames > 0 else 0
    
    print(f"\nDetection Results:")
    print(f"  Total frames: {total_frames}")
    print(f"  Hand detected: {detection_count} times")
    print(f"  Detection rate: {detection_rate:.1f}%")
    
    if detection_rate > 80:
        print("  ✓ EXCELLENT detection!")
    elif detection_rate > 50:
        print("  ⚠ FAIR detection - try better lighting")
    else:
        print("  ✗ POOR detection - improve lighting and hand position")
    
    return detection_rate > 50


def main():
    print("\n" + "="*60)
    print("GESTURE CONTROL DIAGNOSTIC TOOL")
    print("="*60)
    print("\nThis tool will help identify why gestures aren't working.\n")
    
    # Test 1: Check gesture data
    data_ok = check_gesture_data()
    
    if not data_ok:
        print("\n⚠ WARNING: Gesture data has issues!")
        print("Run: python collect_gestures.py to collect more samples")
    
    # Test 2: Check hand detection
    input("\nPress Enter to test hand detection...")
    detection_ok = test_hand_detection()
    
    # Summary
    print("\n" + "="*60)
    print("DIAGNOSTIC SUMMARY")
    print("="*60)
    
    if data_ok and detection_ok:
        print("\n✓ All tests passed!")
        print("\nIf gestures still don't work, check:")
        print("  1. Is YouTube video window ACTIVE? (click on it)")
        print("  2. Are you holding gestures for 1+ seconds?")
        print("  3. Are gestures clear and matching your training data?")
        print("  4. Is there 0.8s cooldown between actions?")
    else:
        print("\n⚠ Issues found:")
        if not data_ok:
            print("  - Gesture data needs attention")
            print("    → Run: python collect_gestures.py")
        if not detection_ok:
            print("  - Hand detection is poor")
            print("    → Improve lighting")
            print("    → Keep hand centered in camera")
            print("    → Move closer to camera (1-2 feet)")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDiagnostic cancelled.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
