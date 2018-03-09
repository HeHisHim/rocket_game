import pygame
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
	#初始化游戏并创建一个屏幕对象
	pygame.init()
	alien_settings = Settings()
	#设置屏幕边框大小
	screen = pygame.display.set_mode((
		alien_settings.screen_width, alien_settings.screen_height
	))
	#改主框标题
	pygame.display.set_caption("Alien Invasion")

	#创建play按钮
	play_button = Button(alien_settings, screen, "Play")

	#创建一个用于存储游戏统计信息的实例
	stats = GameStats(alien_settings)

	#创建记分牌
	sb = Scoreboard(alien_settings, screen, stats)

	#创建飞船实例
	ship = Ship(alien_settings, screen)

	#创建外星人实例
	aliens = Group()

	#创建一个用于存储子弹的编组
	bullets = Group()

	#创建外星人群
	gf.create_fleet(alien_settings, screen, ship, aliens)

	#开始游戏主循环
	while True:

		#在游戏一开始就显示最高得分
		gf.show_high_score_first(stats, sb)

		#游戏内事件管理
		gf.check_events(alien_settings, screen, stats, play_button, ship, aliens, bullets, sb)
		
		if stats.game_active:
			#飞船位置刷新
			ship.update()
			
			#子弹位置刷新
			gf.update_bullets(alien_settings, screen, stats, sb, ship, aliens, bullets)

			#外星人位置刷新
			gf.update_aliens(alien_settings, stats, sb, screen, ship, aliens, bullets)

		#刷新屏幕绘制
		gf.update_screen(alien_settings, screen, stats, sb, ship, aliens, bullets, play_button)

if __name__ == '__main__':
	run_game()