import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from constants import SPRITE_SHEET_OUTPUT_DIR
from deck import Deck


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    os.chdir(SPRITE_SHEET_OUTPUT_DIR)
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    Deck.reload_outdated_decks()
    print("Finished reloading")
    run()
