import requests
import trafilatura

from keybert import KeyBERT

import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')  # noqa

class HtmlUtils:
    _kw_model = KeyBERT()

    @staticmethod
    def extract_text_and_keywords_from_html(html_content):
        content = trafilatura.extract(html_content, include_comments=False, include_tables=False, include_formatting=False)
        if content is None:
            return "", ""
        keywords = HtmlUtils._kw_model.extract_keywords(
            content,
            keyphrase_ngram_range=(1, 3),
            stop_words="english",
            top_n=10
        )
        return content, ','.join(kw for kw, _ in keywords)
    
    @staticmethod
    def extract_text_and_keywords_from_url(url):
        try:
            response = requests.get(url)
            return HtmlUtils.extract_text_and_keywords_from_html(response.text)
        except Exception as e:
            logging.error(f"Error occurred while fetching URL and keywords: {url}, Error: {e}")
            return "", ""