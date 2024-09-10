import pygame
from class_game.game import Game # Importer la classe game depuis le dossier game_class

if __name__ == '__main__':
    pygame.init()
    game_instance = Game()  # Instancier la classe Game
    game_instance.run()      # Lancer la boucle du jeu