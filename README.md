# Vibe Detector & Camera Recorder

A Python-based camera recorder with AI-powered vibe detection that analyzes if people are moving excitedly to music.

## Features

- **Vibe Detection**: Uses Claude's vision API to analyze if people are vibing to music
- **Camera Recording**: Captures images from laptop webcam at configurable intervals
- **Temporal Analysis**: Compares multiple frames to detect movement and energy
- **Customizable**: Configurable duration, intervals, and camera selection
- **AI-Powered**: Leverages Claude's advanced vision capabilities for accurate analysis
- Cross-platform support (Windows, macOS, Linux)
- Easy to use and customize

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Hackathon_Cambridge
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Anthropic API key (required for vibe detection):
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Get your API key from: https://console.anthropic.com/

## Usage

### Vibe Detection (Main Feature)

Detect if someone is vibing to music using AI analysis:

```bash
# Basic usage (10 seconds, 1 second intervals)
python vibe_detector.py

# Quick check (5 seconds, faster captures)
python vibe_detector.py --duration 5 --interval 0.5

# Extended analysis (30 seconds)
python vibe_detector.py --duration 30 --interval 2

# Use external camera
python vibe_detector.py --camera 1

# Pass API key directly
python vibe_detector.py --api-key 'your-key-here'
```

**What it does:**
1. Captures images from your camera at specified intervals
2. Sends images to Claude's vision API for analysis
3. Detects if the person is moving excitedly, dancing, or vibing to music
4. Provides confidence scores and detailed descriptions
5. Shows overall verdict: "PERSON IS VIBING!" or "Not really vibing"

### Camera Recorder Only

Run the camera recorder without AI analysis:

```bash
python camera_recorder.py
```

This will:
- Create a `camera_images` directory
- Capture 5 images from your camera (one every second)
- Save them as `camera_001_<timestamp>.jpg`, `camera_002_<timestamp>.jpg`, etc.

### Custom Usage

You can also import and use the `CameraRecorder` class in your own code:

```python
from camera_recorder import CameraRecorder

# Create a recorder with custom settings
recorder = CameraRecorder(
    output_dir="my_camera_images",  # Custom output directory
    duration=10,                     # Record for 10 seconds
    interval=2,                      # Capture every 2 seconds
    camera_index=0                   # Camera device (0=default, 1=external, etc.)
)

# Start recording
images = recorder.record()

# Access the list of captured image paths
for image in images:
    print(image)
```

### Programmatic Usage

You can also use the components in your own code:

**Vibe Detector:**
```python
from vibe_detector import VibeDetector

detector = VibeDetector(api_key='your-api-key')
result = detector.run(duration=10, interval=1, use_temporal_analysis=True)

if result['is_vibing']:
    print(f"Person is vibing! (Confidence: {result['confidence']}%)")
```

**Vibe Analyzer (analyze existing images):**
```python
from vibe_analyzer import VibeAnalyzer

analyzer = VibeAnalyzer(api_key='your-api-key')

# Analyze single image
result = analyzer.analyze_single_image('path/to/image.jpg')

# Analyze sequence of images
images = ['image1.jpg', 'image2.jpg', 'image3.jpg']
result = analyzer.analyze_sequence(images)

# Temporal comparison (best for detecting movement)
result = analyzer.analyze_with_comparison(images)
```

## Requirements

- Python 3.6+
- OpenCV (opencv-python) for camera access
- NumPy for image processing
- Anthropic SDK for AI-powered vibe detection
- A working webcam/camera
- Anthropic API key (for vibe detection features)

## Output

### Camera Images

Camera images are saved in the `vibe_images` directory (or `camera_images` for standalone recorder) with the following naming convention:

```
camera_001_20231115_143022.jpg
camera_002_20231115_143023.jpg
camera_003_20231115_143024.jpg
...
```

### Vibe Analysis Results

The vibe detector provides detailed analysis output:

```
🎵 🎵 🎵 ... VIBE DETECTOR ... 🎵 🎵 🎵
Checking if you're vibing to the music!

Step 1: Capturing images from camera...
  Duration: 10 seconds
  Interval: 1 second(s)
  Expected captures: 10

[Captures images...]

✓ Successfully captured 10 images

Step 2: Analyzing images with Claude's vision API...

============================================================
TEMPORAL VIBE ANALYSIS
============================================================
Images analyzed: 10
Vibing detected: YES
Confidence: 85%
Movement detected: YES
Energy level: HIGH

Analysis: The person shows significant movement between frames
with raised arms, dancing motions, and visible excitement.
Body position changes indicate rhythmic movement consistent
with dancing to music.

🎉 PERSON IS VIBING!
============================================================
```

## Troubleshooting

**Camera not working?**
- Make sure your camera is not being used by another application
- Check that your camera is properly connected and enabled
- Try different camera indices (0, 1, 2) if you have multiple cameras using `--camera` flag
- On Linux, you may need to install additional packages: `sudo apt-get install libopencv-dev python3-opencv`

**API key issues?**
- Ensure you've set the `ANTHROPIC_API_KEY` environment variable
- Verify your API key is valid at https://console.anthropic.com/
- Check that you have available API credits
- Try passing the key directly with `--api-key` flag

**Vibe detection not accurate?**
- Ensure good lighting for better image quality
- Try longer duration for more frames to analyze (e.g., `--duration 15`)
- Use faster intervals for more data points (e.g., `--interval 0.5`)
- Make sure there's visible movement between frames
- Position yourself fully in frame of the camera

## License

MIT License