import pygame 
pygame.init()

pygame.display.set_mode((1200,800))
pygame.display.set_caption("orami adventure")


runing = True

while runing :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
pygame.quit()