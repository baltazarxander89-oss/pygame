import pygame
import random

class PowerupManager:
    def __init__(self, assets):
        self.assets = assets
        self.drops = []
        self.attack_multiplier = 1
        self.power_timer = 0

    def reset(self):
        self.drops.clear()
        self.attack_multiplier = 1
        self.power_timer = 0

    def maybe_drop(self, x, y):
        if random.randint(1, 4) == 1:
            self.drops.append([x, y, random.choice(["heal", "power"])])

    def update(self, player):
        player_rect = player.get_rect()

        for d in self.drops[:]:
            drop_rect = pygame.Rect(d[0], d[1], 20, 20)

            if player_rect.colliderect(drop_rect):
                if d[2] == "heal":
                    player.hp = min(player.max_hp, player.hp + 25)

                if d[2] == "power":
                    self.attack_multiplier = 2
                    self.power_timer = 1800

                self.drops.remove(d)

        if self.power_timer > 0:
            self.power_timer -= 1

            if self.power_timer == 0:
                self.attack_multiplier = 1

    def draw(self, screen, camera):
        for d in self.drops:
            screen_x = int(d[0] - camera.x)
            screen_y = int(d[1] - camera.y)

            if d[2] == "heal":
                screen.blit(self.assets.heal_powerup, (screen_x - 10, screen_y - 10))
            elif d[2] == "power":
                screen.blit(self.assets.power_powerup, (screen_x - 10, screen_y - 10))