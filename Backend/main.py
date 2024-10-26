import os
import openai

from Backend.Movie_Assembler.create_movie import create_movie
from Backend.Movie_Creator.core import core

problem = '3x + 4 = 7'
solution = 'x = 1'
os.environ["OPENAI_API_KEY"] = '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'
openai.api_key = os.environ["OPENAI_API_KEY"]

core_instance = core(problem, solution, openai.api_key)
video_inputs = core_instance.start()
mov = create_movie(openai.api_key)

mov.create_video_from_inputs(video_inputs, 'final_movie.mp4')