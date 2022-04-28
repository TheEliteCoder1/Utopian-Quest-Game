import pygame, os, json
from subprocess import run
pygame.init()
pygame.font.init()

"""This module is a library that provides colors, fonts, assets, settings & utility functions for the game."""

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (10, 30, 255)

def load_json_data(json_file):
    with open(json_file, 'r') as sf:
        data = sf.read()
        sf.close()
    jsonified_data = json.loads(data)
    return jsonified_data

def save_json_data(json_file, data):
    file=open(json_file, 'w').close()
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

FONTS = {
    'game_info':'assets/fonts/oxygene.ttf',
    'level_editor':'assets/fonts/fira.ttf'
}

LEVEL_OBJECTS = {
    0:{
        "image":"assets/levelObjects/grass.png",
        "descriptor":"Block",
        "size":(40, 40)
    },
    1:{
        "image":"assets/levelObjects/bush.png",
        "descriptor":"Decor",
        "size":(40, 40)
    },
    2:{
        "image":"assets/levelObjects/mushroomRed.png",
        "descriptor":"Decor",        
        "size":(40, 40)
    },
    3:{
        "image":"assets/levelObjects/plant.png",
        "descriptor":"Decor",        
        "size":(40, 40)
    },
    4:{
        "image":"assets/levelObjects/brick2.png",
        "descriptor":"Block",
        "size":(40, 40)
    },
    5:{
        "image":"assets/levelObjects/brick1.png",
        "descriptor":"Block",        
        "size":(40, 40)
    },
    6:{
        "image":"assets/levelObjects/fence.png",
        "descriptor":"Decor",        
        "size":(40, 40)
    },
    7:{
        "image":"assets/levelObjects/chain.png",
        "descriptor":"Decor",        
        "size":(40, 40)
    },
    8:{
        "image":"assets/levelObjects/coinGold.png",
        "descriptor":"Currency",        
        "size":(40, 40)
    },
    9:{
        "image":"assets/levelObjects/gemBlue.png",
        "descriptor":"Currency",        
        "size":(40, 40)
    },
    10:{
        "image":"assets/levelObjects/shieldGold.png",
        "descriptor":"Healer",
        "size":(40, 40)
    },
    11:{
        "image":"assets/levelObjects/cloud3.png",
        "descriptor":"Decor",        
        "size":(45, 40)
    },
    12:{
        "image":"assets/levelObjects/keyRed.png",
        "descriptor":"Goal",        
        "size":(40, 40)
    },
    13:{
        "image":"assets/levelObjects/bomb.png",
        "descriptor":"Explodable",        
        "size":(40, 40)
    },
	14:{
		"image":"assets/levelObjects/flag.png",
		"descriptor":"Decor",
		"size":(50, 50)
	},
    15:{
		"image":"assets/levelObjects/up.png",
		"descriptor":"Block",		
		"size":(40, 40)
	},
    16:{
		"image":"assets/levelObjects/down.png",
		"descriptor":"Block",		
		"size":(40, 40)
	},
    17:{
		"image":"assets/levelObjects/left.png",
		"descriptor":"Block",
		"size":(40, 40)
	},
    18:{
		"image":"assets/levelObjects/right.png",
		"descriptor":"Block",
		"size":(40, 40)
	},
    19:{
		"image":"assets/levelObjects/destroy.png",
		"descriptor":"Block",
		"size":(40, 40)
	},
    20:{
        "image":"assets/animations/dynamite/dynamite-0.png",
        "size":(40, 45),
        "name":"dynamite"
    },
    21:{
        "image":"assets/levelObjects/glurdle.png",
        "size":(40, 40)
    },
    22:{
        "image":"assets/levelObjects/platUp.png",
        "size":(40,40)
    },
    23:{
        "image":"assets/levelObjects/platRight.png",
        "size":(40,40)
    }
}

TRIGGERS = [
    "moveLeft",
    "moveRight",
    "moveUp",
    "moveDown",
	"destroy"
]

BACKGROUNDS = {
    0:{
        "image":"assets/backgrounds/bg_shroom.png"
    },
    1:{
        "image":"assets/backgrounds/bg_grasslands.png"
    },
    2:{
        "image":"assets/backgrounds/bg_desert.png"
    },
    3:{
        "image":"assets/backgrounds/bg_castle.png"
    }
}


def draw_text(screen: pygame.Surface, font_file: str, text: str, 
    font_size: int, color: tuple, pos: tuple, backg=None):
    """Draws text to the screen given a font file and text."""
    font = pygame.font.Font(font_file, font_size)
    if backg == None:
        t = font.render(text, True, color)
    t = font.render(text, True, color, backg)
    textRect = t.get_rect()
    textRect.center = pos
    screen.blit(t, textRect)

def get_usefull_constants(screen: pygame.Surface) -> dict:
    """Get usefull parts of the screen as variables returned in a dict where key is the variable name alongside it's value."""
    center_screen_x = screen.get_width() // 2
    center_screen_y = screen.get_height() // 2
    center_screen_pos = (center_screen_x, center_screen_y)
    margin_y = 50 
    bottom_y = screen.get_height()-50
    constants_dict = {
        "center_screen_x":center_screen_x, 
        "center_screen_y":center_screen_y, 
        "margin_y":margin_y,
        "center_screen_pos":center_screen_pos,
        "bottom_y":bottom_y
    }
    return constants_dict