import pygame
import sys
import random
import os

WHITE = (240, 240, 240)
BLACK = (10, 10, 10)


class Ball:

    def __init__(self, surface, color=WHITE, vel=2):
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

    def collide_x(self):
        self.vel[0] *= -1

    def collide_y(self):
        self.vel[1] *= -1

    def displace(self, amount):
        self.posX += amount

    def reset(self, direction):
        self.posX, self.posY = self.surface.get_width() / 2, self.surface.get_height() / 2
        if direction == "Right":
            self.vel = [random.randrange(2, self.maxVelX + 1), random.randrange(2, self.maxVelY + 1)]
        else:
            self.vel = [random.randrange(-self.maxVelX, -1), random.randrange(-self.maxVelY, -1)]

    def change_color(self, color):
        self.color = color

    def change_vel(self, vel):
        self.maxVelX, self.maxVelY = vel[0], vel[1]
        self.reset("Right")


class Paddle:

    def __init__(self, surface, side, color=WHITE, height_scale=.25):
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

    def move_up(self, pressed):
        if pressed:
            self.vel[1] = -4
        else:
            self.vel[1] = 0
        if not (self.posY <= 0):
            self.update()

    def move_down(self, pressed):
        if pressed:
            self.vel[1] = 4
        else:
            self.vel[1] = 0
        if not (self.posY >= self.surface.get_height() - self.height):
            self.update()

    def reset(self):
        self.posY = self.surface.get_height() / 2 - self.height / 2

    def change_color(self, color):
        self.color = color

    def change_height(self, height_scale):
        self.heightScale = height_scale
        self.height = self.surface.get_height() * self.heightScale
        return height_scale


class Game:

    def __init__(self, surface):
        self.screen = surface
        self.size = self.width, self.height = self.screen.get_width(), self.screen.get_height()
        self.clock = pygame.time.Clock()
        self.ball = Ball(self.screen, WHITE, 2)
        self.player_1 = Paddle(self.screen, 'left')
        self.player_2 = Paddle(self.screen, 'right')
        self.score = [0, 0]
        self.font = pygame.font.Font(os.path.join('data', 'saxmono.ttf'), 54)

    def new_game(self, score=[0, 0]):

        # Set score to zero
        self.score = score

        # Reset player an ball positions
        self.player_1.reset()
        self.player_2.reset()
        self.ball.reset("Right")

        nums = [self.font.render("3", 0, WHITE), self.font.render("2", 0, WHITE), self.font.render("1", 0, WHITE)]

        # Countdown to start game loop
        self.screen.fill(BLACK)
        self.screen.blit(nums[0], (self.screen.get_width() / 2 - nums[0].get_width() / 2, self.screen.get_height() / 2 - nums[0].get_height() / 2))
        pygame.display.flip()
        pygame.time.delay(1000)
        self.screen.fill(BLACK)
        self.screen.blit(nums[1], (self.screen.get_width() / 2 - nums[1].get_width() / 2, self.screen.get_height() / 2 - nums[1].get_height() / 2))
        pygame.display.flip()
        pygame.time.delay(1000)
        self.screen.fill(BLACK)
        self.screen.blit(nums[2], (self.screen.get_width() / 2 - nums[2].get_width() / 2, self.screen.get_height() / 2 - nums[2].get_height() / 2))
        pygame.display.flip()
        pygame.time.delay(1000)

        # Main game loop
        while 1:
            # Set fps to 60
            self.clock.tick_busy_loop(60)

            # Polls event queue for quit event and closes window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # If escape key pressed then draw settings menu
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                return self.score

            # draw black background
            self.screen.fill(BLACK)
            # draw white middle line
            pygame.draw.line(self.screen, WHITE, (self.width / 2, 0), (self.width / 2, self.height))

            # Draw score to screen
            draw_score1 = self.font.render(str(self.score[0]), 0, WHITE)
            draw_score2 = self.font.render(str(self.score[1]), 0, WHITE)
            self.screen.blit(draw_score1, ((self.width * .4), 10))
            self.screen.blit(draw_score2, ((self.width * .57), 10))

            # Movement
            self.player_2.move_up(pygame.key.get_pressed()[pygame.K_UP])
            self.player_2.move_down(pygame.key.get_pressed()[pygame.K_DOWN])

            self.player_1.move_up(pygame.key.get_pressed()[pygame.K_w])
            self.player_1.move_down(pygame.key.get_pressed()[pygame.K_s])

            # Display Paddles
            self.player_1.display()
            self.player_2.display()

            # Y Collisions
            if self.ball.posY + self.ball.radius >= self.height:
                self.ball.collide_y()
            elif self.ball.posY - self.ball.radius <= 0:
                self.ball.collide_y()

            # X Collisions
            if self.width - self.player_2.width / 2 >= self.ball.posX + self.ball.radius >= self.width - self.player_2.width:
                if self.ball.posY - self.ball.radius <= self.player_2.posY + self.player_2.height:
                    if self.ball.posY + self.ball.radius >= self.player_2.posY:
                        if self.width - self.player_2.width / 2 >= self.ball.posX + self.ball.radius > self.width - self.player_2.width:
                            self.ball.displace(self.ball.posX - self.player_2.posX)
                        self.ball.collide_x()

            elif self.player_1.width / 2 <= self.ball.posX - self.ball.radius <= self.player_1.width:
                if self.ball.posY - self.ball.radius <= self.player_1.posY + self.player_1.height:
                    if self.ball.posY + self.ball.radius >= self.player_1.posY:
                        if self.player_1.width / 2 <= self.ball.posX - self.ball.radius < self.player_1.width:
                            self.ball.displace(self.ball.posX - self.player_1.width)
                        self.ball.collide_x()
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
        self.playButton = pygame.image.load(os.path.join('data', 'play_button.png')).convert()
        self.quitButton = pygame.image.load(os.path.join('data', 'quit_button.png')).convert()
        self.settingsButton = pygame.image.load(os.path.join('data', 'settings.png')).convert()
        self.font = pygame.font.Font(os.path.join('data', 'saxmono.ttf'), 54)
        self.logo = self.font.render("P0NG", 0, WHITE)
        self.screen = surface
        self.clock = pygame.time.Clock()

    def draw(self):

        while 1:
            # Set FPS to 60
            self.clock.tick_busy_loop(60)

            # fill screen to black
            self.screen.fill(BLACK)

            # draw logo
            self.screen.blit(self.logo, (self.screen.get_width() / 2 - self.logo.get_width() / 2, self.screen.get_height() / 20))

            # draw buttonZ
            self.screen.blit(self.playButton, (self.screen.get_width() / 2 - self.playButton.get_width() / 2, self.screen.get_height() / 4))
            self.screen.blit(self.settingsButton, (self.screen.get_width() / 2 - self.settingsButton.get_width() / 2, self.screen.get_height() / 4 + self.playButton.get_height() + 5))
            self.screen.blit(self.quitButton, (self.screen.get_width() / 2 - self.quitButton.get_width() / 2, (self.screen.get_height() / 4) + (2 * self.playButton.get_height() + 10)))

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.screen.get_width() / 2 - self.playButton.get_width() / 2 <= pos[0] <= self.screen.get_width() / 2 + self.playButton.get_width() / 2:
                        if self.screen.get_height() / 4 <= pos[1] <= self.screen.get_height() / 4 + self.playButton.get_height():
                            return
                        elif self.screen.get_height() / 4 + self.playButton.get_height() + 5 <= pos[1] <= (self.screen.get_height() / 4 + self.playButton.get_height() + 5) + self.settingsButton.get_height():
                            return "Settings"
                        elif (self.screen.get_height() / 4) + (2 * self.playButton.get_height() + 10) <= pos[1] <= ((self.screen.get_height() / 4) + (2 * self.playButton.get_height() + 10)) + self.quitButton.get_height():
                            sys.exit()

            # Update display
            pygame.display.flip()


class SettingsMenu:

    def __init__(self, surface, ball, player_1, player_2):
        self.screen = surface
        self.ball = ball
        self.player_1 = player_1
        self.player_2 = player_2
        self.clock = pygame.time.Clock()
        self.fontLogo = pygame.font.Font(os.path.join('data', 'saxmono.ttf'), 54)
        self.fontHeading = pygame.font.Font(os.path.join('data', 'saxmono.ttf'), 42)
        self.fontNormal = pygame.font.Font(os.path.join('data', 'saxmono.ttf'), 24)
        self.speedButtons = [pygame.image.load(os.path.join('data', 'slow.png')).convert(), pygame.image.load(os.path.join('data', 'normal.png')).convert(), pygame.image.load(os.path.join('data', 'fast.png')).convert()]
        self.paddleSizeButtons = [pygame.image.load(os.path.join('data', 'small.png')).convert(), pygame.image.load(os.path.join('data', 'normal.png')).convert(), pygame.image.load(os.path.join('data', 'big.png')).convert()]
        self.backButton = pygame.image.load(os.path.join('data', 'arrow.png')).convert()
        self.resetButton = pygame.image.load(os.path.join('data', 'reset.png')).convert()
        self.yesButton = pygame.image.load(os.path.join('data', 'yes.png')).convert()
        self.noButton = pygame.image.load(os.path.join('data', 'no.png')).convert()
        self.currentHeights = [player_1.heightScale, player_2.heightScale]
        self.currentColors = [self.ball.color, self.player_1.color, self.player_2.color]
        self.currentVel = [ball.maxVelX, ball.maxVelY]

    def draw(self):
        settings_logo = self.fontLogo.render("Settings", 0, WHITE)
        headings = [self.fontHeading.render("Ball", 0, WHITE), self.fontHeading.render("Player 1", 0, WHITE), self.fontHeading.render("Player 2", 0, WHITE)]
        color_label = self.fontNormal.render("Color", 0, WHITE)
        height_label = self.fontNormal.render("Height", 0, WHITE)
        speed_label = self.fontNormal.render("Max Speed", 0, WHITE)
        reset_label = self.fontHeading.render("Reset the score?", 0, WHITE)
        colors = [WHITE, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        buttons = [self.speedButtons, self.paddleSizeButtons, self.paddleSizeButtons]
        heights = [.15, .25, .35]
        velocities = [[2, 2], [4, 4], [6, 6]]

        while 1:
            # Set FPS to 60
            self.clock.tick_busy_loop(60)

            # background
            self.screen.fill(BLACK)

            # draw settings logo
            self.screen.blit(settings_logo, (self.screen.get_width() / 2 - settings_logo.get_width() / 2, self.screen.get_height() / 20))

            # draw ballText and playerText
            for i in xrange(len(headings)):
                x = (i + 1) * self.screen.get_width() / (len(headings) + 1) - headings[i].get_width() / 2
                self.screen.blit(headings[i], (x, self.screen.get_height() / 5))
                self.screen.blit(color_label, (x, self.screen.get_height() / 5 + headings[i].get_height() + 10))
                pygame.draw.rect(self.screen, self.currentColors[i], (x, self.screen.get_height() / 5 + headings[i].get_height() + 10 + color_label.get_height() + 10, 20, 20))

            self.screen.blit(speed_label, (self.screen.get_width() / (len(headings) + 1) - headings[0].get_width() / 2, self.screen.get_height() / 5 + headings[0].get_height() + 10 + color_label.get_height() + 10 + 20 + 20))

            for i in xrange(2):
                self.screen.blit(height_label, ((2 + i) * self.screen.get_width() / (len(headings) + 1) - headings[i + 1].get_width() / 2, self.screen.get_height() / 5 + headings[0].get_height() + 10 + color_label.get_height() + 10 + 20 + 20))

            self.screen.blit(buttons[0][(self.currentVel[0] // 2) - 1], (self.screen.get_width() / (len(headings) + 1) - headings[0].get_width() / 2, self.screen.get_height() / 5 + headings[0].get_height() + 10 + color_label.get_height() + 10 + 20 + 20 + height_label.get_height() + 10))
            self.screen.blit(buttons[1][heights.index(self.currentHeights[0])], (2 * self.screen.get_width() / (len(headings) + 1) - headings[1].get_width() / 2, self.screen.get_height() / 5 + headings[1].get_height() + 10 + color_label.get_height() + 10 + 20 + 20 + height_label.get_height() + 10))
            self.screen.blit(buttons[2][heights.index(self.currentHeights[1])], (3 * self.screen.get_width() / (len(headings) + 1) - headings[2].get_width() / 2, self.screen.get_height() / 5 + headings[2].get_height() + 10 + color_label.get_height() + 10 + 20 + 20 + height_label.get_height() + 10))

            self.screen.blit(self.backButton, (0, 0))
            self.screen.blit(self.resetButton, (0, self.screen.get_height() - self.resetButton.get_height()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.screen.get_height() / 5 + headings[0].get_height() + 10 + color_label.get_height() + 10 <= pos[1] <= self.screen.get_height() / 5 + headings[0].get_height() + 10 + color_label.get_height() + 10 + 20:
                        if self.screen.get_width() / (len(headings) + 1) - headings[0].get_width() / 2 <= pos[0] <= (self.screen.get_width() / (len(headings) + 1) - headings[0].get_width() / 2) + 20:
                            self.currentColors[0] = colors[(colors.index(self.currentColors[0]) + 1) % len(colors)]
                            self.ball.change_color(self.currentColors[0])
                        if 2 * self.screen.get_width() / (len(headings) + 1) - headings[1].get_width() / 2 <= pos[0] <= (2 * self.screen.get_width() / (len(headings) + 1) - headings[1].get_width() / 2) + 20:
                            self.currentColors[1] = colors[(colors.index(self.currentColors[1]) + 1) % len(colors)]
                            self.player_1.change_color(self.currentColors[1])
                        if 3 * self.screen.get_width() / (len(headings) + 1) - headings[2].get_width() / 2 <= pos[0] <= (3 * self.screen.get_width() / (len(headings) + 1) - headings[2].get_width() / 2) + 20:
                            self.currentColors[2] = colors[(colors.index(self.currentColors[2]) + 1) % len(colors)]
                            self.player_2.change_color(self.currentColors[2])
                    if self.screen.get_height() / 5 + headings[0].get_height() + 10 + color_label.get_height() + 10 + 20 + 20 + height_label.get_height() + 10 <= pos[1] <= self.screen.get_height() / 5 + headings[0].get_height() + 10 + color_label.get_height() + 10 + 20 + 20 + height_label.get_height() + 10 + self.paddleSizeButtons[0].get_height():
                        if self.screen.get_width() / (len(headings) + 1) - headings[0].get_width() / 2 <= pos[0] <= (self.screen.get_width() / (len(headings) + 1) - headings[0].get_width() / 2) + self.paddleSizeButtons[0].get_width():
                            self.currentVel = velocities[(velocities.index(self.currentVel) + 1) % len(velocities)]
                            self.ball.change_vel(self.currentVel)
                        if 2 * self.screen.get_width() / (len(headings) + 1) - headings[1].get_width() / 2 <= pos[0] <= (2 * self.screen.get_width() / (len(headings) + 1) - headings[1].get_width() / 2) + self.paddleSizeButtons[0].get_width():
                            self.currentHeights[0] = self.player_1.change_height(heights[(heights.index(self.currentHeights[0]) + 1) % len(heights)])
                        if 3 * self.screen.get_width() / (len(headings) + 1) - headings[2].get_width() / 2 <= pos[0] <= (3 * self.screen.get_width() / (len(headings) + 1) - headings[2].get_width() / 2) + self.paddleSizeButtons[0].get_width():
                            self.currentHeights[1] = self.player_2.change_height(heights[(heights.index(self.currentHeights[1]) + 1) % len(heights)])
                    if pos[0] <= self.backButton.get_width() and pos[1] <= self.backButton.get_height():
                        return
                    if pos[0] <= self.resetButton.get_width() and self.screen.get_height() - self.resetButton.get_height() <= pos[1] <= self.screen.get_height():
                        negative = False
                        while 1:
                            pygame.draw.rect(self.screen, WHITE, (self.screen.get_width() / 4 - 5, self.screen.get_height() / 4 - 5, self.screen.get_width() / 2 + 10, self.screen.get_height() / 2 + 10))
                            pygame.draw.rect(self.screen, BLACK, (self.screen.get_width() / 4, self.screen.get_height() / 4, self.screen.get_width() / 2, self.screen.get_height() / 2))
                            self.screen.blit(reset_label, (self.screen.get_width() / 2 - reset_label.get_width() / 2, self.screen.get_height() / 4 + 10))
                            self.screen.blit(self.yesButton, (self.screen.get_width() / 2 - self.yesButton.get_width() - 5, self.screen.get_height() / 2 - self.yesButton.get_height() / 2))
                            self.screen.blit(self.noButton, (self.screen.get_width() / 2 + 5, self.screen.get_height() / 2 - self.noButton.get_height() / 2))

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit()
                                if event.type == pygame.MOUSEBUTTONUP:
                                    pos = pygame.mouse.get_pos()
                                    if self.screen.get_height() / 2 - self.yesButton.get_height() / 2 <= pos[1] <= self.screen.get_height() / 2 + self.yesButton.get_height() / 2:
                                        if self.screen.get_width() / 2 - self.yesButton.get_width() - 5 <= pos[0] <= self.screen.get_width() / 2 - 5:
                                            return "Reset"
                                        elif self.screen.get_width() / 2 + 5 <= pos[0] <= self.screen.get_width() / 2 + 5 + self.noButton.get_width():
                                            negative = True
                                            break

                            if negative:
                                break

                            pygame.display.update((self.screen.get_width() / 4 - 5, self.screen.get_height() / 4 - 5, self.screen.get_width() / 2 + 10, self.screen.get_height() / 2 + 10))

            pygame.display.flip()