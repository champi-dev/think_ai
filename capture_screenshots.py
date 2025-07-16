import os
import tempfile
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions


def capture_screenshots(url, resolutions, save_dir="screenshots"):
    """
    Captures screenshots of a given URL at different resolutions.

    Args:
        url (str): The URL to capture.
        resolutions (list): A list of tuples, where each tuple represents a
                            resolution (width, height).
        save_dir (str, optional): The directory to save the screenshots in.
                                  Defaults to 'screenshots'.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with tempfile.TemporaryDirectory() as temp_dir:
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("headless")
        options.add_argument("--no-sandbox")
        options.add_argument(f"--user-data-dir={temp_dir}")

        service = EdgeService(executable_path="/usr/local/bin/msedgedriver")
        driver = webdriver.Edge(service=service, options=options)

        for width, height in resolutions:
            driver.set_window_size(width, height)
            driver.get(url)
            driver.save_screenshot(os.path.join(save_dir, f"{width}x{height}.png"))

        driver.quit()


if __name__ == "__main__":
    url = "https://thinkai.lat"
    resolutions = [
        (320, 480),
        (768, 1024),
        (1024, 768),
        (1920, 1080),
        (3840, 2160),
    ]
    capture_screenshots(url, resolutions)
