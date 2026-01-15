fps = 30
window_w = 650
window_h = 550
block = 25
cup_h = 20
cup_w = 10

side_freq = 0.12
down_freq = 0.08

side_margin = int((window_w - cup_w * block) / 2) + 80
top_margin = window_h - (cup_h * block) - 25

colors = (
    (0, 240, 240),   # Cyan (I)
    (0, 0, 240),     # Blue (J)
    (240, 160, 0),   # Orange (L)
    (240, 240, 0),   # Yellow (O)
    (0, 240, 0),     # Green (S)
    (160, 0, 240),   # Purple (T)
    (240, 0, 0)      # Red (Z)
)

lightcolors = (
    (100, 255, 255),
    (100, 100, 255),
    (255, 200, 100),
    (255, 255, 100),
    (100, 255, 100),
    (200, 100, 255),
    (255, 100, 100)
)

white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (40, 40, 40)
black = (15, 15, 25)
grid_color = (35, 35, 50)

brd_color = (100, 100, 120)
bg_color = black
txt_color = white
title_color = (0, 240, 240)
info_color = gray

fig_w = 5
fig_h = 5
empty = 'o'

figures = {
    'S': [['ooooo',
           'ooooo',
           'ooxxo',
           'oxxoo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxxo',
           'oooxo',
           'ooooo']],
    'Z': [['ooooo',
           'ooooo',
           'oxxoo',
           'ooxxo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'oxxoo',
           'oxooo',
           'ooooo']],
    'J': [['ooooo',
           'oxooo',
           'oxxxo',
           'ooooo',
           'ooooo'],
          ['ooooo',
           'ooxxo',
           'ooxoo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'oxxxo',
           'oooxo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxoo',
           'oxxoo',
           'ooooo']],
    'L': [['ooooo',
           'oooxo',
           'oxxxo',
           'ooooo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxoo',
           'ooxxo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'oxxxo',
           'oxooo',
           'ooooo'],
          ['ooooo',
           'oxxoo',
           'ooxoo',
           'ooxoo',
           'ooooo']],
    'I': [['ooxoo',
           'ooxoo',
           'ooxoo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'xxxxo',
           'ooooo',
           'ooooo']],
    'O': [['ooooo',
           'ooooo',
           'oxxoo',
           'oxxoo',
           'ooooo']],
    'T': [['ooooo',
           'ooxoo',
           'oxxxo',
           'ooooo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxxo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'oxxxo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'oxxoo',
           'ooxoo',
           'ooooo']]
}
