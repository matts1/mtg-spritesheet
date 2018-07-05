import os
import urllib.request

import requests

from constants import IMAGE_CACHE_DIR


class Card(object):
    def __init__(self, name):
        self.name = name
        self.cache = []

    def __str__(self):
        return self.name

    def is_cached(self):
        return os.path.exists(self.make_image_path()) or os.path.exists(self.make_image_path(0))

    @property
    def local_files(self):
        if not self.cache:
            if os.path.exists(self.make_image_path()):
                self.cache.append(self.make_image_path())
            for f in range(100):
                if os.path.exists(self.make_image_path(f)):
                    self.cache.append(self.make_image_path(f))
                else:
                    break
        if not self.cache:
            self.download()
            return self.local_files
        return self.cache

    def make_image_path(self, number=None):
        name = self.name.replace("/", "_")
        if number is None:
            return os.path.join(IMAGE_CACHE_DIR, name + ".jpg")
        else:
            return os.path.join(IMAGE_CACHE_DIR, name + "_{}.jpg".format(number))

    def download(self):
        if not self.is_cached():
            print("Downloading", self.name)
            response = requests.get('https://api.scryfall.com/cards/named?exact=%s' % self.name.replace(' ', '+'))
            response.raise_for_status()
            json = response.json()
            if 'image_uris' in json:
                image_uri = json['image_uris']['normal']
                urllib.request.urlretrieve(image_uri, self.make_image_path())
            else:
                image_uris = [face['image_uris']['normal'] for face in json['card_faces']]
                for i, uri in enumerate(image_uris):
                    urllib.request.urlretrieve(uri, self.make_image_path(i))


    @property
    def secondary_images(self):
        return self.local_files[1:]

    @property
    def image(self):
        return self.local_files[0]
