@echo off
echo ============================================================
echo   TOUCHLESS VIDEO CONTROL - Starting...
echo ============================================================
echo.
echo Make sure you have:
echo   1. Webcam connected
echo   2. Good lighting
echo   3. A video ready to control (YouTube, Netflix, VLC, etc.)
echo.
echo After the webcam window opens:
echo   - Open and play a video
echo   - CLICK on the video to make it active
echo   - Show gestures to control it!
echo.
echo Press any key to start...
pause >nul
echo.
echo Starting system...
echo.
python main.py
echo.
echo.
echo System stopped.
pause
