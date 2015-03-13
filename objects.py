import pygame, sys, random, os


class Ball:

    def __init__(self, surface, color = (255, 255, 255), velX = 2, velY = 2):
        self.surface = surface
        self.posX, self.posY = surface.get_width() / 2, surface.get_height() / 2
        self.color = color
        self.radius = surface.get_width() / 40
        self.maxVelX, self.maxVelY = velX, velY
        self.vel = [random.randrange(2, self.maxVelX + 1), random.randrange(2, self.maxVelY + 1)]

    def display(self):
        pygame.draw.circle(self.surface, self.color, (self.posX, self.posY), self.radius)

    def update(self):
        self.posX += self.vel[0]
        self.posY += self.vel[1]

    def collideX(self):
        self.vel[0] *= -1

    def collideY(self):
        self.vel[1] *= -1

    def displace(self, amount):
        self.posX += amount

    def reset(self, direction):
        self.posX, self.posY = self.surface.get_width() / 2, self.surface.get_height() / 2
        if direction == "Right":
            self.vel = [random.randrange(2, self.maxVelX + 1), random.randrange(2, self.maxVelY + 1)]
        else:
            self.vel = [random.randrange(-self.maxVelX, -1), random.randrange(-self.maxVelY, -1)]


class Paddle:

    def __init__(self, surface, side, color = (255, 255, 255), height_scale = .25):
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

    def display(self):
        pygame.draw.rect(self.surface, self.color, (self.posX, self.posY, self.width, self.height))

    def update(self):
        self.posY += self.vel[1]

    def moveUp(self, pressed):
        if pressed:
            self.vel[1] = -4
        else:
            self.vel[1] = 0
        if not (self.posY <= 0):
            self.update()

    def moveDown(self, pressed):
        if pressed:
            self.vel[1] = 4
        else:
            self.vel[1] = 0
        if not (self.posY >= self.surface.get_height() - self.height):
            self.update()

    def reset(self):
        self.posY = self.surface.get_height() / 2 - self.height / 2


class Game:

    def __init__(self, surface):
        self.screen = surface
        self.size = self.width, self.height = self.screen.get_width(), self.screen.get_height()
        self.black = (10, 10, 10)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.ball = Ball(self.screen, (255, 0, 0))
        self.player_1 = Paddle(self.screen, 'left')
        self.player_2 = Paddle(self.screen, 'right')
        self.score = [0, 0]
        self.font = pygame.font.Font(None, 54)

    def newGame(self):

        # Set score to zero
        self.score = [0, 0]

        # Reset player an ball positions
        self.player_1.reset()
        self.player_2.reset()
        self.ball.reset("Right")

        # Main game loop
        while 1:
            # Set fps to 60
            self.clock.tick_busy_loop(60)

            # Polls event queue for quit event and closes window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # draw black background
            self.screen.fill(self.black)
            # draw white middle line
            pygame.draw.line(self.screen, self.white, (self.width / 2, 0), (self.width / 2, self.height))

            # Draw score to screen
            draw_score1 = self.font.render(str(self.score[0]), 0, self.white)
            draw_score2 = self.font.render(str(self.score[1]), 0, self.white)
            self.screen.blit(draw_score1, ((self.width * .4), 10))
            self.screen.blit(draw_score2, ((self.width * .57), 10))

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
            elif self.ball.posX + self.ball.radius > self.width - self.player_2.width / 2:
                self.score[0] += 1
                self.ball.reset("Left")
            elif self.ball.posX - self.ball.radius < self.player_1.width / 2:
                self.score[1] += 1
                self.ball.reset("Right")

            # Update ball and display
            self.ball.update()
            self.ball.display()

            pygame.display.flip()


class MainMenu:

    def __init__(self, surface):
        self.playButton = pygame.image.load(os.path.join('img', 'play_button.png'))
        self.quitButton = pygame.image.load(os.path.join('img', 'quit_button.png'))
        self.playButton = self.playButton.convert()
        self.quitButton = self.quitButton.convert()
        self.font = pygame.font.Font(None, 54)
        self.logo = self.font.render("P0NG", 0, (255, 255, 255))
        self.screen = surface
        self.clock = pygame.time.Clock()

    def draw(self):

        while 1:
            self.clock.tick_busy_loop(60)

            # fill screen to black
            self.screen.fill((10, 10, 10))

            # draw logo
            self.screen.blit(self.logo, (self.screen.get_width() / 2 - self.logo.get_width() / 2, 10))

            # draw buttonZ
            self.screen.blit(self.playButton, (self.screen.get_width() / 2 - self.playButton.get_width() / 2, 100))
            self.screen.blit(self.quitButton, (self.screen.get_width() / 2 - self.quitButton.get_width() / 2, 120 + self.quitButton.get_height()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.screen.get_width() / 2 - self.playButton.get_width() / 2 <= pos[0] <= self.screen.get_width() / 2 + self.playButton.get_width() / 2:
                        if self.playButton.get_height() + 100 >= pos[1] >= 100:
                            return
                        elif self.quitButton.get_height() + 120 <= pos[1] <= 2 * self.quitButton.get_height() + 120:
                            sys.exit()

            pygame.display.flip()