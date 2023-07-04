import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize


def summarize_web_page_by_keyword(url, language='english', keywords=[]):
    response = requests.get(url)
    content = response.text

    soup = BeautifulSoup(content, "html.parser")
    title = soup.title.string

    general_summary = f"*General summary* {url} : {title}"

    keyword_summary = generate_keyword_summary(content, language, keywords)

    return general_summary, keyword_summary


def generate_keyword_summary(content, language='english', keywords=[]):
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()

    sentences = sent_tokenize(text)

    keyword_sentences = []
    for sentence in sentences:
        if any(keyword.lower() in sentence.lower() for keyword in keywords):
            keyword_sentences.append(sentence)

    keyword_summary = "*Summary based on Keywords:*"
    for sentence in keyword_sentences:
        keyword_summary += f"\n- {sentence}"

    return keyword_summary

# @app.command("/summarize_url_by_keyword")
# def summarize_url_by_keyword(ack, say, command):
#     ack()
#     try:
#         args = command['text'].split()
#         url = args[0]
#         language = 'english'
#         keywords = args[1:]

#         if len(args) > 1 and args[1].lower() == 'spanish':
#             language = 'spanish'

#         general_summary, keyword_summary = url_summ_keyword.summarize_web_page_by_keyword(
#             url, language, keywords)

#         say(f"{general_summary}\n\n{keyword_summary}")
#     except Exception as e:
#         print(f"Error: {str(e)}")
