from livekit import agents, rtc
from livekit.agents import AgentServer,AgentSession, Agent, room_io
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from tools import get_employee_directory,load_employee_directory

class Assistant(Agent):
    def __init__(self) -> None:
        load_employee_directory()
        super().__init__(
            instructions="""
            You are a real-time voice AI assistant.
            You can look up employee contact information when needed.
            Follow these rules:
            - Use tools when factual lookup is required.
            - Never guess email addresses.
            - Speak concisely and naturally.
            - If the tool has some fields that are ********, that means the user is not 
              allowed to access those fields. Please inform the user that you are not 
              allowed to access those fields.
            """,
            tools=[get_employee_directory],
        )
    async def on_user_message(self, message):
        await self.say(
            "Hello! I can hear you. How can I help?"
        )
    async def on_user_transcript(self, transcript: str, **kwargs):
        print("👂 User said:", transcript)
        await self.say("Hello! I can hear you. How can I help?")
