"""
Gesture Data Collection Script
This script helps collect hand gesture data for training the gesture recognition system.
Run this script to create dataset files for palm, fist, peace, and thumbs_up gestures.
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import time

class GestureDataCollector:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Create gesture_data directory if it doesn't exist
        self.data_dir = "gesture_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Created directory: {self.data_dir}")
    
    def normalize_landmarks(self, landmarks):
        """
        Normalize hand landmarks relative to the wrist position.
        This makes the gesture data translation and scale invariant.
        """
        # Get wrist position (landmark 0)
        wrist = landmarks[0]
        
        # Calculate bounding box to normalize scale
        x_coords = [lm.x for lm in landmarks]
        y_coords = [lm.y for lm in landmarks]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Calculate scale factor
        scale = max(x_max - x_min, y_max - y_min)
        if scale == 0:
            scale = 1
        
        # Normalize each landmark
        normalized = []
        for lm in landmarks:
            norm_x = (lm.x - wrist.x) / scale
            norm_y = (lm.y - wrist.y) / scale
            normalized.extend([norm_x, norm_y])
        
        return normalized
    
    def collect_gesture_data(self, gesture_name, num_samples=30):
        """
        Collect multiple samples of a specific gesture.
        
        Args:
            gesture_name: Name of the gesture (palm, fist, peace, thumbs_up)
            num_samples: Number of samples to collect (default: 30)
        """
        cap = cv2.VideoCapture(0)
        collected_samples = []
        
        print(f"\n{'='*60}")
        print(f"Collecting data for: {gesture_name.upper()}")
        print(f"{'='*60}")
        print(f"Please show the '{gesture_name}' gesture to the camera.")
        print(f"Target: {num_samples} samples")
        print("Press 'SPACE' to capture a sample")
        print("Press 'Q' to finish and save")
        print("Press 'ESC' to cancel")
        print(f"{'='*60}\n")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = self.hands.process(rgb_frame)
            
            # Draw hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS
                    )
            
            # Display collection status
            cv2.putText(frame, f"Gesture: {gesture_name.upper()}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Collected: {len(collected_samples)}/{num_samples}", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "SPACE: Capture | Q: Save | ESC: Cancel", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, (255, 255, 255), 1)
            
            # Show frame
            cv2.imshow('Gesture Data Collection', frame)
            
            # Key handling
            key = cv2.waitKey(1) & 0xFF
            
            # Space bar - capture sample
            if key == 32:  # Space bar
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    normalized_data = self.normalize_landmarks(hand_landmarks.landmark)
                    collected_samples.append(normalized_data)
                    print(f"✓ Sample {len(collected_samples)} captured!")
                    
                    # Visual feedback
                    cv2.putText(frame, "CAPTURED!", (frame.shape[1]//2 - 100, frame.shape[0]//2), 
                               cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                    cv2.imshow('Gesture Data Collection', frame)
                    cv2.waitKey(200)
                    
                    if len(collected_samples) >= num_samples:
                        print(f"\n✓ Target reached! Collected {len(collected_samples)} samples.")
                        print("Press 'Q' to save or continue collecting more samples.")
                else:
                    print("✗ No hand detected! Please show your hand to the camera.")
            
            # Q - save and exit
            elif key == ord('q') or key == ord('Q'):
                if len(collected_samples) > 0:
                    break
                else:
                    print("No samples collected yet!")
            
            # ESC - cancel
            elif key == 27:  # ESC
                print("Collection cancelled.")
                cap.release()
                cv2.destroyAllWindows()
                return False
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Save collected data
        if len(collected_samples) > 0:
            file_path = os.path.join(self.data_dir, f"{gesture_name}.txt")
            with open(file_path, 'w') as f:
                for sample in collected_samples:
                    # Write 42 values (21 landmarks × 2 coordinates) as comma-separated
                    line = ','.join([str(val) for val in sample])
                    f.write(line + '\n')
            
            print(f"\n✓ Successfully saved {len(collected_samples)} samples to {file_path}")
            return True
        
        return False
    
    def collect_all_gestures(self, samples_per_gesture=30):
        """
        Collect data for all four gestures.
        """
        gestures = {
            'palm': 'Open palm (all fingers extended)',
            'fist': 'Closed fist (all fingers folded)',
            'peace': 'Peace sign (index and middle fingers up)',
            'thumbs_up': 'Thumbs up (only thumb extended)'
        }
        
        print("\n" + "="*60)
        print("GESTURE DATA COLLECTION SYSTEM")
        print("="*60)
        print("\nYou will collect data for 4 different gestures:")
        for gesture, description in gestures.items():
            print(f"  • {gesture}: {description}")
        
        print(f"\nSamples per gesture: {samples_per_gesture}")
        print("\nTips for better accuracy:")
        print("  1. Maintain consistent hand distance from camera")
        print("  2. Ensure good lighting")
        print("  3. Keep your hand in the center of the frame")
        print("  4. Vary hand rotation slightly between samples")
        print("="*60)
        
        input("\nPress ENTER to start collection...")
        
        for gesture_name, description in gestures.items():
            print(f"\n\nNext gesture: {gesture_name}")
            print(f"Description: {description}")
            input("Press ENTER when ready...")
            
            success = self.collect_gesture_data(gesture_name, samples_per_gesture)
            
            if not success:
                print(f"Skipped {gesture_name}")
            
            time.sleep(1)
        
        print("\n" + "="*60)
        print("DATA COLLECTION COMPLETE!")
        print("="*60)
        print(f"\nGesture data saved in '{self.data_dir}' directory:")
        for gesture in gestures.keys():
            file_path = os.path.join(self.data_dir, f"{gesture}.txt")
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    lines = len(f.readlines())
                print(f"  ✓ {gesture}.txt ({lines} samples)")
        print("\nYou can now run main.py to use the gesture recognition system!")
        print("="*60 + "\n")
    
    def __del__(self):
        """Cleanup"""
        self.hands.close()


def main():
    collector = GestureDataCollector()
    
    print("\nGesture Data Collection Options:")
    print("1. Collect all gestures (recommended)")
    print("2. Collect individual gesture")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == '1':
        samples = input("Enter number of samples per gesture (default 30): ").strip()
        samples = int(samples) if samples.isdigit() else 30
        collector.collect_all_gestures(samples_per_gesture=samples)
    
    elif choice == '2':
        print("\nAvailable gestures:")
        print("  1. palm")
        print("  2. fist")
        print("  3. peace")
        print("  4. thumbs_up")
        
        gesture_map = {'1': 'palm', '2': 'fist', '3': 'peace', '4': 'thumbs_up'}
        gesture_choice = input("\nEnter gesture number: ").strip()
        
        if gesture_choice in gesture_map:
            gesture_name = gesture_map[gesture_choice]
            samples = input("Enter number of samples (default 30): ").strip()
            samples = int(samples) if samples.isdigit() else 30
            collector.collect_gesture_data(gesture_name, samples)
        else:
            print("Invalid choice!")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
