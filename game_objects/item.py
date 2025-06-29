import glm
import settings as cfg
from game_objects.game_object import GameObject


class Item(GameObject):
    def __init__(self, level_map, tex_id, x, z):
        super().__init__(level_map, tex_id, x, z)

        self.scale = glm.vec3(cfg.ITEM_SETTINGS[tex_id]['scale'])
        self.m_model = self.get_model_matrix()

    def update(self):
        pass
