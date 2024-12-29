import pygame

pygame.init()

width = 1000
height = 600

pygame.display.set_caption("Test")
screen = pygame.display.set_mode((width, height))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0,0,0)) # black
    pygame.display.flip()