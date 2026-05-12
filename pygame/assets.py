import pygame
from settings import WIDTH, HEIGHT, PLAYER_SIZE, BOSS_SIZE, GREEN, YELLOW

class Assets:
    def __init__(self):
        self.load_player()
        self.load_powerups()
        self.load_boss()
        self.load_enemies()
        self.load_background()

    def load_player(self):
        try:
            walk1 = pygame.image.load("characters/walk1.png").convert_alpha()
            walk2 = pygame.image.load("characters/walk2.png").convert_alpha()

            walk1 = pygame.transform.scale(walk1, (PLAYER_SIZE, 50))
            walk2 = pygame.transform.scale(walk2, (PLAYER_SIZE, 50))

            self.walk_right = [walk1, walk2]
            self.walk_left = [
                pygame.transform.flip(walk1, True, False),
                pygame.transform.flip(walk2, True, False)
            ]

            self.player_front = pygame.image.load("characters/player_front.png").convert_alpha()
            self.player_front = pygame.transform.scale(self.player_front, (PLAYER_SIZE, 50))

        except:
            self.walk_right = [
                pygame.Surface((PLAYER_SIZE, 50)),
                pygame.Surface((PLAYER_SIZE, 50))
            ]
            self.walk_left = self.walk_right
            self.player_front = pygame.Surface((PLAYER_SIZE, 50))
            self.player_front.fill((100, 100, 255))

    def load_powerups(self):
        try:
            heal_img = pygame.image.load("game/heal_powerup.png").convert_alpha()
            power_img = pygame.image.load("game/power_powerup.png").convert_alpha()

            self.heal_powerup = pygame.transform.scale(heal_img, (65, 65))
            self.power_powerup = pygame.transform.scale(power_img, (65, 65))

        except:
            self.heal_powerup = pygame.Surface((20, 20))
            self.heal_powerup.fill(GREEN)

            self.power_powerup = pygame.Surface((20, 20))
            self.power_powerup.fill(YELLOW)

    def load_boss(self):
        self.boss_frames = [
            pygame.transform.scale(pygame.image.load("characters/eagle1.png").convert_alpha(), (BOSS_SIZE, BOSS_SIZE)),
            pygame.transform.scale(pygame.image.load("characters/eagle2.png").convert_alpha(), (BOSS_SIZE, BOSS_SIZE)),
            pygame.transform.scale(pygame.image.load("characters/eagle3.png").convert_alpha(), (BOSS_SIZE, BOSS_SIZE))
        ]

    def load_enemies(self):
        self.enemy_normal_frames = [
            pygame.transform.scale(pygame.image.load("characters/idlefront.png").convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load("characters/idleflip2.png").convert_alpha(), (80, 80))
        ]

        self.enemy_tank_frames = [
            pygame.transform.scale(pygame.image.load("characters/idlerat.png").convert_alpha(), (50, 50)),
            pygame.transform.scale(pygame.image.load("characters/walkrat.png").convert_alpha(), (50, 50))
        ]

    def load_background(self):
        self.sky_img = pygame.image.load("background/sky2.png").convert()
        self.sky_img = pygame.transform.scale(self.sky_img, (WIDTH * 2, HEIGHT))