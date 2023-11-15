"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

# Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_SPACING = 5
BRICK_WIDTH = 40  # Width of a brick (in pixels)
BRICK_HEIGHT = 15  # Height of a brick (in pixels)
BRICK_ROWS = 10  # Number of rows of bricks
BRICK_COLS = 10  # Number of columns of bricks
# Vertical offset of the topmost brick from the window top (in pixels)
BRICK_OFFSET = 50
BALL_RADIUS = 10  # Radius of the ball (in pixels)
PADDLE_WIDTH = 75  # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels)
# Vertical offset of the paddle from the window bottom (in pixels)
PADDLE_OFFSET = 50
INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball


class BreakoutGraphics:
    def get_dx(self):
        return self.__dx

    def set_dx(self, value: int):
        self.__dx = value

    def get_dy(self):
        return self.__dy

    def set_dy(self, value: int):
        self.__dy = value

    def dx_rebound(self):
        self.set_dx(-self.get_dx())

    def dy_rebound(self):
        self.set_dy(-self.get_dy())

    def get_bricks_amount(self):
        return self.__bricks_amount

    def set_bricks_amount(self, value: int):
        self.__bricks_amount = value

    def hit_a_brick(self):
        self.set_bricks_amount(self.get_bricks_amount() - 1)

    def ball_move(self):
        self.ball.move(self.__dx, self.__dy)

    def reset_ball(self):
        if self.ball is not None:
            self.window.remove(self.ball)
        self.set_dx(0)
        self.set_dy(0)
        self.ball = GOval(
            self.ball_radius,
            self.ball_radius,
            x=(self.window_width - self.ball_radius) / 2,
            y=(self.window_height - self.ball_radius) / 2,
        )
        self.ball.filled = True
        self.window.add(self.ball)

    def touch_left_wall(self):
        return self.ball.x <= 0

    def touch_right_wall(self):
        return self.ball.x > self.window.width - self.ball.width

    def touch_up_wall(self):
        return self.ball.y <= 0

    def touch_bottom_wall(self):
        return self.ball.y >= self.window.height - self.ball.height

    def ball_left_touch_something(self):
        return self.window.get_object_at(self.ball.x, self.ball.y + self.ball_radius)

    def ball_right_touch_something(self):
        return self.window.get_object_at(
            self.ball.x + self.ball.width, self.ball.y + self.ball_radius
        )

    def ball_top_touch_something(self):
        return self.window.get_object_at(self.ball.x + self.ball_radius, self.ball.y)

    def ball_bottom_touch_something(self):
        return self.window.get_object_at(
            self.ball.x + self.ball_radius, self.ball.y + self.ball.height
        )

    def ball_touch_something(self):
        if self.ball_left_touch_something():
            return self.ball_left_touch_something()
        elif self.ball_right_touch_something():
            return self.ball_right_touch_something()
        elif self.ball_top_touch_something():
            return self.ball_top_touch_something()
        elif self.ball_bottom_touch_something():
            return self.ball_bottom_touch_something()

    def touch_paddle(self):
        return self.ball_touch_something() == self.paddle

    def show_game_over(self):
        game_over_label = GLabel("GAME OVER!")
        game_over_label.font = "-50"
        game_over_label.color = "red"
        self.window.add(
            game_over_label,
            x=(self.window_width - game_over_label.width) / 2,
            y=(self.window_height - game_over_label.height) / 2,
        )

    def show_you_win(self):
        you_win_label = GLabel("YOU WIN!")
        you_win_label.font = "-80"
        you_win_label.color = "red"
        self.window.add(
            you_win_label,
            x=(self.window_width - you_win_label.width) / 2,
            y=(self.window_height - you_win_label.height) / 2,
        )

    def __init__(
        self,
        ball_radius=BALL_RADIUS,
        paddle_width=PADDLE_WIDTH,
        paddle_height=PADDLE_HEIGHT,
        paddle_offset=PADDLE_OFFSET,
        brick_rows=BRICK_ROWS,
        brick_cols=BRICK_COLS,
        brick_width=BRICK_WIDTH,
        brick_height=BRICK_HEIGHT,
        brick_offset=BRICK_OFFSET,
        brick_spacing=BRICK_SPACING,
        title="Breakout",
    ):
        # Create a graphical window, with some extra space
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (
            brick_rows * (brick_height + brick_spacing) - brick_spacing
        )
        self.window = GWindow(
            width=self.window_width, height=self.window_height, title=title
        )

        # Create a paddle
        self.paddle = GRect(
            paddle_width,
            paddle_height,
            x=(self.window_width - paddle_width) / 2,
            y=self.window_height - paddle_offset - paddle_height,
        )
        self.paddle.filled = True
        self.window.add(self.paddle)

        # Center a filled ball in the graphical window
        self.ball_radius = ball_radius
        self.ball = GOval(
            ball_radius,
            ball_radius,
            x=(self.window_width - ball_radius) / 2,
            y=(self.window_height - ball_radius) / 2,
        )
        self.ball.filled = True
        self.window.add(self.ball)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        def ball_velocity_init(mouse):
            # if the ball is moving, do nothing
            if self.__dx != 0 or self.__dy != 0:
                return
            self.__dy = INITIAL_Y_SPEED
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx

        def paddle_move(mouse):
            if (mouse.x - paddle_width / 2) < 0:
                self.paddle.x = 0
            elif (mouse.x + paddle_width / 2) > self.window_width:
                self.paddle.x = self.window_width - paddle_width
            else:
                self.paddle.x = mouse.x - paddle_width / 2

        # Initialize our mouse listeners
        onmouseclicked(ball_velocity_init)
        onmousemoved(paddle_move)

        # Draw bricks
        self.__bricks_amount = brick_rows * brick_cols
        self.bricks = [[0 for _ in range(brick_cols)] for _ in range(brick_rows)]
        for i in range(brick_cols):
            for j in range(brick_rows):
                self.bricks[i][j] = GRect(
                    brick_width,
                    brick_height,
                    x=j * (brick_width + brick_spacing),
                    y=brick_offset + i * (brick_height + brick_spacing),
                )
                self.bricks[i][j].filled = True
                if i < 2:
                    self.bricks[i][j].fill_color = "red"
                elif i < 4:
                    self.bricks[i][j].fill_color = "orange"
                elif i < 6:
                    self.bricks[i][j].fill_color = "yellow"
                elif i < 8:
                    self.bricks[i][j].fill_color = "green"
                else:
                    self.bricks[i][j].fill_color = "blue"
                self.window.add(self.bricks[i][j])
