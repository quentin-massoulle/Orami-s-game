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
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)  # Instancier le joueur

        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)
    
    # Récupérer les touches appuyées et déplacer le joueur
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]  or pressed[pygame.K_z]:
            self.player.mouve(0,- self.player.vitesse)
        if pressed[pygame.K_DOWN]  or pressed[pygame.K_s]:
            self.player.mouve(0,self.player.vitesse)
        if pressed[pygame.K_LEFT]  or pressed[pygame.K_q]:
            self.player.mouve(-self.player.vitesse,0)
        if pressed[pygame.K_RIGHT]  or pressed[pygame.K_d]:
            self.player.mouve(self.player.vitesse,0)

    def run(self):
        clock = pygame.time.Clock()  # Pour gérer le taux de rafraîchissement
        running = True

        while running:
            # Dessiner la carte et les sprites
            self.handle_input()
            self.group.update()
            self.group.center(self.player.rect.center)  # Centrer la caméra sur le joueur
            self.group.draw(self.screen)
            
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()  # Rafraîchir l'écran avec flip()
            clock.tick(60)  # Limiter le jeu à 60 FPS

        pygame.quit()
