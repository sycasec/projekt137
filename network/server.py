import socket
import threading
import pickle


class myServer:

    def __init__(self, host="0.0.0.0", port=7634):
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # Prevent OSError: [Errno 98] Address already in use
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.clientList = []
        self.host=host
        self.port=port

        #Functions to start the server and define listener
        self.server.bind((self.host,self.port))
        self.server.listen(1)

        #Functions to run the server
        self.serverLoop = threading.Thread(target=self.mainLoop)
        self.serverLoop.start()

    def __del__(self):
        self.server.close()

    def mainLoop(self):
        try:
            while True:
                print("Waiting for client")
                conn, addr = self.server.accept()
                self.on_client_connect(conn, addr)
        except KeyboardInterrupt:
            print("Stopped by Ctrl+C")
        finally:
            if self.server:
                self.server.close()

    def clientHandler(self, conn, adr):
        while True:
            c_msg_bin = conn.recv(1024)
            try:
                # Decode string
                c_msg = c_msg_bin.decode()
            except UnicodeDecodeError:
                # Decode data object
                c_msg = pickle.loads(c_msg_bin)

            print(f"message from {adr}: {c_msg}")
            self.broadcast(c_msg_bin)

    def on_client_connect(self, conn, addr):
        conn.send(f"Welcome, {addr}!".encode())

        print("connected with",addr)

        t = threading.Thread(target=self.clientHandler, args=(conn,addr))
        t.start()

        self.clientList.append(conn)

    def broadcast(self,message):
        for conn in self.clientList:
            conn.send(message)

if __name__ == "__main__":
    myServer()