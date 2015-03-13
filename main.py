import objects, pygame

pygame.init()
pygame.font.init()
pygame.key.set_repeat(0, 1)

screen = pygame.display.set_mode((640, 360))

mainMenu = objects.MainMenu(screen)
game = objects.Game(screen)


mainMenu.draw()
game.newGame()