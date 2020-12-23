from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_group(self, event):
        text = event.message.text
        return text.lower() == "group"

    def is_going_to_person(self, event):
        text = event.message.text
        return text.lower() == "person"
    
    def is_going_to_data(self, event):
        text = event.message.text
        return text.lower() == "data"


    def on_enter_group(self, event):
        print("I'm entering group")

        reply_token = event.reply_token
        send_text_message(reply_token, "group")
        #self.go_back(event)

    def on_exit_group(self,  event):
        print("Leaving group")


    def on_enter_person(self, event):
        print("I'm entering person")

        reply_token = event.reply_token
        send_text_message(reply_token, "person")
        self.go_back(event)

    def on_exit_person(self,  event):
        print("Leaving person")

    
    def on_enter_data(self, event):
        print("I'm entering state1")
        reply_token = event.reply_token
        send_text_message(reply_token, "data")

        self.go_back(event)

    def on_exit_data(self, event):
        print("Leaving data")

