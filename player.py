import sys
import os
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
        self.letters_known = []
        self.placar = {}
        self.msg_id = 1
        self.id_list = []

    def enter_game(self):
        self.clnt.connect_to_sequencer(self.name)

    def get_letters(self):
        return self.letters_known

    def try_word(self, tmp):
        word = tmp.text
        tmp.text = "" 
        final_msg = "try#" + word
        print ">>", final_msg
        self.clnt.send_msg(final_msg, self.msg_id, self.name)
        self.msg_id += 1
    def new_letter(self, letter):
        change.put(("add", letter))
        self.letters_known.append(letter)

    def update_state(self):
        while True:
            msg = self.clnt.recv_msg()
            print msg
            for m in msg.split("%"):
                try:
                    identifier, primitive, content = msg.split("#", 2)
                except ValueError:
                    break

                if identifier not in self.id_list:
                    print self.letters_known
                    print "<<", msg
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
                            self.letters_known.remove(letter.upper())
                    elif primitive == "scr":
                        who, points = content.split("#")
                        try:
                            self.placar[who] += int(points)
                        except KeyError:
                            self.placar[who] = int(points)


class ScrabbleApp(App):

    def add_letter(self, letter):
        with self.wid.canvas:
            tmp = Label(text=letter, font_size='40sp',
                        pos=(r() * self.wid.width + self.wid.x,
                             r() * self.wid.height + self.wid.y))
            try:
                self.labels[letter].append(tmp)
            except KeyError:
                self.labels[letter] = [tmp]
            self.wid.add_widget(tmp)

    def remove_letter(self, letter):
        with self.wid.canvas:
            to_remove = self.labels[letter.upper()].pop()
            to_remove.color = (0, 0, 0, 1)
        
    def build(self):
        self.wid = Widget()
        self.labels = {}
        word_receiver = TextInput(text="try word", multiline=False)
        word_receiver.bind(on_text_validate=partial(player.try_word))

        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(word_receiver)

        root = BoxLayout(orientation='vertical')
        root.add_widget(self.wid)
        root.add_widget(layout)

        return root
        

player = Player(sys.argv[1])

app = ScrabbleApp()

def update_gui(dt):
    try:
        primitive, content = change.get_nowait()
        if primitive == "add":
            app.add_letter(content)
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