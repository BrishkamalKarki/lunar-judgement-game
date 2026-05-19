import pygame
import arena

class Game:
    pygame.init()
    pygame.mixer.init()
    arena.Arena(1200, 600)
    pygame.quit()

if __name__ == "__main__": 
    Game()
