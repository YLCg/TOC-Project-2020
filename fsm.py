from transitions.extensions import GraphMachine
from utils import send_text_message, send_button_message, prepare_record
from database import database_create_person, line_insert_record, database_select, database_list,deleteData


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_person(self, event):
        text = event.message.text
        return text.lower() == "person"
    
    def is_going_to_insert(self, event):
        text = event.message.text
        return text.lower() == "insert"
    def is_going_to_select(self, event):
        text = event.message.text
        return text.lower() == "select"
    def is_going_to_input_data(self, event):
        text = event.message.text
        #return text.lower() == "select"
        return True
    def is_going_to_list(self, event):
        text = event.message.text
        if text.lower() == "list" or text.lower() == "name" or text.lower() == "birthday" or text.lower() == "first_solo_album" or text.lower() == "fav_song":
            return True;
        #return text.lower() == "select"
        return False
    def is_going_to_delete(self, event):
        text = event.message.text
        if 'delete' in text:
            return True
        else:
            return False

    def on_enter_person(self, event):
        print("I'm entering person")
        database_create_person()
        print("I'm finish")
        reply_token = event.reply_token
        send_text_message(reply_token, "person")
        #self.go_back(event)

    def on_exit_person(self,  event):
        print("Leaving person")
    
    def on_enter_insert(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請打輸入資料，格式為：\n姓名/生日（例：1994.10.11）/第一張solo專輯/您最喜歡的歌")
        #self.go_back(event)

    def on_exit_insert(self, event):
        print("Leaving insert")

    def on_enter_input_data(self, event):
        text = event.message.text
        if 'insert' in text:
            try:
                record_list = prepare_record(text)
                line_insert_record(record_list)

                reply_token = event.reply_token
                send_text_message(reply_token, "insert success ")
                self.go_back(event)

            except:
                reply_token = event.reply_token
                send_text_message(reply_token, "fail")

        print("I'm entering data")

        reply_token = event.reply_token
        send_text_message(reply_token, "fin the insert")
        self.go_back(event)

    def on_exit_input_data(self, event):
        print("Leaving input_data")

    def on_enter_select(self, event):
        print("I'm entering select")
        reply_token = event.reply_token
        send_text_message(reply_token, "select")
        #self.go_back(event)

    def on_exit_select(self,  event):
        print("Leaving select")

    def on_enter_list(self, event):
        print("I'm entering list")

        text = event.message.text
        repo=database_list(text)
        reply_token = event.reply_token
        send_text_message(reply_token, repo)
        self.go_back(event)

    def on_exit_list(self, event):
        print("Leaving list")


    def on_enter_delete(self, event):
        print("I'm entering delete")

        text = event.message.text

        text_list = text.split('\n')
        message = text_list[1]

        deleteData(message)

        reply_token = event.reply_token
        send_text_message(reply_token, "delete fin")
        self.go_back(event)

    def on_exit_delete(self, event):
        print("Leaving delete")



