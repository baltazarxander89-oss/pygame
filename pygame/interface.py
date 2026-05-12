import pygame
import math


class MainInterface:
    def __init__(self, screen):
        self.screen = screen
        self.title_timer = 0

        self.volume_slider = pygame.Rect(0, 0, 0, 0)
        self.dragging_slider = False

        self.background = pygame.image.load("background/home.png").convert_alpha()
        self.title_board = pygame.image.load("ui/name.png").convert_alpha()
        self.button_board = pygame.image.load("ui/button.png").convert_alpha()

        self.font = pygame.font.Font("fonts/Pixellari.ttf", 29)

        self.start_button = pygame.Rect(0, 0, 0, 0)
        self.settings_button = pygame.Rect(0, 0, 0, 0)
        self.exit_button = pygame.Rect(0, 0, 0, 0)

        self.music_button = pygame.Rect(0, 0, 0, 0)
        self.volume_minus = pygame.Rect(0, 0, 0, 0)
        self.volume_plus = pygame.Rect(0, 0, 0, 0)

        self.show_settings = False
        self.music_on = True
        self.volume = 70

    def draw_button(self, x, y, text):
        mouse_pos = pygame.mouse.get_pos()

        button_w = 260
        button_h = 130

        is_hovered = pygame.Rect(x, y, button_w, button_h).collidepoint(mouse_pos)

        if is_hovered:
            draw_y = y - 8
            scale = 1.05
            brightness = 45
        else:
            draw_y = y
            scale = 1.0
            brightness = 0

        new_w = int(button_w * scale)
        new_h = int(button_h * scale)

        button_img = pygame.transform.scale(self.button_board, (new_w, new_h))
        button_rect = button_img.get_rect(center=(x + button_w // 2, draw_y + button_h // 2))

        if is_hovered:
            shadow_img = button_img.copy()
            shadow_img.fill((0, 0, 0, 120), special_flags=pygame.BLEND_RGBA_MULT)

            self.screen.blit(shadow_img, (button_rect.x + 4, button_rect.y + 4))
            self.screen.blit(shadow_img, (button_rect.x + 6, button_rect.y + 6))
            self.screen.blit(shadow_img, (button_rect.x + 8, button_rect.y + 8))

        if brightness > 0:
            button_img = button_img.copy()
            glow = pygame.Surface(button_img.get_size(), pygame.SRCALPHA)
            glow.fill((brightness, brightness, brightness, 0))
            button_img.blit(glow, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        self.screen.blit(button_img, button_rect)

        shadow = self.font.render(text, False, (90, 55, 35))
        shadow_rect = shadow.get_rect(center=(button_rect.centerx + 2, button_rect.centery + 2))

        text_surface = self.font.render(text, False, (199, 187, 96))
        text_rect = text_surface.get_rect(center=button_rect.center)

        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text_surface, text_rect)

        return button_rect

    def draw_settings_box(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        box_h = 650
        box_w = 600

        box_x = self.screen.get_width() // 2 - box_w // 2
        box_y = self.screen.get_height() // 2 - box_h // 2 + 40

        settings_bg = pygame.image.load("ui/settings.png").convert_alpha()
        settings_bg = pygame.transform.scale(settings_bg, (box_w, box_h))
        self.screen.blit(settings_bg, (box_x, box_y))

        title_font = pygame.font.Font("Minecraft.ttf", 42)
        option_font = pygame.font.Font("Pixellari.ttf", 36)
        small_font = pygame.font.Font("Pixellari.ttf", 28)

        title_shadow = title_font.render("Settings", False, (70, 40, 20))
        title_text = title_font.render("Settings", False, (255, 220, 140))

        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, box_y + 120))

        self.screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title_text, title_rect)

        music_y = box_y + 200
        volume_y = box_y + 270

        left_x = box_x + 95
        right_x = box_x + box_w - 150

        music_text = option_font.render("Music", False, (245, 220, 170))
        self.screen.blit(music_text, (left_x, music_y))

        music_status = "On" if self.music_on else "Off"
        music_color = (120, 255, 120) if self.music_on else (255, 100, 100)

        music_status_text = option_font.render(music_status, False, music_color)
        self.music_button = music_status_text.get_rect(topleft=(right_x, music_y))
        self.screen.blit(music_status_text, self.music_button)

        volume_text = option_font.render("Volume", False, (245, 220, 170))
        self.screen.blit(volume_text, (left_x, volume_y))

        slider_x = box_x + 280
        slider_y = volume_y + 25

        slider_width = 140
        slider_height = 10

        pygame.draw.rect(
            self.screen,
            (40, 25, 15),
            (slider_x, slider_y, slider_width, slider_height),
            border_radius=8
        )

        # filled slider
        fill_width = int((self.volume / 100) * slider_width)

        pygame.draw.rect(
            self.screen,
            (214, 170, 92),
            (slider_x, slider_y, fill_width, slider_height),
            border_radius=8
        )

        # draggable circle
        knob_x = slider_x + fill_width

        pygame.draw.circle(
            self.screen,
            (255, 230, 160),
            (knob_x, slider_y + slider_height // 2),
            12
        )

        self.volume_slider = pygame.Rect(
            slider_x,
            slider_y - 10,
            slider_width,
            30
        )

        volume_number = option_font.render(f"{self.volume}%", False, (255, 255, 255))
        self.screen.blit(volume_number, (slider_x + slider_width + 25, volume_y))

        close_text = small_font.render("Press ESC to close", False, (210, 180, 120))
        close_rect = close_text.get_rect(center=(self.screen.get_width() // 2, box_y + 450))
        self.screen.blit(close_text, close_rect)

    def draw(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        bg = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.screen.blit(bg, (0, 0))

        self.title_timer += 1
        float_y = int(math.sin(self.title_timer * 0.04) * 6)

        title_img = pygame.transform.scale(self.title_board, (468, 223))
        title_rect = title_img.get_rect(center=(screen_width // 2, 170 + float_y))
        self.screen.blit(title_img, title_rect)

        button_y = 450
        button_w = 260
        gap = 45

        total_width = button_w * 3 + gap * 2
        start_x = screen_width // 2 - total_width // 2

        self.settings_button = self.draw_button(start_x, button_y, "Settings")
        self.start_button = self.draw_button(start_x + button_w + gap, button_y, "New Game")
        self.exit_button = self.draw_button(start_x + (button_w + gap) * 2, button_y, "Exit")

        if self.show_settings:
            self.draw_settings_box()

    def handle_event(self, event):
      if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
              self.show_settings = False

      if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:

              if self.show_settings:

                  if self.music_button.collidepoint(event.pos):
                      self.music_on = not self.music_on

                  if self.volume_slider.collidepoint(event.pos):
                      self.dragging_slider = True

                      slider_x = self.volume_slider.x
                      slider_width = self.volume_slider.width

                      mouse_x = event.pos[0]

                      relative_x = mouse_x - slider_x
                      relative_x = max(0, min(slider_width, relative_x))

                      self.volume = int((relative_x / slider_width) * 100)

                  return "settings"

              if self.settings_button.collidepoint(event.pos):
                  self.show_settings = True
                  return "settings"

              if self.start_button.collidepoint(event.pos):
                  return "level_select"

              if self.exit_button.collidepoint(event.pos):
                  return "quit"

      if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
              self.dragging_slider = False

      if event.type == pygame.MOUSEMOTION:
          if self.dragging_slider:

              slider_x = self.volume_slider.x
              slider_width = self.volume_slider.width

              mouse_x = event.pos[0]

              relative_x = mouse_x - slider_x
              relative_x = max(0, min(slider_width, relative_x))

              self.volume = int((relative_x / slider_width) * 100)

      return None