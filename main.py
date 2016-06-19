from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from time import strftime as stime

import time


from kivy.core.audio import SoundLoader

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition


# SCORE = NumericProperty(0)


class PongPaddle(Widget):
    score = NumericProperty(0)
    # time_bounce = time.time()
    # ballsound = SoundLoader.load('misc125.wav')
    

    # def bounce_ball(self, ball):
    #     if self.collide_widget(ball):
    #         print "Rounded Time:" , round(time.time() - self.time_bounce)

    #         if round(time.time() - self.time_bounce) > 0:
    #             vx, vy = ball.velocity
    #             offset = (ball.center_y - self.center_y) / (self.height / 2)
    #             bounced = Vector(-1 * vx, vy)
    #             vel = bounced * 1.1
    #             ball.velocity = vel.x, vel.y + offset
    #             self.ballsound.play()
    #         self.time_bounce = time.time()
            


    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            # self.ballsound.play()
        


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    # time_format = "%I:%M:%S"
    # def on_velocity(self, *args):
    #     print('Time={}\n args = {}'.
    #         format(stime(self.time_format), args))
    #     print(' vel mag: {}\n'.
    #         format(Vector(self.velocity).length()))


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    # started = False


    def __init__ (self, *args, **kwargs):
        super (PongGame, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        #went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y




class StartMenu(ScreenManager):
    # def on_enter(self):
    #     entrancesong = SoundLoader.load('Detective.wav')
    #     self.entrancesong.play()
    pass

class EndMenu(ScreenManager):
    pass



class PongApp(App):
    def build(self):
        self.load_kv('pong.kv')#calls my kivy file
        return StartMenu(transition=WipeTransition())


        # game = PongGame()
        # game.serve_ball()
        # Clock.schedule_interval(game.update, 1.0 / 60.0)
        # return game


if __name__ == '__main__':
    PongApp().run()
