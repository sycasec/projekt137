import pickle
import socket
import threading
import pygame

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
        self.run = True
        self.s.connect((self.host, self.port))

        self.t_receive = threading.Thread(target=self.broadcast_receiver)
        self.t_receive.daemon = True
        self.t_receive.start()

    def broadcast_receiver(self):
        while self.run:
            try:
                s_msg_bin = self.s.recv(1024)

                try:
                    s_msg = s_msg_bin.decode()
                except UnicodeDecodeError:
                    s_msg = pickle.loads(s_msg_bin)

                self.on_receive(s_msg)
            except:
                pass

    def send(self, data):
        try:
            to_send = data.encode()
        except AttributeError:
            to_send = pickle.dumps(data)
        self.s.send(to_send)

    def kill(self):
        self.run = False
        self.t_receive.join(timeout=5)

class GameClient(myClient):
    def __init__(self,
                 receive_keypress,
                 receive_keyboard_state,
                 receive_game_state,
                 event_listener,
                 host="localhost",
                 port=7634,
                 on_receive=None
                 ):
        self.receive_keypress = receive_keypress
        self.receive_keyboard_state = receive_keyboard_state
        self.receive_game_state = receive_game_state
        self.event_listener = event_listener

        if on_receive is None:
            on_receive = self.receive_broadcast

        super().__init__(host, port, on_receive)


    def receive_broadcast(self, msg):
        if isinstance(msg, bytes):
            msg = msg.decode()
        print(f"Broadcast received: {msg}")
        if self.__msg_is_keypress(msg):
            self.receive_keypress(msg)

        elif self.__msg_is_keyboard_state(msg):
            self.receive_keyboard_state(msg)

        elif self.__msg_is_game_state(msg):
            self.receive_game_state(msg)
        else:
            self.event_listener(msg)

    @staticmethod
    def __msg_is_keypress(msg):
        return isinstance(msg, int) and  pygame.K_a <= msg <= pygame.K_z

    @staticmethod
    def __msg_is_keyboard_state(msg):
        try:
            return len(msg) == 26
        except Exception:
            return False

    @staticmethod
    def __msg_is_game_state(msg, delimiter="$"):
        try:
            keys, green_score, red_score = msg.split(delimiter)
            return GameClient.__msg_is_keyboard_state(keys) and  green_score.isdigit() and red_score.isdigit()
        except ValueError:
            return False


if __name__=="__main__":
    myClient()
