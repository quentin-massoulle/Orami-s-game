import pygame
import pytmx
import pyscroll
import time
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
        self.walls = []

        # Récupérer les objets de collision de la carte
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Gérer le joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)  # Instancier le joueur
        self.collition=False
        self.running = True
        self.playing = False

        # gere les colition

        self.last_collision_time = 0
        self.collision_cooldown = 0.4
        # Dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)
    
    # Vérifier les collisions avec les murs
    def collide_with_walls(self, rect):
        for wall in self.walls:
            if rect.colliderect(wall):
                return True
        return False
    
    # Récupérer les touches appuyées et déplacer le joueur
    def handle_input(self):
        # Vérifier si le délai de collision est écoulé
        current_time = time.time()
        if (current_time - self.last_collision_time) >= self.collision_cooldown:
            self.collision = False

        if not self.collision:
            pressed = pygame.key.get_pressed()
            vx, vy = 0, 0

            if pressed[pygame.K_LSHIFT]:
                self.player.vitesse = 3.5
            else:
                self.player.vitesse = 2

            if pressed[pygame.K_UP] or pressed[pygame.K_z]:
                self.player.changeAnimation("up")
                vy = -self.player.vitesse
            if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                self.player.changeAnimation("down")
                vy = self.player.vitesse
            if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
                self.player.changeAnimation("left")
                vx = -self.player.vitesse
            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                self.player.changeAnimation("right")
                vx = self.player.vitesse
            if pressed[pygame.K_ESCAPE]:
                self.running = False
                self.playing = False
            # Déplacement en deux étapes (horizontal puis vertical)
            self.move_player(vx,vy)

            # Gérer les entrées de la manette si elle est connectée
            if self.joystick is not None:
                axis_x = self.joystick.get_axis(0)  # Axe gauche/droite (X)
                axis_y = self.joystick.get_axis(1)  # Axe haut/bas (Y)
                if self.joystick.get_button(0):
                    self.player.vitesse = 3.5
                else:
                    self.player.vitesse = 2
                threshold = 0.2  # Seuil pour ignorer les petites déviations

                # Déplacement horizontal
                if abs(axis_x) > threshold:
                    vx = axis_x * self.player.vitesse
                    if axis_x < 0:
                        self.player.changeAnimation("left")
                    else:
                        self.player.changeAnimation("right")
                
                # Déplacement vertical
                if abs(axis_y) > threshold:
                    vy = axis_y * self.player.vitesse
                    if axis_y < 0:
                        self.player.changeAnimation("up")
                    else:
                        self.player.changeAnimation("down")

                self.move_player(vx,vy)
        else:
            # Attendre que le délai de collision soit écoulé avant de permettre le mouvement
            if (current_time - self.last_collision_time) >= self.collision_cooldown:
                self.collision = False

    def move_player(self,x,y):
       self.player.position=(self.player.position[0]+x,self.player.position[1]+y)

    def update(self):
        # Placeholder pour la logique de mise à jour si nécessaire
        pass

    def mannetteConect(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None

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
        self.mannetteConect()

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
                        self.running = False

                pygame.display.flip()  # Rafraîchir l'écran avec flip()
                clock.tick(60)  # Limiter le jeu à 60 FPS

        pygame.quit()
