from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords

class TextAnalyzer:
    def get_summary(self,text):
        return summarize(text, ratio=0.2)
    def get_keywords(self,text):
        return keywords(text,ratio=0.1)
