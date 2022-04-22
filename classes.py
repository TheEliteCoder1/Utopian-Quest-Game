"""Core game classes go here."""
import pygame

class Dynamite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.start_burning = False
        self.sprites = [] # all frames
        for x in range(12 + 1): # all frames
            self.sprites.append(pygame.image.load(f'assets/animations/dynamite/dynamite-{x}.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

    def burn(self):
        self.start_burning = True


    def update(self, speed):
        if self.start_burning == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.attack_animation = False

        self.image = self.sprites[int(self.current_sprite)]