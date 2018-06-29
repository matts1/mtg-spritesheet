import os

from PIL import Image

from constants import SPRITE_SHEET_OUTPUT_DIR


class SpriteSheet(object):
    @staticmethod
    def create_sprite_sheets(filename, images, width=10, height=7):
        size = width * height
        if len(images) > size:
            filename = filename + "_{number}"

        for i in range(0, len(images), size):
            spritesheet_name = filename.format(number=i // size)
            SpriteSheet.create_sprite_sheet(spritesheet_name, images[i:i + size], width, height)


    @staticmethod
    def create_sprite_sheet(filename, images, width, height):
        images = [Image.open(image) for image in images]

        image_width, image_height = images[0].size
        sheet = SpriteSheet(filename, image_width, image_height, width, height)
        for y in range(height):
            for x in range(width):
                index = y * width + x
                if index < len(images):
                    sheet.paste(images[index], x, y)
        sheet.save()

    def __init__(self, filename, per_image_width, per_image_height, images_wide, images_high):
        self.filename = filename
        self.images_high = images_high
        self.images_wide = images_wide
        self.per_image_height = per_image_height
        self.per_image_width = per_image_width

        self.master = Image.new(
            mode='RGB',
            size=(per_image_width * images_wide, per_image_height * images_high),
            color=(0, 0, 0))  # black

    def paste(self, image, x, y):
        print("Pasting at", x, y)
        self.master.paste(image, (x * self.per_image_width, y * self.per_image_height))

    def save(self):
        print("saving as", self.filename)
        self.master.save(os.path.join(SPRITE_SHEET_OUTPUT_DIR, self.filename + ".png"))