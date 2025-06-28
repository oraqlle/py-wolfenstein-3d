import glm
import pytmx
import settings as cfg


class LevelMap:
    def __init__(self, eng, tmx_file='test.tmx'):
        self.eng = eng
        self.tiled_map = pytmx.TiledMap(f'resources/levels/{tmx_file}')
        self.gid_map = self.tiled_map.tiledgidmap

        self.width = self.tiled_map.width
        self.depth = self.tiled_map.height

        self.wall_map = {}
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

        for ix in range(self.width):
            for iz in range(self.depth):
                if gid := walls.data[iz][ix]:
                    # wall hash map
                    self.wall_map[(ix, iz)] = self.get_id(gid)
