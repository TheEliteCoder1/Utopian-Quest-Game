"""Core game classes go here."""
import pygame, math
from gamelib import LEVEL_OBJECTS

class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(pygame.image.load(LEVEL_OBJECTS[20]["image"]), LEVEL_OBJECTS[20]["size"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.deltaX, self.deltaY = 0, 0

    def update(self, screen_scroll, screen_scroll_y):
        self.deltaY = (self.move_direction) + screen_scroll_y
        self.rect.y += self.deltaY
        self.rect.x += screen_scroll
        self.move_counter += 0.9
        if abs(self.move_counter) > 5:
            self.move_direction *= -1
            self.move_counter *= -1

class Currency(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.currency_spinning_angle = 0

    def update(self, screen, screen_scroll, screen_scroll_y):
        self.currency_spinning_angle += 5
        self.rect.x += screen_scroll
        self.rect.y += screen_scroll_y
        new_width = round(math.sin(math.radians(self.currency_spinning_angle)) * self.rect.width)
        rot_currency = self.image if new_width >= 0 else pygame.transform.flip(
            self.image, True, False)
        rot_currency = pygame.transform.scale(
            rot_currency, (abs(new_width), self.rect.height))
        screen.blit(rot_currency, rot_currency.get_rect(center=(self.rect.topleft[0] + (self.rect.width/4), self.rect.topleft[1])))


class Glurdle(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, duration_factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(pygame.image.load(LEVEL_OBJECTS[21]["image"]), LEVEL_OBJECTS[21]["size"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.speed = speed
        self.duration_factor = duration_factor
        self.deltaX, self.deltaY = 0, 0
        self.vel_y = 0

    def update(self, screen_scroll, screen_scroll_y, world):
        self.deltaX = ((self.move_direction)*self.speed) + screen_scroll
        self.rect.x += self.deltaX
        self.rect.y += self.deltaY + (screen_scroll_y)
        self.move_counter += 1
        if abs(self.move_counter) > self.duration_factor:
            self.move_direction *= -1
            self.move_counter *= -1

        #apply gravity
        self.vel_y += 0.2 * 20
        if self.vel_y > 6:
            self.vel_y
        self.deltaY += self.vel_y

        #check for collision
        for tile in world.objects_list:
            if tile[2] == 'Block':
                # #check collision in the x direction
                # if tile[1].colliderect(self.rect.x + self.deltaX, self.rect.y,
                #                        self.rect.width, self.rect.height):
                #     self.deltaX = 0
                #check for collision in the y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + self.deltaY,
                                       self.rect.width, self.rect.height):
                    #check if below the ground, i.e. jumping
                    if self.vel_y < 0:
                        self.vel_y = 0
                        self.deltaY = tile[1].bottom - self.rect.top
                    #check if above the ground, i.e. falling
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        self.deltaY = tile[1].top - self.rect.bottom


class PlatformRight(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, duration_factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(pygame.image.load(LEVEL_OBJECTS[23]["image"]), LEVEL_OBJECTS[23]["size"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.speed = speed
        self.duration_factor = duration_factor
        self.deltaX, self.deltaY = 0, 0

    def update(self, screen_scroll, screen_scroll_y):
        self.deltaX = ((self.move_direction)*self.speed) + screen_scroll
        self.rect.x += self.deltaX
        self.rect.y += self.deltaY + screen_scroll_y
        self.move_counter += 1
        if abs(self.move_counter) > self.duration_factor:
            self.move_direction *= -1
            self.move_counter *= -1

class PlatformLeft(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, duration_factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(pygame.image.load(LEVEL_OBJECTS[5]["image"]), LEVEL_OBJECTS[5]["size"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.speed = speed
        self.duration_factor = duration_factor
        self.deltaX, self.deltaY = 0, 0

    def update(self, screen_scroll, screen_scroll_y):
        self.deltaX = -((self.move_direction)*self.speed) + screen_scroll
        self.rect.x += self.deltaX
        self.rect.y += self.deltaY + screen_scroll_y
        self.move_counter += 1
        if abs(self.move_counter) > self.duration_factor:
            self.move_direction *= -1
            self.move_counter *= -1

class PlatformDown(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, duration_factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(pygame.image.load(LEVEL_OBJECTS[4]["image"]), LEVEL_OBJECTS[4]["size"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.speed = speed
        self.duration_factor = duration_factor
        self.deltaX, self.deltaY = 0, 0

    def update(self, screen_scroll, screen_scroll_y):
        self.deltaY = (self.move_direction)*self.speed
        self.rect.y -= self.deltaY + screen_scroll_y
        self.rect.x += screen_scroll
        self.move_counter += 1
        if abs(self.move_counter) > self.duration_factor:
            self.move_direction *= -1
            self.move_counter *= -1

class PlatformUp(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, duration_factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(pygame.image.load(LEVEL_OBJECTS[22]["image"]), LEVEL_OBJECTS[22]["size"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.speed = speed
        self.duration_factor = duration_factor
        self.deltaX, self.deltaY = 0, 0

    def update(self, screen_scroll, screen_scroll_y):
        self.deltaY = (self.move_direction)*self.speed
        self.rect.y += self.deltaY + screen_scroll_y
        self.rect.x += screen_scroll
        self.move_counter += 1
        if abs(self.move_counter) > self.duration_factor:
            self.move_direction *= -1
            self.move_counter *= -1

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(pygame.image.load(LEVEL_OBJECTS[12]["image"]), LEVEL_OBJECTS[12]["size"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.deltaX, self.deltaY = 0, 0

    def update(self, screen_scroll, screen_scroll_y):
        self.deltaY = (self.move_direction)
        self.rect.y += self.deltaY + screen_scroll_y
        self.rect.x += screen_scroll
        self.move_counter += 0.9
        if abs(self.move_counter) > 5:
            self.move_direction *= -1
            self.move_counter *= -1