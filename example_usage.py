#!/usr/bin/env python3
"""
Example usage of the ScreenRecorder class.
This demonstrates different ways to use the screen recorder.
"""

from screen_recorder import ScreenRecorder


def example_1_default_settings():
    """Example 1: Use default settings (5 seconds, 1 second interval)"""
    print("=" * 60)
    print("Example 1: Default Settings")
    print("=" * 60)

    recorder = ScreenRecorder()
    screenshots = recorder.record()

    print(f"\nCaptured {len(screenshots)} screenshots")


def example_2_custom_duration():
    """Example 2: Record for 10 seconds with 2 second intervals"""
    print("\n" + "=" * 60)
    print("Example 2: Custom Duration and Interval")
    print("=" * 60)

    recorder = ScreenRecorder(
        output_dir="screenshots_10sec",
        duration=10,
        interval=2
    )
    screenshots = recorder.record()

    print(f"\nCaptured {len(screenshots)} screenshots")


def example_3_rapid_capture():
    """Example 3: Rapid capture - 3 seconds with 0.5 second intervals"""
    print("\n" + "=" * 60)
    print("Example 3: Rapid Capture")
    print("=" * 60)

    recorder = ScreenRecorder(
        output_dir="screenshots_rapid",
        duration=3,
        interval=0.5
    )
    screenshots = recorder.record()

    print(f"\nCaptured {len(screenshots)} screenshots")


if __name__ == "__main__":
    print("Screen Recorder Examples")
    print("\nChoose an example to run:")
    print("1. Default settings (5 seconds, 1 second interval)")
    print("2. Custom duration (10 seconds, 2 second intervals)")
    print("3. Rapid capture (3 seconds, 0.5 second intervals)")

    choice = input("\nEnter choice (1-3) or press Enter for Example 1: ").strip()

    if choice == "2":
        example_2_custom_duration()
    elif choice == "3":
        example_3_rapid_capture()
    else:
        example_1_default_settings()

    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)
