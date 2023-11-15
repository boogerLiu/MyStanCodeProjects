"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 40  # 100 frames per second
NUM_LIVES = 3  # Number of attempts


def main():
    graphics = BreakoutGraphics()
    num_lives = NUM_LIVES

    # Add the animation loop here!
    while True:
        pause(FRAME_RATE)
        if graphics.get_bricks_amount() <= 0:
            graphics.show_you_win()
            break

        if graphics.touch_bottom_wall():
            num_lives -= 1
            if num_lives == 0:
                graphics.show_game_over()
                break
            graphics.reset_ball()

        if graphics.touch_left_wall():
            # Avoid the ball stuck in the wall
            graphics.ball.x = 0
            graphics.dx_rebound()
        elif graphics.touch_right_wall():
            # Avoid the ball stuck in the wall
            graphics.ball.x = graphics.window.width - graphics.ball.width
            graphics.dx_rebound()

        elif graphics.touch_paddle():
            # Avoid the ball stuck in the paddle
            graphics.ball.y = graphics.paddle.y - graphics.ball.height
            graphics.dy_rebound()
        elif graphics.ball_left_touch_something():
            graphics.dx_rebound()
            graphics.window.remove(graphics.ball_left_touch_something())
            graphics.hit_a_brick()
        elif graphics.ball_right_touch_something():
            graphics.dx_rebound()
            graphics.window.remove(graphics.ball_right_touch_something())
            graphics.hit_a_brick()
        elif graphics.ball_top_touch_something():
            graphics.dy_rebound()
            graphics.window.remove(graphics.ball_top_touch_something())
            graphics.hit_a_brick()
        elif graphics.ball_bottom_touch_something():
            graphics.dy_rebound()
            graphics.window.remove(graphics.ball_bottom_touch_something())
            graphics.hit_a_brick()
        graphics.ball_move()


if __name__ == "__main__":
    main()
