import os

from PIL import Image


class SpriteSheet(object):
    WIDTH = 10
    HEIGHT = 7

    @staticmethod
    def create_sprite_sheets(filename, prefix, images):
        size = SpriteSheet.WIDTH * SpriteSheet.HEIGHT
        filename = os.path.join(filename, "{prefix}{index}_{size}.png")

        for i in range(0, len(images), size):
            images_partial = images[i:i + size]
            spritesheet_name = filename.format(prefix=prefix, index=i // size, size=len(images_partial))
            SpriteSheet.create_sprite_sheet(spritesheet_name, images_partial)

    @staticmethod
    def create_sprite_sheet(filename, images):
        images = [Image.open(image) for image in images]

        image_width, image_height = images[0].size
        sheet = SpriteSheet(filename, image_width, image_height, SpriteSheet.WIDTH, SpriteSheet.HEIGHT)

        for y in range(SpriteSheet.HEIGHT):
            for x in range(SpriteSheet.WIDTH):
                index = y * SpriteSheet.WIDTH + x
                if index < len(images):
                    sheet.paste(images[index], x, y)
        sheet.save()

    def __init__(self, filename, per_image_width, per_image_height, images_wide, images_high):
        self.filename = filename
        self.images_high = images_high
        self.images_wide = images_wide
        self.per_image_height = per_image_height
        self.per_image_width = per_image_width

        print("Creating image", filename)
        self.master = Image.new(
            mode='RGB',
            size=(per_image_width * images_wide, per_image_height * images_high),
            color=(0, 0, 0))  # black

    def paste(self, image, x, y):
        self.master.paste(image, (x * self.per_image_width, y * self.per_image_height))

    def save(self):
        print("saving as", self.filename)
        self.master.save(self.filename)
