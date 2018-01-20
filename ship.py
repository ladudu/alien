# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 11:55:25 2017

@author: Administrator
"""

import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super(Ship,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # load ship images and get shapes
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # ship in the screen center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
    def update(self):
        '''根据移动标志调整飞船的位置'''
        # 更新飞船的center值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left>0 :
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center
    def blitme(self):
        self.screen.blit(self.image,self.rect)
    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx