"""
Data Converter Script
Converts existing gesture data from mediapipe folder to the new format.
This allows you to use your already collected gesture samples!
"""

import os
import shutil

def convert_gesture_data():
    """Convert existing gesture data to new format"""
    
    print("\n" + "="*60)
    print("GESTURE DATA CONVERTER")
    print("="*60)
    print("\nConverting existing gesture data from 'mediapipe/' folder")
    print("to 'gesture_data/' folder for the new video control system...\n")
    
    # Mapping: old filename -> new filename
    gesture_mapping = {
        'palm.txt': 'palm.txt',      # Palm stays palm
        'stone.txt': 'fist.txt',      # Stone becomes fist
        # We'll need to create peace and thumbs_up manually
    }
    
    # Create gesture_data directory if it doesn't exist
    if not os.path.exists('gesture_data'):
        os.makedirs('gesture_data')
        print("✓ Created gesture_data directory")
    
    # Copy and convert existing files
    converted = []
    for old_name, new_name in gesture_mapping.items():
        old_path = os.path.join('mediapipe', old_name)
        new_path = os.path.join('gesture_data', new_name)
        
        if os.path.exists(old_path):
            shutil.copy(old_path, new_path)
            print(f"✓ Converted: {old_name} -> {new_name}")
            converted.append(new_name)
        else:
            print(f"⚠ Not found: {old_name}")
    
    # Check what's missing
    required = ['palm.txt', 'fist.txt', 'peace.txt', 'thumbs_up.txt']
    missing = [g for g in required if g not in converted and not os.path.exists(f'gesture_data/{g}')]
    
    print("\n" + "="*60)
    print("CONVERSION COMPLETE!")
    print("="*60)
    
    if converted:
        print("\n✓ Converted gestures:")
        for name in converted:
            print(f"  - {name}")
    
    if missing:
        print(f"\n⚠ Missing gestures: {missing}")
        print("\nYou need to collect data for these gestures:")
        print("  Run: python collect_gestures.py")
        print("  Choose option 2 (collect individual gesture)")
        for gesture in missing:
            gesture_name = gesture.replace('.txt', '')
            print(f"  - Collect: {gesture_name}")
    else:
        print("\n✓ All gesture data ready!")
        print("\nYou can now run: python main.py")
        print("To start controlling videos with hand gestures!")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        convert_gesture_data()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
