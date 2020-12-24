from transitions.extensions import GraphMachine
from utils import send_text_message, send_button_message
from database import database_creat_person


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # def is_going_to_start(self, event):
    #     text = event.message.text
    #     return text.lower() == "start"
    #
    # def is_going_to_group(self, event):
    #     text = event.message.text
    #     return text.lower() == "group"

    def is_going_to_person(self, event):
        text = event.message.text
        return text.lower() == "person"
    
    def is_going_to_insert(self, event):
        text = event.message.text
        return text.lower() == "insert"

    # def on_enter_group(self, event):
    #     print("I'm entering group")
    #
    #     reply_token = event.reply_token
    #     send_text_message(reply_token, "group")
    #     self.go_back(event)
    #
    # def on_exit_group(self,  event):
    #     print("Leaving group")

    def on_enter_person(self, event):
        print("I'm entering person")
        database.database_creat_person()

        reply_token = event.reply_token
        send_text_message(reply_token, "person")
        #self.go_back(event)

    def on_exit_person(self,  event):
        print("Leaving person")
    
    def on_enter_insert(self, event):
        text = event.message.text
        try:
            record_list = utils.prepare_record(text)
            database.line_insert_record(record_list)

            reply_token = event.reply_token
            line_bot_api.reply_message(reply_token, "insert success ")

        except:
            reply_token = event.reply_token
            send_text_message(reply_token, "fail")

        print("I'm entering data")
        reply_token = event.reply_token
        send_text_message(reply_token, "data")

        self.go_back(event)

    def on_exit_insert(self, event):
        print("Leaving data")

