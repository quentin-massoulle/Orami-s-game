import pygame
import pytmx
import pyscroll
from class_game.player import Player  # Importer la classe Player depuis le dossier class_game

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        # Initialisation de la fenêtre de jeu  
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Orami Adventure")
        pygame.mouse.set_visible(False)

        # Chargement de la carte
        tmx_data = pytmx.util_pygame.load_pygame('map/map1.tmx')  # Assurez-vous que le chemin est correct
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3

        # Gérer le joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)  # Instancier le joueur
        self.running = True
        self.playing = False
        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)
    
    # Récupérer les touches appuyées et déplacer le joueur
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LSHIFT]:
            self.player.vitesse = 3.5
        else:
            self.player.vitesse = 2
        if pressed[pygame.K_UP]  or pressed[pygame.K_z]:
            self.player.move(0, -self.player.vitesse)
        if pressed[pygame.K_DOWN]  or pressed[pygame.K_s]:
            self.player.move(0, self.player.vitesse)
        if pressed[pygame.K_LEFT]  or pressed[pygame.K_q]:
            self.player.move(-self.player.vitesse, 0)
        if pressed[pygame.K_RIGHT]  or pressed[pygame.K_d]:
            self.player.move(self.player.vitesse, 0)
        if pressed[pygame.K_ESCAPE]:
            self.running = True
            self.playing = False


    def mannetteConect(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Manette connectée : {self.joystick.get_name()}")
        else:
            self.joystick = None
            print("Pas de manette connectée")

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def display_menu(self):
        """Affiche le menu principal"""
        menu_open = True

        while menu_open:
            self.screen.fill(BLACK)  # Fond du menu
            self.draw_text("ORAMI ADVENTURE", 60, WHITE, self.screen.get_width() // 2, 200)
            self.draw_text("Appuyez sur ENTER pour Commencer", 40, WHITE, self.screen.get_width() // 2, 400)
            self.draw_text("Appuyez sur ESC pour Quitter", 40, WHITE, self.screen.get_width() // 2, 500)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    menu_open = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Touche Enter pour commencer
                        self.playing = True
                        menu_open = False
                    elif event.key == pygame.K_ESCAPE:  # Touche Esc pour quitter
                        self.running = False
                        menu_open = False

    def draw_text(self, text, size, color, x, y):
        """Méthode utilitaire pour afficher du texte"""
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        clock = pygame.time.Clock()  # Pour gérer le taux de rafraîchissement
        running = True

        while self.running:
            if not self.playing:
                self.display_menu()

            while self.playing:
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
