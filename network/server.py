import socket
import threading
import pickle
import time


class myServer:
    def __init__(self, on_drop_connection=None, host="0.0.0.0", port=7634):
        self.on_drop_connection = on_drop_connection
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Prevent OSError: [Errno 98] Address already in use
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.clientList = []
        self.host = host
        self.port = port
        self.serverRun = True

        # Functions to start the server and define listener
        self.server.bind((self.host, self.port))
        self.server.listen(1)

        self.connected_players = 0
        self.status = "WAIT"

        # Functions to run the server
        self.serverLoop = threading.Thread(target=self.mainLoop)
        self.serverLoop.daemon = True
        self.serverLoop.start()

        # Get host IP address
        self.hostAddress = [
            l
            for l in (
                [
                    ip
                    for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                    if not ip.startswith("127.")
                ][:1],
                [
                    [
                        (s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                        for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
                    ][0][1]
                ],
            )
            if l
        ][0][0]

    def __del__(self):
        self.server.close()

    def kill(self):
        self.serverRun = False

        try:
            self.server.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.server.close()

        self.clientList = []
        self.connected_players = 0

    def mainLoop(self):
        try:
            while self.serverRun:
                if self.connected_players == 2 and self.status == "WAIT":
                    self.status = "START"
                    time.sleep(1)
                    self.broadcast("GAME START".encode())
                elif self.status == "WAIT":
                    print("Waiting for client")
                    try:
                        conn, addr = self.server.accept()
                    except:
                        pass

                    self.on_client_connect(conn, addr)
                time.sleep(1)

        except KeyboardInterrupt:
            print("Stopped by Ctrl+C")
        except:
            self.kill()
        finally:
            if self.server:
                self.server.close()

    def clientHandler(self, conn, adr):
        while self.serverRun:
            try:
                c_msg_bin = conn.recv(1024)
                if not c_msg_bin:
                    print("Client disconnected. Destroying server")
                    self.on_drop_connection()
                    break  # Break out of the loop when the client disconnects

                try:
                    # Decode string
                    c_msg = c_msg_bin.decode()
                except UnicodeDecodeError:
                    # Decode data object
                    c_msg = pickle.loads(c_msg_bin)

                print(f"message from {adr}: {c_msg}")
                self.broadcast(c_msg_bin)
            except Exception as e:
                raise e
                break  # Break out of the loop when an exception occurs (e.g., client disconnects)

    def on_client_connect(self, conn, addr):
        try:
            conn.send(f"Welcome, {addr}!".encode())

            print("connected with", addr)

            self.connected_players += 1

            t = threading.Thread(target=self.clientHandler, args=(conn, addr))
            t.start()

            self.clientList.append(conn)
        except:
            self.kill()

    def broadcast(self, message):
        for conn in self.clientList:
            conn.send(message)


if __name__ == "__main__":
    myServer()
