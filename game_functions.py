import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import json

def check_keydown_events(event, ship, alien_settings, screen, bullets, stats, play_button, aliens, sb):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		#创建一颗子弹，并将其加入到编组bullets中
		fire_bullet(ship, alien_settings, screen, bullets)
	elif event.key == pygame.K_q:
		check_high_score(stats, sb)
		sys.exit()
	elif event.key == pygame.K_w:
		alien_settings.bullet_width = 600
	elif event.key == pygame.K_e:
		alien_settings.bullet_width = 3
	elif event.key == pygame.K_p:
		start_game(alien_settings, screen, stats, play_button, ship, aliens, bullets, sb)

def check_keyup_events(event, ship, alien_settings, screen, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(alien_settings, screen, stats, play_button, ship, aliens, bullets, sb):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		#当键盘被按下时，控制移动标记，以持续移动
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ship, alien_settings, screen, bullets, stats, play_button, aliens, sb)
		#当键盘被松开时，控制移动标记，以停止移动
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship, alien_settings, screen, bullets)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(alien_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb)

def update_screen(alien_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	#每次循环时都重绘屏幕
	screen.fill(alien_settings.bg_color)
	#绘制子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	#创建飞船
	ship.blitme()
	#绘制整组外星人
	for alien in aliens.sprites():
		alien.blitme()
	#让最近绘制的屏幕可见，每次循环都重新display来刷新元素

	#显示得分
	sb.show_score()

	#绘制按钮
	if not stats.game_active:
		play_button.draw_button()
		pygame.mouse.set_visible(True)

	pygame.display.flip()

def update_bullets(alien_settings, screen, stats, sb, ship, aliens, bullets):
	bullets.update()

	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	#检查是否有子弹击中了外星人
	#如果是这样，就删除相应的子弹和外星人
	check_bullet_alien_collisions(alien_settings, screen, stats, sb, ship, aliens, bullets)

def fire_bullet(ship, alien_settings, screen, bullets):
	if len(bullets) < alien_settings.bullets_allowed:
		new_bullet = Bullet(alien_settings, screen, ship)
		bullets.add(new_bullet)

def create_fleet(alien_settings, screen, ship, aliens):
	"""创建外星人群"""
	#创建一个外星人，并计算一行可容纳多少个外星人
	#外星人间距为外星人宽度
	alien = Alien(alien_settings, screen)
	# alien_width = alien.rect.width
	# available_space_x = alien_settings.screen_width - 2 * alien_width
	# number_aliens_x = int(available_space_x / (2 * alien_width))
	number_aliens_x = get_number_aliens_x(alien_settings, alien.rect.width)
	number_rows = get_number_rows(alien_settings, ship.rect.height, alien.rect.height)

	#创建外星人群
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			#创建一个外星人并将其加入当前行
			# alien = Alien(alien_settings, screen)
			# alien.x = alien_width + 2 * alien_width * alien_number
			# alien.rect.x = alien.x
			# aliens.add(alien)
			create_alien(alien_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(alien_settings, alien_width):
	"""计算每行可容纳多少个外星人"""
	available_space_x = alien_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def create_alien(alien_settings, screen, aliens, alien_number, row_number):
	"""创建一个外星人并将其放在当前"""
	alien = Alien(alien_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def get_number_rows(alien_settings, ship_height, alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_space_y = (alien_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def check_fleet_edges(alien_settings, aliens):
		"""有外星人到达边缘时采取相应的措施"""
		for alien in aliens.sprites():
			if alien.check_edges():
				change_fleet_direction(alien_settings, aliens)
				break

def change_fleet_direction(alien_settings, aliens):
	"""将整群外星人下移，并改变它们的方向"""
	for alien in aliens.sprites():
		alien.rect.y += alien_settings.fleet_drop_speed
	alien_settings.fleet_direction *= -1


def update_aliens(alien_settings, stats, sb, screen, ship, aliens, bullets):
	"""检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
	check_fleet_edges(alien_settings, aliens)
	aliens.update()

	#检查外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(alien_settings, stats, sb, screen, ship, aliens, bullets)

	check_aliens_bottom(alien_settings, stats, sb, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(alien_settings, screen, stats, sb, ship, aliens, bullets):
	"""响应子弹和外星人的碰撞"""
	#删除发生碰撞的子弹和外星人
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

	if collisions:
		for aliens in collisions.values():
			stats.score += alien_settings.alien_points * len(aliens)

		sb.prep_score()
		check_high_score(stats, sb)

	#删除现有的所有子弹，创建一个新的外星人群。并加快游戏节奏
	if 0 == len(aliens):
		bullets.empty()
		alien_settings.increase_speed()
		#提高等级
		start_new_level(stats, sb)
		create_fleet(alien_settings, screen, ship, aliens)

def ship_hit(alien_settings, stats, sb, screen, ship, aliens, bullets):
	"""响应被外星人撞到的飞船"""
	#将ships_left减1
	if stats.ships_left > 1:
		stats.ships_left -= 1
		#更新记分牌
		sb.prep_ships()

	else:
		stats.ships_left -= 1
		#更新记分牌
		sb.prep_ships()
		stats.game_active = False

	#清空外星人列表和子弹列表
	aliens.empty()
	bullets.empty()

	#创建一群新的外星人，并将飞船放到屏幕低端中央
	create_fleet(alien_settings, screen, ship, aliens)
	ship.center_ship()

	#暂停
	sleep(0.5)

def check_aliens_bottom(alien_settings, stats, sb, screen, ship, aliens, bullets):
	"""检查是否有外星人到达了屏幕底端"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#像飞船被撞到一样进行处理
			ship_hit(alien_settings, stats, sb, screen, ship, aliens, bullets)
			break

def check_play_button(alien_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb):
	#重置游戏统计信息
	if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
		start_game(alien_settings, screen, stats, play_button, ship, aliens, bullets, sb)

def start_game(alien_settings, screen, stats, play_button, ship, aliens, bullets, sb):
	stats.game_active = True

	try:
		load_high_score(stats)
	except FileNotFoundError:
		pass

	stats.reset_stats()
	#重置记分牌图像
	sb.prep_images()
	# sb.show_score()
	#重置游戏设置
	alien_settings.initialize_dynamic_settings()
	#隐藏光标
	pygame.mouse.set_visible(False)
	#清空外星人列表和子弹列表
	aliens.empty()
	bullets.empty()
	#创建一群新的外星人，并让飞船居中
	create_fleet(alien_settings, screen, ship, aliens)
	ship.center_ship()

def check_high_score(stats, sb):
	"""检查是否诞生了新的最高得分"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		dump_high_score(stats)

def start_new_level(stats, sb):
	stats.level += 1
	sb.prep_level()

def load_high_score(stats):
	"""读取最高分"""
	filename = stats.json_high_score
	with open(filename) as file_object:
		stats.high_score = json.load(file_object)


def dump_high_score(stats):
	"""写入最高分"""
	filename = stats.json_high_score
	with open(filename, "w") as file_object: #以写入模式打开文件
	    json.dump(stats.high_score, file_object) #该函数需要两个参数(待写入数据和待存储的文件名)

def show_high_score_first(stats, sb):
	try:
		load_high_score(stats)
	except FileNotFoundError:
		pass

	sb.prep_high_score()
