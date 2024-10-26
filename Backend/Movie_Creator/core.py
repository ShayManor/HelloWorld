from Backend.Movie_Creator.on_screen_text_generator import on_screen_generator
from Backend.Movie_Creator.process_user_data import process_data
from Backend.Movie_Creator.script_generator import script_generator
from Backend.Movie_Creator.video_input import video_input


class core:
    def __init__(self, problem, solution):
        self.problem = problem
        self.solution = solution
        self.apiKey = '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'

    def start(self):
        process = process_data(self.problem, self.solution, apiKey=self.apiKey)
        post_processed_data = process.start_processing()
        if post_processed_data == "Error":
            return False

        script = script_generator(apiKey=self.apiKey, prompt=post_processed_data)
        script = script.start_process()

        sliced_script = script.split('~')
        screen_text_obj = on_screen_generator(apiKey=self.apiKey)
        num_steps = len(sliced_script)

        show_on_screen = []

        if num_steps == 1:
            input = video_input()
            input.set_script(sliced_script[0])
            input.set_on_screen(screen_text_obj.start_process(block=sliced_script[0], pre_block=None, post_block=None))
        else:
            for i in range(num_steps):
                input = video_input()
                input.set_script(sliced_script[i])
                if i == 0:
                    input.set_on_screen(screen_text_obj.start_process(block=sliced_script[i], pre_block=None, post_block=sliced_script[i + 1]))
                elif i == num_steps - 1 and i > 0:
                    input.set_on_screen(screen_text_obj.start_process(block=sliced_script[i], pre_block=sliced_script[i - 1], post_block=None))
                else:
                    input.set_on_screen(screen_text_obj.start_process(block=sliced_script[i], pre_block=sliced_script[i - 1], post_block=sliced_script[i + 1]))
                show_on_screen.append(input)