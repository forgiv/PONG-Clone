import sys, pygame, objects

pygame.init()

size = width, height = 640, 320
screen = pygame.display.set_mode(size)
black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
ball = objects.Ball(screen)

while 1:
    clock.tick_busy_loop(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    ball.display()
    ball.update()

    pygame.display.flip()