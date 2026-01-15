import pygame as pg
import sys
from random import choice, randint
from time import time
from pygame.locals import *
from tetris_set import *
from sounds import init_sounds, play_sound

sounds = None

def pauseScreen():
    pause = pg.Surface((window_w, window_h), pg.SRCALPHA)
    pause.fill((0, 0, 50, 180))
    display_surf.blit(pause, (0, 0))

def main():
    global fps_clock, display_surf, basic_font, big_font, small_font, sounds
    pg.init()
    pg.mixer.init()
    sounds = init_sounds()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((window_w, window_h))
    basic_font = pg.font.SysFont('segoeui', 22)
    big_font = pg.font.SysFont('segoeui', 52, bold=True)
    small_font = pg.font.SysFont('segoeui', 16)
    pg.display.set_caption('Tetris')
    showText('TETRIS')
    while True:
        runTetris()
        play_sound(sounds, 'gameover')
        pauseScreen()
        showText('GAME OVER')

def runTetris():
    global sounds
    cup = emptycup()
    last_move_down = time()
    last_side_move = time()
    last_fall = time()
    going_down = False
    going_left = False
    going_right = False
    points = 0
    level, fall_speed = calcSpeed(points)
    fallingFig = getNewFig()
    nextFig = getNewFig()
    run = True

    while run:
        if fallingFig == None:
            fallingFig = nextFig
            nextFig = getNewFig()
            last_fall = time()
            if not checkPos(cup, fallingFig):
                return

        quitGame()
        
        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pauseScreen()
                    showText('PAUSED')
                    last_fall = time()
                    last_move_down = time()
                    last_side_move = time()
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False

            elif event.type == KEYDOWN:
                if event.key == K_LEFT and checkPos(cup, fallingFig, adjX=-1):
                    fallingFig['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time()
                    play_sound(sounds, 'move')

                elif event.key == K_RIGHT and checkPos(cup, fallingFig, adjX=1):
                    fallingFig['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time()
                    play_sound(sounds, 'move')

                elif event.key == K_UP:
                    fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(figures[fallingFig['shape']])
                    if not checkPos(cup, fallingFig):
                        fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(figures[fallingFig['shape']])
                    else:
                        play_sound(sounds, 'rotate')

                elif event.key == K_DOWN:
                    going_down = True
                    if checkPos(cup, fallingFig, adjY=1):
                        fallingFig['y'] += 1
                    last_move_down = time()

                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, cup_h):
                        if not checkPos(cup, fallingFig, adjY=i):
                            break
                    fallingFig['y'] += i - 1
                    play_sound(sounds, 'drop')

        if (going_left or going_right) and time() - last_side_move > side_freq:
            if going_left and checkPos(cup, fallingFig, adjX=-1):
                fallingFig['x'] -= 1
                play_sound(sounds, 'move')
            elif going_right and checkPos(cup, fallingFig, adjX=1):
                fallingFig['x'] += 1
                play_sound(sounds, 'move')
            last_side_move = time()

        if going_down and time() - last_move_down > down_freq and checkPos(cup, fallingFig, adjY=1):
            fallingFig['y'] += 1
            last_move_down = time()

        if time() - last_fall > fall_speed:
            if not checkPos(cup, fallingFig, adjY=1):
                addToCup(cup, fallingFig)
                play_sound(sounds, 'drop')
                old_level = level
                cleared = clearCompleted(cup)
                if cleared > 0:
                    play_sound(sounds, 'clear')
                points += cleared
                level, fall_speed = calcSpeed(points)
                if level > old_level:
                    play_sound(sounds, 'levelup')
                fallingFig = None
            else:
                fallingFig['y'] += 1
                last_fall = time()

        display_surf.fill(bg_color)
        drawTitle()
        gamecup(cup)
        drawInfo(points, level)
        drawnextFig(nextFig)
        if fallingFig != None:
            drawGhost(cup, fallingFig)
            drawFig(fallingFig)
        pg.display.update()
        fps_clock.tick(fps)


def txtObjects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def stopGame():
    pg.quit()
    sys.exit()

def checkKeys():
    quitGame()
    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def showText(text):
    titleSurf, titleRect = txtObjects(text, big_font, title_color)
    titleRect.center = (int(window_w / 2), int(window_h / 2) - 30)
    display_surf.blit(titleSurf, titleRect)
    
    pressKeySurf, pressKeyRect = txtObjects('Press any key', basic_font, gray)
    pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 40)
    display_surf.blit(pressKeySurf, pressKeyRect)

    while checkKeys() == None:
        pg.display.update()
        fps_clock.tick()

def quitGame():
    for event in pg.event.get(QUIT):
        stopGame()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stopGame()
        pg.event.post(event)

def calcSpeed(points):
    level = int(points / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    if fall_speed < 0.05:
        fall_speed = 0.05
    return level, fall_speed

def getNewFig():
    shape = choice(list(figures.keys()))
    newFigure = {
        'shape': shape,
        'rotation': randint(0, len(figures[shape]) - 1),
        'x': int(cup_w / 2) - int(fig_w / 2),
        'y': -2,
        'color': randint(0, len(colors) - 1)
    }
    return newFigure

def addToCup(cup, fig):
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                cup[x + fig['x']][y + fig['y']] = fig['color']

def emptycup():
    cup = []
    for i in range(cup_w):
        cup.append([empty] * cup_h)
    return cup

def incup(x, y):
    return x >= 0 and x < cup_w and y < cup_h

def checkPos(cup, fig, adjX=0, adjY=0):
    for x in range(fig_w):
        for y in range(fig_h):
            abovecup = y + fig['y'] + adjY < 0
            if abovecup or figures[fig['shape']][fig['rotation']][y][x] == empty:
                continue
            if not incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                return False
            if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty:
                return False
    return True

def isCompleted(cup, y):
    for x in range(cup_w):
        if cup[x][y] == empty:
            return False
    return True

def clearCompleted(cup):
    removed_lines = 0
    y = cup_h - 1
    while y >= 0:
        if isCompleted(cup, y):
            for pushDownY in range(y, 0, -1):
                for x in range(cup_w):
                    cup[x][pushDownY] = cup[x][pushDownY - 1]
            for x in range(cup_w):
                cup[x][0] = empty
            removed_lines += 1
        else:
            y -= 1
    return removed_lines

def convertCoords(block_x, block_y):
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))

def drawBlock(block_x, block_y, color, pixelx=None, pixely=None):
    if color == empty:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(block_x, block_y)
    pg.draw.rect(display_surf, colors[color], (pixelx + 1, pixely + 1, block - 2, block - 2), 0, 3)
    pg.draw.rect(display_surf, lightcolors[color], (pixelx + 1, pixely + 1, block - 5, block - 5), 0, 3)

def drawGhostBlock(block_x, block_y, color, pixelx=None, pixely=None):
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(block_x, block_y)
    ghost_color = tuple(c // 4 for c in colors[color])
    pg.draw.rect(display_surf, ghost_color, (pixelx + 1, pixely + 1, block - 2, block - 2), 0, 3)

def gamecup(cup):
    pg.draw.rect(display_surf, brd_color, (side_margin - 4, top_margin - 4, (cup_w * block) + 8, (cup_h * block) + 8), 3, 5)
    pg.draw.rect(display_surf, (20, 20, 30), (side_margin, top_margin, block * cup_w, block * cup_h))
    
    for i in range(cup_h + 1):
        pg.draw.line(display_surf, grid_color, 
                     (side_margin, top_margin + i * block), 
                     (side_margin + cup_w * block, top_margin + i * block))
    for j in range(cup_w + 1):
        pg.draw.line(display_surf, grid_color, 
                     (side_margin + j * block, top_margin), 
                     (side_margin + j * block, top_margin + cup_h * block))
    
    for x in range(cup_w):
        for y in range(cup_h):
            drawBlock(x, y, cup[x][y])

def drawTitle():
    titleSurf = big_font.render('TETRIS', True, title_color)
    titleRect = titleSurf.get_rect()
    titleRect.topleft = (20, 20)
    display_surf.blit(titleSurf, titleRect)

def drawInfo(points, level):
    pointsSurf = basic_font.render(f'Score: {points}', True, txt_color)
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (20, 100)
    display_surf.blit(pointsSurf, pointsRect)

    levelSurf = basic_font.render(f'Level: {level}', True, txt_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (20, 130)
    display_surf.blit(levelSurf, levelRect)

    controls = [
        ('←/→', 'Move'),
        ('↑', 'Rotate'),
        ('↓', 'Soft drop'),
        ('Enter', 'Hard drop'),
        ('Space', 'Pause'),
        ('Esc', 'Exit')
    ]
    
    start_y = 380
    for i, (key, action) in enumerate(controls):
        keySurf = small_font.render(f'{key}: {action}', True, info_color)
        keyRect = keySurf.get_rect()
        keyRect.topleft = (20, start_y + i * 22)
        display_surf.blit(keySurf, keyRect)

def drawFig(fig, pixelx=None, pixely=None):
    figToDraw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(fig['x'], fig['y'])
    for x in range(fig_w):
        for y in range(fig_h):
            if figToDraw[y][x] != empty:
                drawBlock(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))

def drawGhost(cup, fig):
    ghost_y = fig['y']
    while checkPos(cup, fig, adjY=ghost_y - fig['y'] + 1):
        ghost_y += 1
    
    if ghost_y == fig['y']:
        return
    
    figToDraw = figures[fig['shape']][fig['rotation']]
    pixelx, pixely = convertCoords(fig['x'], ghost_y)
    
    for x in range(fig_w):
        for y in range(fig_h):
            if figToDraw[y][x] != empty:
                drawGhostBlock(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))

def drawnextFig(fig):
    nextSurf = basic_font.render('Next:', True, txt_color)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (20, 200)
    display_surf.blit(nextSurf, nextRect)
    
    box_x = 20
    box_y = 235
    box_size = 120
    pg.draw.rect(display_surf, (20, 20, 30), (box_x, box_y, box_size, box_size), 0, 5)
    pg.draw.rect(display_surf, brd_color, (box_x, box_y, box_size, box_size), 2, 5)
    
    drawFig(fig, pixelx=box_x + 10, pixely=box_y + 10)
