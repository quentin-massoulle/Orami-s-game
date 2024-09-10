import pygame 
pygame.init()

class game :
    def __init__(self) :
        pygame.display.set_mode((1200,800))
        pygame.display.set_caption("orami adventure")

    def run(self):
        runing = True

        while runing :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runing = False
        pygame.quit()