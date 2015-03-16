import pygame, sys, random, os


class Ball:

    def __init__(self, surface, color = (255, 255, 255), vel = 2):
        self.surface = surface
        self.posX, self.posY = surface.get_width() / 2, surface.get_height() / 2
        self.color = color
        self.radius = surface.get_width() / 40
        self.maxVelX, self.maxVelY = vel, vel
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

    def changeColor(self, color):
        self.color = color

    def changeVel(self, vel):
        self.maxVelX, self.maxVelY = vel, vel
        self.reset("Right")


class Paddle:

    def __init__(self, surface, side, color = (255, 255, 255), height_scale = .25):
        self.surface = surface
        self.side = side
        self.color = color
        self.heightScale = height_scale
        self.height = self.surface.get_height() * self.heightScale
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

    def changeColor(self, color):
        self.color = color

    def changeHeight(self, height_scale):
        self.heightScale = height_scale
        self.height = self.surface.get_height() * self.heightScale


class Game:

    def __init__(self, surface):
        self.screen = surface
        self.size = self.width, self.height = self.screen.get_width(), self.screen.get_height()
        self.black = (10, 10, 10)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.ball = Ball(self.screen, (0, 0, 255))
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
            self.screen.blit(self.logo, (self.screen.get_width() / 2 - self.logo.get_width() / 2, self.screen.get_height() / 20))

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


class SettingsMenu:

    def __init__(self, surface, ball, player_1, player_2):
        self.screen = surface
        self.ball = ball
        self.player_1 = player_1
        self.player_2 = player_2
        self.clock = pygame.time.Clock()
        self.fontLogo = pygame.font.Font(None, 54)
        self.fontHeading = pygame.font.Font(None, 42)
        self.fontNormal = pygame.font.Font(None, 24)
        self.speedButtons = [pygame.image.load(os.path.join('img', 'slow.png')), pygame.image.load(os.path.join('img', 'normal.png')), pygame.image.load(os.path.join('img', 'fast.png'))]
        self.speedButtons = [self.speedButtons[0].convert(), self.speedButtons[1].convert(), self.speedButtons[2].convert()]
        self.paddleSizeButtons = [pygame.image.load(os.path.join('img', 'small.png')), pygame.image.load(os.path.join('img', 'normal.png')), pygame.image.load(os.path.join('img', 'big.png'))]
        self.paddleSizeButtons = [self.paddleSizeButtons[0].convert(), self.paddleSizeButtons[1].convert(), self.paddleSizeButtons[2].convert()]
        self.currentHeights = [player_1.heightScale, player_2.heightScale]
        self.currentColors = [self.ball.color, self.player_1.color, self.player_2.color]
        self.currentVel = [ball.maxVelX, ball.maxVelY]

    def draw(self):
        WHITE = (255, 255, 255)
        settingsLogo = self.fontLogo.render("Settings", 0, WHITE)
        headings = [self.fontHeading.render("Ball", 0, WHITE), self.fontHeading.render("Player 1", 0, WHITE), self.fontHeading.render("Player 2", 0, WHITE)]
        colorLabel = self.fontNormal.render("Color", 0, WHITE)
        heightLabel = self.fontNormal.render("Height", 0, WHITE)
        speedLabel = self.fontNormal.render("Max Speed", 0, WHITE)
        colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        buttons = [self.speedButtons, self.paddleSizeButtons, self.paddleSizeButtons]

        while 1:

            self.clock.tick_busy_loop(60)

            # background
            self.screen.fill((10, 10, 10))

            # draw settings logo
            self.screen.blit(settingsLogo, (self.screen.get_width() / 2 - settingsLogo.get_width() / 2, self.screen.get_height() / 20))

            # draw ballText and playerText
            for i in xrange(len(headings)):
                x = (i + 1) * self.screen.get_width() / (len(headings) + 1) - headings[i].get_width() / 2
                self.screen.blit(headings[i], (x, self.screen.get_height() / 5))
                self.screen.blit(colorLabel, (x, self.screen.get_height() / 5 + headings[i].get_height() + 10))
                for j in xrange(5):
                    pygame.draw.rect(self.screen, colors[j], (x + j * 20, self.screen.get_height() / 5 + headings[i].get_height() + 10 + colorLabel.get_height() + 10, 20, 20))

            self.screen.blit(speedLabel, (self.screen.get_width() / (len(headings) + 1) - headings[0].get_width() / 2, self.screen.get_height() / 5 + headings[0].get_height() + 10 + colorLabel.get_height() + 10 + 20 + 20))

            for i in xrange(2):
                self.screen.blit(heightLabel, ((2 + i) * self.screen.get_width() / (len(headings) + 1) - headings[i + 1].get_width() / 2, self.screen.get_height() / 5 + headings[0].get_height() + 10 + colorLabel.get_height() + 10 + 20 + 20))

            for i in xrange(len(buttons)):
                self.screen.blit(buttons[i][0], ((i + 1) * self.screen.get_width() / (len(headings) + 1) - headings[i].get_width() / 2, self.screen.get_height() / 5 + headings[0].get_height() + 10 + colorLabel.get_height() + 10 + 20 + 20 + heightLabel.get_height() + 10))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.flip()