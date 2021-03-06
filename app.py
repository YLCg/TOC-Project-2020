import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message,send_button_message,send_image_message
load_dotenv()


machine = TocMachine(
    states=["person", "insert", "input_data", "select", "list", "delete", "update", "updating", "show_img"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "person",
            "conditions": "is_going_to_person",
        },
        {
            "trigger": "advance",
            "source": "person",
            "dest": "insert",
            "conditions": "is_going_to_insert",
        },
        {
            "trigger": "advance",
            "source": "insert",
            "dest": "input_data",
            "conditions": "is_going_to_input_data",
        },
        {
            "trigger": "advance",
            "source": "person",
            "dest": "select",
            "conditions": "is_going_to_select",
        },
        {
            "trigger": "advance",
            "source": "select",
            "dest": "list",
            "conditions": "is_going_to_list",
        },
        {
            "trigger": "advance",
            "source": "select",
            "dest": "delete",
            "conditions": "is_going_to_delete",
        },
        {
            "trigger": "advance",
            "source": "person",
            "dest": "update",
            "conditions": "is_going_to_update",
        },
        {
            "trigger": "advance",
            "source": "update",
            "dest": "updating",
            "conditions": "is_going_to_updating",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "show_img",
            "conditions": "is_going_to_show_img",
        },
        {"trigger": "go_back",
         "source": ["person", "insert", "select", "input_data", "list", "delete", "update", "updating","show_img"],
         "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
fsm_host = os.getenv("FSM", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)





@app.route("/callback", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        
        response = machine.advance(event)

        if response == False:

            if event.message.text.lower() == 'fsm':
                send_image_message(event.reply_token, fsm_host)
                #send_image_message(event.reply_token, 'https://41e22cc69ba9.ngrok.io/show-fsm')
                #send_image_message(event.reply_token, 'https://f64061070.herokuapp.com/show-fsm')

            elif event.message.text.lower() == "re":
                send_text_message(event.reply_token, "restart")
                machine.go_back(event)
            elif machine.state == "user":
                send_text_message(event.reply_token, "輸入「show fsm」獲得此line bot 的fsm。\n輸入「person」進入資料庫。\n輸入「re」會回到最開始")
            elif machine.state == "update":
                send_text_message(event.reply_token, "請選擇條件\n")
            else:
                send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    #machine.get_graph().draw("fsm.png", prog="dot", format="png")
    #return send_file("fsm.png", mimetype="image/png")
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    #port = os.environ.get("PORT", 8000)
    #app.run(host="0.0.0.0", port=port, debug=True)
    PORT = os.environ['PORT']
    app.run(host="0.0.0.0", port=PORT, debug=True)
