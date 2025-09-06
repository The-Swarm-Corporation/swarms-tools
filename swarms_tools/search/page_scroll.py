"""
IMPROVEMENTS:
- Add control so scrolls in segments and moves on once needed
- Scroll sidebars and topbar options
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import cv2
import numpy as np
import os

def scroll_and_record(url, duration_seconds=10, output_filename="scroll_recording1.mp4", scroll_increment=20, scroll_interval=0.05):
    '''
    Opens the given URL in a headless browser, scrolls in very small increments for the specified duration,
    records the scrolling as a video, and saves it locally.

    Args:
        url (str): The URL to open.
        duration_seconds (int): Total time to scroll and record (in seconds).
        output_filename (str): Name of the output video file.
        scroll_increment (int): Number of pixels to scroll per increment.
        scroll_interval (float): Time (in seconds) between scrolls/frames.
    '''
    # Set up headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use new headless mode for screenshots
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(2)  # Wait for page to load

        # Get page height
        total_height = driver.execute_script("return document.body.scrollHeight")
        current_scroll = 0

        # Prepare video writer
        screenshot = driver.get_screenshot_as_png()
        img_array = np.frombuffer(screenshot, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        height, width, _ = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_filename, fourcc, int(1/scroll_interval), (width, height))

        start_time = time.time()
        while (time.time() - start_time) < duration_seconds:
            # Scroll by small increment
            driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
            current_scroll += scroll_increment
            # Clamp to bottom
            if current_scroll > total_height:
                current_scroll = total_height
                driver.execute_script(f"window.scrollTo(0, {total_height});")
            # Take screenshot
            screenshot = driver.get_screenshot_as_png()
            img_array = np.frombuffer(screenshot, dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            out.write(frame)
            time.sleep(scroll_interval)
        out.release()
        print(f"Scroll recording saved to {os.path.abspath(output_filename)}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# # Example usage
# if __name__ == '__main__':
#     scroll_and_record("https://docs.swarms.ai/capabilities/agent", duration_seconds=10)