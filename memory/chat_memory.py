class ChatMemory:

    def __init__(self):

        self.messages = []

    def add_user_message(

        self,

        message

    ):

        self.messages.append({

            "role": "user",

            "content": message

        })

    def add_ai_message(

        self,

        message

    ):

        self.messages.append({

            "role": "assistant",

            "content": message

        })

    def get_history(self):

        history = ""

        for message in self.messages:

            history += (

                f"{message['role']} : "

                f"{message['content']}\n"

            )

        return history

    def clear(self):

        self.messages = []