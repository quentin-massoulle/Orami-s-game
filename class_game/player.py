from typing import Any
import pygame
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("player_creature_asset/Player.png").convert_alpha()  # Chargement de l'image avec transparence
        self.image = self.get_image(0, 0)  # Récupérer la première image du sprite

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
        self.position = [x, y]  # Assurez-vous que c'est une liste
        self.old_position = self.position.copy()  # Copier la liste
        self.vitesse = 2

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position.copy()  # Copier pour éviter les modifications involontaires
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def save_location(self):
        print("Type of self.position:", type(self.position))  # Affiche le type de self.position
        print("Type of self.old_position:", type(self.old_position))  # Affiche le type de self.old_position 
        self.old_position = self.position.copy()  # Copier la liste

    def move(self, x, y):
        # Modifier la position du joueur
        self.position[0] += x
        self.position[1] += y

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

    def get_image(self, x, y):
        # Découpe l'image du sprite sheet
        image = pygame.Surface([32, 32], pygame.SRCALPHA)  # Surface avec transparence
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
