import socket

def show_board(board, size):
        print "-" * size * 6 + "-"
        for line in board:
            for square in line:
                print '| ', '{: ^2}'.format(square),
            print "|"
            print "-" * size * 6 + "-"

def send_to_sequencer(msg):
    