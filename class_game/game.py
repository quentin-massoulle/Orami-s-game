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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Police d'écriture
font = pygame.font.SysFont('Arial', 30)

# Fonction pour afficher du texte au centre de l'écran

class Game:
    def __init__(self):
        # Initialisation de la fenêtre de jeu  
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Orami Adventure")
        pygame.mouse.set_visible(False)
        self.width, self.height = self.screen.get_size()
        # Chargement de la carte
        tmx_data = pytmx.util_pygame.load_pygame('map/map1.tmx')  # Assurez-vous que le chemin est correct
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3
        self.walls = []
        self.map_accutuelle="map1"
        self.barreVie_X=200
        self.barreVie_y=20 
        self.emplacementBarre_X = 10
        self.emplacementBarre_Y = 10
        # Récupérer les objets de collision de la carte
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.Map= []

        for obj in tmx_data.objects:
            if obj.type == "Map":
                 self.Map.append({
                    'rect': pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                    'name': obj.name,
                })
        
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
            self.playing = False
        # Déplacement en deux étapes (horizontal puis vertical)
        self.player.move(vx,vy)

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

            self.player.move(vx,vy)

    
         
    #verifie er connecte si une mannette est connecter 
    def mannetteConect(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None
    #creation du menue de demarage 
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


    def loading_screen(self,screen):
        loading = True
        progress = 0
        while loading:
            screen.fill(BLACK)
            
            # Texte de chargement

            # Appeler draw_text avec les coordonnées centrées
            self.draw_text("Chargement en cours...", 60, WHITE, screen.get_width() // 2, 200)
            
            # Barre de progression (rectangles)
            pygame.draw.rect(screen, RED, [600, self.height // 2, 500, 30], 2)  # Bordure
            pygame.draw.rect(screen, GREEN, [600, self.height // 2, 5 * progress, 30])  # Barre de remplissage

            pygame.display.flip()

            # Simuler le chargement
            time.sleep(0.01)  # On peut ajuster la durée ici
            progress += 1
            
            if progress >= 100:
                loading = False

            # Gestion des événements pour fermer la fenêtre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

    def changementMap(self, map):
        # Vider les anciens objets (sprites, murs, etc.)
        self.group.empty()  # Vider le groupe de sprites
        self.walls.clear()  # Vider les murs de collision
        self.Map.clear()  # Vider les objets "Map"
        self.screen.fill((0, 0, 0))  # Remplir l'écran de noir pour tout effacer
        self.loading_screen(self.screen)
        # Effacer l'écran pour éviter de garder des artefacts visuels
        pygame.display.flip()  # Mettre à jour l'affichage
            
        # Chargement de la nouvelle carte avec pytmx et pyscroll
        tmx_data = pytmx.util_pygame.load_pygame("map/" + map + ".tmx")  # Chargement du fichier .tmx
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3  # Zoomer sur la carte
        

        
        for obj in tmx_data.objects:
            if obj.type == "Map":
                    self.Map.append({
                    'rect': pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                    'name': obj.name,
                })
                    
        
        # Récupérer les objets de collision de la carte
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))  # Ajouter les rectangles de collision
            
        # Récupérer la position du joueur sur la nouvelle carte
        player_position = tmx_data.get_object_by_name("player_"+self.map_accutuelle)  # Obtenir l'objet nommé "player" dans la carte .tmx
        self.map_accutuelle=map
     
        self.player.position[0]=player_position.x
        self.player.position[1]=player_position.y

        self.player.old_position=self.player.position
        # Mettre à jour la carte actuelle avec le nouveau rendu
        self.map_layer = map_layer
        
        # Ne recréez pas `self.group` ici. Ajoutez juste le joueur au groupe existant
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)  # Ajouter le joueur au groupe de sprites


    def dessiner_barre_vie(self, player):
        proportion_vie = player.PV / player.VieMax
        largeur_actuelle = int(proportion_vie * self.barreVie_X)
        # Dessine une barre rouge pour le fond (vie perdue)
        pygame.draw.rect(self.screen, RED, (self.emplacementBarre_X, self.emplacementBarre_Y, self.barreVie_X, self.barreVie_y))
        # Dessine une barre verte par-dessus (vie restante)
        pygame.draw.rect(self.screen, GREEN,(self.emplacementBarre_X, self.emplacementBarre_Y, largeur_actuelle, self.barreVie_y))
    def update(self):
       
       self.group.update()
       for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) >-1:
               sprite.move_back()
            for obj in self.Map:
                if sprite.feet.colliderect(obj['rect']):  # Si collision avec un objet de la carte
                    print(obj['name'] )
                    NewMap = obj['name'] # Chargement d'une nouvelle carte en fonction de l'objet
                    self.changementMap(NewMap)
            break 
       
        

    #mise en route du jeux 
    def run(self):
        clock = pygame.time.Clock()  # Pour gérer le taux de rafraîchissement
        self.mannetteConect()

        while self.running:
            if not self.playing:
                self.display_menu()

            while self.playing:
                self.player.save_location()
                self.handle_input()
                self.update()
                self.group.center(self.player.rect.center)  # Centrer la caméra sur le joueur

                # Dessiner la carte et les sprites
                self.group.draw(self.screen)

                # Dessiner la barre de vie par-dessus tous les autres éléments
                self.dessiner_barre_vie(self.player)

                # Gérer les événements
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                pygame.display.flip()  # Rafraîchir l'écran avec flip()
                clock.tick(60)  # Limiter le jeu à 60 FPS

        pygame.quit()

