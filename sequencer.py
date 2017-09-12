from receiver import Receiver
from sender import Sender
from threading import Lock

class Sequencer:
    def __init__(self, ip, port):
        self.identifier = 0
        self.rcvr = Receiver(ip, port)
        self.others = []
        
    def send_all():
        