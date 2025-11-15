#!/usr/bin/env python3
"""
Example usage of the CameraRecorder class.
This demonstrates different ways to use the camera recorder.
"""

from camera_recorder import CameraRecorder


def example_1_default_settings():
    """Example 1: Use default settings (5 seconds, 1 second interval)"""
    print("=" * 60)
    print("Example 1: Default Settings")
    print("=" * 60)

    recorder = CameraRecorder()
    images = recorder.record()

    print(f"\nCaptured {len(images)} images")


def example_2_custom_duration():
    """Example 2: Record for 10 seconds with 2 second intervals"""
    print("\n" + "=" * 60)
    print("Example 2: Custom Duration and Interval")
    print("=" * 60)

    recorder = CameraRecorder(
        output_dir="camera_images_10sec",
        duration=10,
        interval=2
    )
    images = recorder.record()

    print(f"\nCaptured {len(images)} images")


def example_3_rapid_capture():
    """Example 3: Rapid capture - 3 seconds with 0.5 second intervals"""
    print("\n" + "=" * 60)
    print("Example 3: Rapid Capture")
    print("=" * 60)

    recorder = CameraRecorder(
        output_dir="camera_images_rapid",
        duration=3,
        interval=0.5
    )
    images = recorder.record()

    print(f"\nCaptured {len(images)} images")


def example_4_external_camera():
    """Example 4: Use external camera (camera_index=1)"""
    print("\n" + "=" * 60)
    print("Example 4: External Camera")
    print("=" * 60)

    recorder = CameraRecorder(
        output_dir="camera_images_external",
        duration=5,
        interval=1,
        camera_index=1  # Try external camera
    )
    try:
        images = recorder.record()
        print(f"\nCaptured {len(images)} images")
    except Exception as e:
        print(f"\nError: {e}")
        print("External camera may not be available. Try camera_index=0 for default camera.")


if __name__ == "__main__":
    print("Camera Recorder Examples")
    print("\nChoose an example to run:")
    print("1. Default settings (5 seconds, 1 second interval)")
    print("2. Custom duration (10 seconds, 2 second intervals)")
    print("3. Rapid capture (3 seconds, 0.5 second intervals)")
    print("4. External camera (camera_index=1)")

    choice = input("\nEnter choice (1-4) or press Enter for Example 1: ").strip()

    try:
        if choice == "2":
            example_2_custom_duration()
        elif choice == "3":
            example_3_rapid_capture()
        elif choice == "4":
            example_4_external_camera()
        else:
            example_1_default_settings()

        print("\n" + "=" * 60)
        print("Example complete!")
        print("=" * 60)
    except Exception as e:
        print(f"\n" + "=" * 60)
        print(f"Error: {e}")
        print("=" * 60)
        print("\nTroubleshooting tips:")
        print("- Make sure your camera is not being used by another application")
        print("- Check that your camera is properly connected")
        print("- Try running with different camera_index (0, 1, 2, etc.)")
