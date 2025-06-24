from meshes.quad_mesh import QuadMesh


class Scene:
    def __init__(self, eng):
        self.eng = eng
        self.quad = QuadMesh(self.eng.app, self.eng.shader_program.quad)

    def update(self):
        pass

    def render(self):
        self.quad.render()
