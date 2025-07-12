import glm
import pygame as pg
import settings as cfg
import random as rnd
from camera import Camera
from texture_id import TextureID as ID
from typing import Tuple
from itertools import cycle


class PlayerAttribs:
    def __init__(self):
        self.health = cfg.PLAYER_INIT_HEALTH
        self.ammo = cfg.PLAYER_INIT_AMMO
        self.weapons = {ID.KNIFE_0: 1, ID.PISTOL_0: 0, ID.RIFLE_0: 0}
        self.weapon_id = ID.KNIFE_0
        self.num_level = 0

    def update(self, player, death=True):
        self.health = player.health
        self.ammo = player.ammo
        self.weapons = player.weapons
        self.weapon_id = ID.KNIFE_0 if death else player.weapon_id


class Player(Camera):
    def __init__(self, eng, position=cfg.PLAYER_POS, yaw=0, pitch=0):
        self.app = eng.app
        self.eng = eng
        self.sound = eng.sound
        self.play = self.sound.play
        super().__init__(position, yaw, pitch)

        # these maps will update when instantiated LevelMap
        self.wall_map = None
        self.door_map = None
        self.item_map = None

        self.ammo = self.eng.player_attribs.ammo
        self.health = self.eng.player_attribs.health

        self.tile_pos: Tuple[int, int] = None

        # weapons
        self.weapons = self.eng.player_attribs.weapons
        self.weapon_id = self.eng.player_attribs.weapon_id
        self.weapon_cycle = cycle(self.eng.player_attribs.weapons.keys())

        self.is_shooting = False

        self.key = None

    def update_tile_pos(self):
        self.tile_pos = int(self.position.x), int(self.position.z)

    def check_npc_hit(self):
        if cfg.WEAPON_SETTINGS[self.weapon_id]['miss_probability'] > rnd.random():
            return None

        if npc_pos := self.eng.ray_casting.run(
                start_pos=self.position,
                dir=self.forward,
                max_dist=cfg.WEAPON_SETTINGS[self.weapon_id]['max_dist'],
                npc_to_player_flag=False
        ):
            npc = self.eng.level_map.npc_map[npc_pos]
            npc.take_damage()

    def pick_up_item(self):
        if self.tile_pos not in self.item_map:
            return None

        item = self.item_map[self.tile_pos]

        if item.tex_id == ID.MED_KIT:
            self.health += cfg.ITEM_SETTINGS[ID.MED_KIT]['value']
            self.health = min(self.health, cfg.PLAYER_MAX_HEALTH)
        elif item.tex_id == ID.AMMO:
            self.ammo += cfg.ITEM_SETTINGS[ID.AMMO]['value']
            self.ammo = min(self.ammo, cfg.PLAYER_MAX_AMMO)
        elif item.tex_id == ID.PISTOL_ICON:
            if not self.weapons[ID.PISTOL_0]:
                self.weapons[ID.PISTOL_0] = 1
                self.switch_weapon(ID.PISTOL_0)
        elif item.tex_id == ID.RIFLE_ICON:
            if not self.weapons[ID.RIFLE_0]:
                self.weapons[ID.RIFLE_0] = 1
                self.switch_weapon(ID.RIFLE_0)
        elif item.tex_id == ID.KEY:
            self.key = 1

        self.play(self.sound.pick_up[item.tex_id])

        del self.item_map[self.tile_pos]

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == cfg.KEYS['INTERACT']:
                self.interact_with_door()

            # weapon hotkeys
            if event.key == cfg.KEYS['WEAPON_1']:
                self.switch_weapon(weapon_id=ID.KNIFE_0)
            elif event.key == cfg.KEYS['WEAPON_2']:
                self.switch_weapon(weapon_id=ID.PISTOL_0)
            elif event.key == cfg.KEYS['WEAPON_3']:
                self.switch_weapon(weapon_id=ID.RIFLE_0)

        # weapon cycling
        if event.type == pg.MOUSEWHEEL:
            self.weapon_id = next(filter(
                lambda id: self.weapons[id] == 1,
                self.weapon_cycle
            ))
            self.switch_weapon(weapon_id=self.weapon_id)

        # shoot
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.shoot()

    def switch_weapon(self, weapon_id):
        if self.weapons[weapon_id] == 1:
            self.weapon_id = weapon_id
            self.weapon_instance.weapon_id = weapon_id

    def shoot(self):
        if self.weapon_id == ID.KNIFE_0:
            self.is_shooting = True
            self.check_npc_hit()
            self.play(self.sound.player_attack[ID.KNIFE_0])
        elif self.ammo:
            consumption = cfg.WEAPON_SETTINGS[self.weapon_id]['ammo_consumption']

            if not self.is_shooting and self.ammo >= consumption:
                self.is_shooting = True
                self.check_npc_hit()
                self.ammo -= consumption
                self.ammo = max(0, self.ammo)
                self.play(self.sound.player_attack[self.weapon_id])

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

        self.check_health()
        self.update_tile_pos()
        self.pick_up_item()

    def check_health(self):
        if self.health <= 0:
            self.play(self.sound.player_death)
            #
            pg.time.wait(5000)
            self.eng.player_attribs = PlayerAttribs()
            self.eng.new_game()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()

        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * cfg.MOUSE_SENSITIVITY)

        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * cfg.MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        velocity = cfg.PLAYER_SPEED * self.app.delta_time
        next_step = glm.vec2()

        if key_state[cfg.KEYS['FORWARD']]:
            next_step = self.move_forward(velocity)

        if key_state[cfg.KEYS['STRAFE_L']]:
            next_step = self.move_left(velocity)

        if key_state[cfg.KEYS['BACK']]:
            next_step = self.move_back(velocity)

        if key_state[cfg.KEYS['STRAFE_R']]:
            next_step = self.move_right(velocity)

       # if key_state[pg.K_q]:
       #     self.move_up(velocity)
       # if key_state[pg.K_e]:
       #     self.move_down(velocity)

        self.move(next_step)

    def move(self, next_step):
        if not self.is_collide(dx=next_step[0]):
            self.position.x += next_step[0]

        if not self.is_collide(dz=next_step[1]):
            self.position.z += next_step[1]

    def is_collide(self, dx=0, dz=0):
        int_pos = (
            int(self.position.x + dx + self.collide_range(dx)),
            int(self.position.z + dz + self.collide_range(dz))
        )

        if int_pos in self.door_map:
            return self.door_map[int_pos].is_closed

        return int_pos in self.wall_map

    def collide_range(self, delta):
        if delta > 0:
            return cfg.PLAYER_SIZE
        elif delta < 0:
            return -cfg.PLAYER_SIZE
        else:
            return 0

    def interact_with_door(self):
        pos = self.position + self.forward
        int_pos = int(pos.x), int(pos.z)

        if int_pos not in self.door_map:
            return None

        door = self.door_map[int_pos]

        if self.key and door.tex_id == ID.KEY_DOOR:
            door.is_closed = not door.is_closed
            self.play(self.sound.player_missed)
            # next level
            pg.time.wait(300)

            self.eng.player_attribs.update(player=self)
            self.eng.player_attribs.num_level += 1
            self.eng.player_attribs.num_level %= cfg.NUM_LEVELS
            self.eng.new_game()
        else:
            door.is_moving = True
            self.play(self.sound.open_door)
            door.is_moving = True

            self.play(self.sound.open_door)
