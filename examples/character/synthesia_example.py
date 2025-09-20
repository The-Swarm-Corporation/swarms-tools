import os
from dotenv import load_dotenv
from swarms_tools.character.synthesia_tool import SynthesiaAPI

load_dotenv()

api_key = os.getenv("SYNTHESIA_API_KEY")
if not api_key:
    print("SYNTHESIA_API_KEY not found in environment variables")
    exit()

synthesia_client = SynthesiaAPI(bearer_key=api_key)

# Create a video with custom configuration
video_payload = {
    "test": True,
    "title": "My AI Generated Video",
    "visibility": "private",
    "aspectRatio": "16:9",
    "script": "Hello! This is an AI-generated video using Synthesia. Welcome to the future of video creation!",
    "avatar": "anna_costume1_cameraA",
    "background": "office_background"
}

response = synthesia_client.create_video(video_payload)
print(f"Video creation response: {response}")

# Also demonstrate the simplified function
simple_response = synthesia_api({})
print(f"Simple API response: {simple_response}")
