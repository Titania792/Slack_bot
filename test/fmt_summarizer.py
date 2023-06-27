import requests
from bs4 import BeautifulSoup
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import re
import textract
from docx import Document


def summarize_document(url, language='english'):
    # Check the file extension
    if re.match(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url):
        print_summary(summarize_web_page(url, language))
    else:
        file_extension = url.split('.')[-1].lower()

        if file_extension == 'txt':
            print_summary(summarize_text_file(url, language))
        elif file_extension == 'pdf':
            print_summary(summarize_pdf_file(url, language))
        elif file_extension in ['doc', 'docx']:
            print_summary(summarize_word_file(url, language))
        else:
            print("Unsupported documentation format.")


def summarize_web_page(url, language='english'):
    # Obtain the content of the web page
    response = requests.get(url)
    content = response.text

    # General summary
    soup = BeautifulSoup(content, "html.parser")
    title = soup.title.string
    if language == 'spanish':
        general_summary = f"Resumen general: {title}"
    else:
        general_summary = f"General summary: {title}"

    # Keywords summary
    keywords_summary = generate_keywords_summary(content, language)

    # Contextual summary using LSA
    parser = HtmlParser.from_string(content, url, Tokenizer(language))
    lsa_summarizer = LsaSummarizer()
    lsa_summary = lsa_summarizer(parser.document, 10)
    if language == 'spanish':
        lsa_summary = "Resumen por contexto utilizando LSA:\n\n" + " ".join(
            str(sentence) for sentence in lsa_summary)
    else:
        lsa_summary = "Contextual summary using LSA:\n\n" + " ".join(
            str(sentence) for sentence in lsa_summary)

    # Contextual summary using LexRank
    lexrank_summarizer = LexRankSummarizer()
    lexrank_summary = lexrank_summarizer(parser.document, 10)
    if language == 'spanish':
        lexrank_summary = "Resumen por contexto utilizando LexRank:\n\n" + " ".join(
            str(sentence) for sentence in lexrank_summary)
    else:
        lexrank_summary = "Contextual summary using LexRank:\n\n" + " ".join(
            str(sentence) for sentence in lexrank_summary)

    # Return the generated summaries
    return general_summary, keywords_summary, lsa_summary, lexrank_summary

    # print_summary(general_summary, keywords_summary,
    #              lsa_summary, lexrank_summary)


def summarize_text_file(file_path, language='english'):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # General summary
    if language == 'spanish':
        general_summary = "Resumen general: Text file"
    else:
        general_summary = "General summary: Text file"

    # Keywords summary
    keywords_summary = generate_keywords_summary(text, language)

    # Contextual summary using LSA
    sentences = sent_tokenize(text)
    parser = Tokenizer(language)
    lsa_summarizer = LsaSummarizer()
    lsa_summary = lsa_summarizer(parser.document_from_sentences(sentences), 3)
    if language == 'spanish':
        lsa_summary = "Resumen por contexto utilizando LSA:\n\n" + " ".join(
            str(sentence) for sentence in lsa_summary)
    else:
        lsa_summary = "Contextual summary using LSA:\n\n" + " ".join(
            str(sentence) for sentence in lsa_summary)

    # Contextual summary using LexRank
    lexrank_summarizer = LexRankSummarizer()
    lexrank_summary = lexrank_summarizer(
        parser.document_from_sentences(sentences), 3)
    if language == 'spanish':
        lexrank_summary = "Resumen por contexto utilizando LexRank:\n\n" + " ".join(
            str(sentence) for sentence in lexrank_summary)
    else:
        lexrank_summary = "Contextual summary using LexRank:\n\n" + " ".join(
            str(sentence) for sentence in lexrank_summary)

    # Return the generated summaries
    return general_summary, keywords_summary, lsa_summary, lexrank_summary


def summarize_pdf_file(file_path, language='english'):
    try:
        text = textract.process(file_path).decode('utf-8')
    except Exception as e:
        print(f"Error occurred while processing PDF file: {e}")
        return None

    # General summary
    if language == 'spanish':
        general_summary = "Resumen general: PDF file"
    else:
        general_summary = "General summary: PDF file"

    # Keywords summary
    keywords_summary = generate_keywords_summary(text, language)

    # Contextual summary using LSA
    sentences = sent_tokenize(text)
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    lsa_summarizer = LsaSummarizer()
    lsa_summary = lsa_summarizer(parser.document, 3)
    if language == 'spanish':
        lsa_summary = "Resumen por contexto utilizando LSA:\n\n" + " ".join(
            str(sentence) for sentence in lsa_summary)
    else:
        lsa_summary = "Contextual summary using LSA:\n\n" + " ".join(
            str(sentence) for sentence in lsa_summary)

    # Contextual summary using LexRank
    lexrank_summarizer = LexRankSummarizer()
    lexrank_summary = lexrank_summarizer(parser.document, 3)
    if language == 'spanish':
        lexrank_summary = "Resumen por contexto utilizando LexRank:\n\n" + " ".join(
            str(sentence) for sentence in lexrank_summary)
    else:
        lexrank_summary = "Contextual summary using LexRank:\n\n" + " ".join(
            str(sentence) for sentence in lexrank_summary)

    # Return the generated summaries
    return general_summary, keywords_summary, lsa_summary, lexrank_summary


def summarize_word_file(file_path, language='english'):
    try:
        document = Document(file_path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs]
        text = "\n".join(paragraphs)
    except Exception as e:
        print(f"Error occurred while processing Word file: {e}")
        return None

    # General summary
    if language == 'spanish':
        general_summary = "Resumen general: Word file"
    else:
        general_summary = "General summary: Word file"

    # Keywords summary
    keywords_summary = generate_keywords_summary(text, language)

    # Contextual summary using LSA
    sentences = sent_tokenize(text)
    parser = Tokenizer(language)
    lsa_summarizer = LsaSummarizer()
    lsa_summary = lsa_summarizer(parser.document_from_sentences(sentences), 3)
    if language == 'spanish':
        lsa_summary = "Resumen por contexto utilizando LSA:\n\n" + " ".join(
            str(sentence) for sentence in lsa_summary)
    else:
        lsa_summary = "Contextual summary using LSA:\n\n" + " ".join(
            str(sentence) for sentence in lsa_summary)

    # Contextual summary using LexRank
    lexrank_summarizer = LexRankSummarizer()
    lexrank_summary = lexrank_summarizer(
        parser.document_from_sentences(sentences), 3)
    if language == 'spanish':
        lexrank_summary = "Resumen por contexto utilizando LexRank:\n\n" + " ".join(
            str(sentence) for sentence in lexrank_summary)
    else:
        lexrank_summary = "Contextual summary using LexRank:\n\n" + " ".join(
            str(sentence) for sentence in lexrank_summary)

    # Return the generated summaries
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
    keywords_summary = "Keywords: " + ", ".join(keywords)
    return keywords_summary


def print_summary(summarize_web_page):
    # def print_summary(general_summary, keywords_summary, lsa_summary, lexrank_summary):
    general_summary, keywords_summary, lsa_summary, lexrank_summary = summarize_web_page
    print("---------------------------------")
    print(general_summary)
    print("---------------------------------")
    print(keywords_summary)
    print("---------------------------------")
    print(lsa_summary)
    print("---------------------------------")
    print(lexrank_summary)
    print("---------------------------------")


# Example usage
# url = "https://aws.amazon.com/es/docker/"
# url = "example.txt"
url = "ab.pdf"
# url = "example.docx"
# url = "example.doc"

summarize_document(url, language='spanish')
