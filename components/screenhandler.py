from screens.home import HomeScreen
from screens.about import AboutScreen
from screens.loading import Waiting
from screens.assignment import ColorAssignment
from screens.countdown import Countdown
from screens.gameover import GameOver
from screens.splash import SplashScreen


class ScreenHandler():
    def __init__(self,screen,WINDOW_WIDTH, WINDOW_HEIGHT, keys_font) -> None:

        self.screen = screen

        #Screens
        self.splash_screen = SplashScreen(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.home_screen = HomeScreen(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.about_screen = AboutScreen(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.assignment_screen = ColorAssignment(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.waiting_screen = Waiting(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.countdown_screen = Countdown(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.gameover_screen = GameOver(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
    
    #Method to switch to a screen
    def switch_screen(self, active_screen, **kwargs):

        if active_screen == "splash":
            return self.splash()
        
        if active_screen == "home":
            return self.home()

        if active_screen == "host":
            return self.host()

        if active_screen == "join":
            return self.join()

        if active_screen == "about":
            return self.about(kwargs["event"])

        if active_screen == "waiting":
            return self.waiting(kwargs["client_type"], kwargs["ip_address"])

        if active_screen == "countdown":
            return self.countdown(kwargs["color"])

        if active_screen == "gameover":
            return self.gameover(kwargs["event"],kwargs["winner"])

    def update_home(self, event):

        result = self.home_screen.handle_event(event)

        if result == 0:
            return "host"

        if result == 1:
            return "join"

        if result == 2:
            return "about"

        if result == 3:
            return "quit"

        return self.home()
    
    def update_waiting(self, event, client_type):
        return self.waiting_screen.handle_event(event, client_type)
        
    def get_host(self):
        return self.waiting_screen.get_final_ip()

    def splash(self):
        if self.splash_screen.render(self.screen):
            return "home"
        
    def home(self):
        self.home_screen.render(self.screen)
        return "home"

    def about(self, event):
        self.about_screen.render(self.screen)

        result = self.about_screen.handle_event(event)

        if result == "back":
            return "home"

        return "about"

    def host(self):
        return "host"

    def join(self):
        return "join"

    def waiting(self, client_type, ip_address):

        self.waiting_screen.ip_address_display(client_type, ip_address)
        self.waiting_screen.update()
        self.waiting_screen.render(self.screen, client_type, ip_address)
            
        return "waiting"

    def begin_countdown(self):
        self.countdown_screen.start_countdown()

    def countdown(self,color):
        self.countdown_screen.render(self.screen,color)
        if self.countdown_screen.is_complete():
            return "play"

        return "countdown"

    def gameover(self, event, winner):
        self.gameover_screen.render(self.screen,winner)
        result = self.gameover_screen.handle_event(event)
        if result == "rematch":
            return "rematch"
        elif result == "home":
            return "home"
        return "gameover"
    
    def clear_loading_inputbox(self):
        self.waiting_screen.clear_inputbox()