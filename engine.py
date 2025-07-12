from shader_program import ShaderProgram
from player import Player
from scene import Scene
from textures import Textures
from sound import Sound
from ray_casting import RayCasting
from level_map import LevelMap
import pygame as pg


class Engine:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = Textures(self)
        self.sound = Sound()

        self.player = None
        self.shader_program = None
        self.scene = None

        self.level_map = None
        self.ray_casting: RayCasting = None

        self.new_game()

    def new_game(self):
        pg.mixer.music.play(-1)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.level_map = LevelMap(self, tmx_file='level_0.tmx')
        self.ray_casting = RayCasting(self)
        self.scene = Scene(self)

    def handle_events(self, event):
        self.player.handle_events(event)

    def update(self):
        self.player.update()
        self.shader_program.update()
        self.scene.update()

    def render(self):
        self.scene.render()
