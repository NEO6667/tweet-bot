import os
import requests
from urllib.parse import urlparse

def download_article_image(image_url, save_path="temp_image.jpg"):
    if not image_url:
        return None

    try:
        response = requests.get(image_url, timeout=10, stream=True)
        response.raise_for_status()

        # Verify it's actually an image
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            return None

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        return save_path
    except Exception as e:
        print(f"Image download failed: {e}")
        return None