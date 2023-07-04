from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def search_messages_by_keyword(channel_id, keywords, language, app, say):
    # Retrieve all messages from the specified channel
    history = app.client.conversations_history(
        token=app._token,
        channel=channel_id
    )["messages"]

    num_msg = 0
    for message in history:
        print("Checking message:", message)
        num_msg += 1

        # Check if the message matches any of the keywords
        matches_keyword = any(
            keyword.lower() in message.get("text", "").lower()
            for keyword in keywords
        )

        if matches_keyword:
            print("Message matches keyword")
            permalink = app.client.chat_getPermalink(
                token=app._token,
                channel=channel_id,
                message_ts=message["ts"]
            )["permalink"]

            # Generate the summary using LSA
            content = message.get("text", "")

            # Language-specific settings
            if language == "english":
                parser = HtmlParser.from_string(content, Tokenizer("english"))
                summarizer = LsaSummarizer()
            elif language == "spanish":
                parser = HtmlParser.from_string(content, Tokenizer("spanish"))
                summarizer = LsaSummarizer()  # Adjust to Spanish-specific summarizer if available

            # Adjust the number of sentences as needed
            summary = summarizer(parser.document, sentences_count=2)

            say(f"Message Link: <{permalink}|Message Link>\nSummary: {summary}")

    say(f"\n{num_msg} messages checked.")


# @app.command("/search_by_keyword")
# def search_by_keyword(ack, say, command):
#     ack()
#     try:
#         # Extract the keywords and channels from the command
#         command_text = command.get("text")
#         keywords = re.findall(r"\b\w+\b", command_text.split("#")[0])
#         print(keywords)
#         channels = re.findall(r"#(\w+)", command_text)
#         print(channels)
#         say(
#             f"I'm searching for messages with these *keywords:* {keywords} in these *channels:* {channels}")

#         for channel in channels:
#             print("Checking channel:", channel)
#             channel_info = app.client.conversations_list(
#                 types="public_channel")["channels"]
#             matching_channels = [
#                 ch for ch in channel_info if ch["name"] == channel]

#             if matching_channels:
#                 print("Found matching channel")
#                 channel_id = matching_channels[0]["id"]
#                 logic.search_messages_by_keyword(
#                     channel_id, keywords, 'english', app, say)
#                 logic.search_messages_by_keyword(
#                     channel_id, keywords, 'spanish', app, say)
#             else:
#                 print("Channel not found:", channel)

#     except SlackApiError as e:
#         print(f"Error searching thread: {e.response['error']}")
