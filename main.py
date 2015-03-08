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

    # Movement
    player_2.moveUp(pygame.key.get_pressed()[pygame.K_UP])
    player_2.moveDown(pygame.key.get_pressed()[pygame.K_DOWN])

    player_1.moveUp(pygame.key.get_pressed()[pygame.K_w])
    player_1.moveDown(pygame.key.get_pressed()[pygame.K_s])

    # Display Paddles
    player_1.display()
    player_2.display()

    # Y Collisions
    if ball.posY + ball.radius >= height:
        ball.collideY()
    elif ball.posY - ball.radius <= 0:
        ball.collideY()

    # X Collisions
    if ball.posX + ball.radius >= width - player_2.width:
        # Right gutter check
        if ball.posX + ball.radius >= width:
            ball.reset()
        # In-facing side of right paddle
        if ball.posY >= player_2.posY and ball.posY <= player_2.posY + player_2.height:
            ball.setVel(-(ball.vel[0] + player_2.vel[0]), ball.vel[1] + player_2.vel[1])
        elif ball.posY - ball.radius <= player_2.posY + player_2.height:
            ball.setVel(ball.vel[0] + player_2.vel[0], ball.vel[1] + player_2.vel[1])
        elif ball.posY + ball.radius >= player_2.posY:
            ball.setVel(ball.vel[0] + player_2.vel[0], ball.vel[1] + player_2.vel[1])
    elif ball.posX - ball.radius <= player_1.width:
        # Right gutter check
        if ball.posX - ball.radius <= 0:
            ball.reset()
        # In-facing side of left paddle
        if ball.posY >= player_1.posY and ball.posY <= player_1.posY + player_1.height:
            ball.setVel(-(ball.vel[0] + player_2.vel[0]), ball.vel[1] + player_1.vel[1])

    ball.update()
    ball.display()

    pygame.display.flip()