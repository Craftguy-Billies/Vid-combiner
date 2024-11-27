import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips

def read_inputs(file="input.txt"):
    with open(file, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    if len(lines) < 3:
        raise ValueError("Input file must contain paths for exactly three videos.")
    return lines[:3]

def process_videos(input_files, output_folder="output"):
    if not all(input_files):
        raise ValueError("Please provide all three input videos.")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    clips = []
    for filepath in input_files:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} not found.")
        clip = VideoFileClip(filepath)
        if clip.duration < 5:
            raise ValueError(f"File {os.path.basename(filepath)} is shorter than 5 seconds.")
        clip = clip.resize(height=720).set_fps(30)  # Resize to 720p30
        clips.append(clip)

    selected_clips = []
    for clip in clips:
        for _ in range(12):
            start = random.uniform(0, clip.duration - 5)
            selected_clips.append(clip.subclip(start, start + 5))

    random.shuffle(selected_clips)

    final_video = concatenate_videoclips(selected_clips[:36], method="compose")
    output_path = os.path.join(output_folder, "combined_video.mp4")
    final_video.write_videofile(output_path, codec="libx264")
    print(f"Video created successfully! Saved to: {output_path}")

if __name__ == "__main__":
    try:
        input_files = read_inputs()
        process_videos(input_files)
    except Exception as e:
        print(f"Error: {e}")
