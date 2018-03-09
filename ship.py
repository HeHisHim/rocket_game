import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	#初始化飞船并设置其初始位置
	def __init__(self, alien_settings, screen):
		super().__init__()
		#属性初始化
		self.screen = screen
		self.alien_settings = alien_settings
		#移动标志初始化
		self.moving_right = False
		self.moving_left = False

		#加载飞船图像并获取外接矩形
		self.image = pygame.image.load("images/ship.png")
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		#将每艘新飞船放在屏幕底部中央
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		#在飞船的属性center中存储小数值
		self.center = float(self.rect.centerx)

	def blitme(self):
		self.screen.blit(self.image, self.rect)

	#根据移动标志调整飞船的位置
	def update(self):
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.alien_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.alien_settings.ship_speed_factor

		self.rect.centerx = self.center

	def center_ship(self):
		self.center = self.screen_rect.centerx
