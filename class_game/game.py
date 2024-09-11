import pygame
import pytmx
import pyscroll
from class_game.player import Player  # Importer la classe Player depuis le dossier class_game

# Initialisation de Pygame
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
        map_layer.zoom = 3

        # Gérer le joueur
        self.player = Player()  # Instancier le joueur

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)

    def run(self):
        running = True
        while running:
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Dessiner la carte et les sprites
            self.group.center(self.player.rect.center)  # Centrer la caméra sur le joueur
            self.group.update()
            self.group.draw(self.screen)

            pygame.display.flip()  # Rafraîchir l'écran avec flip()

        pygame.quit()