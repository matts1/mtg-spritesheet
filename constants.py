import os

IMAGE_CACHE_DIR = "image_cache"
if not os.path.exists(IMAGE_CACHE_DIR):
    os.mkdir(IMAGE_CACHE_DIR)

DECK_INPUT_DIR = "decks"
if not os.path.exists(DECK_INPUT_DIR):
    os.mkdir(DECK_INPUT_DIR)

SPRITE_SHEET_OUTPUT_DIR = "sprite_sheets"
if not os.path.exists(SPRITE_SHEET_OUTPUT_DIR):
    os.mkdir(SPRITE_SHEET_OUTPUT_DIR)
