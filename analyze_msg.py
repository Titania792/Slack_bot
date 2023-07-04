import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer


def analyze_slack_message(message):
    # Check if the message is too short
    if len(message) < 10:
        return "The message is too short to provide a meaningful analysis."

    # Initialize spaCy and load the English model
    nlp = spacy.load("en_core_web_sm")

    # Remove stop words
    stop_words = set(stopwords.words("english"))
    tokens = [token.text for token in nlp(
        message) if token.text.lower() not in stop_words]

    # Perform sentiment analysis using NLTK's SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(message)["compound"]
    sentiment = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"

    # Generate a summary of what the message talks about using extractive summarization
    parser = PlaintextParser.from_string(message, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    print(parser.document)
    summary = summarizer(parser.document, sentences_count=10)[0]

    summarizer2 = LsaSummarizer()
    summary2 = summarizer2(parser.document, sentences_count=10)

    # Construct the analysis response
    analysis = f"The message indicates a {sentiment} sentiment.\n\nSummary LexRank: {summary}\nSummary LSA: {summary2}"

    return analysis
