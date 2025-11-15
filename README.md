# Camera Recorder

A Python-based camera recorder that captures images from your laptop camera at regular intervals.

## Features

- Captures images from laptop webcam at 1-second intervals
- Records for a total duration of 5 seconds (configurable)
- Saves images as JPG files with timestamps
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

## Usage

### Basic Usage

Run the camera recorder with default settings (5 seconds duration, 1 second interval):

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

## Requirements

- Python 3.6+
- OpenCV (opencv-python) for camera access
- NumPy for image processing
- A working webcam/camera

## Output

Camera images are saved in the `camera_images` directory (or your custom directory) with the following naming convention:

```
camera_001_20231115_143022.jpg
camera_002_20231115_143023.jpg
camera_003_20231115_143024.jpg
...
```

## Troubleshooting

**Camera not working?**
- Make sure your camera is not being used by another application
- Check that your camera is properly connected and enabled
- Try different camera indices (0, 1, 2) if you have multiple cameras
- On Linux, you may need to install additional packages: `sudo apt-get install libopencv-dev python3-opencv`

## License

MIT License