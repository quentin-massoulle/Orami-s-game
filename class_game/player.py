import pygame
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Correction de l'appel à super()
        self.sprite_sheet = pygame.image.load("player_creature_asset/Player.png").convert_alpha()  # Chargement de l'image avec transparence
        self.image = self.get_image(0, 0)  # Récupérer la première image du sprite
        self.rect = self.image.get_rect()  # Récupérer le rectangle de l'image

    def get_image(self, x, y):
        # Découpe l'image du sprite sheet
        image = pygame.Surface([32, 32], pygame.SRCALPHA)  # Support avec transparence
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
