import os

from card import Card
from constants import DECK_INPUT_DIR, SPRITE_SHEET_OUTPUT_DIR
from sprite_sheet import SpriteSheet


class Deck(object):
    def __init__(self, filename):
        self.name = filename.rsplit(".", 1)[0]
        self.filename = os.path.join(DECK_INPUT_DIR, filename)
        self._cards = None

    def __str__(self):
        return self.name

    def save(self):
        primary_images = [card.image for card in self.cards]
        secondary_images = [image for c in self.cards for image in c.secondary_images]
        SpriteSheet.create_sprite_sheets(self.name, primary_images)
        if secondary_images:
            SpriteSheet.create_sprite_sheets(self.name + "_secondary", secondary_images)

    @property
    def cards(self):
        if self._cards is None:
            with open(self.filename) as deck:
                cards = []
                for line in deck:
                    if line.rstrip():
                        quantity, card = line.rstrip().split(" ", 1)
                        quantity = int(quantity)
                        for i in range(quantity):
                            cards.append(Card(card))

                self._cards = cards
        return self._cards


    def make_output_path(self, number=None):
        extension = ".png" if number is None else "_{}.png".format(number)
        return os.path.join(SPRITE_SHEET_OUTPUT_DIR, self.name + extension)

    def is_outdated(self):
        input_last_modified = os.path.getmtime(self.filename)
        output_last_modified = 0
        for output in (self.make_output_path(), self.make_output_path(0)):
            if os.path.exists(output):
                output_last_modified = os.path.getmtime(output)
        return output_last_modified < input_last_modified

    @classmethod
    def get_all_decks(cls):
        return [cls(f) for f in os.listdir(DECK_INPUT_DIR)]

    @classmethod
    def reload_outdated_decks(cls):
        print("Reloading outdated decks")
        outdated_decks = [deck for deck in cls.get_all_decks() if deck.is_outdated()]
        for deck in outdated_decks:
            print("Reloading outdated deck", deck)
            deck.save()


if __name__ == "__main__":
    Deck.reload_outdated_decks()
