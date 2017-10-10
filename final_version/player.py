import sys
import os
import string
from random import random as r
from threading import Thread, Lock
from client import Client
import Queue

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock

from functools import partial

SEQUENCER_ADDR = ('localhost', 3333)

change = Queue.Queue()

labels = {}

identifier_lock = Lock()



class Player:
    def __init__(self, name):
        self.name = name
        self.clnt = Client(SEQUENCER_ADDR)
        self.letters_known = {key: 0 for key in string.uppercase}
        self.placar = {}
        self.msg_id = 1
        self.id_list = []
        self.score = None

    def enter_game(self):
        self.clnt.connect_to_sequencer(self.name)

    def get_letters(self):
        return self.letters_known

    def score_as_text(self):
        return '\n'.join(['%s has %s points' % (key, value) for (key, value) in self.placar.items()])

    def try_word(self, tmp):
        word = tmp.text
        tmp.text = "" 
        final_msg = "try#" + word
        print ">>", final_msg
        self.clnt.send_msg(final_msg, self.msg_id, self.name)
        self.msg_id += 1
    def new_letter(self, letter):
        change.put(("add", letter))
        self.letters_known[letter] += 1

    def update_state(self):
        while True:
            msg = self.clnt.recv_msg()
            print msg
            print msg.split("%")
            for m in msg.split("%"):
                try:
                    identifier, primitive, content = m.split("#", 2)
                except ValueError:
                    continue
                print identifier, self.id_list
                if identifier not in self.id_list:
                    print self.letters_known
                    print "<<", m
                    self.id_list.append(identifier)
                    if primitive == "add":
                        self.new_letter(content[0])
                    elif primitive == "msg":
                        to, text = content.split("#")
                        if to == self.name:
                            print text
                    elif primitive == "rmv":
                        for letter in content:
                            change.put(("remove", letter))
                            if self.letters_known[letter.upper()] > 0:
                                self.letters_known[letter.upper()] -= 1
                            else:
                                print "letter not in", self.letters_known
                    elif primitive == "scr":
                        who, points = content.split("#")
                        try:
                            self.placar[who] += int(points)
                        except KeyError:
                            self.placar[who] = int(points)
                        change.put(("score", self.score_as_text()))


class ScrabbleApp(App):

    def add_letter(self, letter):
        with self.wid.canvas:
            print self.wid.height, self.wid.width
            tmp = Label(text=letter, font_size='40sp',
                        pos=(r() * (self.wid.width-100) + self.wid.x,
                             r() * (self.wid.height-100) + self.wid.y))
            try:
                self.labels[letter].append(tmp)
            except KeyError:
                self.labels[letter] = [tmp]
            self.wid.add_widget(tmp)

    def remove_letter(self, letter):
        with self.wid.canvas:
            to_remove = self.labels[letter.upper()].pop()
            to_remove.color = (0, 0, 0, 1)
    
    def update_score(self, content):
        self.score.text = content
        
    def build(self):
        self.wid = Widget()
        self.labels = {}
        word_receiver = TextInput(text="try word", multiline=False)
        word_receiver.bind(on_text_validate=partial(player.try_word))

        self.score = Label(text=player.score_as_text())

        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(self.score)
        layout.add_widget(word_receiver)

        root = BoxLayout(orientation='vertical')
        root.add_widget(self.wid)
        root.add_widget(layout)

        return root
        

try:
    player = Player(sys.argv[1])
except:
    print "try: python player.py PLAYER_NAME"
    exit()
app = ScrabbleApp()

def update_gui(dt):
    try:
        primitive, content = change.get_nowait()
        print primitive, content
        if primitive == "add":
            app.add_letter(content)
        elif primitive == "score":
            app.update_score(content)
        else:
            app.remove_letter(content)

    except Queue.Empty:
        pass

    Clock.schedule_once(update_gui, 0.5)


if __name__ == "__main__":
    threads = []
    player.enter_game()
    threads.append(Thread(target=player.update_state, args=()))
    threads.append(Thread(target=update_gui, args=()))
    for t in threads:
        t.daemon = True
        t.start()
    print "started"
    Clock.schedule_once(update_gui, 1)
    app.run()