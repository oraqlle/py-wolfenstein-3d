import moderngl as mgl
import settings as cfg
import glm


class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.ctx = app.ctx

        # -------- shaders -------- #
        self.level = self.get_program(shader_name='level')
        self.instanced_door = self.get_program(shader_name='instanced_door')
        self.instanced_item = self.get_program(shader_name='instanced_item')
        self.instanced_hud = self.get_program(shader_name='instanced_hud')
        # ------------------------- #

        self.set_uniform_on_init()

    def set_uniform_on_init(self):
        # level
        self.level['m_proj'].write(self.player.m_proj)
        self.level['u_texture_array_0'] = cfg.TEXTURE_UNIT_0

        # instanced door
        self.instanced_door['m_proj'].write(self.player.m_proj)
        self.instanced_door['u_texture_array_0'] = cfg.TEXTURE_UNIT_0

        # instanced item
        self.instanced_item['m_proj'].write(self.player.m_proj)
        self.instanced_item['u_texture_array_0'] = cfg.TEXTURE_UNIT_0

        # instanced HUD object
        self.instanced_hud['u_texture_array_0'] = cfg.TEXTURE_UNIT_0

    def update(self):
        self.level['m_view'].write(self.player.m_view)
        self.instanced_door['m_view'].write(self.player.m_view)
        self.instanced_item['m_view'].write(self.player.m_view)

    def get_program(self, shader_name: str) -> mgl.Program:
        with open(f'shaders/{shader_name}.vert') as vert:
            vertex_shader = vert.read()

        with open(f'shaders/{shader_name}.frag') as frag:
            fragment_shader = frag.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
