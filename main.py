"""
Touchless UI - Hand Gesture Recognition and Control System
This is the main program that recognizes hand gestures in real-time and controls ANY video player.

Universal Video Control Gestures:
- Palm (all fingers extended) → Play/Pause Video (Spacebar)
- Fist (all fingers closed) → Volume Down (Down Arrow)
- Peace (index + middle fingers up) → Volume Up (Up Arrow)
- Thumbs Up (only thumb up) → Fullscreen Toggle (F key)

Works with: YouTube, Netflix, VLC, Windows Media Player, and all video players!
"""

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import os
import time
from collections import deque

class TouchlessUI:
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
        
        # Load gesture data
        self.gesture_data = {}
        self.data_dir = "gesture_data"
        self.load_all_gestures()
        
        # Gesture-to-action mapping for UNIVERSAL VIDEO CONTROL
        self.gesture_actions = {
            'palm': self.play_pause,
            'fist': self.volume_down,
            'peace': self.volume_up,
            'thumbs_up': self.fullscreen_toggle
        }
        
        # Action cooldown to prevent repeated actions
        self.last_action_time = 0
        self.action_cooldown = 0.8  # seconds
        
        # Gesture stability (use majority voting)
        self.gesture_history = deque(maxlen=5)
        
        # PyAutoGUI settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to stop
        pyautogui.PAUSE = 0.1
        
        print("\n✓ Touchless UI System initialized successfully!")
        print(f"✓ Loaded {len(self.gesture_data)} gesture(s)")
    
    def normalize_landmarks(self, landmarks):
        """
        Normalize hand landmarks relative to the wrist position.
        Same normalization used during data collection.
        """
        wrist = landmarks[0]
        
        # Calculate bounding box
        x_coords = [lm.x for lm in landmarks]
        y_coords = [lm.y for lm in landmarks]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Calculate scale
        scale = max(x_max - x_min, y_max - y_min)
        if scale == 0:
            scale = 1
        
        # Normalize
        normalized = []
        for lm in landmarks:
            norm_x = (lm.x - wrist.x) / scale
            norm_y = (lm.y - wrist.y) / scale
            normalized.extend([norm_x, norm_y])
        
        return np.array(normalized)
    
    def load_gesture_file(self, gesture_name):
        """
        Load gesture data from file.
        """
        file_path = os.path.join(self.data_dir, f"{gesture_name}.txt")
        
        if not os.path.exists(file_path):
            print(f"⚠ Warning: {file_path} not found!")
            return None
        
        samples = []
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    values = [float(x) for x in line.split(',')]
                    if len(values) == 42:  # 21 landmarks × 2 coordinates
                        samples.append(np.array(values))
        
        if len(samples) > 0:
            print(f"  ✓ Loaded {gesture_name}: {len(samples)} samples")
            return np.array(samples)
        else:
            print(f"  ✗ No valid samples in {gesture_name}.txt")
            return None
    
    def load_all_gestures(self):
        """
        Load all gesture data files.
        """
        gestures = ['palm', 'fist', 'peace', 'thumbs_up']
        
        print("\nLoading gesture data...")
        for gesture in gestures:
            data = self.load_gesture_file(gesture)
            if data is not None:
                self.gesture_data[gesture] = data
        
        if len(self.gesture_data) == 0:
            print("\n✗ ERROR: No gesture data found!")
            print("Please run 'python collect_gestures.py' first to collect gesture data.")
            raise FileNotFoundError("Gesture data not found. Run collect_gestures.py first.")
    
    def calculate_distance(self, sample1, sample2):
        """
        Calculate Euclidean distance between two gesture samples.
        """
        return np.linalg.norm(sample1 - sample2)
    
    def recognize_gesture(self, hand_landmarks):
        """
        Recognize gesture by comparing with stored samples.
        Uses minimum average distance to all samples of each gesture.
        """
        # Normalize current hand landmarks
        current_sample = self.normalize_landmarks(hand_landmarks)
        
        # Calculate average distance to each gesture
        min_distance = float('inf')
        recognized_gesture = None
        
        for gesture_name, gesture_samples in self.gesture_data.items():
            # Calculate distance to all samples
            distances = [self.calculate_distance(current_sample, sample) 
                        for sample in gesture_samples]
            
            # Use minimum distance (closest match)
            avg_distance = min(distances)
            
            if avg_distance < min_distance:
                min_distance = avg_distance
                recognized_gesture = gesture_name
        
        # Threshold to avoid false positives
        if min_distance > 0.5:  # Adjust this threshold as needed
            return None
        
        return recognized_gesture
    
    def get_stable_gesture(self, current_gesture):
        """
        Use majority voting to stabilize gesture recognition.
        """
        self.gesture_history.append(current_gesture)
        
        # Count occurrences
        if current_gesture is None:
            return None
        
        # Require majority consensus
        gesture_counts = {}
        for g in self.gesture_history:
            if g is not None:
                gesture_counts[g] = gesture_counts.get(g, 0) + 1
        
        if len(gesture_counts) > 0:
            most_common = max(gesture_counts, key=gesture_counts.get)
            if gesture_counts[most_common] >= 3:  # At least 3 out of 5
                return most_common
        
        return None
    
    # ===== Universal Video Control Actions =====
    # These work with YouTube, Netflix, VLC, and most video players!
    
    def play_pause(self):
        """Play/Pause video (Palm gesture) - Works on ALL video players"""
        pyautogui.press('space')  # Universal play/pause key
        print("⏯ Play/Pause")
    
    def volume_up(self):
        """Increase volume (Peace gesture) - Works on ALL video players"""
        pyautogui.press('up')  # Up arrow = volume up (most players)
        print("🔊 Volume Up")
    
    def volume_down(self):
        """Decrease volume (Fist gesture) - Works on ALL video players"""
        pyautogui.press('down')  # Down arrow = volume down (most players)
        print("🔉 Volume Down")
    
    def fullscreen_toggle(self):
        """Toggle fullscreen (Thumbs Up gesture) - Works on most video players"""
        pyautogui.press('f')  # F key = fullscreen toggle
        print("🖥 Fullscreen Toggle")
    
    def execute_action(self, gesture):
        """
        Execute action associated with the recognized gesture.
        Includes cooldown to prevent repeated actions.
        """
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_action_time < self.action_cooldown:
            return
        
        # Execute action
        if gesture in self.gesture_actions:
            try:
                self.gesture_actions[gesture]()
                self.last_action_time = current_time
            except Exception as e:
                print(f"Error executing action: {e}")
    
    def draw_gesture_info(self, frame, gesture, stable_gesture):
        """
        Draw gesture information on the frame.
        """
        height, width = frame.shape[:2]
        
        # Draw semi-transparent overlay at the top
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 120), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
        
        # Current gesture
        if gesture:
            cv2.putText(frame, f"Detected: {gesture.upper()}", (10, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        else:
            cv2.putText(frame, "Detected: None", (10, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 128), 2)
        
        # Stable gesture (what will be executed)
        if stable_gesture:
            cv2.putText(frame, f"Action: {stable_gesture.upper()}", (10, 75), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show action description
            action_desc = {
                'palm': 'Play/Pause',
                'fist': 'Volume Down',
                'peace': 'Volume Up',
                'thumbs_up': 'Fullscreen'
            }
            cv2.putText(frame, f"-> {action_desc.get(stable_gesture, '')}", 
                       (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Instructions at the bottom
        cv2.putText(frame, "Press 'Q' to quit | Move mouse to corner for FAILSAFE", 
                   (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, (255, 255, 255), 1)
        
        return frame
    
    def draw_gesture_legend(self, frame):
        """
        Draw gesture legend on the frame.
        """
        height, width = frame.shape[:2]
        
        # Legend background
        legend_width = 250
        legend_height = 180
        x_start = width - legend_width - 10
        y_start = 10
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (x_start, y_start), 
                     (x_start + legend_width, y_start + legend_height), 
                     (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)
        
        # Legend title
        cv2.putText(frame, "Gestures:", (x_start + 10, y_start + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Gesture list for VIDEO CONTROL
        gestures_info = [
            ("Palm", "Play/Pause", (0, 255, 255)),
            ("Fist", "Vol Down", (0, 255, 255)),
            ("Peace", "Vol Up", (0, 255, 255)),
            ("Thumbs Up", "Fullscreen", (0, 255, 255))
        ]
        
        y_offset = 50
        for gesture, action, color in gestures_info:
            cv2.putText(frame, f"{gesture}: {action}", 
                       (x_start + 10, y_start + y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
            y_offset += 30
        
        return frame
    
    def run(self):
        """
        Main loop: capture video, detect gestures, and execute actions.
        """
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Error: Cannot access webcam!")
            return
        
        print("\n" + "="*60)
        print("TOUCHLESS VIDEO CONTROL - RUNNING")
        print("="*60)
        print("\nUniversal Video Control Gestures:")
        print("  🖐  Palm       → Play/Pause (Spacebar)")
        print("  ✊  Fist       → Volume Down (⬇)")
        print("  ✌  Peace      → Volume Up (⬆)")
        print("  👍  Thumbs Up → Fullscreen Toggle (F)")
        print("\n💡 Works with ANY video player:")
        print("   YouTube, Netflix, VLC, Media Player, etc.")
        print("\n📌 Make sure the video window is active/focused!")
        print("\nPress 'Q' to quit")
        print("Move mouse to screen corner for emergency stop (FAILSAFE)")
        print("="*60 + "\n")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process frame
                results = self.hands.process(rgb_frame)
                
                current_gesture = None
                
                # Detect and recognize gesture
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Draw hand landmarks
                        self.mp_drawing.draw_landmarks(
                            frame, 
                            hand_landmarks, 
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                            self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                        )
                        
                        # Recognize gesture
                        current_gesture = self.recognize_gesture(hand_landmarks.landmark)
                
                # Get stable gesture
                stable_gesture = self.get_stable_gesture(current_gesture)
                
                # Execute action if gesture is stable
                if stable_gesture:
                    self.execute_action(stable_gesture)
                
                # Draw UI elements
                frame = self.draw_gesture_info(frame, current_gesture, stable_gesture)
                frame = self.draw_gesture_legend(frame)
                
                # Show frame
                cv2.imshow('Touchless UI - Hand Gesture Control', frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        
        except pyautogui.FailSafeException:
            print("\n\n✓ FAILSAFE activated - mouse moved to corner")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("\n✓ Touchless UI System stopped")
            print("="*60 + "\n")
    
    def __del__(self):
        """Cleanup"""
        self.hands.close()


def main():
    print("\n" + "="*60)
    print("TOUCHLESS VIDEO CONTROL - HAND GESTURE SYSTEM")
    print("="*60)
    print("\n🎬 Control ANY video without touching the screen!")
    print("   Works with: YouTube, Netflix, VLC, and more...")
    print("="*60)
    
    # Check if gesture data exists
    if not os.path.exists("gesture_data"):
        print("\n✗ ERROR: gesture_data directory not found!")
        print("\nPlease follow these steps:")
        print("  1. Run: python collect_gestures.py")
        print("  2. Collect data for all 4 gestures")
        print("  3. Then run this program again")
        print("="*60 + "\n")
        return
    
    # Check for gesture files
    required_gestures = ['palm', 'fist', 'peace', 'thumbs_up']
    missing_gestures = []
    
    for gesture in required_gestures:
        if not os.path.exists(f"gesture_data/{gesture}.txt"):
            missing_gestures.append(gesture)
    
    if missing_gestures:
        print(f"\n⚠ Warning: Missing gesture data files: {missing_gestures}")
        print("\nRecommendation:")
        print("  Run: python collect_gestures.py")
        print(f"  Collect data for: {', '.join(missing_gestures)}")
        
        response = input("\nContinue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return
    
    # Initialize and run
    try:
        ui = TouchlessUI()
        ui.run()
    
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease run 'python collect_gestures.py' first!")
    
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
