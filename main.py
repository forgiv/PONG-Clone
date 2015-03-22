import objects
import pygame

pygame.init()
pygame.font.init()
pygame.key.set_repeat(0, 1)

screen = pygame.display.set_mode((1280, 720))

mainMenu = objects.MainMenu(screen)
game = objects.Game(screen)
settingsMenu = objects.SettingsMenu(screen, game.ball, game.player_1, game.player_2)

score = []

while 1:
    if mainMenu.draw() == "Settings":
        settingsMenu.draw()
    else:
        while 1:
            if len(score) == 0:
                score = game.new_game()
            else:
                score = game.new_game(score)
            if settingsMenu.draw() == "Reset":
                score = [0, 0]