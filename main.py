import pygame
import random

WIDTH, HEIGHT = 800, 600
# initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Snake')
font = pygame.font.SysFont('consolas', WIDTH // 8)
clock = pygame.time.Clock()

# scale determines size for each tile
scale = 25
# length of snake
length = 1
# array of tale positions
tail = []

# define colors
background_color = (40, 40, 40)
snake_color = (50, 200, 50)
food_color = (210, 80, 80)

# thickness for drawing walls between unconnected tale tiles
wall_thickness = 2

# snake head position
pos = (0, 0)
# movement direction
velocity = (1, 0)
# pick random tile for food
food = (random.randint(0, WIDTH // scale - 1), random.randint(0, HEIGHT // scale - 1))


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
		pygame.draw.rect(screen, snake_color,
						 ((int(tile_pos[0]) * scale + wall_thickness, int(tile_pos[1]) * scale + wall_thickness),
						  (scale - wall_thickness, scale - wall_thickness)))
	# draw a rect to fill gap between neighboring tail elements
	for i in range(len(tail) - 1):
		gap_pos = None
		if tail[i + 1][0] - tail[i][0] == 1:
			gap_pos = ((int(tail[i][0] + 1) * scale, int(tail[i][1]) * scale + wall_thickness),
					   (wall_thickness * 2, scale - wall_thickness))
		elif tail[i + 1][0] - tail[i][0] == -1:
			gap_pos = ((int(tail[i][0]) * scale, int(tail[i][1]) * scale + wall_thickness),
					   (wall_thickness * 2, scale - wall_thickness))
		elif tail[i + 1][1] - tail[i][1] == 1:
			gap_pos = ((int(tail[i][0]) * scale + wall_thickness, int(tail[i][1] + 1) * scale),
					   (scale - wall_thickness, wall_thickness * 2))
		elif tail[i + 1][1] - tail[i][1] == -1:
			gap_pos = ((int(tail[i][0]) * scale + wall_thickness, int(tail[i][1]) * scale),
					   (scale - wall_thickness, wall_thickness * 2))
		try:
			pygame.draw.rect(screen, snake_color, gap_pos)
		except TypeError:
			pass


def constrain(value, minimum, maximum):
	if minimum > value:
		return minimum
	elif maximum < value:
		return maximum
	else:
		return value


# update snake head position
def update_pos():
	global pos
	x = constrain(pos[0] + velocity[0], 0, WIDTH // scale - 1)
	y = constrain(pos[1] + velocity[1], 0, HEIGHT // scale - 1)
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
		for y in range(HEIGHT // scale):
			for x in range(WIDTH // scale):
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
				food = (random.randint(0, WIDTH // scale - 1), random.randint(0, HEIGHT // scale - 1))
				break


def draw():
	screen.fill(background_color)

	# draw food
	pygame.draw.rect(screen, food_color,
					 ((food[0] * scale + wall_thickness, food[1] * scale + wall_thickness),
					  (scale - wall_thickness, scale - wall_thickness)))
	draw_snake()

	pygame.display.update()


while True:
	# input
	inp()

	# logic checks
	update_pos()
	eat()
	check_death()

	# displaying game
	draw()

	# limit game to 10 fps
	clock.tick(10)
