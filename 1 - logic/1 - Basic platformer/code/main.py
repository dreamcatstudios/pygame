import pygame, sys
from settings import * 
from level import Level


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_map,screen)
white = (255,255,255)
black = (0,0,0)
color = black

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_u:
				color = white

			if event.key == pygame.K_y:
				color = black
	screen.fill(color)
	level.run()

	pygame.display.update()
	clock.tick(60)
