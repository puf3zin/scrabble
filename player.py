import sys
import os
from threading import Thread
from select import select
from client import Client

SEQUENCER_ADDR = ('localhost', 3333)

class Player:
    def __init__(self, name):
        self.name = name
        self.clnt = Client(SEQUENCER_ADDR)
        self.letters_known = []

    def enter_game(self):
        self.clnt.connect_to_sequencer(self.name)

    def get_letters(self):
        return self.letters_known

    def try_word(self, word):
        final_msg = "try#" + word
        print final_msg
        self.clnt.send_msg(final_msg)

    def update_state(self):
        while True:
            msg = self.clnt.recv_msg()
            #print msg
            primitive, content = msg.split("#", 1)
            if primitive == "add":
                self.letters_known.append(content[0])
            elif primitive == "msg":
                to, text = content.split("#")
                if to == self.name:
                    print text
            elif primitive == "rmv":
                for letter in content[:-1]:
                    self.letters_known.remove(letter)

if __name__ == "__main__":
    player = Player("player 1")
    player.enter_game()
    t = Thread(target=player.update_state, args=())
    t.daemon = True
    t.start()
    timeout = 1
    while True:
        print player.get_letters()
        print "Enter something:",
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            new_word = sys.stdin.readline()
            player.try_word(new_word)
        else:
            #pass
            os.system('clear')