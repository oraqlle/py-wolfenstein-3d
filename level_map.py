import glm
import pytmx
import settings as cfg
from game_objects.door import Door


class LevelMap:
    def __init__(self, eng, tmx_file='test.tmx'):
        self.eng = eng
        self.tiled_map = pytmx.TiledMap(f'resources/levels/{tmx_file}')
        self.gid_map = self.tiled_map.tiledgidmap

        self.width = self.tiled_map.width
        self.depth = self.tiled_map.height

        self.wall_map = {}
        self.floor_map = {}
        self.ceiling_map = {}

        self.door_map = {}
        self.parse_level()

    def get_id(self, gid):
        return self.gid_map[gid] - 1

    def parse_level(self):
        # player spawn location obj
        player = self.tiled_map.get_layer_by_name('player').pop()
        player_pos = glm.vec3(
            player.x / cfg.TEX_SIZE,
            cfg.PLAYER_HEIGHT,
            player.y / cfg.TEX_SIZE
        )
        self.eng.player.position = player_pos

        walls = self.tiled_map.get_layer_by_name('walls')
        floors = self.tiled_map.get_layer_by_name('floors')
        ceilings = self.tiled_map.get_layer_by_name('ceilings')

        for ix in range(self.width):
            for iz in range(self.depth):
                if gid := walls.data[iz][ix]:
                    # wall hash map
                    self.wall_map[(ix, iz)] = self.get_id(gid)

                if gid := floors.data[iz][ix]:
                    # floor hash map
                    self.floor_map[(ix, iz)] = self.get_id(gid)

                if gid := ceilings.data[iz][ix]:
                    # ceiling hash map
                    self.ceiling_map[(ix, iz)] = self.get_id(gid)

        # get doors
        door_objects = self.tiled_map.get_layer_by_name('doors')

        for obj in door_objects:
            pos = int(obj.x / cfg.TEX_SIZE), int(obj.y / cfg.TEX_SIZE)
            door = Door(self, tex_id=self.get_id(obj.gid), x=pos[0], z=pos[1])
            self.door_map[pos] = door

        self.eng.player.wall_map = self.wall_map
        self.eng.player.door_map = self.door_map
