import pygame
import random
import math

class EnemyManager:
    def __init__(self, assets):
        self.assets = assets
        self.enemies = []
        self.anim_timer = 0
        self.anim_index = 0

    def reset(self):
        self.enemies.clear()
        self.anim_timer = 0
        self.anim_index = 0

    def spawn_enemy(self, stage_level, map_width, map_height, collision_rects):
        while True:
            x = random.randint(100, map_width - 100)
            y = random.randint(100, map_height - 100)

            enemy_rect = pygame.Rect(x, y, 40, 40)

            blocked = False
            for wall in collision_rects:
                if enemy_rect.colliderect(wall):
                    blocked = True
                    break

            if not blocked:
                break

        if stage_level == 1:
            if random.randint(1, 5) == 1:
                return [x, y, 3, "tank"]

            return [x, y, 1, "normal"]

        if random.randint(1, 4) == 1:
            return [x, y, 5, "elite"]

        return [x, y, 2, "normal2"]

    def update_animation(self):
        self.anim_timer += 1

        if self.anim_timer >= 20:
            self.anim_timer = 0
            self.anim_index += 1

    def update_ai(self, player, collision_rects, map_width, map_height):
        for e in self.enemies[:]:
            dx = player.x - e[0]
            dy = player.y - e[1]

            dist = math.sqrt(dx * dx + dy * dy)

            if dist != 0:
                dx /= dist
                dy /= dist

                speed_enemy = 1.0 if e[3] in ["tank", "elite"] else 1.5

                new_enemy_x = e[0] + dx * speed_enemy
                enemy_rect_x = pygame.Rect(new_enemy_x, e[1], 40, 40)

                blocked_x = False
                for wall in collision_rects:
                    if enemy_rect_x.colliderect(wall):
                        blocked_x = True
                        break

                if not blocked_x:
                    e[0] = new_enemy_x

                new_enemy_y = e[1] + dy * speed_enemy
                enemy_rect_y = pygame.Rect(e[0], new_enemy_y, 40, 40)

                blocked_y = False
                for wall in collision_rects:
                    if enemy_rect_y.colliderect(wall):
                        blocked_y = True
                        break

                if not blocked_y:
                    e[1] = new_enemy_y

                e[0] = max(0, min(map_width - 40, e[0]))
                e[1] = max(0, min(map_height - 40, e[1]))

            if abs(e[0] - player.x) < 40 and abs(e[1] - player.y) < 40:
                player.hp -= 1

    def draw(self, screen, camera, player):
        for e in self.enemies:
            screen_x = int(e[0] - camera.x)
            screen_y = int(e[1] - camera.y)

            if e[3] == "normal":
                frames = self.assets.enemy_normal_frames
            elif e[3] == "tank":
                frames = self.assets.enemy_tank_frames
            else:
                frames = self.assets.enemy_normal_frames

            enemy_img = frames[self.anim_index % len(frames)]

            if player.x < e[0]:
                enemy_img = pygame.transform.flip(enemy_img, True, False)

            screen.blit(
                enemy_img,
                (
                    screen_x - enemy_img.get_width() // 2,
                    screen_y - enemy_img.get_height() // 2
                )
            )