import pygame
import math
from settings import BOSS_SIZE, BOSS_MAX_HP, RED, GREEN, BLACK, WHITE

class Boss:
    def __init__(self, assets):
        self.assets = assets
        self.x = 400
        self.y = 100
        self.size = BOSS_SIZE
        self.hp = BOSS_MAX_HP
        self.max_hp = BOSS_MAX_HP
        self.timer = 0
        self.alive = False

        self.anim_timer = 0
        self.anim_index = 0

        self.enemy_bullets = []

    def reset(self):
        self.x = 400
        self.y = 100
        self.hp = self.max_hp
        self.timer = 0
        self.alive = False
        self.anim_timer = 0
        self.anim_index = 0
        self.enemy_bullets.clear()

    def update_animation(self):
        self.anim_timer += 1

        if self.anim_timer >= 15:
            self.anim_timer = 0
            self.anim_index += 1

    def shoot(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        dist = math.sqrt(dx * dx + dy * dy)

        if dist == 0:
            return

        dx /= dist
        dy /= dist

        self.enemy_bullets.append([self.x + 60, self.y + 60, dx, dy])

    def update(self, player, projectile_manager, map_width, map_height):
        if not self.alive:
            return False

        dx = player.x - self.x
        dy = player.y - self.y

        dist = math.sqrt(dx * dx + dy * dy)

        if dist != 0:
            dx /= dist
            dy /= dist

        self.x += dx
        self.y += dy

        self.x = max(0, min(map_width - self.size, self.x))
        self.y = max(0, min(map_height - self.size, self.y))

        self.timer += 1

        if self.timer >= 60:
            self.shoot(player)
            self.timer = 0

        for eb in self.enemy_bullets[:]:
            eb[0] += eb[2] * 7
            eb[1] += eb[3] * 7

            if abs(eb[0] - player.x) < 30 and abs(eb[1] - player.y) < 30:
                player.hp -= 10
                self.enemy_bullets.remove(eb)

            elif eb[0] < 0 or eb[0] > map_width or eb[1] < 0 or eb[1] > map_height:
                self.enemy_bullets.remove(eb)

        for b in projectile_manager.bullets[:]:
            if self.x < b[0] < self.x + self.size and self.y < b[1] < self.y + self.size:
                self.hp -= 1
                projectile_manager.bullets.remove(b)

        if self.hp <= 0:
            self.alive = False
            return True

        return False

    def draw_bullets(self, screen, camera):
        for eb in self.enemy_bullets:
            screen_x = int(eb[0] - camera.x)
            screen_y = int(eb[1] - camera.y)

            pygame.draw.circle(screen, RED, (screen_x, screen_y), 8)

    def draw(self, screen, camera, player, font):
        if not self.alive:
            return

        screen_boss_x = int(self.x - camera.x)
        screen_boss_y = int(self.y - camera.y)

        boss_img = self.assets.boss_frames[self.anim_index % len(self.assets.boss_frames)]

        boss_dx = player.x - self.x
        if boss_dx < 0:
            boss_img = pygame.transform.flip(boss_img, True, False)

        screen.blit(boss_img, (screen_boss_x, screen_boss_y))

        bar_width = 120
        bar_height = 12

        pygame.draw.rect(screen, BLACK, (screen_boss_x, screen_boss_y - 18, bar_width, bar_height))
        pygame.draw.rect(
            screen,
            GREEN,
            (screen_boss_x, screen_boss_y - 18, bar_width * (self.hp / self.max_hp), bar_height)
        )

        screen.blit(
            font.render(f"Boss HP: {self.hp}", True, WHITE),
            (screen_boss_x, screen_boss_y - 45)
        )