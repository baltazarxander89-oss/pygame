import pygame
import pytmx

class MapManager:
    def __init__(self):
        self.tmx_data = pytmx.load_pygame("map/map2.tmx")

        self.map_img = pygame.image.load("map/map2.png").convert_alpha()
        self.floor_img = pygame.image.load("map/floor.png").convert_alpha()
        self.props_img = pygame.image.load("map/props.png").convert_alpha()

        self.width = self.map_img.get_width()
        self.height = self.map_img.get_height()

        self.floor_img = pygame.transform.scale(self.floor_img, (self.width, self.height))
        self.props_img = pygame.transform.scale(self.props_img, (self.width, self.height))

        self.collision_rects = []

        for layer in self.tmx_data.objectgroups:
            if layer.name == "collision":
                for obj in layer:
                    self.collision_rects.append(
                        pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    )

    def draw_floor(self, screen, camera):
        screen.blit(self.floor_img, (-int(camera.x), -int(camera.y)))

    def draw_props(self, screen, camera):
        screen.blit(self.props_img, (-int(camera.x), -int(camera.y)))