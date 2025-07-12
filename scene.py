from game_objects.hud import HUD
from meshes.level_mesh import LevelMesh
from meshes.instanced_quad_mesh import InstancedQuadMesh
from game_objects.weapon import Weapon
from meshes.weapon_mesh import WeaponMesh


class Scene:
    def __init__(self, eng):
        self.eng = eng

        # door objects and mesh
        self.doors = self.eng.level_map.door_map.values()
        self.instanced_door_mesh = InstancedQuadMesh(
            self.eng,
            self.doors,
            self.eng.shader_program.instanced_door
        )

        # item objects and mesh
        self.items = self.eng.level_map.item_map.values()
        self.instanced_item_mesh = InstancedQuadMesh(
            self.eng,
            self.items,
            self.eng.shader_program.instanced_billboard
        )

        # npc objects
        self.npcs = self.eng.level_map.npc_map.values()
        self.instanced_npcs_mesh = InstancedQuadMesh(
            self.eng,
            self.npcs,
            self.eng.shader_program.instanced_billboard
        )

        # objects objects and mesh
        self.hud = HUD(eng)
        self.instanced_hud_mesh = InstancedQuadMesh(
            self.eng,
            self.hud.objects,
            self.eng.shader_program.instanced_hud
        )

        # weapon objects and 'HUD' meshes
        self.weapon = Weapon(eng)
        self.waepon_mesh = WeaponMesh(
                eng,
                self.weapon,
                self.eng.shader_program.weapon
        )

        # level mesh
        self.level_mesh = LevelMesh(self.eng)

    def update(self):
        for door in self.doors:
            door.update()

        for item in self.items:
            item.update()

        for npc in self.npcs:
            npc.update()

        self.hud.update()
        self.weapon.update()

    def render(self):
        self.level_mesh.render()
        self.instanced_door_mesh.render()
        self.instanced_item_mesh.render()
        self.instanced_npcs_mesh.render()
        self.instanced_hud_mesh.render()
        self.waepon_mesh.render()
