import time

import matplotlib.pyplot as plt
import numpy as np
import os

from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip, concatenate_audioclips
)
from Backend.Movie_Creator.video_input import video_input
from Backend.Movie_Assembler.script_to_audio import script_to_audio

class create_movie:
    def __init__(self, api_key):
        self.api_key = api_key

    def escape_latex(self, text):
        special_chars = ['#', '$', '%', '&', '~', '_', '^', '{', '}']  # Exclude backslash
        for char in special_chars:
            text = text.replace(char, '\\' + char)
        return text

    def render_latex_to_image(self, latex_str, output_image='latex_image.png'):
        plt.rcParams.update({
            "text.usetex": True,
            "font.size": 24,  # Adjust as needed
            "text.latex.preamble": r"\usepackage{amsmath}"
        })
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.axis('off')

        # Do not replace backslashes or wrap the string in $...$

        print(f"Final LaTeX string to render: {latex_str}")

        ax.text(
            0.5, 0.5, latex_str,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes
        )
        try:
            plt.savefig(output_image, bbox_inches='tight', pad_inches=0.1, dpi=300)
            print(f"Image saved as {output_image}")
        except Exception as e:
            print(f'Error with LaTeX shown on screen: {e}')
            raise
        plt.close(fig)

    def create_video_from_inputs(self, video_inputs, output_video='final_movie.mp4'):
        start_time = time.time()
        silence_duration = 0.25  # 0.25 seconds of silence between audio clips

        audio_clips = []
        audio_durations = []
        start_times = []
        current_time = 0.0

        n_channels = None  # Will be set after the first audio clip is loaded

        # Generate audio clips and calculate start times
        for i, video_input in enumerate(video_inputs):
            audio_file = f"{i:03}audio.mp3"

            # Generate audio for each script
            audio_generator = script_to_audio(self.api_key)
            audio_generator.convert(video_input.script, i)

            audio_clip = AudioFileClip(audio_file)
            if n_channels is None:
                n_channels = audio_clip.nchannels  # Get the number of channels from the first clip
            audio_clips.append(audio_clip)
            audio_duration = audio_clip.duration
            audio_durations.append(audio_duration)
            start_times.append(current_time)
            current_time += audio_duration

            # Add silence after each audio clip except the last one
            if i < len(video_inputs) - 1:
                silence_clip = self.make_silence(silence_duration, n_channels=n_channels)
                audio_clips.append(silence_clip)
                current_time += silence_duration

        # Concatenate all audio clips
        final_audio = concatenate_audioclips(audio_clips)

        # Prepare video clips
        video_width, video_height = 1280, 720  # HD resolution

        # Load and resize background image
        bg_clip = ImageClip('background.jpeg').set_duration(final_audio.duration).resize((video_width, video_height))

        # List to hold all the line clips
        line_clips = []

        cumulative_lines = []

        for i, video_input in enumerate(video_inputs):
            line_id = f"{i:03}"
            image_file = f"latex_image_{line_id}.png"

            # Build cumulative lines
            cumulative_lines.append(self.escape_latex(video_input.on_screen))
            cumulative_text = r' \\ '.join(cumulative_lines)  # Use raw string for LaTeX line breaks

            # Wrap cumulative_text in align* environment
            cumulative_text = r'\begin{align*}' + cumulative_text + r'\end{align*}'

            # Print the cumulative_text for debugging
            print(f"Cumulative LaTeX text: {cumulative_text}")

            # Render LaTeX image for the cumulative lines
            self.render_latex_to_image(cumulative_text, image_file)

            # Create ImageClip for the cumulative image
            line_clip = ImageClip(image_file).set_duration(final_audio.duration - start_times[i])
            line_clip = line_clip.set_position('center')
            line_clip = line_clip.set_start(start_times[i])

            # Add fade-in effect at the start
            fade_duration = 0.5  # Duration of fade-in
            line_clip = line_clip.fadein(fade_duration)

            line_clips.append(line_clip)

        # Composite all clips together
        video_clip = CompositeVideoClip([bg_clip] + line_clips, size=(video_width, video_height))
        video_clip = video_clip.set_audio(final_audio)

        # Write the video file
        video_clip.write_videofile(
            output_video,
            fps=24,
            codec='libx264',
            preset='medium',
            bitrate="5000k",
            audio_codec='aac',
            threads=4
        )

        # Clean up image and audio files
        for i in range(len(video_inputs)):
            line_id = f"{i:03}"
            image_file = f"latex_image_{line_id}.png"
            audio_file = f"{i:03}audio.mp3"
            if os.path.exists(image_file):
                os.remove(image_file)
            if os.path.exists(audio_file):
                os.remove(audio_file)

        print(f"Total time taken: {time.time() - start_time} seconds.")

    def make_silence(self, duration, fps=44100, n_channels=2):
        total_samples = int(duration * fps)
        array = np.zeros((total_samples, n_channels))
        return AudioArrayClip(array, fps=fps)
