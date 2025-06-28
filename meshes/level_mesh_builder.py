import numpy as np


class LevelMeshBuilder:
    def __init__(self, mesh):
        self.mesh = mesh
        self.map = mesh.eng.level_map

    def add_data(self, vertex_data, index, *vertices):
        for vertex in vertices:
            for attr in vertex:
                vertex_data[index] = attr
                index += 1

        return index

    def is_blocked(self, x, z):
        if not (0 <= x < self.map.width and 0 <= z < self.map.depth):
            return True

        return (x, z) in self.map.wall_map

    def build_mesh(self):
        vertex_data = np.empty(
            [self.map.width * self.map.depth * self.mesh.fmt_size * 18],
            dtype='uint16'
        )

        index = 0

        for x in range(self.map.width):
            for z in range(self.map.depth):
                # flats
                if pos_not_in_wall_map := (x, z) not in self.map.wall_map:
                    # floor
                    if (x, z) in self.map.floor_map:
                        tex_id = self.map.floor_map[(x, z)]
                        face_id = 0

                        v0 = (x    , 0, z    , tex_id, face_id)
                        v1 = (x + 1, 0, z    , tex_id, face_id)
                        v2 = (x + 1, 0, z + 1, tex_id, face_id)
                        v3 = (x    , 0, z + 1, tex_id, face_id)

                        index = self.add_data(
                            vertex_data,
                            index,
                            v0, v3, v2, v0, v2, v1
                        )

                    # ceiling
                    if (x, z) in self.map.ceiling_map:
                        tex_id = self.map.ceiling_map[(x, z)]
                        face_id = 1

                        v0 = (x    , 1, z    , tex_id, face_id)
                        v1 = (x + 1, 1, z    , tex_id, face_id)
                        v2 = (x + 1, 1, z + 1, tex_id, face_id)
                        v3 = (x    , 1, z + 1, tex_id, face_id)

                        index = self.add_data(
                            vertex_data,
                            index,
                            v0, v2, v3, v0, v1, v2
                        )

                # wall faces
                if pos_not_in_wall_map:
                    continue

                tex_id = self.map.wall_map[(x, z)]

                # wall back face
                if not self.is_blocked(x, z - 1):
                    face_id = 2

                    # fmt: off
                    v0 = (x    , 0, z, tex_id, face_id)
                    v1 = (x    , 1, z, tex_id, face_id)
                    v2 = (x + 1, 1, z, tex_id, face_id)
                    v3 = (x + 1, 0, z, tex_id, face_id)
                    # fmt: on

                    index = self.add_data(
                        vertex_data,
                        index,
                        v0, v1, v2, v0, v2, v3
                    )

                # wall front face
                if not self.is_blocked(x, z + 1):
                    face_id = 3

                    # fmt: off
                    v0 = (x    , 0, z + 1, tex_id, face_id)
                    v1 = (x    , 1, z + 1, tex_id, face_id)
                    v2 = (x + 1, 1, z + 1, tex_id, face_id)
                    v3 = (x + 1, 0, z + 1, tex_id, face_id)
                    # fmt: on

                    index = self.add_data(
                        vertex_data,
                        index,
                        v0, v2, v1, v0, v3, v2
                    )

                # wall right face
                if not self.is_blocked(x + 1, z):
                    face_id = 4

                    # fmt: off
                    v0 = (x + 1, 0, z    , tex_id, face_id)
                    v1 = (x + 1, 1, z    , tex_id, face_id)
                    v2 = (x + 1, 1, z + 1, tex_id, face_id)
                    v3 = (x + 1, 0, z + 1, tex_id, face_id)
                    # fmt: on

                    index = self.add_data(
                        vertex_data,
                        index,
                        v0, v1, v2, v0, v2, v3
                    )

                # wall left face
                if not self.is_blocked(x - 1, z):
                    face_id = 5

                    # fmt: off
                    v0 = (x, 0, z    , tex_id, face_id)
                    v1 = (x, 1, z    , tex_id, face_id)
                    v2 = (x, 1, z + 1, tex_id, face_id)
                    v3 = (x, 0, z + 1, tex_id, face_id)
                    # fmt: on

                    index = self.add_data(
                        vertex_data,
                        index,
                        v0, v2, v1, v0, v3, v2
                    )

        return vertex_data[:index]
