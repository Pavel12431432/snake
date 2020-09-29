import pygame
import random

# define constants
WIDTH, HEIGHT = 1000, 600
SCALE = 50  # scale determines size for each tile
BACKGROUND_COLOR = (40, 40, 40)  # define colors
SNAKE_COLOR = (50, 200, 50)
FOOD_COLOR = (210, 80, 80)
WALL_THICKNESS = 2  # thickness for drawing walls between unconnected tale tiles

# init pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Snake')
font = pygame.font.SysFont('consolas', WIDTH // 8)
clock = pygame.time.Clock()

# length of snake
length = 1
# array of tale positions
tail = []

# snake head position
pos = (0, 0)
# movement direction
velocity = (1, 0)
# pick random tile for food
food = (random.randint(0, WIDTH // SCALE - 1), random.randint(0, HEIGHT // SCALE - 1))


# handle input
def inp():
	global velocity, food
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		# set velocity depending on pressed arrow key
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				velocity = (0, -1)
			elif event.key == pygame.K_DOWN:
				velocity = (0, 1)
			elif event.key == pygame.K_LEFT:
				velocity = (-1, 0)
			elif event.key == pygame.K_RIGHT:
				velocity = (1, 0)
			else:
				return event.key


def draw_snake():
	# loop over every tail element
	for tile_pos in tail:
		# draw tail element
		pygame.draw.rect(screen, SNAKE_COLOR,
						 ((int(tile_pos[0]) * SCALE + WALL_THICKNESS, int(tile_pos[1]) * SCALE + WALL_THICKNESS),
						  (SCALE - WALL_THICKNESS, SCALE - WALL_THICKNESS)))
	# draw a rect to fill gap between neighboring tail elements
	for i in range(len(tail) - 1):
		gap_pos = None
		if tail[i + 1][0] - tail[i][0] == 1:
			gap_pos = ((int(tail[i][0] + 1) * SCALE, int(tail[i][1]) * SCALE + WALL_THICKNESS),
					   (WALL_THICKNESS * 2, SCALE - WALL_THICKNESS))
		elif tail[i + 1][0] - tail[i][0] == -1:
			gap_pos = ((int(tail[i][0]) * SCALE, int(tail[i][1]) * SCALE + WALL_THICKNESS),
					   (WALL_THICKNESS * 2, SCALE - WALL_THICKNESS))
		elif tail[i + 1][1] - tail[i][1] == 1:
			gap_pos = ((int(tail[i][0]) * SCALE + WALL_THICKNESS, int(tail[i][1] + 1) * SCALE),
					   (SCALE - WALL_THICKNESS, WALL_THICKNESS * 2))
		elif tail[i + 1][1] - tail[i][1] == -1:
			gap_pos = ((int(tail[i][0]) * SCALE + WALL_THICKNESS, int(tail[i][1]) * SCALE),
					   (SCALE - WALL_THICKNESS, WALL_THICKNESS * 2))
		try:
			pygame.draw.rect(screen, SNAKE_COLOR, gap_pos)
		except TypeError:
			pass


# update snake head position
def update_pos():
	global pos
	x = min(max(pos[0] + velocity[0], 0), WIDTH // SCALE - 1)
	y = min(max(pos[1] + velocity[1], 0), HEIGHT // SCALE - 1)
	pos = x, y
	# append the current pos to the tail
	tail.append(pos)
	# if food hasn't been eaten then remove last element of tail
	if len(tail) > length:
		tail.pop(0)


def eat():
	global length, food
	# check if food has been eaten
	if pos == food:
		length += 1
		# create array of valid positions to place food
		valid = []
		for y in range(HEIGHT // SCALE):
			for x in range(WIDTH // SCALE):
				if (x, y) not in tail:
					valid.append((x, y))
		# if no valid spaces are found then the snake has filled the screen
		if not valid:
			print('YOU WIN!')
			quit()
		food = random.choice(valid)


def check_death():
	global pos, tail, velocity, length, food
	# check if the snake's head position is the same as a tail part
	if pos in tail[:-1]:
		# display game over
		screen.blit(font.render('GAME OVER', True, (255, 255, 255)), (WIDTH // 5, 50))
		pygame.display.update()
		while True:
			# infinite loop runs until space is pressed
			if inp() == pygame.K_SPACE:
				# reset game
				tail = []
				length = 1
				pos = (0, 0)
				velocity = (1, 0)
				food = (random.randint(0, WIDTH // SCALE - 1), random.randint(0, HEIGHT // SCALE - 1))
				break


def draw():
	screen.fill(BACKGROUND_COLOR)

	# draw food
	pygame.draw.rect(screen, FOOD_COLOR,
					 ((food[0] * SCALE + WALL_THICKNESS, food[1] * SCALE + WALL_THICKNESS),
					  (SCALE - WALL_THICKNESS, SCALE - WALL_THICKNESS)))
	draw_snake()

	pygame.display.update()


while True:
	# input
	for i in range(100):
		inp()

	# logic checks
	update_pos()
	eat()
	check_death()

	# display game
	draw()

	# limit game to 10 fps
	clock.tick(10)
