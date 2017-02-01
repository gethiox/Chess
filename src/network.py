import socket


class Network:
    def __init__(self, game):
        self.cnx = socket.socket()
        self.game = game
        self.socket = None

    @staticmethod
    def handle_client(client_socket):
        request = client_socket.recv(1024)

        print(request.decode())

        client_socket.close()

    def host(self, host='127.0.0.1', port=5678):
        self.cnx.bind((host, port))
        self.cnx.listen(1)
        while True:
            connection, addr = self.cnx.accept()
            print('nawiązano połączenie z %s!' % addr[0])
            while True:
                data = connection.recv(4096)
                if not data:
                    print('nodata')
                    break
                if 'kurwa' in data.decode():
                    connection.send('404 ERROR: TY WULGARNY KUTASIE!'.encode())
                else:
                    connection.send('200 OK: dane ok ziomek.'.encode())
                    print(data.decode())
                if data.decode() == 'exit':
                    break
            connection.close()
            print('zakończono połączenie z %s!' % addr[0])
        self.cnx.close()

    def join(self, host='127.0.0.1', port=5678):
        self.cnx.connect((host, port))
        while True:
            data = input()
            self.cnx.send(data.encode())
            response = self.cnx.recv(4096)
            print(response.decode())
            if data == 'exit':
                break
        self.cnx.close()

    def move(self, move):
        if self.socket is not None:
            self.game.move(move)
            self.cnx.send(move.encode())

        else:
            raise Exception('No active connection')