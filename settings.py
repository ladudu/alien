# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 11:40:15 2017

@author: Administrator
"""

class Settings():
    """存储游戏《外星人入侵》的所有设置的类"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # 飞船的设置

        self.ship_limit = 2
        # 子弹的设置

        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullet_allowed = 3

        #外星人设置

        self.fleet_drop_speed = 10

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1

        # 外星人点数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1

        # 记分
        self.alien_points = 50
    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        # 提高外星人点数
        self.alien_points = int(self.alien_points * self.score_scale)