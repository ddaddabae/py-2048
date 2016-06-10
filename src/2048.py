import pygame, sys
from pygame.locals import *
import pygame.locals
from pygame import key,event
import random

pygame.init()

display = pygame.display.set_mode((200,200))
pygame.display.set_caption('2048 game')

LineColor = pygame.Color(0, 0, 0)
BoxColor = pygame.Color(200, 200, 150)
FontColor = pygame.Color(50, 150, 50)
BGColor = pygame.Color(255, 255, 255)

lineArr = []
for pos in range(50,200,50):
    lineArr.append((0, pos))
    lineArr.append((200, pos))
    lineArr.append((200, pos + 50))
lineArr.append((200, 0))
lineArr.append((0, 0))
for pos in range(50, 200, 50):
    lineArr.append((pos, 0))
    lineArr.append((pos, 200))
    lineArr.append((pos + 50, 200))

def moveBox(items, direction:int):
    newList = []
    moved = False

    if direction == pygame.K_DOWN:
        for i in range(4):
            for j in range(3, -1, -1):
                for k in range(j - 1, -1, -1):
                    if items[i][k] == 0:
                        continue
                    elif items[i][j] == items[i][k]:
                        items[i][k] = 0
                        items[i][j] *= 2
                        j = k - 1
                        moved = True
                        break
                    else:
                        break
            for j in range(3, -1, -1):
                if items[i][j] != 0:
                    continue
                else:
                    for k in range(j - 1, -1, -1):
                        if items[i][k] != 0:
                            items[i][j] = items[i][k]
                            items[i][k] = 0
                            moved = True
                            break
    elif direction == pygame.K_UP:
        for i in range(4):
            for j in range(4):
                for k in range(j + 1, 4, 1):
                    if items[i][k] == 0:
                        continue
                    elif items[i][j] == items[i][k]:
                        items[i][k] = 0
                        items[i][j] *= 2
                        j = k + 1
                        moved = True
                        break
                    else:
                        break
            for j in range(4):
                if items[i][j] != 0:
                    continue
                else:
                    for k in range(j + 1, 4, 1):
                        if items[i][k] != 0:
                            items[i][j] = items[i][k]
                            items[i][k] = 0
                            moved = True
                            break
    elif direction == pygame.K_LEFT:
        for i in range(4):
            for j in range(4):
                for k in range(j + 1, 4, 1):
                    if items[k][i] == 0:
                        continue
                    elif items[j][i] == items[k][i]:
                        items[k][i] = 0
                        items[j][i] *= 2
                        j = k + 1
                        moved = True
                        break
                    else:
                        break
            for j in range(4):
                if items[j][i] != 0:
                    continue
                else:
                    for k in range(j + 1, 4, 1):
                        if items[k][i] != 0:
                            items[j][i] = items[k][i]
                            items[k][i] = 0
                            moved = True
                            break
    elif direction == pygame.K_RIGHT:
        for i in range(4):
            for j in range(3, -1, -1):
                for k in range(j - 1, -1, -1):
                    if items[k][i] == 0:
                        continue
                    elif items[j][i] == items[k][i]:
                        items[k][i] = 0
                        items[j][i] *= 2
                        j = k + 1
                        moved = True
                        break
                    else:
                        break
            for j in range(3, -1, -1):
                if items[j][i] != 0:
                    continue
                else:
                    for k in range(j - 1, -1, -1):
                        if items[k][i] != 0:
                            items[j][i] = items[k][i]
                            items[k][i] = 0
                            moved = True
                            break

    return moved

def getRandomBox(items):
    while True:
        randPos = random.randint(0, 15)
        if items[randPos % 4][randPos // 4] == 0:
            newVal = random.randint(0, 10)
            return [randPos % 4, randPos // 4, 4 if newVal > 9 else 2]

def drawBox(box):
    x, y, val = box
    print("In printBox method")
    print(x, y, val)

    box = pygame.draw.rect(display, BoxColor, (x * 50 + 2, y * 50 + 2, 48, 48), 0)
    display.fill(BoxColor, box)
    display.fill(BoxColor, box.inflate(-5, -5))

    valueDp = pygame.font.SysFont('verdana',22).render(str(val), True, FontColor)
    valueBox = valueDp.get_rect()

    valueBox.center = (x * 50 + 25, y * 50 + 26)
    display.blit(valueDp, valueBox)

def redraw():
    display.fill(BGColor)
    pygame.draw.lines(display, LineColor, False, lineArr, 1)

    for i in range(4):
        for j in range(4):
            if items[i][j] != 0:
                drawBox([i, j, items[i][j]])
    pygame.display.update()

items = [[0 for x in range(4)] for y in range(4)]
initx, inity, initval = getRandomBox(items)
items[initx][inity] = initval
redraw()

continueGame = True
while continueGame:
    for curEvent in pygame.event.get():
        if curEvent.type == pygame.QUIT:
            continueGame = False
            break
        elif curEvent.type == pygame.KEYDOWN:
            if curEvent.key in (pygame.K_LEFT,pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                moved = moveBox(items, curEvent.key)
                # draw boxes EXCEPT new one
                if moved and len(items) < 16:
                    newBox = getRandomBox(items)
                    items[newBox[0]][newBox[1]] = newBox[2]
                redraw()
