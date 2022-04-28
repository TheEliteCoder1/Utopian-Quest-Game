"""Core game classes go here."""
import pygame, math
from gamelib import LEVEL_OBJECTS


class Dynamite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.start_burning = True
        self.sprites = []  # all frames
        for x in range(12 + 1):  # all frames
            self.sprites.append(
                pygame.transform.scale(
                    pygame.image.load(LEVEL_OBJECTS[20]["image"]),
                    (LEVEL_OBJECTS[20]["size"])))
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

class Glurdle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(LEVEL_OBJECTS[21]["image"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.deltaX, self.deltaY = 0, 0
        self.vel_y = 0

    def update(self, screen_scroll, world, grav):
        self.deltaX = (self.move_direction + screen_scroll)
        self.rect.x += self.deltaX
        self.rect.y += self.deltaY
        self.move_counter += 1
        if abs(self.move_counter) > 45:
            self.move_direction *= -1
            self.move_counter *= -1

        #apply gravity
        self.vel_y += grav * 10
        if self.vel_y > 6:
            self.vel_y
        self.deltaY += self.vel_y

        for tile in world.objects_list:
            if tile[2] == 'Block':
                #check for collision in the y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + self.deltaY,
                                       35, 35):
                    if self.vel_y < 0:
                        self.vel_y = 0
                        self.deltaY = tile[1].bottom - self.rect.top
                        #check if above the ground, i.e. falling
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        self.deltaY = tile[1].top - self.rect.bottom


class PlatformRight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(LEVEL_OBJECTS[23]["image"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.deltaX, self.deltaY = 0, 0

    def update(self, screen_scroll):
        self.deltaX = (self.move_direction + screen_scroll)
        self.rect.x += self.deltaX
        self.move_counter += 1
        if abs(self.move_counter) > 45:
            self.move_direction *= -1
            self.move_counter *= -1
        

class PlatformUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(LEVEL_OBJECTS[22]["image"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.deltaX, self.deltaY = 0, 0

    def update(self, screen_scroll):
        self.deltaY = (self.move_direction)
        self.rect.y += self.deltaY
        self.rect.x += screen_scroll
        self.move_counter += 1
        if abs(self.move_counter) > 45:
            self.move_direction *= -1
            self.move_counter *= -1
        
    
