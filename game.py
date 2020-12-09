import pygame, random
import tkinter as tk
from tkinter import messagebox

# Game Variables
WIDTH = 320
ROWS = 16

class Cube:
    def __init__(self, pos, dx=1, dy=0, color=(255, 0, 0)):
        self.pos = pos
        self.dx = dx
        self.dy = dy
        self.color = color

    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)

    def draw(self, surf):
        dis = WIDTH // ROWS
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surf, self.color, (i*dis+1, j*dis+1, dis - 1, dis - 1))

class Snake:
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dx = 1
        self.dy = 0
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and self.dx != 1:
                    self.dx = -1
                    self.dy = 0
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]

                elif keys[pygame.K_RIGHT] and self.dx != -1:
                    self.dx = 1
                    self.dy = 0
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]

                elif keys[pygame.K_UP] and self.dy != 1:
                    self.dx = 0
                    self.dy = -1
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]

                elif keys[pygame.K_DOWN] and self.dy != -1:
                    self.dx = 0
                    self.dy = 1
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]

        for ind, cube in enumerate(self.body):
            pos = cube.pos[:]

            if pos in self.turns:
                turn = self.turns[pos]
                cube.move(turn[0], turn[1])

                if ind == len(self.body) - 1:
                    self.turns.pop(pos)
            else:
                if cube.dx == -1 and cube.pos[0] <= 0: cube.pos = (ROWS - 1, cube.pos[1])
                elif cube.dx == 1 and cube.pos[0] >= ROWS - 1: cube.pos = (0, cube.pos[1])
                elif cube.dy == 1 and cube.pos[1] >= ROWS - 1: cube.pos = (cube.pos[0], 0)
                elif cube.dy == -1 and cube.pos[1] <= 0: cube.pos = (cube.pos[0], ROWS - 1)
                else: cube.move(cube.dx, cube.dy)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dx = 1
        self.dy = 0

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dx, tail.dy
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dx = dx
        self.body[-1].dy = dy

    def draw(self, surf):
        for ind, cube in enumerate(self.body):
            cube.draw(surf)

def randomSnack(item):
    global ROWS

    pos = item.body

    while True:
        x = random.randint(0, ROWS - 1)
        y = random.randint(0, ROWS - 1)

        if len(list(filter(lambda z:z.pos == (x,y), pos))) > 0:
            continue
        else:
            break
    return (x, y)

snake = Snake((255, 0, 0), (10, 10))
snack = Cube(randomSnack(snake), color=(0, 255, 0))

def drawGrid(surf):
    sizeBtwn = WIDTH // ROWS

    x = 0
    y = 0

    for i in range(ROWS):
        x += sizeBtwn
        y += sizeBtwn

        pygame.draw.line(surf, (100, 100, 100), (x, 0), (x, WIDTH))
        pygame.draw.line(surf, (100, 100, 100), (0, y), (WIDTH, y))

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)

    try: 
        root.destroy()
    except:
        pass

def redrawWindow(surf):
    global snake, snack
    surf.fill((0, 0, 0))
    drawGrid(surf)
    snake.draw(surf)
    snack.draw(surf)
    pygame.display.update()

def main():
    try:
        global snake, snack
        window = pygame.display.set_mode((WIDTH, WIDTH))
        flag = True
        clock = pygame.time.Clock()

        while flag:
            pygame.time.delay(50)
            clock.tick(10)
            snake.move()

            if snake.body[0].pos == snack.pos:
                snake.addCube()
                snack = Cube(randomSnack(snake), color=(0, 255, 0))

            for x in range(len(snake.body)):
                if snake.body[x].pos in list(map(lambda z:z.pos, snake.body[x+1:])):
                    print('Score: ', len(snake.body))
                    message_box("You Lost", "Play again...")
                    snake.reset((10, 10))
                    break

            redrawWindow(window)

    except KeyboardInterrupt:
        print("Game Closed!")
        pygame.quit()

main()