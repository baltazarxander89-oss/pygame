import pygame
import math
from settings import WHITE

class ProjectileManager:
    def __init__(self):
        self.bullets = []

    def reset(self):
        self.bullets.clear()

    def shoot(self, player, mouse_x, mouse_y, camera):
        world_mx = mouse_x + camera.x
        world_my = mouse_y + camera.y

        px = player.x + player.size // 2
        py = player.y + player.size // 2

        dx = world_mx - px
        dy = world_my - py

        dist = math.sqrt(dx * dx + dy * dy)

        if dist != 0:
            dx /= dist
            dy /= dist

        self.bullets.append([px, py, dx, dy])

    def update(self, map_width, map_height):
        for b in self.bullets[:]:
            b[0] += b[2] * 10
            b[1] += b[3] * 10

            if b[0] < 0 or b[0] > map_width or b[1] < 0 or b[1] > map_height:
                self.bullets.remove(b)

    def handle_enemy_collision(self, enemy_manager, attack_multiplier):
        kills_added = 0
        points_added = 0
        killed_positions = []

        for e in enemy_manager.enemies[:]:
            for b in self.bullets[:]:
                if abs(e[0] - b[0]) < 20 and abs(e[1] - b[1]) < 20:
                    self.bullets.remove(b)
                    e[2] -= 1 * attack_multiplier

                    if e[2] <= 0:
                        enemy_manager.enemies.remove(e)
                        kills_added += 1
                        points_added += 10
                        killed_positions.append((e[0], e[1]))

                    break

        return kills_added, points_added, killed_positions

    def draw(self, screen, camera):
        for b in self.bullets:
            screen_x = int(b[0] - camera.x)
            screen_y = int(b[1] - camera.y)

            pygame.draw.circle(screen, WHITE, (screen_x, screen_y), 5)