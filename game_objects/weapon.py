import settings as cfg
import glm
from game_objects.game_object import GameObject


class Weapon(GameObject):
    def __init__(self, eng):
        self.eng = eng
        self.app = eng.app

        self.player = eng.player
        self.weapon_id = self.player.weapon_id
        self.player.weapon_instance = self

        self.pos = cfg.WEAPON_POS
        self.rot = 0
        self.scale = glm.vec3(
            cfg.WEAPON_SCALE / cfg.ASPECT_RATIO,
            cfg.WEAPON_SCALE,
            0
        )
        self.m_model = self.get_model_matrix()

        self.frame = 0
        self.anim_counter = 0

    def update(self):
        if self.player.is_shooting and self.app.anim_trigger:
            self.anim_counter += 1

            if self.anim_counter == cfg.WEAPON_ANIM_PERIODS:
                self.anim_counter = 0
                self.frame += 1

                if self.frame == cfg.WEAPON_NUM_FRAMES:
                    self.frame = 0
                    self.player.is_shooting = False
