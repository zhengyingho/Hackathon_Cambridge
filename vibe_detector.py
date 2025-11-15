#!/usr/bin/env python3
"""
Vibe Detector
Captures images from camera and analyzes them to detect if people are vibing to music.
"""

import os
import sys
import argparse
from camera_recorder import CameraRecorder
from vibe_analyzer import VibeAnalyzer


class VibeDetector:
    def __init__(self, api_key=None):
        """
        Initialize the vibe detector.

        Args:
            api_key (str, optional): Anthropic API key. If not provided, will use ANTHROPIC_API_KEY env variable.
        """
        self.analyzer = VibeAnalyzer(api_key=api_key)

    def run(self, duration=10, interval=1, output_dir="vibe_images", camera_index=0, use_temporal_analysis=True):
        """
        Run the vibe detection process.

        Args:
            duration (int): Recording duration in seconds
            interval (float): Capture interval in seconds
            output_dir (str): Directory to save images
            camera_index (int): Camera device index
            use_temporal_analysis (bool): Use temporal comparison for better results

        Returns:
            dict: Analysis results
        """
        print(f"\n{'🎵 '*20}")
        print(f"VIBE DETECTOR - Checking if you're vibing to the music!")
        print(f"{'🎵 '*20}\n")

        # Step 1: Capture images
        print(f"Step 1: Capturing images from camera...")
        print(f"  Duration: {duration} seconds")
        print(f"  Interval: {interval} second(s)")
        print(f"  Expected captures: {int(duration / interval)}\n")

        recorder = CameraRecorder(
            output_dir=output_dir,
            duration=duration,
            interval=interval,
            camera_index=camera_index
        )

        try:
            images = recorder.record()

            if not images:
                print("Error: No images were captured!")
                return None

            print(f"\n✓ Successfully captured {len(images)} images\n")

            # Step 2: Analyze images
            print(f"Step 2: Analyzing images with Claude's vision API...")

            if use_temporal_analysis and len(images) > 1:
                result = self.analyzer.analyze_with_comparison(images)
            else:
                result = self.analyzer.analyze_sequence(images)

            return result

        except Exception as e:
            print(f"Error during vibe detection: {e}")
            return None


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Detect if someone is vibing to music using camera and AI analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (10 seconds, 1 second intervals)
  python vibe_detector.py

  # Quick check (5 seconds, 0.5 second intervals)
  python vibe_detector.py --duration 5 --interval 0.5

  # Extended analysis (30 seconds, 2 second intervals)
  python vibe_detector.py --duration 30 --interval 2

  # Use external camera
  python vibe_detector.py --camera 1

  # Analyze frame-by-frame instead of temporal comparison
  python vibe_detector.py --no-temporal

Environment:
  ANTHROPIC_API_KEY must be set with your Anthropic API key
        """
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=10,
        help="Recording duration in seconds (default: 10)"
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Time between captures in seconds (default: 1.0)"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="vibe_images",
        help="Directory to save images (default: vibe_images)"
    )

    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera device index (default: 0)"
    )

    parser.add_argument(
        "--no-temporal",
        action="store_true",
        help="Disable temporal comparison analysis (analyze frames individually)"
    )

    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Anthropic API key (or set ANTHROPIC_API_KEY environment variable)"
    )

    args = parser.parse_args()

    # Check for API key
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: Anthropic API key is required!")
        print("\nPlease either:")
        print("  1. Set the ANTHROPIC_API_KEY environment variable:")
        print("     export ANTHROPIC_API_KEY='your-api-key-here'")
        print("  2. Pass it as an argument:")
        print("     python vibe_detector.py --api-key 'your-api-key-here'")
        sys.exit(1)

    # Create and run detector
    try:
        detector = VibeDetector(api_key=api_key)

        result = detector.run(
            duration=args.duration,
            interval=args.interval,
            output_dir=args.output_dir,
            camera_index=args.camera,
            use_temporal_analysis=not args.no_temporal
        )

        if result:
            print("\n✓ Vibe detection complete!")
            if result.get('is_vibing'):
                print("\n🎉 🎊 🎉 Keep vibing! 🎉 🎊 🎉")
            else:
                print("\n💡 Tip: Try moving more energetically to the music!")
        else:
            print("\n✗ Vibe detection failed")
            sys.exit(1)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nVibe detection interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
