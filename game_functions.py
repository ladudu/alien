# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 12:10:47 2017

@author: Administrator
"""
import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import  Alien
def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_SPACE:
        #创建一颗子弹，并将其加入到编组bullets中
        if len(bullets) < ai_settings.bullet_allowed:
            new_bullet = Bullet(ai_settings,screen,ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()
def check_events(ai_settings,screen,stats,play_button,ship,bullets):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keyup_events(event,ship)
            elif event.type == pygame.KEYUP:
                check_keydown_events(event,ai_settings,screen,ship,bullets)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                check_play_button(stats, play_button, mouse_x, mouse_y)
def check_play_button(stats, play_button, mouse_x, mouse_y):
    """在玩家单击play按钮时开始游戏"""
    if play_button.rect.collidepoint(mouse_x,mouse_y):
        stats.game_active = True
def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button):
    """更新屏幕上的图像,并切换到新的屏幕"""
    # 每次循环都要重置屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()
    #如果游戏处于非激活状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,ship,alients,bullets):
    """更新子弹的位置，并删除已经消失的子弹"""
    #更新子弹的位置
    bullets.update()
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0 :
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,ship,alients,bullets)

def check_bullet_alien_collisions(ai_settings,screen,ship,alients,bullets):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, alients, True, True);

    if len(alients) == 0:
        # 删除现有的子弹并创建新的外星人
        bullets.empty()
        create_fleet(ai_settings,screen,ship,alients)

def get_number_aliens_x(ai_settings,alien_width):
    """计算可容纳多少外星人"""
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x
def get_number_rqws(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height

    number_rows  = int(available_space_y/(2 * alien_height))

    return number_rows
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien  = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    #创建一个外星人并计算一行可容纳多少个外星人
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rqws(ai_settings,ship.rect.height,alien.rect.height)

    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建第一个外星人并将其加入当前行
            create_alien(ai_settings,screen,aliens,alien_number,row_number)
def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break;
def change_fleet_direction(ai_settings,aliens):
    """将整行外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    #响应被外星人撞到的飞船
    if stats.ships_left > 0 :
        # 讲ship_left -1
        stats.ships_left -= 1

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人并将飞船放到屏幕底部中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    """检查是否有外星人到达底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样处理
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    """
    检查外星人是否位于边缘位置，并更新整群外星人的位置
    """
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        #print("Ship Hit!!!")
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)