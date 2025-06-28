from shader_program import ShaderProgram
from player import Player
from scene import Scene
from textures import Textures
from level_map import LevelMap


class Engine:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = Textures(self)

        self.player = None
        self.shader_program = None
        self.scene = None

        self.level_map = None

        self.new_game()

    def new_game(self):
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.level_map = LevelMap(self, tmx_file='level_0.tmx')
        self.scene = Scene(self)

    def handle_events(self, event):
        self.player.handle_events(event)

    def update(self):
        self.player.update()
        self.shader_program.update()
        self.scene.update()

    def render(self):
        self.scene.render()
