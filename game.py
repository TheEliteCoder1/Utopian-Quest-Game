import math
import csv
from gamelib import *
from classes import Glurdle, PlatformUp, PlatformRight, PlatformDown, PlatformLeft, Key, HealthPotion, Currency

screen_width, screen_height = 700, 500
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Utopian Quest")
pygame.display.set_icon(pygame.image.load("game_icon.png"))
screen_constants = get_usefull_constants(screen)
running = True
fps = 120
clock = pygame.time.Clock()
GRAVITY = 0.2
ROWS = 100
TILE_SIZE = 45
bg_scroll = 0
screen_scroll = 0
screen_scroll_y = 0
SCROLL_THRESH = 300
SCROLL_THRESH_Y = 92
COLS = 200
level = load_json_data('workflow.json')["start_level"]
MAX_LEVELS = 10
bg_img = load_json_data(f'levels/{level}.json')["bg_img"]
background = pygame.image.load(bg_img).convert()
editable_objects = load_json_data(f'levels/{level}.json')["editable_objects"]
# health_potion_img = pygame.transform.scale(pygame.image.load(LEVEL_OBJECTS[20]["image"]), (46, 46))

# define player action variables
moving_left = False
moving_right = False

# background music
music = pygame.mixer.music.load("assets/music/music.mp3")
pygame.mixer.music.play(-1)

# fx
coin_fx = pygame.mixer.Sound('assets/music/coin.mp3')
coin_fx.set_volume(1)

level_end_fx = pygame.mixer.Sound('assets/music/level_end.wav')
level_end_fx.set_volume(1)

explosive_fx = pygame.mixer.Sound('assets/music/explosion.wav')
explosive_fx.set_volume(1)

death_fx = pygame.mixer.Sound('assets/music/death.wav')
death_fx.set_volume(1)

jump_fx = pygame.mixer.Sound('assets/music/jump.wav')
jump_fx.set_volume(1)

destroy_fx = pygame.mixer.Sound('assets/music/destroy.wav')
destroy_fx.set_volume(1)

triggered_fx = pygame.mixer.Sound('assets/music/triggered.wav')
triggered_fx.set_volume(1)

uptrigger_fx = pygame.mixer.Sound('assets/music/uptrigger.wav')
uptrigger_fx.set_volume(1)

hurt_fx = pygame.mixer.Sound('assets/music/hurt.wav')
hurt_fx.set_volume(1)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, character, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.shoot_cooldown = 0
        self.direction = 1
        self.health = 200
        self.max_health = 200
        self.vel_y = 0
        self.jump = False
        self.react_to_explosion = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #ai specific variables
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0

        #load all images for the players
        animation_types = ['Idle', 'Run', "Jump", 'Death']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(
                os.listdir(f'assets/player/{character}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f'assets/player/{character}/{animation}/{i}.png'
                ).convert_alpha()
                img = pygame.transform.scale(img, (int(
                    img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.vision = pygame.Rect(30, 0, 150, 20)
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.below_moving = False

        for tile in world.objects_list:
            for trigger in world.triggers:
                if (tile[1][0], tile[1][1]) == (trigger[0], trigger[1]):
                    tile.append(trigger[2])

    def update(self):
        self.update_animation()
        self.check_alive()

    def move(self, moving_left, moving_right):
        #reset movement variables
        screen_scroll = 0
        screen_scroll_y = 0
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            jump_fx.play()
            self.vel_y = -7
            self.jump = False
            self.in_air = True
        if self.react_to_explosion == True and self.in_air == False:
            self.vel_y = -11
            self.react_to_explosion = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY * 2
        if self.vel_y > 6:
            self.vel_y
        dy += self.vel_y


        #check for collision
        level_complete = False
        for tile in world.objects_list:
            if tile[2] == 'Block':
                #check collision in the x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y,
                                       self.width, self.height):
                    dx = 0
                #check for collision in the y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy,
                                       self.width, self.height):
                    #check if below the ground, i.e. jumping
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    #check if above the ground, i.e. falling
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom
                    try:
                        trigger = tile[3]
                        move_x = 10
                        move_y = 5
                        if trigger == 0:
                            if self.rect.x > 0 + tile[0].get_width():
                                triggered_fx.play()
                                tile[1].x -= move_x
                        if trigger == 1:
                            if self.rect.x < screen.get_width() - tile[0].get_width():
                                triggered_fx.play()
                                tile[1].x += move_x
                        if trigger == 2:
                            if self.rect.y > 0 + tile[0].get_height():
                                uptrigger_fx.play()
                                tile[1].y -= move_y
                        if trigger == 3:
                            if self.rect.y < screen.get_height(
                            ) - tile[0].get_height():
                                triggered_fx.play(1)
                                tile[1].y += move_y
                        if trigger == 4:
                            destroy_fx.play()
                            world.objects_list.remove(tile)
                    except:
                        pass
            elif tile[2] == 'Explodable':
                if tile[1].colliderect(
                        self.rect.x + dx, self.rect.y, self.width,
                        self.height) or tile[1].colliderect(
                            self.rect.x, self.rect.y + dy, self.width,
                            self.height):
                    explosive_fx.play()
                    self.react_to_explosion = True
                    self.health -= 30
                    world.objects_list.remove(tile)
            elif tile[2] == 'Goal':
                if tile[1].colliderect(
                        self.rect.x + dx, self.rect.y, self.width + 3,
                        self.height) or tile[1].colliderect(
                            self.rect.x, self.rect.y + dy, self.width,
                            self.height):
                    level_complete = True

        if pygame.sprite.spritecollide(self, key_group, False):
            level_complete = True

        for platform in platform_group:
            if platform.deltaY == 0:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.below_moving = False
                    dx = 0
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                    if self.below_moving == False:
                        dx = platform.deltaX
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # if on top 
                    if platform.rect.top > self.rect.bottom:
                        self.below_moving = False
                        self.vel_y = 0
                        self.in_air = False
                    elif self.rect.top >= platform.rect.bottom:
                        self.below_moving = True
                        self.vel_y = 0
            else:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    #check for collision in the y direction
                    if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        #check if below the ground, i.e. jumping
                        if self.vel_y < 0 and platform.rect.top > self.rect.bottom:
                            self.vel_y = 0
                            dy = platform.rect.bottom - self.rect.top
                        #check if above the ground, i.e. falling
                        elif self.vel_y >= 0 and platform.rect.top < self.rect.bottom:
                            self.vel_y = 0
                            self.in_air = False
                            dy = platform.rect.top - self.rect.bottom
                        

        if pygame.sprite.spritecollide(self, glurdle_group, False):
            hurt_fx.play()
            self.vel_y = -7
            self.in_air = True
            self.health -= 25
            glurdle_group.remove(pygame.sprite.spritecollide(self, glurdle_group, False))
            
        if pygame.sprite.spritecollide(self, currency_group, False):
            coin_fx.play()
            currency_group.remove(pygame.sprite.spritecollide(self, currency_group, False))

        if pygame.sprite.spritecollide(self, health_potion_group, False):
            health_potion_group.remove(pygame.sprite.spritecollide(self, health_potion_group, False))
            if self.health < 100:
                self.health += 15

        #check if fallen off the map
        if self.rect.bottom > (ROWS * TILE_SIZE) - screen_height:
            self.health = 0

        #check if going off the edges of the screen
        if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
            dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

        #update scroll based on player position
        if (self.rect.right > screen_width - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - screen_width)\
         or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
            self.rect.x -= dx
            screen_scroll = -dx

        if (self.rect.top > (screen_height - SCROLL_THRESH_Y)) or (self.rect.bottom < SCROLL_THRESH_Y):
            self.rect.y -= dy
            screen_scroll_y = -dy


        return screen_scroll, screen_scroll_y, level_complete

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(4)
            pygame.mixer.music.stop()
            death_fx.play()
            pygame.time.delay(5000)
            pygame.mixer.music.play(-1)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, False, False),
                    self.rect)


# store tiles in list
img_list = []
for x in list(LEVEL_OBJECTS.keys()):
    img = pygame.transform.scale(pygame.image.load(LEVEL_OBJECTS[x]["image"]),
                                 LEVEL_OBJECTS[x]["size"])
    img_list.append(img)

# sprite groups
glurdle_group = pygame.sprite.Group()
currency_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
health_potion_group  = pygame.sprite.Group()

def draw_bg(screen, background):
    screen.fill((255, 255, 255))
    width = background.get_width()
    for x in range(5):
        screen.blit(background, ((x * width) - bg_scroll * 0.5, 0))


class World():
    def __init__(self):
        self.objects_list = []
        self.triggers = []
        
    def process_data(self, data, trigger_data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0 and tile < 20 and tile != 8 and tile != 9 and tile != 12 and tile != 4 and tile != 5:
                    img = pygame.transform.scale(
                        pygame.image.load(LEVEL_OBJECTS[tile]["image"]),
                        LEVEL_OBJECTS[tile]["size"])
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = [
                        img, img_rect, LEVEL_OBJECTS[tile]["descriptor"]
                	]
                    self.objects_list.append(tile_data)
                elif tile == 4:
                    for idx, obj in editable_objects.items():
                        if obj["descriptor"] == "PlatformDown" and (obj["pos"][0], obj["pos"][1]) == (x * TILE_SIZE, y * TILE_SIZE):
                            platform = PlatformDown(x * TILE_SIZE, y * TILE_SIZE, obj["speed"], obj["duration_factor"])
                            platform_group.add(platform)
                elif tile == 5:
                    for idx, obj in editable_objects.items():
                        if obj["descriptor"] == "PlatformLeft" and (obj["pos"][0], obj["pos"][1]) == (x * TILE_SIZE, y * TILE_SIZE):
                            platform = PlatformLeft(x * TILE_SIZE, y * TILE_SIZE, obj["speed"], obj["duration_factor"])
                            platform_group.add(platform)
                elif tile == 12:
                    key = Key(x * TILE_SIZE, y * TILE_SIZE)
                    key_group.add(key)
                elif tile == 8 or tile == 9:
                    currency = Currency(x * TILE_SIZE, y * TILE_SIZE, LEVEL_OBJECTS[tile]["image"])
                    currency_group.add(currency)
                elif tile == 20:
                    health_potion = HealthPotion(x * TILE_SIZE, y * TILE_SIZE)
                    health_potion_group.add(health_potion)
                elif tile == 21:
                    for idx, obj in editable_objects.items():
                        if obj["descriptor"] == "Glurdle" and (obj["pos"][0], obj["pos"][1]) == (x * TILE_SIZE, y * TILE_SIZE):
                            glurdle = Glurdle(x * TILE_SIZE, y * TILE_SIZE, obj["speed"], obj["duration_factor"])
                            glurdle_group.add(glurdle)
                elif tile == 22:
                    for idx, obj in editable_objects.items():
                        if obj["descriptor"] == "PlatformUp" and (obj["pos"][0], obj["pos"][1]) == (x * TILE_SIZE, y * TILE_SIZE):
                            platform = PlatformUp(x * TILE_SIZE, y * TILE_SIZE, obj["speed"], obj["duration_factor"])
                            platform_group.add(platform)
                elif tile == 23:
                    for idx, obj in editable_objects.items():
                        if obj["descriptor"] == "PlatformRight" and (obj["pos"][0], obj["pos"][1]) == (x * TILE_SIZE, y * TILE_SIZE):
                            platform = PlatformRight(x * TILE_SIZE, y * TILE_SIZE, obj["speed"], obj["duration_factor"])
                            platform_group.add(platform)
                    
        for y, row in enumerate(trigger_data):
            for x, trigger in enumerate(row):
                if trigger >= 0:
                    tri = (x * TILE_SIZE, y * TILE_SIZE, trigger)
                    self.triggers.append(tri)

    def draw(self):
        for tile in self.objects_list:
            tile[1][0] += screen_scroll
            tile[1][1] += screen_scroll_y
            screen.blit(tile[0], tile[1])

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# create empty trigger list
trigger_data = []
for row in range(ROWS):
    r = [-1] * COLS
    trigger_data.append(r)
#load in level data and create world
with open(f'levels/{level}.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
with open(f'levels/{level}-triggers.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, trigger in enumerate(row):
            trigger_data[x][y] = int(trigger)

world = World()
world.process_data(world_data, trigger_data)
player = Player(screen, 50, 0, "Boro", 1, 5)

while running:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True

        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

        if event.type == pygame.MOUSEMOTION:
            # When mouse is hovering
            pass

        if event.type == pygame.MOUSEBUTTONDOWN:
            # When mouse is clicking
            pass

    # draw game every frame.
    draw_bg(screen, background)
    world.draw()
    platform_group.draw(screen)
    key_group.draw(screen)
    glurdle_group.draw(screen)
    player.update()
    player.draw()
    draw_text(screen, FONTS['game_info'], "LEVEL: " + str(level), 30,
              (0, 0, 0), (75, screen_constants['margin_y'] - 30))
    
    #draw_text(screen, FONTS['game_info'], "FPS: " + str(round(clock.get_fps())), 30,
              #(0, 0, 0), (625, screen_constants['margin_y'] - 30))

    if player.health > 130 and player.health < 160:
        health_color = (255, 255, 0)
    elif player.health > 160:
        health_color = (0, 255, 0)
    elif player.health < 100:
        health_color = (255, 0, 0)
    elif player.health == 0:
        health_color = None
    if health_color != None:
        health_rect = pygame.Rect(10, screen_constants['margin_y'] - 10, player.health, 30)
        pygame.draw.rect(screen, health_color, health_rect)
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, screen_constants['margin_y'] - 10, player.max_health, 30), width=3, border_radius=5)
    if player.alive:
        platform_group.update(screen_scroll, screen_scroll_y)         
        key_group.update(screen_scroll, screen_scroll_y)
        health_potion_group.update(screen_scroll, screen_scroll_y)
        glurdle_group.update(screen_scroll, screen_scroll_y, world)
        currency_group.update(screen, screen_scroll, screen_scroll_y)
        if player.in_air:
            player.update_action(2)  #2: jump
        elif moving_left or moving_right:
            player.update_action(1)  #1: run
        else:
            player.update_action(0)  #0: idle
        screen_scroll, screen_scroll_y, level_complete = player.move(moving_left, moving_right)
        bg_scroll -= screen_scroll
        if level_complete:
            pygame.mixer.music.stop()
            level_end_fx.play()
            pygame.time.delay(5000)
            pygame.mixer.music.play(-1)
            level += 1
            bg_scroll = 0
            world_data = []
            key_group.empty()
            health_potion_group.empty()
            platform_group.empty()
            currency_group.empty()
            glurdle_group.empty()
            for row in range(ROWS):
                r = [-1] * COLS
                world_data.append(r)
            # create empty trigger list
            trigger_data = []
            for row in range(ROWS):
                r = [-1] * COLS
                trigger_data.append(r)
            #load in level data and create world
            bg_img = load_json_data(f'levels/{level}.json')["bg_img"]
            background = pygame.image.load(bg_img).convert()
            editable_objects = load_json_data(f'levels/{level}.json')["editable_objects"]
            with open(f'levels/{level}.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            with open(f'levels/{level}-triggers.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, trigger in enumerate(row):
                        trigger_data[x][y] = int(trigger)
            world = World()
            world.process_data(world_data, trigger_data)
            player = Player(screen, 50, 0, "Boro", 1, 5)
    else:
        bg_scroll = 0
        world_data = []
        platform_group.empty()
        key_group.empty()
        health_potion_group.empty()
        glurdle_group.empty()
        currency_group.empty()
        for row in range(ROWS):
            r = [-1] * COLS
            world_data.append(r)
        # create empty trigger list
        trigger_data = []
        for row in range(ROWS):
            r = [-1] * COLS
            trigger_data.append(r)
        #load in level data and create world
        bg_img = load_json_data(f'levels/{level}.json')["bg_img"]
        background = pygame.image.load(bg_img).convert()
        editable_objects = load_json_data(f'levels/{level}.json')["editable_objects"]
        with open(f'levels/{level}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
        with open(f'levels/{level}-triggers.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, trigger in enumerate(row):
                    trigger_data[x][y] = int(trigger)
        world = World()
        world.process_data(world_data, trigger_data)
        player = Player(screen, 50, 0, "Boro", 1, 5)
        

    pygame.display.update()
