import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer


class QAModel:
    def __init__(self):
        self.model_name = "distilbert-base-cased-distilled-squad"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
        self.model.eval()
        self.max_len = 512

    def to_qa_ids(self, encoded_question, context_ids):
        return encoded_question + context_ids + [self.tokenizer.sep_token_id]

    def extract_answer(self, question, contexts):
        max_score = (-10000000)
        answer = ""
        for context in contexts:
            input_ids = self.to_qa_ids(question, context)
            with torch.no_grad():
                start_scores, end_scores = self.model(torch.tensor([input_ids]))
                all_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
                score = torch.max(start_scores) + torch.max(end_scores)
                if score > max_score:
                    max_score = score
                    answer = self.tokenizer.convert_tokens_to_string(
                        all_tokens[torch.argmax(start_scores): torch.argmax(end_scores) + 1])  #TODO: optimize this line
        return answer

    def split_context(self, context, question_len):
        max_len = self.max_len - question_len
        sentences = map(self.tokenizer.tokenize, map(lambda s: s + '.', context.split('.')))
        contexts = [[]]
        for sentence in sentences:
            if len(sentence) > max_len:
                raise NotImplemented  # sentence is too long
            elif len(contexts[-1]) + len(sentence) > max_len:
                contexts.append(list())
            contexts[-1] += sentence
        return contexts

    def forward(self, question, context):
        question_ids = self.tokenizer.encode(question)
        contexts_tokens = self.split_context(context, len(question_ids))
        contexts_ids = map(self.tokenizer.convert_tokens_to_ids, contexts_tokens)
        return self.extract_answer(question_ids, contexts_ids)









