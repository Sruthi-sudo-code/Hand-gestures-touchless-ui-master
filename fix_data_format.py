"""
Fix Gesture Data Format
Converts the existing gesture data to the correct format for the system.
Each line should have exactly 42 values (21 landmarks x 2 coordinates).
"""

import os
import re

def clean_and_reformat_file(input_file, output_file):
    """Clean and reformat gesture data file"""
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Remove all spaces and newlines, keep only numbers and commas
    content = content.replace(' ', '').replace('\n', ',')
    
    # Split by comma and filter out empty strings
    values = [v.strip() for v in content.split(',') if v.strip()]
    
    # Group into sets of 42 values (21 landmarks × 2 coordinates)
    samples = []
    for i in range(0, len(values), 42):
        if i + 42 <= len(values):
            sample = values[i:i+42]
            samples.append(','.join(sample))
    
    # Write reformatted data
    with open(output_file, 'w') as f:
        for sample in samples:
            f.write(sample + '\n')
    
    return len(samples)


def main():
    print("\n" + "="*60)
    print("GESTURE DATA FORMAT FIXER")
    print("="*60)
    print("\nReformatting gesture data to correct format...\n")
    
    gestures = ['palm', 'fist', 'peace', 'thumbs_up']
    data_dir = 'gesture_data'
    
    total_samples = 0
    
    for gesture in gestures:
        input_file = os.path.join(data_dir, f'{gesture}.txt')
        
        if os.path.exists(input_file):
            # Create backup
            backup_file = os.path.join(data_dir, f'{gesture}_backup.txt')
            with open(input_file, 'r') as f_in, open(backup_file, 'w') as f_out:
                f_out.write(f_in.read())
            
            # Reformat
            try:
                samples = clean_and_reformat_file(input_file, input_file)
                print(f"✓ {gesture}.txt - Reformatted {samples} samples")
                total_samples += samples
            except Exception as e:
                print(f"✗ {gesture}.txt - Error: {e}")
        else:
            print(f"⚠ {gesture}.txt - Not found")
    
    print("\n" + "="*60)
    print("REFORMATTING COMPLETE!")
    print("="*60)
    print(f"\nTotal samples reformatted: {total_samples}")
    print("\nBackup files created in gesture_data/ folder")
    print("(Files ending with _backup.txt)")
    print("\nYou can now run: python main.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
