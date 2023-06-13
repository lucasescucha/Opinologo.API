import IClassifier

import openai
import json
import os

from requestsDispatcher import RequestsDispatcher

class ChatGPTClassifier(IClassifier):
    def __init__(self) -> None:
        super().__init__()

        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
        self.CHATGPT_MODEL = 'text-davinci-003'
        self.CHATGPT_PROMPT = os.getenv('CHATGPT_PROMPT')
        self.CHATGPT_TEMPERATURE = 0
        self.CHATGPT_MAX_TOKENS = 4097
        self.CHATGPT_STOP = ["*"]
        self.CHATGPT_MAX_RPM = 60

    def classifySentences(self, sentences: list) -> list:
        def request(sentence):
            response = openai.Completion.create(
                model = self.CHATGPT_MODEL,
                prompt = self.CHATGPT_PROMPT.format(sentence),
                temperature = self.CHATGPT_TEMPERATURE,
                max_tokens = self.CHATGPT_MAX_TOKENS,
                stop = self.CHATGPT_STOP
            )

            for result in json.loads(response.choices[0].text):
                yield result.calificacion
    
        dispatcher = RequestsDispatcher(request, self.CHATGPT_MAX_RPM)
        return dispatcher.dispatchRequests(sentences)
