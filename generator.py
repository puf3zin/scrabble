import random
import string
import time

from client import Client

VOWELS = "AEIOU"
CONSONANTS = "".join(set(string.uppercase) - set(VOWELS))

SEQUENCER_ADDR = ('localhost', 3333)

class Generator:
    def __init__(self, name):
        self.name = name
        self.clnt = Client(SEQUENCER_ADDR)
        self.msg_id = 1

    def enter_game(self):
        self.clnt.connect_to_sequencer(self.name)

    def generate_letter(self):
        choice = random.choice(["vowels", "consonants", "consonants"])
        if choice == "vowels":
            letter = random.choice(VOWELS)
        elif choice == "consonants":
            letter = random.choice(CONSONANTS)
        final_msg = "add#" + letter
        print final_msg
        self.clnt.send_msg(final_msg, self.msg_id, self.name)
        self.msg_id += 1


if __name__ == "__main__":
    letterman = Generator("generator 1")
    letterman.enter_game()
    while True:
        time.sleep(2)
        letterman.generate_letter()