from client import Client
from threading import Thread
import os
import time
import urllib, json

SEQUENCER_ADDR = ('localhost', 3333)

class Judge:
    def __init__(self, name):
        self.name = name
        self.clnt = Client(SEQUENCER_ADDR)
        self.letters_known = []

    def get_letters(self):
        return self.letters_known

    def enter_game(self):
        self.clnt.connect_to_sequencer(self.name)

    def remove_letters(self, letters):
        final_msg = "rmv#" + letters
        print final_msg
        self.clnt.send_msg(final_msg)

    def search_word(word):
        url = "http://dicionario-aberto.net/search-json/" + word
        response = urllib.urlopen(url)
        try:
            data = json.loads(response.read())
            return True
        except ValueError:
            return False
    def update_state(self):
        while True:
            letters_are_ok = True
            msg = self.clnt.recv_msg()
            #print msg
            primitive, content = msg.split("#", 1)
            if primitive == "add":
                self.letters_known.append(content[0])
            elif primitive == "rmv":
                for letter in content[:-1]:
                    print letter
                    self.letters_known.remove(letter)
            elif primitive == "msg":
                to, text = content.split("#")
                if to == self.name:
                    print text
            elif primitive == "try":
                for letter in content[:-1]:
                    if letter not in self.letters_known:  
                        letters_are_ok = False
                        break
                word_exists = self.search_word(content[:-1])
                if letters_are_ok and word_exists:
                    self.remove_letters(content)          


if __name__ == "__main__":
    judge = Judge("judge 1")
    judge.enter_game()
    t = Thread(target=judge.update_state, args=())
    t.daemon = True
    t.start()
    timeout = 1
    while True:
        print judge.get_letters()
        time.sleep(timeout)
        os.system("clear")