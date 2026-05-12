import pygame


class PauseMenu:
    def __init__(self, screen):
        self.screen = screen

        self.volume_slider = pygame.Rect(0, 0, 0, 0)
        self.dragging_slider = False
        self.music_button = pygame.Rect(0, 0, 0, 0)

        self.music_on = True
        self.volume = 70

        self.title_font = pygame.font.Font("fonts/Minecraft.ttf", 45)
        self.button_font = pygame.font.Font("fonts/Pixellari.ttf", 32)

        self.resume_button = pygame.Rect(0, 0, 0, 0)
        self.quit_button = pygame.Rect(0, 0, 0, 0)

    def draw(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 90))
        self.screen.blit(overlay, (0, 0))

        box_w = 500
        box_h = 400
        box_x = screen_width // 2 - box_w // 2
        box_y = screen_height // 2 - box_h // 2

        pygame.draw.rect(self.screen, (66, 40, 24), (box_x, box_y, box_w, box_h), border_radius=12)
        pygame.draw.rect(self.screen, (214, 170, 92), (box_x, box_y, box_w, box_h), 6, border_radius=12)

        title_shadow = self.title_font.render("Paused", False, (70, 40, 20))
        title_text = self.title_font.render("Paused", False, (255, 220, 140))

        title_rect = title_text.get_rect(center=(screen_width // 2, box_y + 70))

        self.screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title_text, title_rect)

        self.resume_button = pygame.Rect(screen_width // 2 - 130, box_y + 245, 260, 60)
        self.quit_button = pygame.Rect(screen_width // 2 - 130, box_y + 315, 260, 60)

        # MUSIC
        music_y = box_y + 130
        volume_y = box_y + 185

        left_x = box_x + 60
        right_x = box_x + 360

        music_text = self.button_font.render("Music", False, (245, 220, 170))
        self.screen.blit(music_text, (left_x, music_y))

        music_status = "On" if self.music_on else "Off"
        music_color = (120, 255, 120) if self.music_on else (255, 100, 100)

        music_status_text = self.button_font.render(music_status, False, music_color)

        self.music_button = music_status_text.get_rect(topleft=(right_x, music_y))

        self.screen.blit(music_status_text, self.music_button)

        # VOLUME
        volume_text = self.button_font.render("Volume", False, (245, 220, 170))
        self.screen.blit(volume_text, (left_x, volume_y))

        slider_x = box_x + 220
        slider_y = volume_y + 18

        slider_width = 160
        slider_height = 10

        pygame.draw.rect(
            self.screen,
            (40, 25, 15),
            (slider_x, slider_y, slider_width, slider_height),
            border_radius=8
        )

        fill_width = int((self.volume / 100) * slider_width)

        pygame.draw.rect(
            self.screen,
            (214, 170, 92),
            (slider_x, slider_y, fill_width, slider_height),
            border_radius=8
        )

        knob_x = slider_x + fill_width

        pygame.draw.circle(
            self.screen,
            (255, 230, 160),
            (knob_x, slider_y + slider_height // 2),
            10
        )

        self.volume_slider = pygame.Rect(
            slider_x,
            slider_y - 10,
            slider_width,
            30
        )

        volume_number = self.button_font.render(
            f"{self.volume}%",
            False,
            (255, 255, 255)
        )

        self.screen.blit(volume_number, (slider_x + slider_width + 20, volume_y))

        self.draw_button(self.resume_button, "Resume")
        self.draw_button(self.quit_button, "Back to home")

    def draw_button(self, rect, text):
        mouse_pos = pygame.mouse.get_pos()

        color = (100, 60, 35) if rect.collidepoint(mouse_pos) else (75, 45, 25)

        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, (214, 170, 92), rect, 4, border_radius=10)

        label = self.button_font.render(text, False, (255, 230, 160))
        label_rect = label.get_rect(center=rect.center)

        self.screen.blit(label, label_rect)

    def handle_event(self, event):

      if event.type == pygame.MOUSEBUTTONDOWN:

          if event.button == 1:

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

              if self.resume_button.collidepoint(event.pos):
                  return "resume"

              if self.quit_button.collidepoint(event.pos):
                  return "quit_menu"

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