import settings as cfg
import moderngl as mgl
import pygame as pg
import sys
from engine import Engine


class Game:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, cfg.MAJOR_VER)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, cfg.MINOR_VER)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, cfg.DEPTH_SIZE)

        pg.display.set_mode(cfg.WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.delta_time = 0.0
        self.time = 0.0

        pg.mouse.set_visible(False)
        # Must be after setting visibility off to correctly setup virtual
        # input for mouse
        pg.event.set_grab(True)

        self.is_running = True
        self.engine = Engine(self)

    def update(self):
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f'{self.clock.get_fps():.0f}')

        self.engine.update()

    def render(self):
        self.ctx.clear(color=cfg.BG_COLOUR)
        self.engine.render()
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        pg.quit()
        sys.exit()


if __name__ == '__main__':
    app = Game()
    app.run()
