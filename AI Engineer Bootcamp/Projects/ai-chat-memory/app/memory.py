from langchain_core.messages import HumanMessage, AIMessage


class ChatMemory:
    def __init__(self, max_messages: int = 10):
        self.history = []
        self.max_messages = max_messages

    def add_user_message(self, message: str):
        self.history.append(
            HumanMessage(content=message)
        )
        self._trim_history()

    def add_ai_message(self, message: str):
        self.history.append(
            AIMessage(content=message)
        )
        self._trim_history()

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []

    def _trim_history(self):
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]