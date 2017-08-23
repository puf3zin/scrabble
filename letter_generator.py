import time
import random
import string

class Letterman:
    def __init__(self, period):
        self.period = period

    def generate_letter(self):
        return random.choice(string.ascii_uppercase)

    def work(self):
        while True:
            time.sleep(self.period)
            letter = self.generate_letter()
            send_to_sequencer(letter)

if __name__ == "__main__":
    ltr = Letterman(1)
    ltr.work()