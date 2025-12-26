# Touchless UI - Hand Gesture Control System

A real-time hand gesture recognition system that allows touchless control of your computer using webcam-based hand tracking. Control mouse actions and scrolling with simple hand gestures!

![Touchless UI Demo](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange.svg)

## 🎯 Features

- **Real-time Hand Tracking**: Uses MediaPipe for accurate hand landmark detection
- **4 Gesture Controls**:
  - 🖐 **Palm** (all fingers extended) → Scroll Up
  - ✊ **Fist** (closed hand) → Scroll Down
  - ✌ **Peace** (index + middle fingers) → Left Mouse Click
  - 👍 **Thumbs Up** → Right Mouse Click
- **Custom Gesture Training**: Collect your own gesture data for personalized recognition
- **Stable Recognition**: Uses majority voting to prevent false positives
- **Visual Feedback**: Real-time display of detected gestures and actions

## 🛠 Technologies Used

- **Python 3.7+**: Core programming language
- **OpenCV**: Video capture and image processing
- **MediaPipe**: Hand landmark detection (21 keypoints)
- **NumPy**: Numerical computations
- **PyAutoGUI**: System control (mouse and scrolling)

## 📋 Requirements

- Python 3.7 or higher
- Webcam
- Windows/Linux/macOS

## 🚀 Installation

### Step 1: Clone or Download the Repository

```bash
cd touchless-ui-master
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- opencv-python
- mediapipe
- numpy
- pyautogui

## 📖 Usage Guide

### Step 1: Collect Gesture Data (First Time Only)

Before using the system, you need to collect training data for the 4 gestures.

```bash
python collect_gestures.py
```

**Instructions:**
1. Choose option 1 to collect all gestures
2. For each gesture:
   - Position your hand in front of the webcam
   - Press **SPACE** to capture samples (30 recommended)
   - Press **Q** when done with that gesture
3. Gesture data will be saved in `gesture_data/` directory

**Tips for Better Accuracy:**
- Ensure good lighting
- Keep hand in center of frame
- Maintain consistent distance from camera
- Vary hand rotation slightly between samples
- Make clear, distinct gestures

### Step 2: Run the Touchless UI System

Once gesture data is collected, run the main program:

```bash
python main.py
```

**Controls:**
- Show gestures to the webcam to perform actions
- Press **Q** to quit
- Move mouse to screen corner for emergency stop (FAILSAFE)

## 🎮 Gesture Guide

| Gesture | Description | Action |
|---------|-------------|--------|
| 🖐 **Palm** | All fingers extended, hand open | **Scroll Up** |
| ✊ **Fist** | All fingers closed into fist | **Scroll Down** |
| ✌ **Peace** | Index and middle fingers up | **Left Click** |
| 👍 **Thumbs Up** | Only thumb extended upward | **Right Click** |

## 📁 Project Structure

```
touchless-ui-master/
│
├── main.py                 # Main gesture recognition and control system
├── collect_gestures.py     # Gesture data collection script
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── gesture_data/          # Gesture training data (created after collection)
│   ├── palm.txt
│   ├── fist.txt
│   ├── peace.txt
│   └── thumbs_up.txt
│
└── detection.py           # (Legacy - not used in current system)
└── control.py             # (Legacy - not used in current system)
```

## 🔧 How It Works

### 1. **Hand Detection**
- Webcam captures video frames
- MediaPipe detects hand and extracts 21 landmarks
- Each landmark has (x, y) coordinates

### 2. **Feature Extraction**
- Landmarks are normalized relative to wrist position
- Scale-invariant representation (42 features: 21 landmarks × 2 coordinates)

### 3. **Gesture Recognition**
- Current hand landmarks compared with stored gesture samples
- Euclidean distance calculated to find closest match
- Majority voting used for stability (5-frame window)

### 4. **Action Execution**
- Recognized gesture mapped to system action
- Cooldown period prevents repeated actions
- PyAutoGUI executes mouse/scroll commands

## ⚙️ Configuration

You can adjust these parameters in `main.py`:

```python
# In TouchlessUI.__init__():
self.action_cooldown = 0.8          # Cooldown between actions (seconds)
self.gesture_history = deque(maxlen=5)  # Frames for majority voting

# In recognize_gesture():
if min_distance > 0.5:  # Gesture recognition threshold
    return None

# In execute_action():
pyautogui.scroll(3)  # Scroll amount (adjust as needed)
```

## 🐛 Troubleshooting

### "No gesture data found" error
**Solution**: Run `python collect_gestures.py` first to create training data

### Webcam not detected
**Solution**: 
- Check if webcam is connected and working
- Try changing camera index in code: `cv2.VideoCapture(1)` instead of `cv2.VideoCapture(0)`

### Poor gesture recognition
**Solution**:
- Recollect gesture data with more samples
- Ensure good lighting conditions
- Keep hand at consistent distance from camera
- Make clear, exaggerated gestures
- Adjust recognition threshold in code

### Actions triggering too frequently
**Solution**: Increase `action_cooldown` value in `main.py`

## 🎓 Educational Value

This project demonstrates:
- **Computer Vision**: Real-time video processing
- **Machine Learning**: Feature extraction and pattern matching
- **Human-Computer Interaction**: Gesture-based interfaces
- **System Programming**: OS-level control via Python
- **Data Collection**: Creating custom training datasets

## 🔮 Future Enhancements

- [ ] Add more gestures (rock, OK sign, etc.)
- [ ] Volume control gestures
- [ ] Presentation control mode
- [ ] Virtual keyboard input
- [ ] Multi-hand gesture support
- [ ] Machine learning classifier (SVM/Random Forest)
- [ ] Gesture customization GUI
- [ ] Gesture recording and playback

## 📝 License

This project is open-source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 👏 Acknowledgments

- **MediaPipe** by Google for hand tracking
- **OpenCV** for computer vision tools
- **PyAutoGUI** for system control capabilities

## 📧 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are correctly installed
3. Verify your webcam is working
4. Try recollecting gesture data

---

**Enjoy your touchless UI experience! 🎉**
