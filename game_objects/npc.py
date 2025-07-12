import settings as cfg
import random as rnd
import glm
from game_objects.game_object import GameObject
from game_objects.item import Item
from typing import Tuple


class NPC(GameObject):
    def __init__(self, level_map, tex_id, x, z):
        super().__init__(level_map, tex_id, x, z)

        self.level_map = level_map
        self.player = self.eng.player
        self.npc_id = tex_id

        self.scale = cfg.NPC_SETTINGS[self.npc_id]['scale']
        self.speed = cfg.NPC_SETTINGS[self.npc_id]['speed']
        self.size = cfg.NPC_SETTINGS[self.npc_id]['size']
        self.attack_dist = cfg.NPC_SETTINGS[self.npc_id]['attack_dist']
        self.health = cfg.NPC_SETTINGS[self.npc_id]['health']
        self.damage = cfg.NPC_SETTINGS[self.npc_id]['damage']
        self.hit_probability = cfg.NPC_SETTINGS[self.npc_id]['hit_probability']
        self.item_to_drop = cfg.NPC_SETTINGS[self.npc_id]['drop_item']

        self.anim_periods = cfg.NPC_SETTINGS[self.npc_id]['anim_periods']
        self.anim_counter = 0
        self.frame = 0
        self.is_animated = True

        # states: walk, attack, hurt, death
        self.num_frames = None
        self.state_tex_id = None
        self.set_state(state='walk')

        self.is_player_spotted: bool = False
        self.path_to_player: Tuple[int, int] = None
        self.tile_pos: Tuple[int, int] = None

        self.is_alive = True
        self.is_hurt = False

        self.play = self.eng.sound.play
        self.sound = self.eng.sound

        self.m_model = self.get_model_matrix()

    def update(self):
        if self.is_hurt:
            self.set_state(state='hurt')
        elif self.health > 0:
            self.update_tile_position()
            self.ray_to_player()
            self.get_path_to_player()

            if not self.attack():
                self.move_to_player()
        else:
            self.is_alive = False
            self.set_state(state='death')

        self.animate()

        # set current texture
        self.tex_id = self.state_tex_id + self.frame

    def attack(self):
        if not self.is_player_spotted:
            return False

        if glm.length(self.player.position.xz - self.pos.xz) > self.attack_dist:
            return False

        dir_to_player = glm.normalize(self.player.position - self.pos)

        if self.eng.ray_casting.run(self.pos, dir_to_player):
            self.set_state(state='attack')

            if self.app.sound_trigger:
                self.play(self.sound.enemy_attack[self.npc_id])

            if rnd.random() < self.hit_probability:
                self.player.health -= self.damage
                self.play(self.sound.player_hurt)

            return True

    def take_damage(self):
        self.health -= cfg.WEAPON_SETTINGS[self.player.weapon_id]['damage']
        self.is_hurt = True

        if not self.is_player_spotted:
            self.is_player_spotted = True

    def ray_to_player(self):
        if not self.is_player_spotted:
            dir_to_player = glm.normalize(self.player.position - self.pos)

            if self.eng.ray_casting.run(self.pos, dir_to_player):
                self.is_player_spotted = True
                self.play(self.sound.spotted[self.npc_id])

    def get_path_to_player(self):
        if not self.is_player_spotted:
            return None

        self.path_to_player = self.eng.path_finder.find(
            start_pos=self.tile_pos,
            end_pos=self.player.tile_pos
        )

    def move_to_player(self):
        if not self.path_to_player:
            return None

        self.set_state(state='walk')

        dir_vec = glm.normalize(
            glm.vec2(self.path_to_player) + cfg.HALF_WALL_SIZE - self.pos.xz
        )
        delta_vec = dir_vec * self.speed * self.app.delta_time

        # collisions
        if not self.check_collision(dx=delta_vec.x):
            self.pos.x += delta_vec.x
        if not self.check_collision(dz=delta_vec.y):
            self.pos.z += delta_vec.y

        # open doors
        door_map = self.level_map.door_map
        if self.tile_pos in door_map:
            door = door_map[self.tile_pos]
            if door.is_closed:
                door.is_moving = True

        # translate
        self.m_model = self.get_model_matrix()

    def check_collision(self, dx=0, dz=0):
        int_pos = (
            int(self.pos.x + dx + (self.size if dx >
                0 else -self.size if dx < 0 else 0)),
            int(self.pos.z + dz + (self.size if dz >
                0 else -self.size if dz < 0 else 0))
        )

        return (int_pos in self.level_map.wall_map or
                int_pos in (self.level_map.npc_map.keys() - {self.tile_pos}))

    def update_tile_position(self):
        self.tile_pos = int(self.pos.x), int(self.pos.z)

    def set_state(self, state='walk'):
        self.num_frames = cfg.NPC_SETTINGS[self.npc_id]['num_frames'][state]
        self.state_tex_id = cfg.NPC_SETTINGS[self.npc_id]['state_tex_id'][state]
        self.frame %= self.num_frames

    def animate(self):
        if not (self.is_animated and self.app.anim_trigger):
            return None

        self.anim_counter += 1

        if self.anim_counter == self.anim_periods:
            self.anim_counter = 0
            self.frame = (self.frame + 1) % self.num_frames

            if self.is_hurt:
                self.is_hurt = False

            elif not self.is_alive and self.frame == self.num_frames - 1:
                self.is_animated = False
                self.drop_item()
                self.play(self.eng.sound.death[self.npc_id])

    def drop_item(self):
        if self.item_to_drop is not None:
            self.level_map.item_map[self.tile_pos] = Item(
                self.level_map,
                self.item_to_drop,
                x=self.tile_pos[0],
                z=self.tile_pos[1]
            )
