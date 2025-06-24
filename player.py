import pygame as pg
import settings as cfg
from camera import Camera


class Player(Camera):
    def __init__(self, eng, position=cfg.PLAYER_POS, yaw=-90, pitch=0):
        self.app = eng.app
        self.eng = eng
        super().__init__(position, yaw, pitch)

    def handle_events(self, events):
        pass

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()

        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * cfg.MOUSE_SENSITIVITY)

        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * cfg.MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        velocity = cfg.PLAYER_SPEED * self.app.delta_time

        if key_state[pg.K_w]:
            self.move_forward(velocity)

        if key_state[pg.K_a]:
            self.move_left(velocity)

        if key_state[pg.K_s]:
            self.move_back(velocity)

        if key_state[pg.K_d]:
            self.move_right(velocity)

        if key_state[pg.K_q]:
            self.move_up(velocity)

        if key_state[pg.K_e]:
            self.move_down(velocity)
