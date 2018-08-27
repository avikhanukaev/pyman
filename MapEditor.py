from Consts import map_objects, colors, screen_resolution
import Consts
import pygame
from Map import Map, MapView


class MapEditor:

    def __init__(self):
        self.display = pygame.display.set_mode([screen_resolution['w'], screen_resolution['h']])
        pygame.display.set_caption("PyMan MapEditor")
        self.map_controller = Map()
        self.map_view = MapView(self.map_controller, self.display)
        self.quit_editor = False
        self.clock = pygame.time.Clock()

    @property
    def mouse_rect(self):
        x, y = pygame.mouse.get_pos()
        return [int(x / Consts.slice_width), int(y / Consts.slice_height)]

    def mouse_click(self):
        left, middle, right = pygame.mouse.get_pressed()
        col, row = self.mouse_rect
        if left:
            self.map_controller.set(row, col, map_obj='border')
        elif right:
            self.map_controller.set(row, col, map_obj='empty')

    def save_map(self):
        fd = open('./new_map.map', 'w')
        fd.write(str(self.map_controller))
        fd.close()

    def run(self):
        while not self.quit_editor:
            self.map_view.show()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_editor = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if pygame.key.get_mods() & pygame.KMOD_LCTRL:
                            self.save_map()
            self.clock.tick(20)
        pygame.quit()


MapEditor().run()

