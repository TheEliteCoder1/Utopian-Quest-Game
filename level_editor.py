import pygame, csv
import tkinter
from tkinter import Tk
from tkinter.messagebox import showerror
import button
from gamelib import *
import pygame_menu

pygame.init()
pygame.font.init()

side_panel = 220
side_panel_tabs = ["Tiles", "Triggers", "Backgrounds", "Grounds", "Edit"]
side_panel_tab = "Tiles"
bottom_panel = 110
edit_object = None
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
ROWS = 100
MAX_COLS = 200
TILE_SIZE = 45
current_tile = 0
current_background = 0
current_ground = 0
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll = 0
y_scroll = (ROWS * TILE_SIZE) - screen_height
scroll_speed = 1
editable_objects = {}

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# store tiles in list
img_list = []
for x in list(LEVEL_OBJECTS.keys()):
    img = pygame.transform.scale(pygame.image.load(LEVEL_OBJECTS[x]["image"]),
                                 LEVEL_OBJECTS[x]["size"])
    img_list.append(img)

# store backgrounds in list
background_list = []
for x in list(BACKGROUNDS.keys()):
    img = pygame.transform.scale(pygame.image.load(BACKGROUNDS[x]["image"]), (35, 35)) # preview size
    background_list.append(img)

# create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = current_ground

# World Background
bg_img = load_json_data(f'levels/{level}.json')["bg_img"]
background = pygame.image.load(bg_img).convert()

# World Ground tile
ground_tile = load_json_data(f'levels/{level}.json')["ground_tile"]

# World editable objects
editable_objects = load_json_data(f'levels/{level}.json')["editable_objects"]

edit_menu_theme = pygame_menu.themes.THEME_DARK.copy()
edit_menu_theme.widget_font = pygame_menu.font.FONT_NEVIS
edit_menu_theme.title_font_size = 30
edit_menu_theme.widget_font_size = 15
edit_menu_theme.title_font = pygame_menu.font.FONT_NEVIS
edit_menu_theme.title_font_shadow = True

editor_data = {
    "obj_idx":None
}

def save_changes():
    if editor_data["obj_idx"] != None:
        if editable_objects[editor_data["obj_idx"]]["descriptor"] == "PlatformUp" or editable_objects[editor_data["obj_idx"]]["descriptor"] == "PlatformRight" or editable_objects[editor_data["obj_idx"]]["descriptor"] == "Glurdle" or editable_objects[editor_data["obj_idx"]]["descriptor"] == "PlatformDown" or editable_objects[editor_data["obj_idx"]]["descriptor"] == "PlatformLeft":
            new_obj = {"descriptor":editable_objects[editor_data["obj_idx"]]["descriptor"], "pos":editable_objects[editor_data["obj_idx"]]["pos"], "speed":int(edit_menu.get_widget('Speed').get_value()), "duration_factor":int(edit_menu.get_widget('Duration Factor').get_value())}
            editable_objects[editor_data["obj_idx"]] = new_obj

edit_menu = pygame_menu.Menu('Object Editor', width=220, height=450, position=(100, 0, True), theme=edit_menu_theme)
edit_menu.add.label(f'OBJ: None', label_id='descriptor', max_char=-1)
edit_menu.add.text_input('Speed', default=4,
              textinput_id='Speed',
              input_type=pygame_menu.locals.INPUT_TEXT)
edit_menu.add.text_input('DRF', default=60,
              textinput_id='Duration Factor',
              input_type=pygame_menu.locals.INPUT_TEXT)
edit_menu.add.button("Save", save_changes, button_id='Savebtn')

def edit_menu_render(obj_descriptor: str, key: str):
    if obj_descriptor == "PlatformUp":
            editor_data["obj_idx"] = key
            edit_menu.get_widget('descriptor').set_title(f'OBJ: {obj_descriptor} | ID: {key}')
            edit_menu.get_widget('Speed').set_value(obj["speed"])
            edit_menu.get_widget('Duration Factor').set_value(obj["duration_factor"])
    elif obj_descriptor == "PlatformRight":
            editor_data["obj_idx"] = key
            edit_menu.get_widget('descriptor').set_title(f'OBJ: {obj_descriptor} | ID: {key}')
            edit_menu.get_widget('Speed').set_value(obj["speed"])
            edit_menu.get_widget('Duration Factor').set_value(obj["duration_factor"])
    elif obj_descriptor == "PlatformLeft":
            editor_data["obj_idx"] = key
            edit_menu.get_widget('descriptor').set_title(f'OBJ: {obj_descriptor} | ID: {key}')
            edit_menu.get_widget('Speed').set_value(obj["speed"])
            edit_menu.get_widget('Duration Factor').set_value(obj["duration_factor"])
    elif obj_descriptor == "PlatformDown":
            editor_data["obj_idx"] = key
            edit_menu.get_widget('descriptor').set_title(f'OBJ: {obj_descriptor} | ID: {key}')
            edit_menu.get_widget('Speed').set_value(obj["speed"])
            edit_menu.get_widget('Duration Factor').set_value(obj["duration_factor"])
    elif obj_descriptor == "Glurdle":
            editor_data["obj_idx"] = key
            edit_menu.get_widget('descriptor').set_title(f'OBJ: {obj_descriptor} | ID: {key}')
            edit_menu.get_widget('Speed').set_value(obj["speed"])
            edit_menu.get_widget('Duration Factor').set_value(obj["duration_factor"])
    
       
        

# draw grid
def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0),
                         (c * TILE_SIZE - scroll, screen_height))

    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE - y_scroll),
                         (screen_width, c * TILE_SIZE - y_scroll))


# drawing world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile],
                            (x * TILE_SIZE - scroll, y * TILE_SIZE - y_scroll))

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
                    screen, (0, 0, 0), (x * TILE_SIZE - scroll, y * TILE_SIZE - y_scroll),
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
    text = LEVEL_OBJECTS[i]["image"].partition("/")[-1].partition(
                     "/")[-1].replace(".png", "") if "name" not in list(LEVEL_OBJECTS[i].keys()) else LEVEL_OBJECTS[i]["name"]
    tile_text = (screen, FONTS["level_editor"],
                 text, 12, (0, 0, 0),
                 (tile_button.rect.centerx, tile_button.rect.centery + 34))
    button_list.append({"button": tile_button, "text": tile_text})
    button_col += 1
    if button_col == 3:
        button_row += 1.5
        button_col = 0

# creating background buttons
background_buttons_list = []
background_button_col, background_button_row = 0, 0
for i in range(len(background_list)):
    background_button = button.IconButton(screen_width + (100 * background_button_col) + 40, 75 * background_button_row + 50, background_list[i], 1)
    background_button_text = (screen, FONTS["level_editor"], BACKGROUNDS[i]["image"].partition("/")[-1].partition("/")[-1].replace(".png", ""), 14, (0,0,0), (background_button.rect.centerx, background_button.rect.centery + 34))
    background_buttons_list.append({"button": background_button, "text": background_button_text})
    background_button_col += 1
    if background_button_col == 2:
        background_button_row += 1.5
        background_button_col = 0

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
    save_json_data(f'levels/{level}.json', {"bg_img":bg_img, "ground_tile":ground_tile, "editable_objects":editable_objects})



while running:
    clock.tick(fps)

    # draw background and text
    screen.fill((255, 213, 128))
    width = background.get_width()
    height = background.get_height()
    for x in range(5):
        screen.blit(background, ((x * width) - scroll * 0.5, 0))
    draw_grid()
    draw_world()
    draw_trigger_list()

    #save and load data
    if save_button.draw(screen):
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
        y_scroll = (ROWS * TILE_SIZE) - screen_height
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
        ground_tile = load_json_data(f'levels/{level}.json')["ground_tile"]
        editable_objects = load_json_data(f'levels/{level}.json')["editable_objects"]
        background = pygame.image.load(bg_img).convert()
		

    # drawing level info
    draw_text(screen, FONTS['game_info'], "LEVEL: " + str(level), 30,
              (0, 0, 0), (75, screen_constants['margin_y'] - 30))
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
        edit_menu.disable()
        button_count = 0
        for button_count, i in enumerate(button_list):
            if i['button'].draw(screen):
                current_tile = button_count
            draw_text(i['text'][0], i['text'][1], i['text'][2], i['text'][3],
                      i['text'][4], i['text'][5])

        # highlight the selected tile
        pygame.draw.rect(screen, WHITE, button_list[current_tile]["button"].rect,
                         2)
    elif side_panel_tab == "Backgrounds":
        edit_menu.disable()
        background_count = 0
        for background_count, i in enumerate(background_buttons_list):
            if i['button'].draw(screen):
                current_background = background_count
                bg_img = BACKGROUNDS[current_background]["image"]
                background = pygame.image.load(bg_img).convert()
            draw_text(i['text'][0], i['text'][1], i['text'][2], i['text'][3],
                      i['text'][4], i['text'][5])

        # highlight the selected background
        pygame.draw.rect(screen, WHITE, background_buttons_list[current_background]["button"].rect, 2)

    elif side_panel_tab == "Edit":
        edit_menu.enable()

    elif side_panel_tab == "Grounds":
        edit_menu.disable()
        ground_count = 0
        for ground_count, i in enumerate(button_list):
            if i['button'].draw(screen):
                current_ground = ground_count
                ground_tile = LEVEL_OBJECTS[current_ground]["image"]
                # create ground
                for tile in range(0, MAX_COLS):
                    world_data[ROWS - 1][tile] = current_ground
            draw_text(i['text'][0], i['text'][1], i['text'][2], i['text'][3], i['text'][4], i['text'][5])

        # highlight the selected ground
        pygame.draw.rect(screen, WHITE, button_list[current_ground]["button"].rect, 2)
            

    elif side_panel_tab == 'Triggers':
        edit_menu.disable()
        trigger_count = 0
        for trigger_count, i in enumerate(trigger_list):
            pygame.draw.circle(*i['button'])
            pygame.draw.circle(i['button'][0], (255, 255, 255),
                               i['button'][2],
                               i['button'][3],
                               width=2)
            draw_text(*i['desc_text'])
            draw_text(*i['num'])
        # highlight the selected trigger
        try:
            pygame.draw.circle(screen, (255,0,0), (trigger_list[selected_trigger]["rect"].x + (TILE_SIZE/2), trigger_list[selected_trigger]["rect"].y + 22), radius=20, width=2)
        except:
            selected_trigger = 0

    # scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - screen_width:
        scroll += 5 * scroll_speed
    if scroll_up == True and y_scroll > 0:
       y_scroll -= 5 * scroll_speed 
    if scroll_down == True and y_scroll < (ROWS * TILE_SIZE) - screen_height:
       y_scroll += 5 * scroll_speed 
    # add new tiles to screen
    # get mouse position
    mpos = pygame.mouse.get_pos()
    x = (mpos[0] + scroll) // TILE_SIZE
    y = (mpos[1] + y_scroll) // TILE_SIZE
    if side_panel_tab == 'Tiles':
        # check that the coordinates are within the tile area
        if mpos[0] < screen_width and mpos[1] < screen_height:
            # update tile value
            if pygame.mouse.get_pressed()[0] == 1:
                try:
                    if world_data[y][x] != current_tile:
                        world_data[y][x] = current_tile
                        # checking for editable objects
                        if len(list(editable_objects.keys())) > 0:
                            if current_tile == 22:
                                editable_objects[int(list(editable_objects.keys())[-1])+1] = {
                                    "descriptor":"PlatformUp",
                                    "pos":(x * TILE_SIZE, y * TILE_SIZE),
                                    "speed":4,
                                    "duration_factor":60
                                }
                            if current_tile == 23:
                                editable_objects[int(list(editable_objects.keys())[-1])+1] = {
                                    "descriptor":"PlatformRight",
                                    "pos":(x * TILE_SIZE, y * TILE_SIZE),
                                    "speed":4,
                                    "duration_factor":60
                                }
                            if current_tile == 21:
                                editable_objects[int(list(editable_objects.keys())[-1])+1] = {
                                    "descriptor":"Glurdle",
                                    "pos":(x * TILE_SIZE, y * TILE_SIZE),
                                    "speed":4,
                                    "duration_factor":45
                                }
                            if current_tile == 4:
                                editable_objects[int(list(editable_objects.keys())[-1])+1] = {
                                    "descriptor":"PlatformDown",
                                    "pos":(x * TILE_SIZE, y * TILE_SIZE),
                                    "speed":4,
                                    "duration_factor":45
                                }
                            if current_tile == 5:
                                editable_objects[int(list(editable_objects.keys())[-1])+1] = {
                                    "descriptor":"PlatformLeft",
                                    "pos":(x * TILE_SIZE, y * TILE_SIZE),
                                    "speed":4,
                                    "duration_factor":45
                                }
                        else:
                            if current_tile == 22:
                                editable_objects["0"] = {
                                    "descriptor":"PlatformUp",
                                    "pos":(x * TILE_SIZE, y * TILE_SIZE),
                                    "speed":4,
                                    "duration_factor":60
                                }
                            if current_tile == 23:
                                editable_objects["0"] = {
                                    "descriptor":"PlatformRight",
                                    "pos":(x * TILE_SIZE, y * TILE_SIZE),
                                    "speed":4,
                                    "duration_factor":60
                                }
                            if current_tile == 21:
                                editable_objects["0"] = {
                                    "descriptor":"Glurdle",
                                    "pos":(x * TILE_SIZE, y * TILE_SIZE),
                                    "speed":4,
                                    "duration_factor":45
                                }
                            if current_tile == 4:
                                editable_objects["0"] = {
                                    "descriptor":"PlatformDown",
                                    "pos":(x * TILE_SIZE, y * TILE_SIZE),
                                    "speed":4,
                                    "duration_factor":45
                                }
                            if current_tile == 5:
                                editable_objects["0"] = {
                                    "descriptor":"PlatformLeft",
                                    "pos":(x * TILE_SIZE, y * TILE_SIZE),
                                    "speed":4,
                                    "duration_factor":45
                                }
                            
                except:
                    pass
            if pygame.mouse.get_pressed()[2] == 1:
                world_data[y][x] = -1
                for key in list(editable_objects.keys()):
                    if (editable_objects[key]["pos"][0], editable_objects[key]["pos"][1]) == (x * TILE_SIZE, y * TILE_SIZE):
                        editable_objects.pop(key)
                        
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
    elif side_panel_tab == 'Edit':
        if mpos[0] < screen_width and mpos[1] < screen_height:
            if pygame.mouse.get_pressed()[0] == 1:
                for key, obj in editable_objects.items():
                    if (obj["pos"][0], obj["pos"][1]) == (x * TILE_SIZE, y * TILE_SIZE):
                        edit_object = pygame.Rect(obj["pos"][0]-scroll, obj["pos"][1], TILE_SIZE, TILE_SIZE)
                        edit_menu_render(obj["descriptor"], key)

        if edit_object != None:
            pygame.draw.rect(screen, (255,255,255), edit_object, 5)
                        
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            save_json_data("workflow.json", {"start_level":0})
            running = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if side_panel_tab != "Edit":
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    scroll_left = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    scroll_right = True
                if event.key == pygame.K_w:
                    scroll_up = True
                if event.key == pygame.K_s:
                    scroll_down = True
                if event.key == pygame.K_RSHIFT:
                    scroll_speed = 5
            if event.key == pygame.K_1 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                side_panel_tab = side_panel_tabs[0]
            if event.key == pygame.K_2 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                side_panel_tab = side_panel_tabs[1]
            if event.key == pygame.K_3 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                side_panel_tab = side_panel_tabs[2]
            if event.key == pygame.K_4 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                side_panel_tab = side_panel_tabs[3]
            if event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_CTRL:
                side_panel_tab = side_panel_tabs[4]
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if side_panel_tab == "Triggers":
                if event.key == pygame.K_w and selected_trigger > 0:
                    selected_trigger -= 1
                if event.key == pygame.K_s and selected_trigger < len(TRIGGERS):
                    selected_trigger += 1
            if event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_CTRL:
                try:
                    save_json_data("workflow.json", {"start_level":level})
                    run("python game.py")
                except Exception as E:
                    window = Tk()
                    window.withdraw()
                    window.attributes("-topmost", True)
                    tkinter.messagebox.showerror(title="Level-Debugger [TestMode] Error.", message=f"Failed to execute level because Python or the Subprocess Module was not Installed Properly. Contact RaphTheCoder for help. DETAILS: {E}")
                    window.destroy()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scroll_right = False
            if event.key == pygame.K_w:
                scroll_up = False
            if event.key == pygame.K_s:
                scroll_down = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    if edit_menu.is_enabled():
        edit_menu.update(events)
        edit_menu.draw(screen)

    pygame.display.update()