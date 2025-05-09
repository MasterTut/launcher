#!/bin/python3

#Setting file
import os
NAME = "TVLauncher"
#Colors 

WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 150, 255)
DARK_BLUE = (10, 10, 74)
RED = (255, 0, 0)
BLACK = (0,0,0)
# Project Root directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

resolutionWidth = 1920 
resolutionHeight = 1080
#resolutionWidth, resolutionHeight = info.current_w, info.current_h

#Display Settings
WINDOW_SIZE = (resolutionWidth, resolutionHeight)
FPS = 60

#Font Settings 
FONT_PATH = os.path.join(BASE_DIR, "Assets", "Fonts", "GoMonoNerdFont-Bold.ttf")
FONT_SIZE = 30

# Colors
BACKGROUND_COLOR = WHITE  # White
TEXT_COLOR = BLACK  # Black
BUTTON_COLOR = (100, 100, 200)  # Blue-ish


# Asset paths
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "Assets", "Images", "background2.jpg")
TEST_BUTTON_IMAGE = os.path.join(BASE_DIR, "Assets", "Images", "testing.png")
MUSIC = os.path.join(BASE_DIR, "Assets", "Sound", "Music","space-trip.mp3")
CLICK_SOUND = os.path.join(BASE_DIR, "Assets", "Sound", "click.mp3")
APPS_PATH = os.path.join(BASE_DIR, "apps.json")
