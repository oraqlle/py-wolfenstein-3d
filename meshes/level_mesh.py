from meshes.base_mesh import BaseMesh
from meshes.level_mesh_builder import LevelMeshBuilder


class LevelMesh(BaseMesh):
    def __init__(self, eng):
        super().__init__()

        self.eng = eng
        self.ctx = self.eng.ctx
        self.program = self.eng.shader_program.level

        self.vbo_format = '3u2 1u2 1u2'
        self.fmt_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())

        self.attrs = ('in_position', 'in_tex_id', 'face_id')

        self.mesh_builder = LevelMeshBuilder(self)
        self.vao = self.get_vao()

    def get_vertex_data(self):
        vertex_data = self.mesh_builder.build_mesh()
        print(f'Num level vertices: {len(vertex_data) // 5 * 3}')
        return vertex_data
