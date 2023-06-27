import requests
from bs4 import BeautifulSoup
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def analyze_documentation(link):
    # Fetch the HTML content from the documentation link
    response = requests.get(link)
    html_content = response.content

    # Parse the HTML content using sumy's HtmlParser
    parser = HtmlParser.from_string(html_content, link, Tokenizer("english"))
    document = parser.document

    # Initialize LexRankSummarizer and set the number of sentences in the summary
    summarizer = LexRankSummarizer()
    summary_sentences_count = 3  # Adjust the number of sentences in the summary as needed

    # Generate the summary
    summary = summarizer(document, summary_sentences_count)

    # Join the summary sentences into a single string
    summary_text = ' '.join(str(sentence) for sentence in summary)

    return summary_text


# Example usage
documentation_link = 'https://docs.docker.com/get-started/02_our_app/'
summary = analyze_documentation(documentation_link)
print(summary)
