import random
import string
import time

from client import Client

SEQUENCER_ADDR = ('localhost', 3333)

class Generator:
    def __init__(self, name):
        self.name = name
        self.clnt = Client(SEQUENCER_ADDR)

    def enter_game(self):
        self.clnt.connect_to_sequencer(self.name)

    def generate_letter(self):
        letter = random.choice(string.ascii_uppercase)
        final_msg = "add#" + letter
        print final_msg
        self.clnt.send_msg(final_msg)


if __name__ == "__main__":
    letterman = Generator("generator 1")
    letterman.enter_game()
    while True:
        time.sleep(2)
        letterman.generate_letter()