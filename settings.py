import glm
import math
import pygame as pg
from texture_id import TextureID as ID

# OpenGL settings
MAJOR_VER = 3
MINOR_VER = 3
DEPTH_SIZE = 24

# resolution
WIN_RES = glm.vec2(1280, 720)

# colours
BG_COLOUR = glm.vec3(0.1, 0.16, 0.25)

# textures
TEX_SIZE = 256
TEXTURE_UNIT_0 = 0
NUM_TEXTURES = len(ID)

# Camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)
NEAR = 0.01
FAR = 2000.0
PITCH_MAX = glm.radians(89)

# player
PLAYER_SPEED = 0.0035
PLAYER_SIZE = 0.15
PLAYER_ROT_SPEED = 0.003
PLAYER_HEIGHT = 0.6
PLAYER_POS = glm.vec3(1.5, PLAYER_HEIGHT, 1.5)
MOUSE_SENSITIVITY = 0.0015

# player stats
PLAYER_INIT_HEALTH = 80
PLAYER_INIT_AMMO = 25
PLAYER_MAX_HEALTH = 100
PLAYER_MAX_AMMO = 999

# control keys
KEYS = {
    'FORWARD': pg.K_w,
    'BACK': pg.K_s,
    'UP': pg.K_SPACE,
    'DOWN': pg.K_LCTRL,
    'STRAFE_L': pg.K_a,
    'STRAFE_R': pg.K_d,
    'INTERACT': pg.K_e,
    'WEAPON_1': pg.K_1,
    'WEAPON_2': pg.K_2,
    'WEAPON_3': pg.K_3,
}

# walls
WALL_SIZE = 1
HALF_WALL_SIZE = WALL_SIZE / 2

# animations
ANIM_DOOR_SPEED = 0.03

# timer
SYNC_PULSE = 10  # ms

# item settings
ITEM_SETTINGS = {
    ID.AMMO: {
        'scale': 0.2,
        'value': 8
    },
    ID.MED_KIT: {
        'scale': 0.3,
        'value': 20
    },
    ID.PISTOL_ICON: {
        'scale': 1.0
    },
    ID.RIFLE_ICON: {
        'scale': 1.0
    },
    ID.KEY: {
        'scale': 0.9
    }
}

# hud object settings
ID.HEALTH_DIGIT_0 = 0 + NUM_TEXTURES
ID.HEALTH_DIGIT_1 = 1 + NUM_TEXTURES
ID.HEALTH_DIGIT_2 = 2 + NUM_TEXTURES
ID.AMMO_DIGIT_0 = 3 + NUM_TEXTURES
ID.AMMO_DIGIT_1 = 4 + NUM_TEXTURES
ID.AMMO_DIGIT_2 = 5 + NUM_TEXTURES
ID.FPS_DIGIT_0 = 6 + NUM_TEXTURES
ID.FPS_DIGIT_1 = 7 + NUM_TEXTURES
ID.FPS_DIGIT_2 = 8 + NUM_TEXTURES
ID.FPS_DIGIT_3 = 9 + NUM_TEXTURES

HUD_SETTINGS = {
    ID.HEALTH_DIGIT_0: {
        'scale': 0.1,
        'pos': glm.vec2(0.85, -0.95),
    },
    ID.HEALTH_DIGIT_1: {
        'scale': 0.1,
        'pos': glm.vec2(0.90, -0.95),
    },
    ID.HEALTH_DIGIT_2: {
        'scale': 0.1,
        'pos': glm.vec2(0.95, -0.95),
    },
    ID.AMMO_DIGIT_0: {
        'scale': 0.1,
        'pos': glm.vec2(-0.95, -0.95),
    },
    ID.AMMO_DIGIT_1: {
        'scale': 0.1,
        'pos': glm.vec2(-0.90, -0.95),
    },
    ID.AMMO_DIGIT_2: {
        'scale': 0.1,
        'pos': glm.vec2(-0.85, -0.95),
    },
    ID.AMMO: {
        'scale': 0.25,
        'pos': glm.vec2(-0.9, -0.82),
    },
    ID.MED_KIT: {
        'scale': 0.25,
        'pos': glm.vec2(0.9, -0.82),
    },
    ID.FPS_DIGIT_0: {
        'scale': 0.11,
        'pos': glm.vec2(-0.75, 0.87),
    },
    ID.FPS_DIGIT_1: {
        'scale': 0.11,
        'pos': glm.vec2(-0.68, 0.87),
    },
    ID.FPS_DIGIT_2: {
        'scale': 0.11,
        'pos': glm.vec2(-0.61, 0.87),
    },
    ID.FPS_DIGIT_3: {
        'scale': 0.11,
        'pos': glm.vec2(-0.54, 0.87),
    },
    ID.FPS: {
        'scale': 0.35,
        'pos': glm.vec2(-0.89, 0.74),
    },
    ID.YELLOW_SCREEN: {
        'scale': 4.0,
        'pos': glm.vec2(0.0, -2.0),
    },
    ID.RED_SCREEN: {
        'scale': 4.0,
        'pos': glm.vec2(0.0, -2.0),
    },
}
