import matplotlib.pyplot as plt
import pyttsx3

from Backend.Movie_Creator.video_input import video_input


import matplotlib.pyplot as plt
import time
import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip

# Import your script_to_audio class
from Backend.Movie_Assembler.script_to_audio import script_to_audio

class create_movie:
    def __init__(self, api_key):
        self.api_key = api_key

    def render_latex_to_image(self, latex_str, output_image='latex_image.png'):
        plt.rcParams.update({
            "text.usetex": True,
            "font.size": 24,
            "text.latex.preamble": r"\usepackage{amsmath}"
        })
        fig, ax = plt.subplots(figsize=(6, 1.5))
        ax.axis('off')
        ax.text(0.5, 0.5, f"${latex_str}$", horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes)
        plt.savefig(output_image, bbox_inches='tight', pad_inches=0.1, dpi=100)
        plt.close(fig)

    def create_custom_video_from_input(self, video_details: video_input, index, output_video='final_video.mp4'):
        start_time = time.time()
        unique_id = f"{index:03}"  # Format index as three digits with leading zeros
        image_file = f"latex_image_{unique_id}.png"
        audio_file = f"{unique_id}audio.mp3"

        print("Rendering LaTeX to image...")
        self.render_latex_to_image(video_details.on_screen, image_file)
        print("LaTeX rendering complete.")

        print("Generating audio from script...")
        # Use your script_to_audio class to generate the audio
        audio_generator = script_to_audio(self.api_key)
        audio_generator.convert(video_details.script, index)
        print("Audio generation complete.")

        print("Creating video clip...")
        # Ensure the audio file has been generated before proceeding
        if not os.path.exists(audio_file):
            print(f"Error: Audio file '{audio_file}' was not found.")
            return

        audio_clip = AudioFileClip(audio_file)
        audio_duration = audio_clip.duration

        bg_clip = ImageClip('background.jpeg').set_duration(audio_duration)
        # bg_clip = ImageClip('background.jpeg').set_duration(audio_duration).resize(height=720)

        latex_clip = ImageClip(image_file).set_duration(audio_duration).set_position('center')

        video_clip = CompositeVideoClip([bg_clip, latex_clip])

        # Set the audio
        video_clip = video_clip.set_audio(audio_clip)

        print("Writing video file...")
        video_clip.write_videofile(output_video, fps=15, codec='libx264', preset='ultrafast')
        print("Video file created.")

        # Clean up
        os.remove(image_file)
        # Optionally, remove the audio file if not needed
        # os.remove(audio_file)

        print(f"Total time taken: {time.time() - start_time} seconds.")
