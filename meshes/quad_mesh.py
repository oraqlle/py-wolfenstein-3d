import numpy as np
from meshes.base_mesh import BaseMesh


class QuadMesh(BaseMesh):
    def __init__(self, app, shader_program):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = shader_program

        self.vbo_format = '4f 2f'
        self.attrs = ('in_position', 'in_uv')
        self.vao = self.get_vao()

    def get_vertex_data(self):
        vertices = [
            (0.5, 0.5, 0.0), (-0.5, 0.5, 0.0), (-0.5, -0.5, 0.0),
            (0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0),
        ]

        colours = [
            (0, 1, 0), (1, 0, 0), (1, 1, 0),
            (0, 1, 0), (1, 1, 0), (0, 0, 1),
        ]

        vertex_data = np.hstack([vertices, colours], dtype='float32')
        return vertex_data
