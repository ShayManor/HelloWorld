from openai import OpenAI
from typing import Optional


class script_generator:
    def __init__(self, pre_block: Optional[str], block: str, post_block: Optional[str]):
        self.client = OpenAI()
        self.client.api_key = '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'
        self.assistant_id = 'asst_CoRUsRi8KqrdnZIP4UyCi2WY'
        self.prompt = "Script before block: " + pre_block + "\nBlock script: " + block + "\nScript after block: " + post_block

    def start_process(self):
        assistant = self.client.beta.assistants.retrieve(
            assistant_id=self.assistant_id
        )
        thread = self.client.beta.threads.create(
            messages=[{"role": "user", "content": self.prompt}]
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        if run.status == 'completed':
            messages = self.client.beta.threads.messages.list(thread_id=run.thread_id)
            ai_response = messages.data[0].content[0].text.value
            return ai_response
        else:
            return "Error"