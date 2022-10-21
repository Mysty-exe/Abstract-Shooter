import pygame
import sys

pygame.init()
width, height = 800, 800
fps = 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Top Down Shooter')
clock = pygame.time.Clock()

while True:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(fps)
    pygame.display.update()
