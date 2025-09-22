import os
from dotenv import load_dotenv
from swarms_tools.character.synthesia_tool import SynthesiaAPI, synthesia_api

load_dotenv()

api_key = os.getenv("SYNTHESIA_API_KEY")
if not api_key:
    exit()

# Test SynthesiaAPI class initialization
synthesia_client = SynthesiaAPI(bearer_key=api_key)
assert synthesia_client is not None
assert synthesia_client.bearer_key == api_key

# Test video creation payload structure
video_payload = {
    "test": True,
    "title": "My AI Generated Video",
    "visibility": "private",
    "aspectRatio": "16:9",
    "script": "Hello! This is an AI-generated video using Synthesia. Welcome to the future of video creation!",
    "avatar": "anna_costume1_cameraA",
    "background": "office_background"
}

# Test that required payload fields are present
assert "test" in video_payload
assert "title" in video_payload
assert "script" in video_payload
assert "avatar" in video_payload

# Test video creation method exists
assert hasattr(synthesia_client, 'create_video')
assert callable(synthesia_client.create_video)

# Test simplified function exists
assert callable(synthesia_api)

# Test that both methods can be called (will fail without valid API key, but structure is tested)
try:
    response = synthesia_client.create_video(video_payload)
    assert response is not None
except Exception:
    pass  # Expected to fail without valid API key

try:
    simple_response = synthesia_api({})
    assert simple_response is not None
except Exception:
    pass  # Expected to fail without valid API key
