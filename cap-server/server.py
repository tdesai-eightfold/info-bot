from dotenv import load_dotenv
import asyncio
import os
from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, room_io
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from agent import Assistant

load_dotenv(".env.local")
print(os.getenv("LIVEKIT_AGENT_NAME"))
server = AgentServer()

@server.rtc_session()
async def my_agent(ctx: agents.JobContext):
    print("🚀 AGENT DISPATCHED")
    print("🏷 ROOM:", ctx.room.name)

    session = AgentSession(
        stt="assemblyai/universal-streaming:en",
        llm="openai/gpt-4.1-mini",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    #Logging Mistake-3
    def on_data(data: bytes, participant: rtc.Participant):
        msg = data.decode()
        print(f"📩 FROM {participant.identity}: {msg}")

        asyncio.create_task(
            session.send_data(
                f"Agent received: {msg}".encode()
            )
        )

    session.on("data", on_data)

    await session.start(
        room=ctx.room,
        agent=Assistant(),
    )

    await session.say("Agent connected")


if __name__ == "__main__":
    agents.cli.run_app(server)
