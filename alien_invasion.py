import sys
import pygame
from ship import Ship
from alien import Alien
from settings import Settings
from game_stats import GameStats
from scoreboard import  Scoreboard
from button import Button
from pygame.sprite import Group
import game_functions as gf
def run_game():
    ai_settings = Settings()
    # inital game and create display
    screen = pygame.display.set_mode(
            (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建一个用于存储统计信息的实例
    stats = GameStats(ai_settings)
    # create ship
    ship = Ship(ai_settings,screen)

    #创建一个用于存储子弹的编组
    bullets = Group()
    aliens = Group()
    #创建一个外星人
    #alien = Alien(ai_settings,screen)
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #创建Button按钮
    play_button = Button(ai_settings,screen,"Play")

    # 创建存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    # stat main loop
    while True:
        gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)
       # print(len(bullets))
        gf.update_screen(ai_settings,screen,stats, sb, ship,aliens,bullets,play_button)

run_game()