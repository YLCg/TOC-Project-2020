import os
import datetime
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(reply_token, title, text, btn):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            #thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"
def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"


def prepare_record(text):
    text_list = text.split('\n')

    record_list = []

    for i in text_list[1:]:
        temp_list = i.split('/')

        temp_name = temp_list[0]
        print(temp_name)

        year = temp_list[1].split('.')[0]
        month = temp_list[1].split('.')[1]
        day = temp_list[1].split('.')[2]
        d = datetime.date(int(year), int(month), int(day))

        first_solo_album = temp_list[2]
        fav_song = temp_list[3]

        record = (temp_name, d, first_solo_album, fav_song)
        record_list.append(record)

    return record_list

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
