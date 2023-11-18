import pickle
import socket
import threading

class myClient:    
    def __init__(self, host="localhost", port=7634):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.s.connect((self.host, self.port))

        t_receive = threading.Thread(target=self.broadcast_receiver)
        t_receive.start()

        t_send = threading.Thread(target=self.sender)
        t_send.start()

    def broadcast_receiver(self, expect_string=False):
        while True:
            s_msg = self.s.recv(1024)

            if expect_string:
                print("Broadcast message received: ", s_msg.decode())       
                continue

            print("Broadcast message received: ", pickle.loads(s_msg))       


    def sender(self, data=None, expect_string=False):
        if data is None:
            data = {"I am": "a dummy placeholder"}

        if expect_string:
            while True:
                self.s.send(input("Input message to send: ").encode())        
        else: 
            while True:
                input("Press enter to send data")
                self.s.send(pickle.dumps(data))

if __name__=="__main__":
    myClient()