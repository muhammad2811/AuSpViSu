from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def combine(extension, timeStamps, path):
    # Load the video
    video = VideoFileClip(f"{path}.{extension}")
    
    # Create a list to hold the subclips
    subclips = []
    
    for timestamp in timeStamps:
        start_time = max(0, timestamp - 20)  # Ensure start_time is not negative
        end_time = min(video.duration, timestamp + 10)  # Ensure end_time does not exceed video duration
        subclip = video.subclip(start_time, end_time)
        subclips.append(subclip)
    
    # Concatenate all subclips into one video
    final_clip = concatenate_videoclips(subclips)
    # path = f'{os.getcwd()}/{vid}'	
    # Save the final video
    final_clip.write_videofile(f"{path}_combined.{extension}", codec='libx264')
    
    # Close the video files
    video.close()
    final_clip.close()

# Example usage
# combine("mp4", [50, 85, 120], "comb")
