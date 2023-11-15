from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmousemoved
import random

from breakoutgraphics import BreakoutGraphics

PADDLE_WIDTH = 75  # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels)
# Vertical offset of the paddle from the window bottom (in pixels)
PADDLE_OFFSET = 50

TELEPORT_PADDLE_WIDTH = 5


class TeleportPanel(BreakoutGraphics):
    # Add two teleport paddles beside the paddle,
    # which can teleport the ball to random position from left or right wall
    def __init__(
        self,
        paddle_width=PADDLE_WIDTH,
        paddle_height=PADDLE_HEIGHT,
        paddle_offset=PADDLE_OFFSET,
    ) -> None:
        BreakoutGraphics.__init__(
            self,
            paddle_width=PADDLE_WIDTH,
            paddle_height=PADDLE_HEIGHT,
            paddle_offset=PADDLE_OFFSET,
        )

        self.teleport_paddle_left = GRect(
            TELEPORT_PADDLE_WIDTH,
            paddle_height,
            x=(self.window_width - paddle_width) / 2 - TELEPORT_PADDLE_WIDTH,
            y=self.window_height - paddle_offset - paddle_height,
        )
        self.teleport_paddle_left.filled = True
        self.teleport_paddle_left.fill_color = "red"
        self.window.add(self.teleport_paddle_left)

        self.teleport_paddle_right = GRect(
            TELEPORT_PADDLE_WIDTH,
            paddle_height,
            x=(self.window_width - paddle_width) / 2 + paddle_width,
            y=self.window_height - paddle_offset - paddle_height,
        )
        self.teleport_paddle_right.filled = True
        self.teleport_paddle_right.fill_color = "red"
        self.window.add(self.teleport_paddle_right)

        def paddle_move(mouse):
            if (mouse.x - paddle_width / 2) < 0:
                self.paddle.x = TELEPORT_PADDLE_WIDTH
                self.teleport_paddle_left.x = 0
                self.teleport_paddle_right.x = paddle_width + TELEPORT_PADDLE_WIDTH
            elif (mouse.x + paddle_width / 2) > self.window_width:
                self.paddle.x = self.window_width - paddle_width - TELEPORT_PADDLE_WIDTH
                self.teleport_paddle_left.x = (
                    self.window_width - paddle_width - 2 * TELEPORT_PADDLE_WIDTH
                )
                self.teleport_paddle_right.x = self.window_width - TELEPORT_PADDLE_WIDTH
            else:
                self.paddle.x = mouse.x - paddle_width / 2
                self.teleport_paddle_left.x = (
                    mouse.x - paddle_width / 2 - TELEPORT_PADDLE_WIDTH
                )
                self.teleport_paddle_right.x = mouse.x + paddle_width / 2

        onmousemoved(paddle_move)

    def ball_speed_up(self):
        self.set_dx(self.get_dx() * 1.11)
        self.set_dy(self.get_dy() * 1.11)

    def touch_teleport_paddle(self):
        return (
            self.ball_touch_something() == self.teleport_paddle_left
            or self.ball_touch_something() == self.teleport_paddle_right
        )

    def teleport(self):
        self.ball.x = random.choice([0, self.window_width - self.ball.width])
        self.ball.y = random.randint(
            0, self.window_height - PADDLE_OFFSET - self.ball.height
        )
        # The price of using teleport is the ball speed up
        self.ball_speed_up()
