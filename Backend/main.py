import json
import os
import openai

from Backend.Api.export_file import aws_uploader
from Backend.Movie_Assembler.create_movie import create_movie
from Backend.Movie_Assembler.upload_video import YouTubeUploader, main
from Backend.Movie_Creator.core import core


class solver:
    def __init__(self, problem):
        self.problem = problem
        # self.solution = solution
        self.link = ''
        os.environ["GCP_API_KEY"] = 'AIzaSyBMc19g-80j9BmdlDLZLfR7D7ZBZiBWaAc'
        os.environ[
            "OPENAI_API_KEY"] = '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'
        openai.api_key = os.environ["OPENAI_API_KEY"]

        # yt = YouTubeUploader('/HelloWorld/Secrets/client_secrets.json')

    def upload(self):
        core_instance = core(self.problem, openai.api_key)
        video_inputs = core_instance.start()
        mov = create_movie(openai.api_key)
        movie_name = mov.create_video_from_inputs(video_inputs)
        mov.create_video_from_inputs(video_inputs, movie_name)
        self.link = aws_uploader().upload(file_path=movie_name)
        return self.to_json()

    def to_json(self):
        return json.dumps({'url': self.link})

# solver(problem, solution).upload(False)
