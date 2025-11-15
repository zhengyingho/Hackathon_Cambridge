#!/usr/bin/env python3
"""
Camera Recorder
Captures images from laptop camera at 1-second intervals for 5 seconds.
"""

import time
import os
from datetime import datetime
import cv2


class CameraRecorder:
    def __init__(self, output_dir="camera_images", duration=5, interval=1, camera_index=0):
        """
        Initialize the camera recorder.

        Args:
            output_dir (str): Directory to save camera images
            duration (int): Total recording duration in seconds
            interval (int): Time interval between captures in seconds
            camera_index (int): Camera device index (0 for default camera)
        """
        self.output_dir = output_dir
        self.duration = duration
        self.interval = interval
        self.camera_index = camera_index
        self.images = []

    def setup_output_directory(self):
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")
        else:
            print(f"Using existing output directory: {self.output_dir}")

    def capture_image(self, camera, filename):
        """
        Capture an image from the camera.

        Args:
            camera: OpenCV VideoCapture object
            filename (str): Name of the file to save the image

        Returns:
            str: Path to the saved image file
        """
        # Read frame from camera
        ret, frame = camera.read()

        if not ret:
            raise Exception("Failed to capture image from camera")

        # Save the image
        filepath = os.path.join(self.output_dir, filename)
        cv2.imwrite(filepath, frame)

        return filepath

    def record(self):
        """
        Start recording from the camera.
        Captures images at specified intervals for the specified duration.
        """
        self.setup_output_directory()

        print(f"Initializing camera...")

        # Initialize camera
        camera = cv2.VideoCapture(self.camera_index)

        if not camera.isOpened():
            raise Exception(f"Could not open camera {self.camera_index}")

        # Set camera properties for better quality (optional)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Allow camera to warm up
        time.sleep(0.5)

        print(f"Starting camera recording...")
        print(f"Duration: {self.duration} seconds")
        print(f"Interval: {self.interval} second(s)")
        print(f"Expected captures: {self.duration // self.interval}")
        print("-" * 50)

        start_time = time.time()
        capture_count = 0

        try:
            while time.time() - start_time < self.duration:
                # Calculate current elapsed time
                elapsed = time.time() - start_time

                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"camera_{capture_count + 1:03d}_{timestamp}.jpg"

                # Capture image
                try:
                    filepath = self.capture_image(camera, filename)
                    capture_count += 1
                    self.images.append(filepath)
                    print(f"[{elapsed:.1f}s] Captured: {filename}")
                except Exception as e:
                    print(f"Error capturing image: {e}")

                # Wait for the next interval
                next_capture_time = start_time + (capture_count * self.interval)
                sleep_time = next_capture_time - time.time()

                if sleep_time > 0:
                    time.sleep(sleep_time)

        finally:
            # Release the camera
            camera.release()

        print("-" * 50)
        print(f"Recording complete!")
        print(f"Total captures: {capture_count}")
        print(f"Images saved to: {os.path.abspath(self.output_dir)}")

        return self.images


def main():
    """Main function to run the camera recorder."""
    # Create recorder with default settings: 5 seconds duration, 1 second interval
    recorder = CameraRecorder(
        output_dir="camera_images",
        duration=5,
        interval=1
    )

    # Start recording
    try:
        images = recorder.record()

        # Display captured files
        print("\nCaptured files:")
        for i, filepath in enumerate(images, 1):
            print(f"  {i}. {filepath}")

    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("- Make sure your camera is not being used by another application")
        print("- Check that your camera is properly connected")
        print("- Try running with different camera_index (0, 1, 2, etc.)")


if __name__ == "__main__":
    main()
