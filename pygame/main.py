import pygame
import random

from interface import MainInterface
from level_select import LevelSelection
from pause_menu import PauseMenu

from settings import WIDTH, HEIGHT, FPS
from assets import Assets
from map_manager import MapManager
from camera import Camera
from player import Player
from enemy_manager import EnemyManager
from projectile_manager import ProjectileManager
from powerup_manager import PowerupManager
from boss import Boss
from music_manager import MusicManager
from hud import HUD

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Pixel Quest")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Pixellari.ttf", 22)

assets = Assets()
game_map = MapManager()
camera = Camera()
player = Player(assets)
enemies = EnemyManager(assets)
projectiles = ProjectileManager()
powerups = PowerupManager(assets)
boss = Boss(assets)
music = MusicManager()
hud = HUD()

interface = MainInterface(screen)
level_select = LevelSelection(screen)
pause_menu = PauseMenu(screen)

kills = 0
points = 0

stage = 1
stage1_complete = False
stage2_unlocked = False
game_over = False

game_state = "menu"
paused = False

sky_scroll = 0


def reset_game():
    global kills, points
    global stage, stage1_complete, stage2_unlocked, game_over
    global sky_scroll

    player.reset()
    enemies.reset()
    projectiles.reset()
    powerups.reset()
    boss.reset()
    camera.reset()

    kills = 0
    points = 0

    stage = 1
    stage1_complete = False
    stage2_unlocked = False
    game_over = False

    sky_scroll = 0


# --- MAIN LOOP ---
running = True

while running:
    clock.tick(FPS)
    music.play()

    # --- EVENTS ---
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ---------------- MENU ----------------
        if game_state == "menu":
            action = interface.handle_event(event)

            if action == "level_select":
                game_state = "level_select"

            if action == "quit":
                running = False

        # ------------ LEVEL SELECT ------------
        elif game_state == "level_select":
            action = level_select.handle_event(event)

            if action == "level1":
                reset_game()
                game_state = "game"

            if action == "back":
                game_state = "menu"

        # ---------------- GAME ----------------
        elif game_state == "game":

            # PAUSE MENU
            if paused:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False

                action = pause_menu.handle_event(event)
                music.update_from_pause_menu(pause_menu)

                if action == "resume":
                    paused = False

                if action == "quit_menu":
                    paused = False
                    game_state = "menu"

                continue

            # OPEN PAUSE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()

                    # PAUSE BUTTON
                    if hud.pause_button.collidepoint((mx, my)):
                        paused = True
                        continue

                    # GAME OVER BUTTONS
                    if game_over:
                        restart_rect, home_rect = hud.get_game_over_buttons()

                        if restart_rect.collidepoint((mx, my)):
                            reset_game()
                            game_over = False
                            continue

                        elif home_rect.collidepoint((mx, my)):
                            game_state = "menu"
                            game_over = False
                            continue

                    # STAGE COMPLETE BUTTON
                    elif stage2_unlocked and 350 < mx < 550 and 320 < my < 380:
                        stage = 2
                        stage2_unlocked = False
                        enemies.enemies.clear()
                        powerups.drops.clear()
                        boss.enemy_bullets.clear()

                        for _ in range(20):
                            enemies.enemies.append(
                                enemies.spawn_enemy(
                                    2,
                                    game_map.width,
                                    game_map.height,
                                    game_map.collision_rects
                                )
                            )

                        continue

            # SHOOT / CLICK
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not stage2_unlocked:
                mx, my = pygame.mouse.get_pos()
                projectiles.shoot(player, mx, my, camera)

    # --- MENU DRAW ---
    if game_state == "menu":
        interface.draw()
        pygame.display.update()
        continue

    if game_state == "level_select":
        level_select.draw()
        pygame.display.update()
        continue

    if paused:
        pause_menu.draw()
        pygame.display.update()
        continue

    # --- GAME UPDATE ---
    camera.update(player.x, player.y, game_map.width, game_map.height)

    boss.update_animation()
    enemies.update_animation()

    player.handle_movement(game_map.collision_rects, game_map.width, game_map.height)

    # --- ENEMY SPAWN ---
    if not game_over:
        if stage == 1 and not boss.alive:
            if random.randint(1, 35) == 1:
                enemies.enemies.append(
                    enemies.spawn_enemy(
                        1,
                        game_map.width,
                        game_map.height,
                        game_map.collision_rects
                    )
                )

        if stage == 1 and kills >= 100 and not boss.alive and not stage1_complete:
            boss.alive = True
            enemies.enemies = [e for e in enemies.enemies if e[3] in ["tank", "elite"]]

    enemies.update_ai(player, game_map.collision_rects, game_map.width, game_map.height)

    projectiles.update(game_map.width, game_map.height)

    kills_added, points_added, killed_positions = projectiles.handle_enemy_collision(
        enemies,
        powerups.attack_multiplier
    )

    kills += kills_added
    points += points_added

    if stage == 1 and not boss.alive:
        for x, y in killed_positions:
            powerups.maybe_drop(x, y)

    powerups.update(player)

    # --- BOSS LOGIC ---
    if boss.alive and not game_over:
        boss_defeated = boss.update(player, projectiles, game_map.width, game_map.height)

        if boss_defeated:
            stage1_complete = True
            stage2_unlocked = True

    # --- GAME OVER ---
    if player.hp <= 0 and not game_over:
        game_over = True
        boss.alive = False
        enemies.enemies.clear()
        boss.enemy_bullets.clear()

    # --- DRAW GAME ---
    sky_scroll -= 0.3

    if sky_scroll <= -assets.sky_img.get_width():
        sky_scroll = 0

    screen.blit(assets.sky_img, (sky_scroll, 0))
    screen.blit(assets.sky_img, (sky_scroll + assets.sky_img.get_width(), 0))

    game_map.draw_floor(screen, camera)

    enemies.draw(screen, camera, player)
    projectiles.draw(screen, camera)
    boss.draw_bullets(screen, camera)
    powerups.draw(screen, camera)

    player.draw(screen, camera)

    game_map.draw_props(screen, camera)

    boss.draw(screen, camera, player, font)

    hud.draw_pause_button(screen)
    hud.draw_player_panel(screen, player, points, kills)

    # --- STAGE COMPLETE ---
    if stage2_unlocked:
        hud.draw_stage_complete(screen, font)

    # --- GAME OVER SCREEN ---
    if game_over:
        hud.draw_game_over(screen)

    pygame.display.update()

pygame.quit()