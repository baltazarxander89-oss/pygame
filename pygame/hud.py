import pygame
from settings import WIDTH, HEIGHT, BLACK, GREEN

class HUD:
    def __init__(self):
        self.ui_font = pygame.font.Font("fonts/Pixellari.ttf", 28)
        self.small_ui = pygame.font.Font("fonts/Pixellari.ttf", 22)
        self.pause_button = pygame.Rect(WIDTH - 80, 20, 50, 50)

    def update_pause_button(self):
        self.pause_button = pygame.Rect(WIDTH - 80, 20, 50, 50)

    def draw_pause_button(self, screen):
        self.update_pause_button()

        pygame.draw.rect(screen, (40, 25, 15), self.pause_button, border_radius=10)
        pygame.draw.rect(screen, (214, 170, 92), self.pause_button, 4, border_radius=10)

        pygame.draw.rect(screen, (255, 220, 140), (WIDTH - 62, 30, 8, 30), border_radius=3)
        pygame.draw.rect(screen, (255, 220, 140), (WIDTH - 46, 30, 8, 30), border_radius=3)

    def draw_player_panel(self, screen, player, points, kills):
        pygame.draw.rect(screen, (40, 25, 15), (15, 15, 280, 120), border_radius=10)
        pygame.draw.rect(screen, (214, 170, 92), (15, 15, 280, 120), 4, border_radius=10)

        hp_text = self.ui_font.render("HP", False, (255, 220, 140))
        screen.blit(hp_text, (30, 28))

        pygame.draw.rect(screen, (20, 10, 10), (90, 35, 170, 24), border_radius=8)

        hp_width = int(170 * (player.hp / player.max_hp))

        pygame.draw.rect(
            screen,
            (120, 255, 120),
            (90, 35, hp_width, 24),
            border_radius=8
        )

        points_text = self.small_ui.render(f"Points : {points}", False, (255, 230, 160))
        screen.blit(points_text, (30, 75))

        kills_text = self.small_ui.render(f"Kills : {kills}", False, (255, 230, 160))
        screen.blit(kills_text, (30, 102))

    def draw_stage_complete(self, screen, font):
        pygame.draw.rect(screen, BLACK, (250, 200, 400, 200))
        screen.blit(font.render("STAGE 1 COMPLETE", True, GREEN), (300, 220))

        pygame.draw.rect(screen, GREEN, (350, 320, 200, 60))
        screen.blit(font.render("CONTINUE", True, BLACK), (380, 340))

    def draw_game_over(self, screen):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        box_w = 500
        box_h = 320
        box_x = WIDTH // 2 - box_w // 2
        box_y = HEIGHT // 2 - box_h // 2

        pygame.draw.rect(screen, (35, 20, 15), (box_x, box_y, box_w, box_h), border_radius=20)
        pygame.draw.rect(screen, (214, 170, 92), (box_x, box_y, box_w, box_h), 5, border_radius=20)

        shadow_text = self.ui_font.render("GAME OVER", False, (40, 0, 0))
        main_text = self.ui_font.render("GAME OVER", False, (255, 60, 60))

        text_x = box_x + box_w // 2 - main_text.get_width() // 2
        text_y = box_y + 45

        screen.blit(shadow_text, (text_x + 3, text_y + 3))
        screen.blit(main_text, (text_x, text_y))

        restart_rect = pygame.Rect(box_x + 150, box_y + 140, 200, 60)
        home_rect = pygame.Rect(box_x + 150, box_y + 225, 200, 60)

        pygame.draw.rect(screen, (214, 170, 92), restart_rect, border_radius=12)
        pygame.draw.rect(screen, (80, 45, 25), restart_rect, 4, border_radius=12)

        restart_text = self.small_ui.render("RESTART", False, BLACK)
        restart_x = restart_rect.centerx - restart_text.get_width() // 2
        restart_y = restart_rect.centery - restart_text.get_height() // 2

        screen.blit(restart_text, (restart_x, restart_y))

        pygame.draw.rect(screen, (214, 170, 92), home_rect, border_radius=12)
        pygame.draw.rect(screen, (80, 45, 25), home_rect, 4, border_radius=12)

        home_text = self.small_ui.render("HOME", False, BLACK)
        home_x = home_rect.centerx - home_text.get_width() // 2
        home_y = home_rect.centery - home_text.get_height() // 2

        screen.blit(home_text, (home_x, home_y))

    def get_game_over_buttons(self):
        box_w = 500
        box_h = 320
        box_x = WIDTH // 2 - box_w // 2
        box_y = HEIGHT // 2 - box_h // 2

        restart_rect = pygame.Rect(box_x + 150, box_y + 140, 200, 60)
        home_rect = pygame.Rect(box_x + 150, box_y + 225, 200, 60)

        return restart_rect, home_rect