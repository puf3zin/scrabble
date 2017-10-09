import sys
from client import Client
from threading import Thread, Lock
import os
import time
import urllib, json
from nltk.corpus import wordnet

SEQUENCER_ADDR = ('localhost', 3333)
identifier_lock = Lock()

class Judge:
    def __init__(self, name):
        self.name = name
        self.clnt = Client(SEQUENCER_ADDR)
        self.letters_known = []
        self.msg_id = 1
        self.id_list = []

    def get_letters(self):
        return self.letters_known

    def enter_game(self):
        self.clnt.connect_to_sequencer(self.name)

    def remove_letters(self, letters, identifier):
        name, num = identifier.split("++")
        final_msg = "rmv#" + letters
        print final_msg
        identifier_lock.acquire()
        self.clnt.send_msg(final_msg, num, "r." + name)
        self.msg_id += 1
        identifier_lock.release()
    
    def scored(self, player, identifier, word):
        name, num = identifier.split("++")
        points = len(word)
        final_msg = "scr#" + player + "#" + str(points) 
        print final_msg
        identifier_lock.acquire()
        self.clnt.send_msg(final_msg, num, "%s." + name)
        self.msg_id += 1
        identifier_lock.release()

    def search_word(self, word):
        if not wordnet.synsets(word.lower()):
            return False
        else:
            return True

    def update_state(self):
        while True:
            letters_are_ok = True
            msg = self.clnt.recv_msg()
            print "<<", msg
            identifier, primitive, content = msg.split("#", 2)
            player, _ = identifier.split("++")
            if identifier not in self.id_list:
                self.id_list.append(identifier)
                if primitive == "add":
                    self.letters_known.append(content[0])

                elif primitive == "rmv":
                    print msg
                    for letter in content:
                        print letter.upper()
                        try:
                            self.letters_known.remove(letter.upper())
                        except ValueError:
                            print "letter not in", self.letters_known

                elif primitive == "msg":
                    to, text = content.split("#")
                    if to == self.name:
                        print text

                elif primitive == "try":
                    print content
                    letters = len(content)
                    for letter in self.letters_known:
                        for ch in content:
                            print letter, ch.upper()
                            if letter == ch.upper():
                                letters -= 1
                                break
                    if letters >= 0:
                        continue
                    print "as letras sao validas", letters
                    word_exists = self.search_word(content)
                    print "a palavra existe?:", word_exists
                    if word_exists:
                        self.remove_letters(content, identifier)
                        print "removed"          
                        self.scored(player, identifier, content)
                        print "scored"


if __name__ == "__main__":
    judge = Judge(sys.argv[1])
    judge.enter_game()
    t = Thread(target=judge.update_state, args=())
    t.daemon = True
    t.start()
    timeout = 1
    while True:
        print judge.get_letters()
        #print judge.id_list
        time.sleep(timeout)
        #os.system("clear")