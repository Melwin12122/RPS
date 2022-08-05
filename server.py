import socket
from threading import Thread


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

players = []

def handle_client(conn, addr):
    # name = conn.recv(64).decode('utf-8')
    players.append(conn)
    connected = True
    print(addr, " joined.")
    name = conn.recv(32)
    try:
        while not len(players) == 2:
            pass
        else:
            for player in players:
                if player is not conn:
                    player.send(name)
            while connected:
                msg = conn.recv(1)
                for player in players:
                    if player is not conn:
                        player.send(msg)
    except:
        players.remove(conn)


        

def start():
    server.listen(2)
    while True:
        conn, addr = server.accept()
        thread = Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()

