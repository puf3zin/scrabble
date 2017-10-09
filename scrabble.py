from utils import show_board

class Scrabble:
    def __init__(self, board_size, port):
        self.ip = ''
        self.port = port
        self.players = []
        self.board_size = board_size
        self.board = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def get_board(self):
        return self.board

    def insert_letter(self, letter):
        self.board.append(letter)

    def remove_letters(self, word):
        for c in word:
            for letter in self.board:
                if letter is c:
                    self.board.remove(letter)
                    break

    def handle(self, con):
        cmd = ""
        tmp = []
        while True:
            msg = con.recv(256)
            if msg == "quit":
                break
            try:
                cmd, pos, size, buff = msg.split('#', 3)
                print "done"
            except ValueError:
                print "connection cloooOOOsed"
                break
            pos = int(pos)
            size = int(size)
            print msg
            if cmd == "read":
                self.sem.acquire()
                value = self.partition.read(pos, size)
                self.sem.release()
                con.send(value)

            elif cmd == "write":
                self.sem.acquire()
                value = self.partition.write(pos, buff)
                self.sem.release()
                con.send(value)

    def serve(self):
        origin = (self.ip, self.port)
        self.sock.bind(origin)
        self.sock.listen(50)
        while True:
            try:
                print "server online"
                con, client = self.sock.accept()
            except KeyboardInterrupt:
                print "server será desligado assim que " \
                      "a última conexão for encerrada"
                break

            print "received connection:", client
            h = Thread(target=self.handle, args=(con, ))
            h.start()

def main():
    a = Scrabble(8)
    show_board(a.get_board())

if __name__ == "__main__":
    main()