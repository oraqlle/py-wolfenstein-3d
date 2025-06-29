import glm
import math
import pygame as pg

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
