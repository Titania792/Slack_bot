import requests
from bs4 import BeautifulSoup
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import re


def summarize_web_page(url, language='english'):
    # Obtain the content of the web page
    response = requests.get(url)
    content = response.text

    # General summary
    soup = BeautifulSoup(content, "html.parser")
    title = soup.title.string
    if language == 'spanish':
        general_summary = f"*Resumen general* {url} : {title}"
    else:
        general_summary = f"*General summary* {url} : {title}"

    # Keywords summary
    keywords_summary = generate_keywords_summary(content, language)

    # Contextual summary using LSA
    parser = HtmlParser.from_string(content, url, Tokenizer(language))
    lsa_summarizer = LsaSummarizer()
    lsa_summary = lsa_summarizer(parser.document, 10)
    if language == 'spanish':
        lsa_summary = "*Resumen por contexto utilizando LSA:*\n\n" + " ".join(
            str(sentence) for sentence in lsa_summary)
    else:
        lsa_summary = "*Contextual summary using LSA:*\n\n" + " ".join(
            str(sentence) for sentence in lsa_summary)

    # Contextual summary using LexRank
    lexrank_summarizer = LexRankSummarizer()
    lexrank_summary = lexrank_summarizer(parser.document, 10)
    if language == 'spanish':
        lexrank_summary = "*Resumen por contexto utilizando LexRank:*\n\n" + " ".join(
            str(sentence) for sentence in lexrank_summary)
    else:
        lexrank_summary = "*Contextual summary using LexRank:*\n\n" + " ".join(
            str(sentence) for sentence in lexrank_summary)

    # Return the generated summaries
    # return general_summary, keywords_summary, lsa_summary, lexrank_summary
    return general_summary, keywords_summary, lsa_summary, lexrank_summary


def generate_keywords_summary(content, language='english'):
    # Remove HTML tags and extract text content
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()

    # Tokenize the content into individual words
    tokens = word_tokenize(text)

    # Remove stopwords (common words with little meaning)
    stop_words = set(stopwords.words(language))
    filtered_tokens = [token.lower() for token in tokens if token.lower(
    ) not in stop_words and re.match(r'^[a-zA-Z0-9]+$', token)]

    # Calculate word frequencies
    fdist = FreqDist(filtered_tokens)

    # Get the most frequent keywords
    top_keywords = fdist.most_common(3)

    # Extract only the keyword part from (keyword, frequency) tuples
    keywords = [keyword for keyword, _ in top_keywords]

    # Generate the keywords summary
    keywords_summary = "*Keywords:* " + ", ".join(keywords)
    return keywords_summary


# def print_summary(general_summary, keywords_summary, lsa_summary, lexrank_summary):
#     # def print_summary(summarize_web_page):
#     # general_summary, keywords_summary, lsa_summary, lexrank_summary = summarize_web_page
#     print("---------------------------------")
#     print(general_summary)
#     print("---------------------------------")
#     print(keywords_summary)
#     print("---------------------------------")
#     print(lsa_summary)
#     print("---------------------------------")
#     print(lexrank_summary)
#     print("---------------------------------")


# Example usage
# english_url = "https://aws.amazon.com/docker/"
# spanish_url = "https://aws.amazon.com/es/docker/#:~:text=Docker%20le%20permite%20entregar%20c%C3%B3digo,manera%20fiable%20en%20cualquier%20lugar."
# general_en, keywords_en, lsa_en, lexrank_en = summarize_web_page(
#     english_url, language='english')
# general_es, keywords_es, lsa_es, lexrank_es = summarize_web_page(
#     spanish_url, language='spanish')

# print_summary(summarize_web_page(english_url, language='english'))
# print_summary(summarize_web_page(spanish_url, language='spanish'))

# summarize_web_page(spanish_url, language='spanish')
