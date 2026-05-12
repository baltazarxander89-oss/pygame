from settings import WIDTH, HEIGHT

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, player_x, player_y, map_width, map_height):
        self.x = player_x - WIDTH // 2
        self.y = player_y - HEIGHT // 2

        self.x = max(0, min(max(0, map_width - WIDTH), self.x))
        self.y = max(0, min(max(0, map_height - HEIGHT), self.y))

        self.x = int(self.x)
        self.y = int(self.y)

    def reset(self):
        self.x = 0
        self.y = 0