import os
import urllib.request

IMAGE_CACHE_DIR = "image_cache"
if not os.path.exists(IMAGE_CACHE_DIR):
    os.mkdir(IMAGE_CACHE_DIR)

DECK_INPUT_DIR = "decks"
if not os.path.exists(DECK_INPUT_DIR):
    os.mkdir(DECK_INPUT_DIR)

SPRITE_SHEET_OUTPUT_DIR = "sprite_sheets"
if not os.path.exists(SPRITE_SHEET_OUTPUT_DIR):
    os.mkdir(SPRITE_SHEET_OUTPUT_DIR)

CARD_BACK_FILE = os.path.join(SPRITE_SHEET_OUTPUT_DIR, "back.jpg")
if not os.path.exists(CARD_BACK_FILE):
    print("Downloading card back file")
    urllib.request.urlretrieve("https://d1u5p3l4wpay3k.cloudfront.net/mtgsalvation_gamepedia/thumb/f/f8/Magic_card_back.jpg/429px-Magic_card_back.jpg?version=d581d48ea4f0bfe8670c2e8a4cae3c98", CARD_BACK_FILE)