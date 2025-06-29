import glm
import pygame as pg
import settings as cfg
from camera import Camera


class Player(Camera):
    def __init__(self, eng, position=cfg.PLAYER_POS, yaw=0, pitch=0):
        self.app = eng.app
        self.eng = eng
        super().__init__(position, yaw, pitch)

        # these maps will update when instantiated LevelMap
        self.wall_map = None
        self.door_map = None

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == cfg.KEYS['INTERACT']:
                self.interact_with_door()

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

        if int_pos in self.door_map:
            door = self.door_map[int_pos]
            door.is_moving = True
