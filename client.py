import socket
from threading import Thread

class Client:
    def __init__(self, sequencer_address):
        self.seq_ip, self.seq_port = sequencer_address
        
    def connect_to_sequencer(self, name):
        self.con_to_seq = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.con_to_seq.connect((self.seq_ip, self.seq_port))
                break
            except socket.error:
                self.seq_port += 1
                print self.seq_port
        self.send_msg("msg#" + name + " has joined the game")

    def send_msg(self, msg):
        self.con_to_seq.send(msg)

    def recv_msg(self):
        result = self.con_to_seq.recv(256)
        return result