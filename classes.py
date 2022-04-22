"""Core game classes go here."""
import pygame
from gamelib import LEVEL_OBJECTS

class Dynamite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.start_burning = True
        self.sprites = [] # all frames
        for x in range(12 + 1): # all frames
            self.sprites.append(pygame.transform.scale(pygame.image.load(LEVEL_OBJECTS[22]["image"]), (LEVEL_OBJECTS[22]["size"])))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, speed):
        if self.start_burning == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.start_burning = False

        self.image = self.sprites[int(self.current_sprite)]