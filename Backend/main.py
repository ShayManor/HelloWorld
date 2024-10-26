import os
import openai

from Backend.Movie_Assembler.create_movie import create_movie
from Backend.Movie_Assembler.upload_video import YouTubeUploader, main
from Backend.Movie_Creator.core import core

problem = '3x + 4 = 7'
solution = 'x = 1'


class solver:
    def __init__(self, problem, solution):
        self.problem = problem
        self.solution = solution
        os.environ["GCP_API_KEY"] = 'AIzaSyBMc19g-80j9BmdlDLZLfR7D7ZBZiBWaAc'
        os.environ[
            "OPENAI_API_KEY"] = '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'
        openai.api_key = os.environ["OPENAI_API_KEY"]

        # yt = YouTubeUploader('/HelloWorld/Secrets/client_secrets.json')

    def upload(self, upload):
        movie_name = 'final_movie.mp4'
        # core_instance = core(problem, solution, openai.api_key)
        # video_inputs = core_instance.start()
        # mov = create_movie(openai.api_key)
        if (upload):
            # mov.create_video_from_inputs(video_inputs, movie_name)
            return main(movie_name, problem)


solver(problem, solution).upload(False)
