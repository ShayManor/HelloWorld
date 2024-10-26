from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip

def create_fade_text_video(script, output_filename='output_video.mp4', duration_per_text=5, fade_duration=1):
    """
    Creates a video with text fading in and out.

    :param script: List of strings, each string is a text to display.
    :param output_filename: The name of the output video file.
    :param duration_per_text: Duration each text stays on the screen (including fade in/out), in seconds.
    :param fade_duration: Duration of the fade in/out effects, in seconds.
    """
    clips = []
    for text in script:
        # Create a TextClip object with specified properties
        txt_clip = TextClip(
            text,
            fontsize=50,
            color='white',
            size=(1280, 720),
            method='caption',
            align='center',
            font='Arial-Bold'
        )

        # Set the duration of the clip
        txt_clip = txt_clip.set_duration(duration_per_text)

        # Apply fade in and fade out effects
        txt_clip = txt_clip.crossfadein(fade_duration).crossfadeout(fade_duration)

        # Position the text in the center
        txt_clip = txt_clip.set_position('center')

        # Create a background clip (black background)
        bg_clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=duration_per_text)

        # Composite the text over the background
        comp_clip = CompositeVideoClip([bg_clip, txt_clip])

        # Add the composite clip to the list
        clips.append(comp_clip)

    # Concatenate all the composite clips
    final_clip = concatenate_videoclips(clips, method='compose')

    # Write the final video file
    final_clip.write_videofile(output_filename, fps=24)

