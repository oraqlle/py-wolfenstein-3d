from meshes.level_mesh import LevelMesh
from meshes.instanced_quad_mesh import InstancedQuadMesh


class Scene:
    def __init__(self, eng):
        self.eng = eng

        # door objects
        self.doors = self.eng.level_map.door_map.values()

        # door mesh
        self.instanced_door_mesh = InstancedQuadMesh(
            self.eng,
            self.doors,
            self.eng.shader_program.instanced_door
        )

        # level mesh
        self.level_mesh = LevelMesh(self.eng)

    def update(self):
        for door in self.doors:
            door.update()

    def render(self):
        self.level_mesh.render()
        self.instanced_door_mesh.render()
