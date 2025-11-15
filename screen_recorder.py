#!/usr/bin/env python3
"""
Desktop Screen Recorder
Captures desktop screenshots at 1-second intervals for 5 seconds.
"""

import time
import os
from datetime import datetime
from mss import mss
from PIL import Image


class ScreenRecorder:
    def __init__(self, output_dir="screenshots", duration=5, interval=1):
        """
        Initialize the screen recorder.

        Args:
            output_dir (str): Directory to save screenshots
            duration (int): Total recording duration in seconds
            interval (int): Time interval between captures in seconds
        """
        self.output_dir = output_dir
        self.duration = duration
        self.interval = interval
        self.screenshots = []

    def setup_output_directory(self):
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")
        else:
            print(f"Using existing output directory: {self.output_dir}")

    def capture_screen(self, filename):
        """
        Capture a screenshot of the entire screen.

        Args:
            filename (str): Name of the file to save the screenshot
        """
        with mss() as sct:
            # Get the first monitor (primary monitor)
            monitor = sct.monitors[1]

            # Capture the screen
            screenshot = sct.grab(monitor)

            # Convert to PIL Image
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

            # Save the image
            filepath = os.path.join(self.output_dir, filename)
            img.save(filepath)

            return filepath

    def record(self):
        """
        Start recording the screen.
        Captures screenshots at specified intervals for the specified duration.
        """
        self.setup_output_directory()

        print(f"Starting screen recording...")
        print(f"Duration: {self.duration} seconds")
        print(f"Interval: {self.interval} second(s)")
        print(f"Expected captures: {self.duration // self.interval}")
        print("-" * 50)

        start_time = time.time()
        capture_count = 0

        while time.time() - start_time < self.duration:
            # Calculate current elapsed time
            elapsed = time.time() - start_time

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{capture_count + 1:03d}_{timestamp}.png"

            # Capture screenshot
            try:
                filepath = self.capture_screen(filename)
                capture_count += 1
                self.screenshots.append(filepath)
                print(f"[{elapsed:.1f}s] Captured: {filename}")
            except Exception as e:
                print(f"Error capturing screenshot: {e}")

            # Wait for the next interval
            next_capture_time = start_time + (capture_count * self.interval)
            sleep_time = next_capture_time - time.time()

            if sleep_time > 0:
                time.sleep(sleep_time)

        print("-" * 50)
        print(f"Recording complete!")
        print(f"Total captures: {capture_count}")
        print(f"Screenshots saved to: {os.path.abspath(self.output_dir)}")

        return self.screenshots


def main():
    """Main function to run the screen recorder."""
    # Create recorder with default settings: 5 seconds duration, 1 second interval
    recorder = ScreenRecorder(
        output_dir="screenshots",
        duration=5,
        interval=1
    )

    # Start recording
    screenshots = recorder.record()

    # Display captured files
    print("\nCaptured files:")
    for i, filepath in enumerate(screenshots, 1):
        print(f"  {i}. {filepath}")


if __name__ == "__main__":
    main()
