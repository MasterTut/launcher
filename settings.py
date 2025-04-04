#!/bin/python3

#Setting file
import os
NAME = "TVLauncher"


# Project Root directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

resolutionWidth = 1920 
resolutionHeight = 1080
#resolutionWidth, resolutionHeight = info.current_w, info.current_h

#Display Settings
WINDOW_SIZE = (resolutionWidth, resolutionHeight)
FPS = 60

#Font Settings 
FONT_PATH = os.path.join(BASE_DIR, "Assets", "Fonts", "JetBrainsMonoNLNerdFontPropo-Regular.ttf")
FONT_SIZE = 30

# Colors
BACKGROUND_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)  # Black
BUTTON_COLOR = (100, 100, 200)  # Blue-ish


# Asset paths
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "Assets", "Images", "background2.jpg")
TEST_BUTTON_IMAGE = os.path.join(BASE_DIR, "Assets", "Images", "testing.png")
CLICK_SOUND = os.path.join(BASE_DIR, "Assets", "Sound", "click.wav")
APPS_PATH = os.path.join(BASE_DIR, "apps.json")
