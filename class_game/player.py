from typing import Any
import pygame
pygame.init()

class Player(pygame.sprite.Sprite):

    
    def __init__(self, x, y):#  inisialise le joueur avec cordonner x et y pour le placement sur la map au lancement 
        super().__init__()
        self.sprite_sheet = pygame.image.load("player_creature_asset/Player.png").convert_alpha()  # Chargement de l'image avec transparence
        self.image = self.get_image(0, 0)  # Récupérer la première image du sprite
        self.PV=100
        self.VieMax=100

        # Dictionnaire contenant les animations pour chaque direction
        self.images = {
            "down": [self.get_image(0, 0), self.get_image(32, 0), self.get_image(64, 0)],
            "left": [self.get_image(0, 32), self.get_image(32, 32), self.get_image(64, 32)],
            "right": [self.get_image(0, 64), self.get_image(32, 64), self.get_image(64, 64)],
            "up": [self.get_image(0, 96), self.get_image(32, 96), self.get_image(64, 96)]
        }
        self.last_update = 0
        self.animation_speed = 100
        self.rect = self.image.get_rect()  # Récupérer le rectangle de l'image
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.animation_index = 0
        self.position = [x, y]  # position du joueur 
        self.old_position = self.position.copy()  # ancienne position du joueur 
        self.vitesse = 2 #vitesse du joueur 

    #update du deplacement du sprite joueur 
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    #retour en arrierre sur le deplacement du joueur  
    def move_back(self):
        self.position = self.old_position.copy()  # Copier pour éviter les modifications involontaires
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    #sauvegarde la possition du joeur si retour en arriere neccessaire lors de collition
    def save_location(self):
        self.old_position = self.position.copy()  # Copier la liste

    #deplacemen du joueur 
    def move(self, x, y):
        # Modifier la position du joueur
        self.position[0] += x
        self.position[1] += y


    #change les animation du joeur en fonction de la direction du deplacement 
    def changeAnimation(self, direction):
        # Obtenir le temps actuel
        current_time = pygame.time.get_ticks()

        # Vérifier si suffisamment de temps s'est écoulé depuis la dernière animation
        if current_time - self.last_update > self.animation_speed:
            # Mettre à jour l'heure de la dernière animation
            self.last_update = current_time
            
            # Obtenir l'image correcte en fonction de la direction et de l'animation courante
            self.image = self.images[direction][self.animation_index]
            
            # Incrémenter l'index de l'animation
            self.animation_index += 1
            
            # Remettre à zéro l'animation si elle atteint la fin de la liste
            if self.animation_index >= len(self.images[direction]):
                self.animation_index = 0
    #revoie l'image du joueur 
    def get_image(self, x, y):
        # Découpe l'image du sprite sheet
        image = pygame.Surface([32, 32], pygame.SRCALPHA)  # Surface avec transparence
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
