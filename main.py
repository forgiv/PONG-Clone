import sys, pygame, objects

pygame.init()
pygame.key.set_repeat(0, 1)

size = width, height = 640, 320
screen = pygame.display.set_mode(size)
black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
ball = objects.Ball(screen)
player_1 = objects.Paddle(screen, 'left')
player_2 = objects.Paddle(screen, 'right')

while 1:
    clock.tick_busy_loop(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    pygame.draw.line(screen, white, (width / 2, 0), (width / 2, height))

    if pygame.key.get_pressed()[pygame.K_UP] != 0:
        player_2.moveUp()
    if pygame.key.get_pressed()[pygame.K_DOWN] != 0:
        player_2.moveDown()
    if pygame.key.get_pressed()[pygame.K_w] != 0:
        player_1.moveUp()
    if pygame.key.get_pressed()[pygame.K_s] != 0:
        player_1.moveDown()

    player_1.display()
    player_2.display()

    #ball.update()
    #ball.display()

    pygame.display.flip()