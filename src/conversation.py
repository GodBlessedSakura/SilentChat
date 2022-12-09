from revChatGPT.revChatGPT import Chatbot


class ConversationBot():

    def __init__(self, config, reply, conversation_id):
        self.chatbot = Chatbot(config, conversation_id=conversation_id)
        self.first_interact = False
        if not conversation_id:  # No historical chat
            self.chatbot.reset_chat()  # Forgets conversation
            self.first_interact = True
        self.chatbot.refresh_session(
        )  # Uses the session_token to get a new bearer token
        self.reply = reply

    def reset(self):
        self.chatbot.reset_chat()
        self.first_interact = True

    def action(self, user_action):
        if not user_action:
            user_action = '如果我什么都不说，你要怎么回复我。'
        if user_action[-1] != "。":
            user_action = user_action + "。"
        prompt = user_action
        resp = self.chatbot.get_chat_response(
            prompt
        )  # Sends a request to the API and returns the response by OpenAI
        self.response = resp["message"]
