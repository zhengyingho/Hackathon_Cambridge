# Desktop Screen Recorder

A Python-based desktop screen recorder that captures screenshots at regular intervals.

## Features

- Captures desktop screenshots at 1-second intervals
- Records for a total duration of 5 seconds (configurable)
- Saves screenshots as PNG images with timestamps
- Cross-platform support (Windows, macOS, Linux)

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

Run the screen recorder with default settings (5 seconds duration, 1 second interval):

```bash
python screen_recorder.py
```

This will:
- Create a `screenshots` directory
- Capture 5 screenshots (one every second)
- Save them as `screenshot_001_<timestamp>.png`, `screenshot_002_<timestamp>.png`, etc.

### Custom Usage

You can also import and use the `ScreenRecorder` class in your own code:

```python
from screen_recorder import ScreenRecorder

# Create a recorder with custom settings
recorder = ScreenRecorder(
    output_dir="my_screenshots",  # Custom output directory
    duration=10,                   # Record for 10 seconds
    interval=2                     # Capture every 2 seconds
)

# Start recording
screenshots = recorder.record()

# Access the list of captured screenshot paths
for screenshot in screenshots:
    print(screenshot)
```

## Requirements

- Python 3.6+
- mss (for fast screen capture)
- Pillow (for image processing)

## Output

Screenshots are saved in the `screenshots` directory (or your custom directory) with the following naming convention:

```
screenshot_001_20231115_143022.png
screenshot_002_20231115_143023.png
screenshot_003_20231115_143024.png
...
```

## License

MIT License