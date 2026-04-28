import time
import os
import signal
import threading
from dotenv import load_dotenv
from tools import client_tools
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

try:
    import websockets.exceptions
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False

load_dotenv()
print(f"Client tools registered: {list(client_tools.tools.keys())}")

agent_id = os.getenv("AGENT_ID")
api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=api_key)

_session_ended = False
_session_lock = threading.Lock()

def safe_end_session():
    global _session_ended
    with _session_lock:
        if _session_ended:
            return
        _session_ended = True
    try:
        time.sleep(0.5)  
        conversation.end_session()
    except OSError:
        pass  
    except Exception as e:
        if WEBSOCKETS_AVAILABLE and isinstance(e, websockets.exceptions.ConnectionClosedOK):
            pass  
        else:
            print(f"[Session End Warning]: {e}")

conversation = Conversation(
    client,
    agent_id,
    client_tools=client_tools,
    requires_auth=bool(api_key),
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=lambda response: print(f"Agent: {response}"),
    callback_agent_response_correction=lambda original, corrected: print(f"Agent: {original} -> {corrected}"),
    callback_user_transcript=lambda transcript: print(f"User: {transcript}"),
)

conversation.start_session()
signal.signal(signal.SIGINT, lambda sig, frame: safe_end_session())

try:
    conversation_id = conversation.wait_for_session_end()
except OSError:
    conversation_id = None
    print("[Info] Audio stream closed during session end (non-critical).")
except Exception as e:
    conversation_id = None
    if WEBSOCKETS_AVAILABLE and isinstance(e, websockets.exceptions.ConnectionClosedOK):
        print("[Info] WebSocket closed cleanly.")
    else:
        print(f"[Warning] Unexpected error during session: {e}")
finally:
    time.sleep(1)

print(f"Conversation ID: {conversation_id}")
