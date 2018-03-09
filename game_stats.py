import json

class GameStats():
	"""跟踪游戏的统计信息"""

	def __init__(self, alien_settings):
		self.alien_settings = alien_settings
		#游戏刚启动时处于活动状态
		self.game_active = False
		#json文件中的high_score
		self.json_high_score = "highscore.json"
		#在任何情况下都不应重置最高得分
		self.high_score = 0
		self.reset_stats()

	def reset_stats(self):
		"""初始化在游戏运行期间可能变化的统计数据"""
		self.ships_left = self.alien_settings.ship_limit
		self.score = 0
		self.level = 1