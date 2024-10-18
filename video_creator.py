import glob
import re
import cv2
import os
from typing import Optional


def assemble_video(input_pattern: str, output_path: str, fps: int) -> Optional[None]:
    """
    Assembles a video from PNG files following the format name_{index}.png.
    Uses all images found and creates a video with the specified FPS.

    Args:
        input_pattern (str): The glob pattern for the input files (e.g., "path/to/files/name_*.png").
        output_path (str): The path where the video will be saved (e.g., "output/video.mp4").
        fps (int): Frames per second for the video.

    Returns:
        None
    """

    # Step 1: Get all files matching the glob pattern
    file_paths = glob.glob(input_pattern)

    if not file_paths:
        print("No files found matching the pattern.")
        return

    # Step 2: Extract the index from the file name and sort files by index
    def get_index(filename: str) -> int:
        match = re.search(r"_(\d+)\.png", filename)
        return int(match.group(1)) if match else -1

    # Sort files based on their index
    sorted_files = sorted(file_paths, key=get_index)

    # Step 3: Read the first image to determine video dimensions
    first_frame = cv2.imread(sorted_files[0])

    if first_frame is None:
        print(f"Error reading the first image: {sorted_files[0]}")
        return

    height, width, _ = first_frame.shape

    # Step 4: Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 format
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Step 5: Loop through the sorted images and write frames to the video
    for img_path in sorted_files:
        frame = cv2.imread(img_path)

        if frame is None:
            print(f"Error reading image {img_path}")
            continue

        video_writer.write(frame)

    # Step 6: Release the video writer
    video_writer.release()
    print(f"Video successfully saved to {output_path}")