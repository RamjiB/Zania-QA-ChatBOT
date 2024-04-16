
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from utils import download_file, llm_chatbot_response
import json

from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

load_dotenv('.env')

SLACK_BOT_TOKEN=os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN=os.environ.get("SLACK_APP_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL_NAME = os.environ.get("GPT_MODEL_NAME")

if SLACK_APP_TOKEN is None or SLACK_BOT_TOKEN is None or OPENAI_API_KEY is None or MODEL_NAME is None:
    exit()

app = App(token=SLACK_BOT_TOKEN)

#Message handler for Slack
@app.message(".*")
def message_handler(body, say):
    """Receives the input from user and send the response

    Args:
        body: information of user text and files will be available here by slack client
        say: slack function to send the response to UI
    """
    download_status=400
    message="Upload a PDF file, and ask your questions seperated by new line for each question\nFor Example: \n1.Who is the CEO?\n2.What is the name of the company?"
    try:
        questions = body['event'].get("text")
        if body["event"].get("files"):
            pdf_url = body['event']["files"][0].get("url_private")
            download_status, message = download_file(pdf_url)
        llm_response = llm_chatbot_response(questions, download_status, message)
        if not isinstance(llm_response, str):
            llm_response = f"```{json.dumps(llm_response, indent = 2)}```"
    except Exception:
        llm_response = "Hi, How can I help you?"
    say(llm_response)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
