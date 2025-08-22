from clients import CrewAiClient
from models import Conversation, Message


class MessageSubmissionService:
    def __init__(self, conversation: Conversation):
        self._conversation = conversation
        self._client = CrewAiClient()

    def send_message(self, message: Message):
        inputs = {"id": self._conversation.id, "user_message": message.model_dump()}
        kickoff_id = self._client.kickoff(inputs)
        result_json = self._client.status(kickoff_id)
        return Message(**result_json["history"][-1])
