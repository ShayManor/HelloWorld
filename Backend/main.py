import os

import openai

from Backend.Movie_Assembler.create_movie import create_movie
from Backend.Movie_Creator.core import core

problem = '3x + 4 = 7'
solution = 'x = 1'
# api_key = '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'
os.environ["OPENAI_API_KEY"] = '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'
openai.api_key = os.environ["OPENAI_API_KEY"]

core = core(problem, solution, openai.api_key)
video_inputs = core.start()
mov = create_movie(openai.api_key)
for i, input in enumerate(video_inputs):
    mov.create_custom_video_from_input(input, i)
