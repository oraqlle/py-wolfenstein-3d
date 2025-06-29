import glm
from game_objects.game_object import GameObject


class Door(GameObject):
    def __init__(self, level_map, tex_id, x, z):
        super().__init__(level_map, tex_id, x, z)

        self.rot = self.get_rot(x, z)
        self.m_model = self.get_model_matrix()

    def update(self):
        pass

    def get_rot(self, x, z):
        wall_map = self.level_map.wall_map
        if (x, z - 1) in wall_map and (x, z + 1) in wall_map:
            return glm.half_pi()
        return 0
