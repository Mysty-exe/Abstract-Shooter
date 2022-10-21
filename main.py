import pygame
import sys

pygame.init()
width, height = 800, 800
fps = 60
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Top Down Shooter')
clock = pygame.time.Clock()
x, y = 150, 150
direction = ''
speed = 3

while True:

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    pos = pygame.mouse.get_pos()

    if keys[pygame.K_w] and direction != 'down':
        direction = 'up'
        y -= speed
    if keys[pygame.K_s] and direction != 'up':
        direction = 'down'
        y += speed
    if keys[pygame.K_a] and direction != 'right':
        direction = 'left'
        x -= speed
    if keys[pygame.K_d] and direction != 'left':
        direction = 'right'
        x += speed

    clock.tick(fps)
    pygame.display.update()
