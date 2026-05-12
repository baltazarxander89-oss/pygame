import pygame
import math


class LevelSelection:
    def __init__(self, screen):
        self.screen = screen
        self.bg_scroll = 0
        self.title_timer = 0

        self.background = pygame.image.load("background/sky2.png").convert_alpha()
        self.font = pygame.font.Font("fonts/Daydream.otf", 40)
        self.small_font = pygame.font.Font("fonts/Pixellari.ttf", 36)

        self.level1_button = pygame.Rect(0, 0, 0, 0)
        self.back_button = pygame.Rect(0, 0, 0, 0)

    def draw(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        mouse_pos = pygame.mouse.get_pos()

        self.bg_scroll -= 0.3

        bg_height = screen_height
        bg_width = int(self.background.get_width() * (bg_height / self.background.get_height()))

        bg = pygame.transform.scale(self.background, (bg_width, bg_height))

        if self.bg_scroll <= -bg_width:
            self.bg_scroll = 0

        self.screen.blit(bg, (self.bg_scroll, 0))
        self.screen.blit(bg, (self.bg_scroll + bg_width, 0))

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        # title (level selection)
        self.title_timer += 1

        float_y = int(math.sin(self.title_timer * 0.04) * 6)

        title_shadow = self.font.render("Level Selection", False, (40, 20, 10))

        # outline
        outline_color = (120, 70, 35)

        outline1 = self.font.render("Level Selection", False, outline_color)
        outline2 = self.font.render("Level Selection", False, outline_color)
        outline3 = self.font.render("Level Selection", False, outline_color)
        outline4 = self.font.render("Level Selection", False, outline_color)

        # main text
        title = self.font.render("Level Selection", False, (255, 220, 140))

        title_rect = title.get_rect(center=(screen_width // 2, 120 + float_y))

        # draw shadow
        self.screen.blit(title_shadow, (title_rect.x + 5, title_rect.y + 5))

        # draw outline
        self.screen.blit(outline1, (title_rect.x - 2, title_rect.y))
        self.screen.blit(outline2, (title_rect.x + 2, title_rect.y))
        self.screen.blit(outline3, (title_rect.x, title_rect.y - 2))
        self.screen.blit(outline4, (title_rect.x, title_rect.y + 2))

        # draw main text
        self.screen.blit(title, title_rect)

        # LEVEL 1 BUTTON
        base_rect = pygame.Rect(screen_width // 2 - 150, 250, 300, 90)

        hovered = base_rect.collidepoint(mouse_pos)

        if hovered:
            draw_rect = pygame.Rect(base_rect.x, base_rect.y - 8, 300, 90)
            color = (120, 75, 45)
        else:
            draw_rect = base_rect
            color = (90, 55, 35)

        self.level1_button = draw_rect

        # shadow
        shadow_rect = draw_rect.copy()
        shadow_rect.x += 6
        shadow_rect.y += 6

        pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect, border_radius=12)

        pygame.draw.rect(self.screen, color, draw_rect, border_radius=12)
        pygame.draw.rect(self.screen, (214, 170, 92), draw_rect, 5, border_radius=12)

        level1_text = self.small_font.render("Level 1", False, (255, 230, 160))
        level1_rect = level1_text.get_rect(center=draw_rect.center)
        self.screen.blit(level1_text, level1_rect)

        # BACK BUTTON
        base_back = pygame.Rect(screen_width // 2 - 100, 400, 200, 70)

        hovered_back = base_back.collidepoint(mouse_pos)

        if hovered_back:
            back_rect = pygame.Rect(base_back.x, base_back.y - 8, 200, 70)
            back_color = (100, 60, 40)
        else:
            back_rect = base_back
            back_color = (70, 40, 25)

        self.back_button = back_rect

        back_shadow = back_rect.copy()
        back_shadow.x += 6
        back_shadow.y += 6

        pygame.draw.rect(self.screen, (0, 0, 0), back_shadow, border_radius=12)

        pygame.draw.rect(self.screen, back_color, back_rect, border_radius=12)
        pygame.draw.rect(self.screen, (214, 170, 92), back_rect, 4, border_radius=12)

        back_text = self.small_font.render("Back", False, (255, 230, 160))
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.level1_button.collidepoint(event.pos):
                    return "level1"

                if self.back_button.collidepoint(event.pos):
                    return "back"

        return None