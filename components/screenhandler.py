from screens.home import HomeScreen
from screens.about import AboutScreen
from screens.loading import Waiting
from screens.assignment import ColorAssignment
from screens.countdown import Countdown
from screens.gameover import GameOver


class ScreenHandler():
    def __init__(self,screen,WINDOW_WIDTH, WINDOW_HEIGHT, keys_font) -> None:

        self.screen = screen

        #Screens
        self.home_screen = HomeScreen(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.about_screen = AboutScreen(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.assignment_screen = ColorAssignment(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.waiting_screen = Waiting(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.countdown_screen = Countdown(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)
        self.gameover_screen = GameOver(WINDOW_WIDTH, WINDOW_HEIGHT, keys_font)

    #Method to switch to a screen
    def switch_screen(self, active_screen, event):

        if active_screen == "home":
            return self.home(event)

        if active_screen == "host":
            return self.host()

        if active_screen == "join":
            return self.join()

        if active_screen == "about":
            return self.about(event)

        if active_screen == "waiting":
            return self.waiting()


        if active_screen == "countdown":
            return self.countdown()

    def home(self, event):
        self.home_screen.render(self.screen)

        result = self.home_screen.handle_event(event)

        if result == 0:
            return "host"

        if result == 1:
            return "join"

        if result == 2:
            return "about"

        if result == 3:
            return "quit"

        return "home"

    def about(self, event):
        self.about_screen.render(self.screen)

        result = self.about_screen.handle_event(event)

        if result == "back":
            return "home"

        return "about"

    def host(self):
        return "waiting"

    def join(self):
        return "waiting"

    def waiting(self):
        self.waiting_screen.update()
        self.waiting_screen.render(self.screen)

        return "waiting"

    def begin_countdown(self):
        self.countdown_screen.start_countdown()

    def countdown(self):
        self.countdown_screen.render(self.screen)
        if self.countdown_screen.is_complete():
            return "play"

        return "countdown"

