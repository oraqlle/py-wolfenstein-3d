import moderngl as mgl
import numpy as np
from collections.abc import Iterable
from game_objects.game_object import GameObject
from meshes.quad_mesh import QuadMesh


class InstancedQuadMesh:
    def __init__(self, eng, objects: Iterable[GameObject], shader_program: mgl.Program):
        self.ctx = eng.app.ctx
        self.program = shader_program

        self.objects = objects
        self.num_instances = len(objects)

        # quad buffers for instancing
        self.quad_vbo = self.ctx.buffer(QuadMesh.get_vertex_data(self))

        # data buffers for instancing
        self.m_model_vbo: mgl.Buffer = None
        self.tex_id_vbo: mgl.Buffer = None

        self.vao = self.get_vao()

    def update_buffers(self):
        m_model_list, tex_id_list = [], []

        for obj in self.objects:
            m_model_list += sum(obj.m_model.to_list(), [])
            tex_id_list += [obj.tex_id]

        self.m_model_vbo = self.ctx.buffer(np.array(m_model_list, dtype='float32'))
        self.tex_id_vbo = self.ctx.buffer(np.array(tex_id_list, dtype='int32'))

    def get_vao(self):
        self.update_buffers()

        vao = self.ctx.vertex_array(
            self.program,
            [
                (self.quad_vbo, '4f 2f /v', 'in_position', 'in_uv'),  # per vertex
                (self.m_model_vbo, '16f /i', 'm_model',),  # per instance
                (self.tex_id_vbo, '1i /i', 'in_tex_id'),  # per instance
            ],
            skip_errors=True
        )

        return vao

    def render(self):
        if len(self.objects):
            self.vao = self.get_vao()
            self.vao.render(instances=self.num_instances)
