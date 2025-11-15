#!/usr/bin/env python3
"""
Vibe Analyzer
Analyzes images using Claude's vision API to detect if people are vibing to music.
"""

import os
import base64
from typing import List, Dict
from anthropic import Anthropic


class VibeAnalyzer:
    def __init__(self, api_key=None):
        """
        Initialize the vibe analyzer with Claude API.

        Args:
            api_key (str, optional): Anthropic API key. If not provided, will use ANTHROPIC_API_KEY env variable.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or pass it to the constructor.")

        self.client = Anthropic(api_key=self.api_key)

    def encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 string.

        Args:
            image_path (str): Path to the image file

        Returns:
            str: Base64 encoded image
        """
        with open(image_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")

    def analyze_single_image(self, image_path: str) -> Dict[str, any]:
        """
        Analyze a single image to detect if person is vibing.

        Args:
            image_path (str): Path to the image file

        Returns:
            dict: Analysis result with 'is_vibing', 'confidence', and 'description'
        """
        print(f"Analyzing image: {os.path.basename(image_path)}")

        # Encode image
        image_data = self.encode_image(image_path)

        # Create message with vision
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyze this image and determine if the person in it is moving in an exciting way or "vibing" to music.

Consider the following:
- Body position and posture (dancing, swaying, moving rhythmically)
- Facial expressions (joy, excitement, energy)
- Arm/hand movements (raised, waving, gesturing)
- Overall energy level
- Signs of dancing or rhythmic movement

Respond in this exact format:
VIBING: [YES/NO]
CONFIDENCE: [0-100]
DESCRIPTION: [Brief description of what you observe about the person's movement and energy]"""
                        }
                    ],
                }
            ],
        )

        # Parse response
        response_text = message.content[0].text

        # Extract information
        lines = response_text.strip().split('\n')
        is_vibing = False
        confidence = 0
        description = ""

        for line in lines:
            if line.startswith("VIBING:"):
                is_vibing = "YES" in line.upper()
            elif line.startswith("CONFIDENCE:"):
                try:
                    confidence = int(''.join(filter(str.isdigit, line)))
                except ValueError:
                    confidence = 50
            elif line.startswith("DESCRIPTION:"):
                description = line.replace("DESCRIPTION:", "").strip()

        return {
            "image_path": image_path,
            "is_vibing": is_vibing,
            "confidence": confidence,
            "description": description,
            "raw_response": response_text
        }

    def analyze_sequence(self, image_paths: List[str]) -> Dict[str, any]:
        """
        Analyze a sequence of images to detect vibing patterns over time.

        Args:
            image_paths (list): List of image file paths in chronological order

        Returns:
            dict: Overall analysis including individual results and summary
        """
        print(f"\n{'='*60}")
        print(f"Analyzing sequence of {len(image_paths)} images")
        print(f"{'='*60}\n")

        individual_results = []

        # Analyze each image
        for i, image_path in enumerate(image_paths, 1):
            print(f"\n[{i}/{len(image_paths)}] ", end="")
            result = self.analyze_single_image(image_path)
            individual_results.append(result)

            print(f"  → Vibing: {'YES' if result['is_vibing'] else 'NO'} "
                  f"(Confidence: {result['confidence']}%)")
            print(f"  → {result['description']}")

        # Calculate overall metrics
        vibing_count = sum(1 for r in individual_results if r['is_vibing'])
        avg_confidence = sum(r['confidence'] for r in individual_results) / len(individual_results)
        vibing_percentage = (vibing_count / len(individual_results)) * 100

        # Determine overall vibe status
        overall_vibing = vibing_percentage >= 50

        summary = {
            "total_images": len(image_paths),
            "vibing_images": vibing_count,
            "vibing_percentage": vibing_percentage,
            "average_confidence": avg_confidence,
            "overall_vibing": overall_vibing,
            "individual_results": individual_results
        }

        # Print summary
        print(f"\n{'='*60}")
        print(f"VIBE ANALYSIS SUMMARY")
        print(f"{'='*60}")
        print(f"Total images analyzed: {summary['total_images']}")
        print(f"Images showing vibing: {summary['vibing_images']}")
        print(f"Vibing percentage: {summary['vibing_percentage']:.1f}%")
        print(f"Average confidence: {summary['average_confidence']:.1f}%")
        print(f"\nOverall verdict: {'🎉 PERSON IS VIBING!' if overall_vibing else '😐 Not really vibing'}")
        print(f"{'='*60}\n")

        return summary

    def analyze_with_comparison(self, image_paths: List[str]) -> Dict[str, any]:
        """
        Analyze multiple images together to detect movement and vibing.
        Compares consecutive frames to identify changes.

        Args:
            image_paths (list): List of image file paths in chronological order

        Returns:
            dict: Analysis result comparing images over time
        """
        if len(image_paths) < 2:
            return self.analyze_sequence(image_paths)

        print(f"\n{'='*60}")
        print(f"Analyzing {len(image_paths)} images with temporal comparison")
        print(f"{'='*60}\n")

        # Encode all images
        encoded_images = []
        for image_path in image_paths:
            encoded_images.append({
                "path": image_path,
                "data": self.encode_image(image_path)
            })

        # Create content with multiple images
        content = []
        for i, img in enumerate(encoded_images):
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": img["data"],
                },
            })

        # Add analysis prompt
        content.append({
            "type": "text",
            "text": f"""Analyze this sequence of {len(image_paths)} images captured over time to determine if the person is vibing or dancing to music.

Look for:
1. Changes in body position between frames (movement, dancing)
2. Raised arms, rhythmic gestures, or dance moves
3. Facial expressions showing joy or excitement
4. Progressive movement that suggests dancing or vibing to music
5. Energy and enthusiasm in their poses

Compare the images and identify any movement patterns that indicate the person is:
- Dancing or moving rhythmically
- Showing excitement or energy
- Vibing to music
- Engaging in any celebratory movements

Respond in this format:
VIBING: [YES/NO]
CONFIDENCE: [0-100]
MOVEMENT_DETECTED: [YES/NO]
ENERGY_LEVEL: [LOW/MEDIUM/HIGH]
DESCRIPTION: [Detailed description of observed movements, changes between frames, and overall vibe]"""
        })

        # Make API call
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
        )

        # Parse response
        response_text = message.content[0].text
        lines = response_text.strip().split('\n')

        is_vibing = False
        confidence = 0
        movement_detected = False
        energy_level = "UNKNOWN"
        description = ""

        for line in lines:
            if line.startswith("VIBING:"):
                is_vibing = "YES" in line.upper()
            elif line.startswith("CONFIDENCE:"):
                try:
                    confidence = int(''.join(filter(str.isdigit, line)))
                except ValueError:
                    confidence = 50
            elif line.startswith("MOVEMENT_DETECTED:"):
                movement_detected = "YES" in line.upper()
            elif line.startswith("ENERGY_LEVEL:"):
                energy_level = line.replace("ENERGY_LEVEL:", "").strip()
            elif line.startswith("DESCRIPTION:"):
                description = line.replace("DESCRIPTION:", "").strip()

        result = {
            "total_images": len(image_paths),
            "is_vibing": is_vibing,
            "confidence": confidence,
            "movement_detected": movement_detected,
            "energy_level": energy_level,
            "description": description,
            "raw_response": response_text
        }

        # Print summary
        print(f"{'='*60}")
        print(f"TEMPORAL VIBE ANALYSIS")
        print(f"{'='*60}")
        print(f"Images analyzed: {result['total_images']}")
        print(f"Vibing detected: {'YES' if result['is_vibing'] else 'NO'}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Movement detected: {'YES' if result['movement_detected'] else 'NO'}")
        print(f"Energy level: {result['energy_level']}")
        print(f"\nAnalysis: {result['description']}")
        print(f"\n{'🎉 PERSON IS VIBING!' if is_vibing else '😐 Not really vibing'}")
        print(f"{'='*60}\n")

        return result


def main():
    """Example usage of VibeAnalyzer."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python vibe_analyzer.py <image_path> [image_path2] ...")
        print("\nOr set image paths in the script and run without arguments")
        sys.exit(1)

    # Initialize analyzer
    try:
        analyzer = VibeAnalyzer()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set your ANTHROPIC_API_KEY environment variable:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)

    # Get image paths from command line
    image_paths = sys.argv[1:]

    # Analyze
    if len(image_paths) == 1:
        result = analyzer.analyze_single_image(image_paths[0])
        print(f"\nResult: {'VIBING!' if result['is_vibing'] else 'Not vibing'}")
    else:
        # Use temporal comparison for better results
        result = analyzer.analyze_with_comparison(image_paths)


if __name__ == "__main__":
    main()
