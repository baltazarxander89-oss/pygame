import pygame

class MusicManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_enabled = True
        self.music_volume = 0.7
        self.music_file = "music/game_start.mp3"

    def play(self):
        if not self.music_enabled:
            pygame.mixer.music.pause()
            return

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1)

        pygame.mixer.music.unpause()
        pygame.mixer.music.set_volume(self.music_volume)

    def update_from_pause_menu(self, pause_menu):
        self.music_enabled = pause_menu.music_on
        self.music_volume = pause_menu.volume / 100
        self.play()