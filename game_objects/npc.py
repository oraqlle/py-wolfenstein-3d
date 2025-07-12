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

        self.m_model = self.get_model_matrix()

    def update(self):
        pass
