import os
from datetime import datetime

import pyautogui

from cheattest.constants import IMAGES_DIR
from cheattest.commands.base import BaseCommand


class ScreenCommand(BaseCommand):
    """Takes whole screenshot, saves downscaled version
       to the specified folder.
    """

    def __init__(self, image_quality: int = 100, **kwargs):
        self.image_quality = image_quality

    def do(self):
        screenshot = pyautogui.screenshot()
        when_taken = datetime.utcnow().isoformat()
        image_filepath = os.path.join(IMAGES_DIR, when_taken + ".jpeg")
        
        os.makedirs(os.path.dirname(image_filepath), exist_ok=True)
        screenshot.save(image_filepath)

        # lower image quality for lower size
        if self.image_quality < 100:
            os.system(f"mogrify -quality {self.image_quality} {image_filepath}")
