import pygame
from settings import PLAYER_SIZE, PLAYER_SPEED, PLAYER_MAX_HP

class Player:
    def __init__(self, assets):
        self.assets = assets
        self.x = 790
        self.y = 690
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP

        self.walk_index = 0
        self.walk_timer = 0

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def reset(self):
        self.x = 790
        self.y = 690
        self.hp = self.max_hp
        self.walk_index = 0
        self.walk_timer = 0

    def handle_movement(self, collision_rects, map_width, map_height):
        keys = pygame.key.get_pressed()

        self.moving_left = keys[pygame.K_a]
        self.moving_right = keys[pygame.K_d]
        self.moving_up = keys[pygame.K_w]
        self.moving_down = keys[pygame.K_s]

        new_x = self.x
        new_y = self.y

        if self.moving_left:
            new_x -= self.speed
        if self.moving_right:
            new_x += self.speed
        if self.moving_up:
            new_y -= self.speed
        if self.moving_down:
            new_y += self.speed

        future_rect = pygame.Rect(new_x, new_y, self.size, self.size)

        blocked = False
        for wall in collision_rects:
            if future_rect.colliderect(wall):
                blocked = True
                break

        if not blocked:
            self.x = new_x
            self.y = new_y

        self.x = max(0, min(map_width - self.size, self.x))
        self.y = max(0, min(map_height - self.size, self.y))

        self.animate()

    def animate(self):
        moving = self.moving_left or self.moving_right or self.moving_up or self.moving_down

        if moving:
            self.walk_timer += 1

            if self.walk_timer >= 10:
                self.walk_timer = 0
                self.walk_index = (self.walk_index + 1) % 2
        else:
            self.walk_index = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen, camera):
        player_screen_x = int(self.x - camera.x)
        player_screen_y = int(self.y - camera.y)

        if self.moving_left:
            player_img = self.assets.walk_left[self.walk_index]
        elif self.moving_right:
            player_img = self.assets.walk_right[self.walk_index]
        else:
            player_img = self.assets.player_front

        shadow_img = player_img.copy()
        shadow_img.fill((0, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(shadow_img, (player_screen_x + 4, player_screen_y + 6))

        screen.blit(player_img, (player_screen_x, player_screen_y))