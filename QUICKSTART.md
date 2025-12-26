
# Touchless UI - Hand Gesture Control System

## \ud83d\ude80 Get Started in 3 Simple Steps

### Step 1: Install Dependencies (2 minutes)
Open your terminal in this directory and run:

```bash# QUICK START GUIDE
pip install -r requirements.txt
```

Wait for installation to complete. This installs:
- opencv-python (for camera and video)
- mediapipe (for hand detection)
- numpy (for calculations)
- pyautogui (for mouse control)

---

### Step 2: Collect Gesture Data (5-10 minutes)
Run the data collection script:

```bash
python collect_gestures.py
```

Follow the on-screen instructions:

1. **Choose option 1** (collect all gestures)
2. **Enter number of samples**: 30 (recommended)

For each gesture:
- Position your hand clearly in front of webcam
- Press **SPACE** to capture each sample
- Press **Q** when you have enough samples
- Move to next gesture

**Gestures to collect:**
- \ud83d\udd90 **PALM**: Open hand, all fingers extended
- \u270a **FIST**: Closed hand, all fingers down
- \u270c **PEACE**: Index and middle fingers up (peace sign)
- \ud83d\udc4d **THUMBS UP**: Only thumb pointing up

**Tips:**
- Good lighting is important
- Keep hand in center of frame
- Vary hand angle slightly between samples
- Make clear, exaggerated gestures

---

### Step 3: Run the System
Start the touchless UI:

```bash
python main.py
```

**You're now controlling your computer with hand gestures!**

---

## \ud83c\udfae How to Use

Once the system is running:

| Your Gesture | What Happens |
|-------------|--------------|
| \ud83d\udd90 Show **PALM** | Screen **scrolls up** |
| \u270a Show **FIST** | Screen **scrolls down** |
| \u270c Show **PEACE** | **Left mouse click** |
| \ud83d\udc4d Show **THUMBS UP** | **Right mouse click** |

**To Exit:**
- Press **Q** key
- OR move mouse to corner of screen (FAILSAFE)

---

## \ud83d\udd27 Troubleshooting

**Problem: "No gesture data found" error**
- Solution: Run `python collect_gestures.py` first

**Problem: Webcam not working**
- Check if webcam is connected
- Close other apps using webcam
- Try different USB port

**Problem: Gestures not recognized**
- Make sure you collected enough samples (30+ per gesture)
- Ensure good lighting
- Make clear, exaggerated gestures
- Try recollecting data

**Problem: Actions happening too fast**
- The system has built-in cooldown (0.8 seconds)
- You can adjust this in main.py if needed

---

## \ud83d\udcdd What's Happening Behind the Scenes

1. **Webcam** captures your hand
2. **MediaPipe** detects 21 points on your hand
3. **System** compares these points with your training data
4. **Matches** your gesture to palm/fist/peace/thumbs_up
5. **Executes** the corresponding action

---

## \ud83d\udc4d Best Practices

\u2705 **DO:**
- Keep hand at consistent distance from camera
- Use good lighting
- Make clear, distinct gestures
- Hold gesture for 1 second
- Collect 30+ samples per gesture

\u274c **DON'T:**
- Cover the camera
- Use in dark room
- Make subtle gestures
- Overlap different gestures
- Rush through data collection

---

## \ud83c\udf93 Example Usage Scenarios

**Browsing Web:**
- Palm up: Scroll up through webpage
- Fist: Scroll down through webpage
- Peace: Click on links

**Watching Videos:**
- Fist: Scroll to find video
- Peace: Click to play/pause

**Presentations:**
- Palm up: Scroll up through slides
- Fist: Scroll down through slides
- Peace: Click to advance

---

## \ud83d\udcac Need Help

1. Read the troubleshooting section above
2. Check README.md for detailed documentation
3. Verify all dependencies installed correctly
4. Try recollecting gesture data

---

## ✨ Enjoy Your Touchless Experience

You're now ready to control your computer without touching anything!

**Remember:**
- Practice makes perfect
- Clear gestures work best
- Have fun experimenting!

---

## \ud83d\udcc4 File Overview

- `main.py` - Main program (run this after collecting data)
- `collect_gestures.py` - Data collection tool (run this first)
- `requirements.txt` - Python packages needed
- `gesture_data/` - Your training data (created automatically)
- `README.md` - Full documentation

---

**First time? Start with Step 1 above! \ud83d\udc46**
