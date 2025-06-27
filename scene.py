from meshes.level_mesh import LevelMesh
from meshes.quad_mesh import QuadMesh


class Scene:
    def __init__(self, eng):
        self.eng = eng
        self.quad = QuadMesh(eng.app, eng.shader_program)
        #self.level_mesh = LevelMesh(self.eng)

    def update(self):
        pass

    def render(self):
        self.quad.render()
