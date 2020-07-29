from datetime import datetime as dt
from model import QAModel
import re


class Bot:
    def __init__(self):
        self.qa_model = QAModel()

    def reply(self, context, log):
        assert isinstance(context, str)
        assert isinstance(log, list)
        if not log:
            return self.message(self.prolog())
        return self.message(self.conversate(log[-1], context))

    def prolog(self):
        return "Hello! I'm the buisness question answering bot. ask me any question in regard to the buisness."

    def ans(self, question, context):
        try:
            answer = self.qa_model.forward(question, context)
        except:
            return "I'm struggling to find an answer."
        if answer in {"", " ", "[CLS]"}:
            return "I couldn't find an answer. try to ask differently."
        return self.normalize(answer)


    def conversate(self, question, context):
        if question['sender'] == 'bot':
            return "Ask me a question!"
        try:
            answer = self.qa_model.forward(question['text'], context)
        except:
            return "I'm struggling to find an answer."
        if answer in {"", " ", "[CLS]"}:
            return "I couldn't find an answer. try to ask differently."
        return self.normalize(answer)

    def normalize(self, answer):
        answer = re.sub(' ,', ',', answer)
        answer = re.sub(' ’ ', '’', answer)
        answer = answer[0].upper() + answer[1:]
        return answer + '.'

    def message(self, text):
        return {"sender": "bot", "datetime": str(dt.now()), "text": text}
