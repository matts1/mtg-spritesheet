import os
import urllib

import requests
from requests import HTTPError

from constants import IMAGE_CACHE_DIR, DECK_INPUT_DIR, SPRITE_SHEET_OUTPUT_DIR
from sprite_sheet import SpriteSheet


def download_card_image(card):
    image_cache_path = os.path.join(IMAGE_CACHE_DIR, card + ".png")
    if not os.path.exists(image_cache_path):
        print("Downloading", card)
        json = get_json(card)
        image_uri = json['image_uris']['png']
        urllib.request.urlretrieve(image_uri, image_cache_path)
    return image_cache_path


def load_deck(deck_name):
    deck_filename = os.path.join(DECK_INPUT_DIR, deck_name + ".txt")
    with open(deck_filename) as deck:
        cards = []
        for line in deck:
            if line.rstrip():
                quantity, card = line.rstrip().split(" ", 1)
                quantity = int(quantity)
                card_file = download_card_image(card)
                for i in range(quantity):
                    cards.append(card_file)

        print("Downloaded all cards")

        SpriteSheet.create_sprite_sheets(deck_name, cards)


def get_json(card_name):
    response = requests.get('https://api.scryfall.com/cards/named?exact=%s' % card_name.replace(' ', '+'))
    response.raise_for_status()
    return response.json()


def is_outdated(deck):
    deck_last_modified = os.path.getmtime(os.path.join(DECK_INPUT_DIR, deck + ".txt"))
    output_last_modified = 0
    for extension in (".png", "_0.png"):
        output_path = os.path.join(SPRITE_SHEET_OUTPUT_DIR, deck + extension)
        if os.path.exists(output_path):
            output_last_modified = os.path.getmtime(output_path)
    return output_last_modified < deck_last_modified


def get_all_decks():
    all_decks = os.listdir(DECK_INPUT_DIR)
    return [deck.rsplit(".", 1)[0] for deck in all_decks]


def reload_outdated_decks():
    print("Reloading outdated decks")
    outdated_decks = [deck for deck in get_all_decks() if is_outdated(deck)]
    for deck in outdated_decks:
        print("Reloading outdated deck", deck)
        load_deck(deck)

if __name__ == "__main__":
    reload_outdated_decks()
