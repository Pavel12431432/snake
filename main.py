import pygame
import random

WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Snake')
font = pygame.font.SysFont('consolas', 100)
clock = pygame.time.Clock()

scale = 20
length = 1
tail = []

background_color = (40, 40, 40)
snake_color = (50, 200, 50)

pos = (0, 0)
velocity = (1, 0)
food = (random.randint(0, WIDTH // scale - 1), random.randint(0, HEIGHT // scale - 1))


def inp():
	global velocity, food
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				velocity = (0, -1)
			elif event.key == pygame.K_DOWN:
				velocity = (0, 1)
			elif event.key == pygame.K_LEFT:
				velocity = (-1, 0)
			elif event.key == pygame.K_RIGHT:
				velocity = (1, 0)


def draw_snake():
	for pos in tail:
		pygame.draw.rect(screen, snake_color, ((int(pos[0]) * scale, int(pos[1]) * scale), (scale, scale)))


def draw_walls():
	for i in range(WIDTH // scale):
		pygame.draw.line(screen, background_color, (i * scale, 0), (i * scale, HEIGHT - 1), 2)
	for i in range(HEIGHT // scale):
		pygame.draw.line(screen, background_color, (0, i * scale), (WIDTH - 1, i * scale), 2)


def constrain(value, min, max):
	if min > value:
		return min
	elif max < value:
		return max
	else:
		return value


def update_pos():
	global pos
	x = constrain(pos[0] + velocity[0], 0, WIDTH // scale - 1)
	y = constrain(pos[1] + velocity[1], 0, HEIGHT // scale - 1)
	pos = x, y
	tail.append(pos)
	if len(tail) > length:
		tail.pop(0)


def eat():
	global length, food
	if pos == food:
		length += 1
		valid = []
		for y in range(HEIGHT // scale):
			for x in range(WIDTH // scale):
				if (x, y) not in tail:
					valid.append((x, y))
		if not valid:
			screen.blit(font.render('YOU WIN!', True, (255, 255, 255)), (50, 50))
			pygame.display.update()
			while True:
				inp()
		food = random.choice(valid)


def die():
	if pos in tail[:-1]:
		screen.blit(font.render('GAME OVER', True, (255, 255, 255)), (50, 50))
		pygame.display.update()
		while True:
			inp()


def draw():
	screen.fill(background_color)

	pygame.draw.rect(screen, (210, 80, 80), ((food[0] * scale, food[1] * scale), (scale, scale)))
	draw_snake()
	draw_walls()

	pygame.display.update()


while True:
	inp()

	update_pos()
	eat()
	die()

	draw()
	clock.tick(10)