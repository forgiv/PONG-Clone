import pygame

class Ball:

    def __init__ (self, surface, color = (255, 255, 255), radius = 15, velX = 2, velY = 2):
        self.surface = surface
        self.posX, self.posY = surface.get_width() / 2, surface.get_height() / 2
        self.color = (color)
        self.radius = radius
        self.vel = [velX, velY]

    def display (self):
        pygame.draw.circle(self.surface, self.color, (self.posX, self.posY), self.radius)

    def update (self):
        self.posX += self.vel[0]
        self.posY += self.vel[1]

    def collideY (self):
        self.vel[1] *= -1

    def setVel (self, x, y):
        self.vel = [x, y]

    def reset (self):
        self.posX, self.posY = self.surface.get_width() / 2, self.surface.get_height() / 2
        self.vel = [2, 2]

class Paddle:

    def __init__ (self, surface, side, color = (255, 255, 255), height_scale = .25):
        self.surface = surface
        self.side = side
        self.color = color
        self.height = self.surface.get_height() * height_scale
        self.width = self.surface.get_width() / 40
        self.vel = [0, 0]
        self.posY = self.surface.get_height() / 2 - self.height / 2
        if side == 'left':
            self.posX = 0
        elif side == 'right':
            self.posX = self.surface.get_width() - self.width
        else:
            print "ERROR: Paddle initialized incorrectly"

    def display (self):
        pygame.draw.rect(self.surface, self.color, (self.posX, self.posY, self.width, self.height))

    def update (self):
        self.posY += self.vel[1]

    def moveUp (self, pressed):
        if pressed:
            self.vel[1] = -4
        else:
            self.vel[1] = 0
        if not (self.posY <= 0):
            self.update()

    def moveDown (self, pressed):
        if pressed:
            self.vel[1] = 4
        else:
            self.vel[1] = 0
        if not (self.posY >= self.surface.get_height() - self.height):
            self.update()