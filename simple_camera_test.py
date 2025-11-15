#!/usr/bin/env python3
"""
Simple Camera Test Script
Tests camera access with multiple fallback options
"""

import sys
import os

def test_with_opencv():
    """Test camera using OpenCV"""
    try:
        import cv2
        import numpy as np

        print("Testing camera with OpenCV...")
        print("-" * 50)

        # Try to open camera
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            print("Camera 0 not available, trying camera 1...")
            camera = cv2.VideoCapture(1)

        if camera.isOpened():
            print("✓ Camera opened successfully!")

            # Try to read a frame
            ret, frame = camera.read()

            if ret:
                print(f"✓ Frame captured! Size: {frame.shape}")

                # Save test image
                output_file = "test_camera_capture.jpg"
                cv2.imwrite(output_file, frame)
                print(f"✓ Test image saved: {output_file}")

                # Show camera info
                width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
                print(f"✓ Camera resolution: {int(width)}x{int(height)}")
            else:
                print("✗ Failed to capture frame")

            camera.release()
            return True
        else:
            print("✗ Could not open any camera")
            return False

    except ImportError:
        print("✗ OpenCV (cv2) not installed")
        print("  Install with: pip install opencv-python")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_mock_camera():
    """Test with mock camera (no hardware needed)"""
    try:
        import cv2
        import numpy as np

        print("\nTesting with MOCK camera (no hardware required)...")
        print("-" * 50)

        # Create a test image
        img = np.zeros((480, 640, 3), dtype=np.uint8)

        # Add colored gradient
        for i in range(480):
            color_val = int((i / 480) * 255)
            img[i, :] = [color_val, 128, 255 - color_val]

        # Add text
        cv2.putText(img, "MOCK CAMERA TEST", (150, 240),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

        # Save test image
        output_file = "mock_camera_test.jpg"
        cv2.imwrite(output_file, img)

        print(f"✓ Mock camera test successful!")
        print(f"✓ Test image created: {output_file}")
        print(f"✓ Image size: {img.shape}")

        return True

    except ImportError:
        print("✗ OpenCV (cv2) not installed")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def check_video_devices():
    """Check available video devices on Linux"""
    print("\nChecking available video devices...")
    print("-" * 50)

    if os.path.exists("/dev"):
        video_devices = [f for f in os.listdir("/dev") if f.startswith("video")]
        if video_devices:
            print("Found video devices:")
            for device in sorted(video_devices):
                print(f"  /dev/{device}")
        else:
            print("No /dev/video* devices found")
    else:
        print("Cannot check /dev directory (not Linux?)")


def main():
    print("=" * 50)
    print("SIMPLE CAMERA TEST")
    print("=" * 50)

    # Parse arguments
    use_mock = "--mock" in sys.argv or "-m" in sys.argv

    if use_mock:
        print("Running in MOCK mode (no camera required)\n")
        test_mock_camera()
    else:
        # Check for video devices
        check_video_devices()
        print()

        # Try real camera first
        success = test_with_opencv()

        if not success:
            print("\n" + "=" * 50)
            print("Real camera test failed. Trying mock camera...")
            print("=" * 50)
            test_mock_camera()
            print("\nTIP: Run with --mock flag to skip real camera test")

    print("\n" + "=" * 50)
    print("Test complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
