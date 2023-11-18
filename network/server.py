import socket
import threading
import pickle


class myServer:

    def __init__(self) -> None:
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # Prevent OSError: [Errno 98] Address already in use
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.clientList = []
        self.host="0.0.0.0"
        self.port=7634

        #Functions to start the server and define listener
        self.server.bind((self.host,self.port))
        self.server.listen(1)

        #Functions to run the server
        try:
            while True:
                print("Waiting for client")
                conn, addr = self.server.accept()
                conn.send(f"Welcome, {addr}!".encode())

                print("connected with",addr)

                t = threading.Thread(target=self.clientHandler, args=(conn,addr))
                t.start()

                self.clientList.append(conn)
        except KeyboardInterrupt:
            print("Stopped by Ctrl+C")
        finally:
            if self.server:
                self.server.close()

    def __del__(self):
        self.server.close()

    def clientHandler(self, conn, adr, expect_string=False):
        while True:

            if expect_string:
                c_messg_bin = conn.recv(1024)
                # Convert binary data to string
                c_messg = c_messg_bin.decode()
                print(adr,": message from client: ",c_messg)
                self.broadcast(c_messg_bin)
                continue

            c_data_bin =conn.recv(1024)
            # Convert binary data to Python object
            c_data = pickle.loads(c_data_bin)
            self.broadcast(c_data)

    def broadcast(self,message):
        for conn in self.clientList:
            conn.send(message)

if __name__ == "__main__":
    myServer()