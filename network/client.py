import pickle
import socket
import threading

class myClient:    
    def __init__(self, 
                 host="localhost", 
                 port=7634, 
                 on_receive=lambda msg: print(f"Broadcast message received: {msg}")
                 ):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.on_receive = on_receive
        self.s.connect((self.host, self.port))

        t_receive = threading.Thread(target=self.broadcast_receiver)
        t_receive.start()

    def broadcast_receiver(self):
        while True:
            s_msg_bin = self.s.recv(1024)

            try:
                s_msg = s_msg_bin.decode()
            except UnicodeDecodeError:
                s_msg = pickle.loads(s_msg_bin)

            self.on_receive(s_msg)


    def send(self, data):
        try:
            to_send = data.encode()
        except AttributeError:
            to_send = pickle.dumps(data)
        self.s.send(to_send)

if __name__=="__main__":
    myClient()