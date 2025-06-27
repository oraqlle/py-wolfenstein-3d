from meshes.level_mesh import LevelMesh


class Scene:
    def __init__(self, eng):
        self.eng = eng
        self.level_mesh = LevelMesh(self.eng)

    def update(self):
        pass

    def render(self):
        self.level_mesh.render()
