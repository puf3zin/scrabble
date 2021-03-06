import socket
from threading import Thread, Lock


send_lock = Lock()
increase_lock = Lock()
class Receiver:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cons = []

    def close_connection(self):
        self.sock.close()
    
    def handle(self, con):
        while True:
            try:
                msg = con.recv(256)
            except socket.error as e:
                print e
                break   
            try:
                _, primitive = msg.split("#", 1)
            except ValueError:
                break
            if primitive != "add":
                print msg
            self.send_everyone(msg)
             
    def send_everyone(self, msg):
        send_lock.acquire()
        for con in self.cons:
            try:
                con.send(msg)
            except socket.error as e:
                print e
                self.cons.remove(con)

        
        send_lock.release()
            
    def serve(self):
        while True:
            origin = (self.ip, self.port)
            try:
                self.sock.bind(origin)
                break
            except socket.error:
                self.port += 1
                print self.port
        self.sock.listen(50)
        while True:
            try:
                print "server online"
                con, client = self.sock.accept()
            except KeyboardInterrupt:
                print "server sera desligado assim que " \
                      "a ultima conexao for encerrada"
                break
            print "received connection:", client
            self.cons.append(con)
            h = Thread(target=self.handle, args=(con, ))
            h.daemon = True
            h.start()


if __name__ == "__main__":
    receiver = Receiver('localhost', 3333)
    receiver.serve()