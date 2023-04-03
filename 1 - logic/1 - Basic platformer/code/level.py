import pygame 
from tiles import Tile 
from settings import tile_size, screen_width
from player import Player
from particles import ParticleEffect

class Level:
	def __init__(self,level_data,surface):
		self.level_data = level_data
		self.white_tiles_enabled = True
		self.black_tiles_enabled = False
		# level setup
		self.display_surface = surface 
		self.setup_level(level_data)
		self.world_shift = 0
		self.current_x = 0

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

	def redraw_level(self):
		player_pos = self.player.sprite.rect.topleft
		self.tiles.empty()  # remove all current tiles
		self.setup_level(self.level_data)  # redraw level with updated tile settings
		self.player.sprite.rect.topleft = player_pos

	def disable_black_tiles(self):
		self.black_tiles_enabled = False
		self.redraw_level()  # redraw level after disabling black tiles

	def enable_black_tiles(self):
		self.black_tiles_enabled = True
		self.redraw_level()  # redraw level after enabling black tiles

	def disable_white_tiles(self):
		self.white_tiles_enabled = False
		self.redraw_level()  # redraw level after disabling white tiles

	def enable_white_tiles(self):
		self.white_tiles_enabled = True
		self.redraw_level()  # redraw level after enabling white tiles

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def setup_level(self,layout):
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()

		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size

				if cell == 'X' and self.white_tiles_enabled:  # only create white tiles if flag is True
					tile = Tile((x, y), tile_size, 'white')
					self.tiles.add(tile)
				elif cell == 'Y' and self.black_tiles_enabled:  # only create black tiles if flag is True
					tile = Tile((x, y), tile_size, 'black')
					self.tiles.add(tile)
				elif cell == 'Z':  # only create black tiles if flag is True
					tile = Tile((x, y), tile_size, 'grey')
					self.tiles.add(tile)
				if cell == 'P' and not self.player.sprites():  # only create player sprite if one does not already exist
					player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
					self.player.add(player_sprite)


	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def run(self):
		# dust particles 
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

		# level tiles
		self.tiles.update(self.world_shift)
		self.tiles.draw(self.display_surface)
		self.scroll_x()


		# player
		self.player.update()
		self.horizontal_movement_collision()
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()
		self.player.draw(self.display_surface)


