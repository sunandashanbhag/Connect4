import pygame
import random
pygame.init()

size = (320, 280)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 but Worse")

done = False
clock = pygame.time.Clock()

pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            break
        if event.type==pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())