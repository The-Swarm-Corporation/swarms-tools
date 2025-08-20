import os
import httpx
from loguru import logger
from dotenv import load_dotenv

load_dotenv()  # Load environment variables


class SynthesiaAPI:
    def __init__(
        self, bearer_key: str = os.getenv("SYNTHESIA_API_KEY")
    ):
        """
        Initialize the Synthesia API client with a bearer key.

        Args:
            bearer_key (str): The bearer key for authentication.
        """
        self.url = "https://api.synthesia.io/v2/videos"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {bearer_key}",
        }

    def create_video(self, payload: dict) -> str:
        """
        Create a video using the Synthesia API.

        Args:
            payload (dict): The payload for the video creation request.

        Returns:
            str: The response text from the API.
        """
        try:
            response = httpx.post(
                self.url, json=payload, headers=self.headers
            )
            response.raise_for_status()
            logger.info("Video creation request sent successfully.")
            return response.text
        except httpx.RequestException as e:
            logger.error(f"Failed to create video: {e}")
            return "Failed to create video"


def synthesia_api(payload: dict) -> str:
    """
    Create a video using the Synthesia API.

    Args:
        payload (dict): The payload for the video creation request.

    Returns:
        str: The response text from the API.
    """
    synthesia = SynthesiaAPI()
    payload = {
        "test": True,
        "title": "My first Synthetic video",
        "visibility": "private",
        "aspectRatio": "16:9",
    }
    response = synthesia.create_video(payload)
    return response
