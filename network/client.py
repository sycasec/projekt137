import pickle
import socket
import threading

class myClient:    
    def __init__(self, host="0.0.0.0", port=7634):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.s.connect((self.host, self.port))

        t_receive = threading.Thread(target=self.broadcast_receiver)
        t_receive.start()

        t_send = threading.Thread(target=self.sender)
        t_send.start()

    def broadcast_receiver(self):
        while True:
            s_msg_bin = self.s.recv(1024)

            try:
                s_msg = s_msg_bin.decode()
            except UnicodeDecodeError:
                s_msg = pickle.loads(s_msg_bin)

            print("Broadcast message received: ", s_msg)       


    def sender(self, data=None, data_is_string=False):
        if data is None:
            data = {"I am": "a dummy placeholder"}

        while True:
            if data_is_string:
                data = input("Input message to send: ")
                to_send = data.encode()
            else:
                input("Press enter to send data")
                to_send = pickle.dumps(data)
            self.s.send(to_send)

if __name__=="__main__":
    myClient()