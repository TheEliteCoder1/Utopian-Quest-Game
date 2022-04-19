import pygame, csv
import tkinter
from tkinter import Tk
import button
from gamelib import *

pygame.init()
pygame.font.init()

side_panel = 220
side_panel_tabs = ["Tiles", "Triggers"]
side_panel_tab = "Tiles"
bottom_panel = 100
level_number = 0
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode(
    (screen_width + side_panel, screen_height + bottom_panel))
pygame.display.set_caption("Level Editor")
pygame.display.set_icon(pygame.image.load("editor_icon.png"))
screen_constants = get_usefull_constants(screen)
running = True
fps = 60
clock = pygame.time.Clock()

# define editor variables
level = 0
ROWS = 15
MAX_COLS = 200
TILE_SIZE = screen_height // ROWS
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

ground_tile = 0
# create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = ground_tile

# store tiles in list
img_list = []
for x in list(LEVEL_OBJECTS.keys()):
    img = pygame.transform.scale(pygame.image.load(LEVEL_OBJECTS[x]["image"]),
                                 LEVEL_OBJECTS[x]["size"])
    img_list.append(img)

# World Background
bg_img = load_json_data(f'levels/{level}.json')["bg_img"]
background = pygame.image.load(bg_img).convert()


# draw grid
def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0),
                         (c * TILE_SIZE - scroll, screen_height))

    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE),
                         (screen_width, c * TILE_SIZE))


# drawing world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile],
                            (x * TILE_SIZE - scroll, y * TILE_SIZE))


# create empty trigger list
trigger_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    trigger_data.append(r)


def draw_trigger_list():
    for y, row in enumerate(trigger_data):
        for x, trigger in enumerate(row):
            if trigger >= 0:
                re = pygame.draw.circle(
                    screen, (0, 0, 0), (x * TILE_SIZE - scroll, y * TILE_SIZE),
                    0)
                pygame.draw.circle(
                    screen, (0, 0, 0),
                    (re.x + TILE_SIZE / 2, re.y + TILE_SIZE / 2), 20)
                pygame.draw.circle(
                    screen, (255, 255, 255),
                    (re.x + TILE_SIZE / 2, re.y + TILE_SIZE / 2),
                    20,
                    width=2)
                draw_text(screen, FONTS["level_editor"], str(trigger), 18,
                          (255, 255, 255),
                          (re.x + TILE_SIZE / 2, re.y + TILE_SIZE / 2))


# creating buttons
button_list = []
button_col, button_row = 0, 0
for i in range(len(img_list)):
    tile_button = button.IconButton(screen_width + (60 * button_col) + 30,
                                    50 * button_row + 20, img_list[i], 1)
    tile_text = (screen, FONTS["level_editor"],
                 LEVEL_OBJECTS[i]["image"].partition("/")[-1].partition(
                     "/")[-1].replace(".png", ""), 12, (0, 0, 0),
                 (tile_button.rect.centerx, tile_button.rect.centery + 34))
    button_list.append({"button": tile_button, "text": tile_text})
    button_col += 1
    if button_col == 3:
        button_row += 1.5
        button_col = 0

# Triggers
trigger_list = []
selected_trigger = 0
trigger_col, trigger_row = 0, 0
for i in range(len(TRIGGERS)):
    re = pygame.draw.circle(screen, (0, 0, 0), (screen_width + (100 * trigger_col) + 50, 75 * trigger_row + 50), 0)
    trigger_btn = (screen, (0, 0, 0), (re.x + TILE_SIZE / 2, re.y + TILE_SIZE / 2), 20)
    trigger_desc_text = (screen, FONTS["level_editor"], TRIGGERS[i], 15, (0,0,0), (re.x + TILE_SIZE / 2,(re.y + TILE_SIZE / 2) + 35))
    trigger_num_txt = (screen, FONTS["level_editor"], str(i), 18, (255,255,255), (re.x + TILE_SIZE / 2, re.y + TILE_SIZE / 2))
                       
    trigger_list.append({
        "button": trigger_btn,
        "desc_text": trigger_desc_text,
        "num": trigger_num_txt,
        "rect":re
    })
    trigger_col += 1
    if trigger_col == 2:
        trigger_row += 1.5
        trigger_col = 0

#create buttons
save_img = pygame.image.load('assets/images/save_btn.png').convert_alpha()
load_img = pygame.image.load('assets/images/load_btn.png').convert_alpha()
save_button = button.IconButton(screen_width // 2 + 80,
                                screen_height + bottom_panel - 70, save_img, 1)
load_button = button.IconButton(screen_width // 2 + 180,
                                screen_height + bottom_panel - 70, load_img, 1)


def save_data():
    root.destroy()
    with open(f'levels/{level}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in world_data:
            writer.writerow(row)
    with open(f'levels/{level}-triggers.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in trigger_data:
            writer.writerow(row)
    save_json_data(f'levels/{level}.json',
                   {})


while running:
    clock.tick(fps)

    # draw background and text
    screen.fill((255, 213, 128))
    width = background.get_width()
    for x in range(4):
        screen.blit(background, ((x * width) - scroll * 0.5, 0))
    draw_grid()
    draw_world()
    draw_trigger_list()

    #save and load data
    if save_button.draw(screen):
        # save level data
        # window = Tk()
        # window.withdraw()
        # window.attributes("-topmost", True)
        root = tkinter.Tk()
        root.geometry('400x100')
        root.title("Confirm Overwite Level")
        label = tkinter.Label(root,
                              text="Overite the Levels's Data and Save?",
                              wraplength=400,
                              justify='center')
        label.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        button = tkinter.Button(root,
                                text="CANCEL",
                                command=lambda: root.destroy())
        button2 = tkinter.Button(root, text="OK", command=lambda: save_data())
        button.pack(side="left", fill="none", expand=True)
        button2.pack(side="right", fill="none", expand=True)
        root.mainloop()
    if load_button.draw(screen):
        #load in level data
        #reset scroll back to the start of the level 
        scroll = 0
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
        bg_img = load_json_data(f'levels/{level}.json')["bg_img"]
        background = pygame.image.load(bg_img).convert()
		

    # drawing level info
    draw_text(screen, FONTS['game_info'], "LEVEL: " + str(level), 30,
              (194, 255, 255), (75, screen_constants['margin_y'] - 30))
    draw_text(screen,
              font_file=FONTS['game_info'],
              text="Press Up or Down to change level".upper(),
              font_size=19,
              color=BLACK,
              pos=(210, screen_height + bottom_panel - 50))
    # draw tile side_panel
    pygame.draw.rect(
        screen, (255, 213, 128),
        (screen_width, 0, side_panel, screen_height + bottom_panel))

    # draw side_panel tab
    if side_panel_tab == 'Tiles':
        button_count = 0
        for button_count, i in enumerate(button_list):
            if i['button'].draw(screen):
                current_tile = button_count
            draw_text(i['text'][0], i['text'][1], i['text'][2], i['text'][3],
                      i['text'][4], i['text'][5])

        # highlight the selected tile
        pygame.draw.rect(screen, RED, button_list[current_tile]["button"].rect,
                         2)
    elif side_panel_tab == 'Triggers':
        # highlight the selected trigger
        # try:
        pygame.draw.rect(screen, (255,0,0), trigger_list[])
        # except:
        #     selected_trigger = 0
        trigger_count = 0
        for trigger_count, i in enumerate(trigger_list):
            pygame.draw.circle(*i['button'])
            pygame.draw.circle(i['button'][0], (255, 255, 255),
                               i['button'][2],
                               i['button'][3],
                               width=2)
            draw_text(*i['desc_text'])
            draw_text(*i['num'])

    # scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - screen_width:
        scroll += 5 * scroll_speed

    # add new tiles to screen
    # get mouse position
    mpos = pygame.mouse.get_pos()
    x = (mpos[0] + scroll) // TILE_SIZE
    y = mpos[1] // TILE_SIZE
    if side_panel_tab == 'Tiles':
        # check that the coordinates are within the tile area
        if mpos[0] < screen_width and mpos[1] < screen_height:
            # update tile value
            if pygame.mouse.get_pressed()[0] == 1:
                try:
                    if world_data[y][x] != current_tile:
                        world_data[y][x] = current_tile
                except:
                    pass
            if pygame.mouse.get_pressed()[2] == 1:
                try:
                    world_data[y][x] = -1
                except:
                    pass
    elif side_panel_tab == 'Triggers':
        if mpos[0] < screen_width and mpos[1] < screen_height:
            if pygame.mouse.get_pressed()[0] == 1:
                try:
                    if trigger_data[y][x] != selected_trigger:
                        trigger_data[y][x] = selected_trigger
                except:
                    pass
            if pygame.mouse.get_pressed()[2] == 1:
                try:
                    trigger_data[y][x] = -1
                except:
                    pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scroll_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
            if event.key == pygame.K_1:
                side_panel_tab = side_panel_tabs[0]
            if event.key == pygame.K_2:
                side_panel_tab = side_panel_tabs[1]
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_w and selected_trigger > 0:
                selected_trigger -= 1
            if event.key == pygame.K_s and selected_trigger < len(TRIGGERS):
                selected_trigger += 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()
