import pygame

class Ball:

    def __init__ (self, surface, color = (255, 255, 255), radius = 20, velX = 2, velY = 2):
        self.surface = surface
        self.posX, self.posY = surface.get_width() / 2, surface.get_height() / 2
        self.color = (color)
        self.radius = radius
        self.velX, self.velY = velX, velY

    def display (self):
        pygame.draw.circle(self.surface, self.color, (self.posX, self.posY), self.radius)

    def update (self):
        if self.posX + self.radius >= self.surface.get_width() or self.posX - self.radius <= 0:
            self.velX *= -1
        if self.posY + self.radius >= self.surface.get_height() or self.posY - self.radius <= 0:
            self.velY *= -1
        self.posX += self.velX
        self.posY += self.velY

class Paddle:

    def __init__ (self, surface, side, color = (255, 255, 255), length_scale = .25):
        self.surface = surface
        self.side = side
        self.color = color
        self.length = self.surface.get_height() * length_scale
        self.width = self.surface.get_width() / 40
        self.vel = 4
        self.posY = self.surface.get_height() / 2 - self.length / 2
        if side == 'left':
            self.posX = 0
        elif side == 'right':
            self.posX = self.surface.get_width() - self.width
        else:
            print "ERROR: Paddle initialized incorrectly"

    def display (self):
        pygame.draw.rect(self.surface, self.color, (self.posX, self.posY, self.width, self.length))

    def moveUp (self):
        if not (self.posY <= 0):
            self.posY -= self.vel

    def moveDown (self):
        if not (self.posY >= self.surface.get_height() - self.length):
            self.posY += self.vel