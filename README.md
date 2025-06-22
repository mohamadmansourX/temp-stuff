# MediaPipe Pose Tracker Workspace

This workspace contains a web-based pose tracking application using MediaPipe that analyzes posture in real-time.

## Files

- `index.html` - Main HTML file with the web interface
- `lateral_neck_tilt.js` - JavaScript module containing pose analysis functions for lateral_neck_tilt

## Features

- Real-time pose detection using MediaPipe
- Posture analysis (shoulder and head alignment)
- Visual feedback on camera feed
- Console logging of posture status

## Usage

1. Open the workspace in VS Code
2. Start a local web server (recommended for HTTPS support)
3. Open `index.html` in a web browser
4. Grant camera permissions when prompted
5. View real-time pose analysis in the console

## Requirements

- Modern web browser with WebRTC support
- Camera access
- HTTPS connection (recommended for camera access)

## Functions

### `checkInitialPosition(landmarks, shoulderTol, headTol)`

Analyzes pose landmarks to determine if the person is in a proper initial position.

**Parameters:**
- `landmarks` - Array of pose landmarks from MediaPipe
- `shoulderTol` - Tolerance for shoulder angle (default: 10 degrees)
- `headTol` - Tolerance for head angle (default: 10 degrees)

**Returns:**
```javascript
{
  ok: boolean,           // true if posture is correct
  issues: string[],      // array of detected issues
  metrics: {
    shoulder_angle: { value: number, rule: string },
    head_angle: { value: number, rule: string }
  }
}
```
