import objects, pygame

pygame.init()
pygame.font.init()
pygame.key.set_repeat(0, 1)

screen = pygame.display.set_mode((640, 360))

mainMenu = objects.MainMenu(screen)
game = objects.Game(screen)
settingsMenu = objects.SettingsMenu(screen, game.ball, game.player_1, game.player_2)

settingsMenu.draw()
#mainMenu.draw()
#game.newGame()