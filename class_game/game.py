import pygame
import pytmx
import pyscroll
pygame.init()
class Game:
    def __init__(self):
        # Initialisation de la fenêtre de jeu
        self.screen = pygame.display.set_mode((960, 800))
        pygame.display.set_caption("Orami Adventure")

        # Chargement de la carte
        tmx_data = pytmx.util_pygame.load_pygame('map/map1.tmx')  # Assurez-vous que le chemin est correct
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    def run(self):
        running = True
        while running:
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Dessiner la carte
            self.group.draw(self.screen)
            pygame.display.flip()  # Rafraîchir l'écran avec flip()

        pygame.quit()