from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from slack_sdk.errors import SlackApiError
import re
import url_summarizer
from analyze_msg import analyze_slack_message
# from datetime import datetime
# import time
# import url_summ_keyword
# from langdetect import detect
# from sumy.summarizers.lsa import LsaSummarizer
# from sumy.summarizers.lex_rank import LexRankSummarizer
# from nltk.tokenize import sent_tokenize

# Obtener tokens de autenticación desde variables de entorno
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')

# print(SLACK_APP_TOKEN)
# print(SLACK_BOT_TOKEN)

# Crear una instancia de la aplicación Bolt
app = App(token=SLACK_BOT_TOKEN)


@app.command("/summarize_url")
def summarize_url(ack, say, command):
    ack()
    try:
        args = command['text'].split()
        urls = []
        languages = []
        current_language = 'english'

        for arg in args:
            if re.match(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', arg):
                urls.append(arg)
                languages.append(current_language)
                if current_language == 'spanish':
                    current_language = 'english'
            elif arg.lower() == 'spanish':
                current_language = 'spanish'

        for url, language in zip(urls, languages):
            general_summary, keywords_summary, lsa_summary, lexrank_summary = url_summarizer.summarize_web_page(
                url, language)
            say(f"{general_summary}\n\n{keywords_summary}\n\n{lsa_summary}\n\n{lexrank_summary}")
    except SlackApiError as e:
        print(f"Error: {e.response['error']}")


@app.command("/search_by_keyword")
def search_by_keyword(ack, say, command):
    ack()
    try:
        # Extract the keywords and channels from the command
        command_text = command.get("text")
        keywords = re.findall(r"\b\w+\b", command_text.split("#")[0])
        print(keywords)
        channels = re.findall(r"#(\w+)", command_text)
        print(channels)
        say(
            f"I'm searching for messages with these *keywords:* {keywords} in these *channels:* {channels}")

        for channel in channels:
            print("Checking channel:", channel)
            channel_info = app.client.conversations_list(
                types="public_channel")["channels"]
            matching_channels = [
                ch for ch in channel_info if ch["name"] == channel]

            if matching_channels:
                print("Found matching channel")
                channel_id = matching_channels[0]["id"]

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

                        # Perform analysis on the matched message
                        analysis = analyze_slack_message(message["text"])

                        say(f"{analysis}\n<{permalink}|Message Link>")

                say(f"\n{num_msg} messages checked.")
            else:
                print("Channel not found:", channel)

    except SlackApiError as e:
        print(f"Error searching messages: {e.response['error']}")


@app.command("/search_thread")
def search_thread(ack, say, command):
    ack()
    try:
        # Extract the keywords and channels from the command
        command_text = command.get("text")
        keywords = re.findall(r"\b\w+\b", command_text.split("#")[0])
        print(keywords)
        channels = re.findall(r"#(\w+)", command_text)
        print(channels)
        say(
            f"I'm searching for messages with these *keywords:* {keywords} in these *channels:* {channels}")

        for channel in channels:
            print("Checking channel:", channel)
            channel_info = app.client.conversations_list(
                types="public_channel")["channels"]
            matching_channels = [
                ch for ch in channel_info if ch["name"] == channel]

            if matching_channels:
                print("Found matching channel")
                channel_id = matching_channels[0]["id"]

                # Retrieve all messages from the specified channel
                history = app.client.conversations_history(
                    token=app._token, channel=channel_id)["messages"]

                num_msg = 0
                for message in history:
                    if "thread_ts" in message:
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

                            # Get the entire thread
                            thread = app.client.conversations_replies(
                                token=app._token,
                                channel=channel_id,
                                ts=message["thread_ts"]
                            )["messages"]

                            # Combine all messages in the thread
                            thread_messages = " ".join(
                                msg["text"] for msg in thread)

                            # Perform analysis on the combined thread messages
                            analysis = analyze_slack_message(thread_messages)

                            say(f"{analysis}\n<{permalink}|Message Link>")

                say(f"\n{num_msg} messages checked.")
            else:
                print("Channel not found:", channel)

    except SlackApiError as e:
        print(f"Error searching messages: {e.response['error']}")


@app.event("app_mention")
def mention_handler(body, say):
    say('Hello, JARVIS here, alive and ready to help!')
    # Hi! I'm here to help you. Please provide a detailed description of the problem and, if possible, links to any relevant resources or previous discussions in the channel.


@app.command("/help")
def help(ack, body, say):
    ack()
    commands = [
        {
            "command": "/summarize_url",
            "description": "Summarize the content of a web page.",
            "usage": "/summarize_url [URL1] [URL2] ... [URLN]"
        },
        {
            "command": "/summarize_url_by_keyword",
            "description": "Summarize a web page based on a specific topic.",
            "usage": "/summarize_url_by_keyword [URL] [keyword]"
        },
        {
            "command": "/summarize_format",
            "description": "Summarize other types of documentation like PDF and TXT.",
            "usage": "/summarize_format [file URL]"
        },
        {
            "command": "/summarize_format_by_keyword",
            "description": "Summarize a file based on a specific topic.",
            "usage": "/summarize_format_by_keyword [file URL] [keyword]"
        },
        {
            "command": "/search_by_keyword",
            "description": "Search for messages containing specific keywords in channels.",
            "usage": "/search_by_keyword [keyword1] [keyword2] ... [keywordN] #[channel1] #[channel2] ... #[channelN]"
        },
        {
            "command": "/search_thread",
            "description": "Search for messages with specific keywords within threads in channels.",
            "usage": "/search_thread [keyword1] [keyword2] ... [keywordN] #[channel1] #[channel2] ... #[channelN]"
        },
        {
            "command": "/analyze_it",
            "description": "Analyze a message or thread and provide a summary.",
            "usage": "/analyze_it [permalink]"
        }
    ]

    help_message = "Hi, I'm JARVIS and I'm here to help you!\n\n"

    for cmd in commands:
        help_message += f"*Command:* {cmd['command']}\n"
        help_message += f"*Description:* {cmd['description']}\n"
        help_message += f"*Usage:* `{cmd['usage']}`\n\n"

    say(help_message)


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


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

#                 # Retrieve all messages from the specified channel
#                 history = app.client.conversations_history(
#                     token=app._token,
#                     channel=channel_id
#                 )["messages"]

#                 num_msg = 0
#                 for message in history:
#                     print("Checking message:", message)
#                     num_msg += 1

#                     # Check if the message matches any of the keywords
#                     matches_keyword = any(
#                         keyword.lower() in message.get("text", "").lower()
#                         for keyword in keywords
#                     )

#                     if matches_keyword:
#                         print("Message matches keyword")
#                         permalink = app.client.chat_getPermalink(
#                             token=app._token,
#                             channel=channel_id,
#                             message_ts=message["ts"]
#                         )["permalink"]
#                         say(f"<{permalink}|Message Link>")

#                 say(f"\n{num_msg} messages checked.")
#             else:
#                 print("Channel not found:", channel)

#     except SlackApiError as e:
#         print(f"Error searching thread: {e.response['error']}")
