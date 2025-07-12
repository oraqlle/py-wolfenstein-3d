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
        self.drop_item = cfg.NPC_SETTINGS[self.npc_id]['drop_item']

        self.anim_periods = cfg.NPC_SETTINGS[self.npc_id]['anim_periods']
        self.anim_counter = 0
        self.frame = 0
        self.is_animated = True

        # states: walk, attack, hurt, death
        self.num_frames = None
        self.state_tex_id = None
        self.set_state(state='walk')

        self.is_player_spotted: bool = False
        self.tile_pos: Tuple[int, int] = None

        self.is_alive = True
        self.is_hurt = False

        self.play = self.eng.sound.play
        self.sound = self.eng.sound

        self.m_model = self.get_model_matrix()

    def update(self):
        self.update_tile_position()
        self.ray_to_player()
        self.animate()

        # set current texture
        self.tex_id = self.state_tex_id + self.frame

    def ray_to_player(self):
        if not self.is_player_spotted:
            dir_to_player = glm.normalize(self.player.position - self.pos)

            if self.eng.ray_casting.run(self.pos, dir_to_player):
                self.is_player_spotted = True
                self.play(self.sound.spotted[self.npc_id])

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
