from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from datetime import datetime
from slack_sdk.errors import SlackApiError
import time
import url_summarizer

# Obtener tokens de autenticación desde variables de entorno
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')


# Crear una instancia de la aplicación Bolt
app = App(token=SLACK_BOT_TOKEN)


@app.event("app_mention")
def mention_handler(body, say):
    say('Hello, JARVIS here, alive and ready to help!')
    # Hi! I'm here to help you. Please provide a detailed description of the problem and, if possible, links to any relevant resources or previous discussions in the channel.


@app.command("/help")
def help(body, say):
    say("Hi, I'm JARVIS and I'm here to help you!\nYou can ask me about any problem you may have and I'm going to try to help you going through the steps of solving it.")


@app.command("/summarize_url")
def url_documentation(ack, say, command):
    ack()
    # say(f"From your message: {command['command']} {command['text']}\n")
    urls = command['text'].split()
    # print(urls)
    for url in urls:
        general_summary, keywords_summary, lsa_summary, lexrank_summary = url_summarizer.summarize_web_page(
            url)
        say(f"{general_summary}\n\n{keywords_summary}\n\n{lsa_summary}\n\n{lexrank_summary}")
        # say(general_summary)
        # say(keywords_summary)
        # say(lexrank_summary)
        # say("---------------------------------")


@app.command("/Jarvis")
def see_problem():
    pass


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
