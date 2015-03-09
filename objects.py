import pygame, sys

class Ball:

    def __init__ (self, surface, color = (255, 255, 255), velX = 2, velY = 2):
        self.surface = surface
        self.posX, self.posY = surface.get_width() / 2, surface.get_height() / 2
        self.color = (color)
        self.radius = surface.get_width() / 40
        self.vel = [velX, velY]

    def display (self):
        pygame.draw.circle(self.surface, self.color, (self.posX, self.posY), self.radius)

    def update (self):
        self.posX += self.vel[0]
        self.posY += self.vel[1]

    def collideX (self):
        self.vel[0] *= -1

    def collideY (self):
        self.vel[1] *= -1

    def displace(self, amount):
        self.posX += amount

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

    def reset (self):
        self.posY = self.surface.get_height() / 2 - self.height / 2

class Game:

    def __init__(self, size):
        pygame.init()
        pygame.key.set_repeat(0, 1)
        self.size = self.width, self.height = size
        self.screen = pygame.display.set_mode(size)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.ball = Ball(self.screen)
        self.player_1 = Paddle(self.screen, 'left')
        self.player_2 = Paddle(self.screen, 'right')

    def newGame (self):
        while 1:
            self.clock.tick_busy_loop(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.black)
            pygame.draw.line(self.screen, self.white, (self.width / 2, 0), (self.width / 2, self.height))

            # Movement
            self.player_2.moveUp(pygame.key.get_pressed()[pygame.K_UP])
            self.player_2.moveDown(pygame.key.get_pressed()[pygame.K_DOWN])

            self.player_1.moveUp(pygame.key.get_pressed()[pygame.K_w])
            self.player_1.moveDown(pygame.key.get_pressed()[pygame.K_s])

            # Display Paddles
            self.player_1.display()
            self.player_2.display()

            # Y Collisions
            if self.ball.posY + self.ball.radius >= self.height:
                self.ball.collideY()
            elif self.ball.posY - self.ball.radius <= 0:
                self.ball.collideY()

            # X Collisions
            if self.width - self.player_2.width / 2 >= self.ball.posX + self.ball.radius >= self.width - self.player_2.width:
                if self.ball.posY - self.ball.radius <= self.player_2.posY + self.player_2.height:
                    if self.ball.posY + self.ball.radius >= self.player_2.posY:
                        if self.width - self.player_2.width / 2 >= self.ball.posX + self.ball.radius > self.width - self.player_2.width:
                            self.ball.displace(self.ball.posX - self.player_2.posX)
                        self.ball.collideX()

            elif self.player_1.width / 2 <= self.ball.posX - self.ball.radius <= self.player_1.width:
                if self.ball.posY - self.ball.radius <= self.player_1.posY + self.player_1.height:
                    if self.ball.posY + self.ball.radius >= self.player_1.posY:
                        if self.player_1.width / 2 <= self.ball.posX - self.ball.radius < self.player_1.width:
                            self.ball.displace(self.ball.posX - self.player_1.width)
                        self.ball.collideX()
            elif (self.ball.posX + self.ball.radius > self.width - self.player_2.width / 2) or (self.ball.posX - self.ball.radius < self.player_1.width / 2):
                self.ball.reset()


            self.ball.update()
            self.ball.display()

            pygame.display.flip()