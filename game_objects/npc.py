import settings as cfg
import random as rnd
from game_objects.game_object import GameObject
from game_objects.item import Item


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

        self.m_model = self.get_model_matrix()

    def update(self):
        self.animate()

        # set current texture
        self.tex_id = self.state_tex_id + self.frame

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
