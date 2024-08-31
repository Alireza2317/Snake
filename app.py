import sys
import pygame as pg
from random import randint

# speed
DELAY = 150
FPS = 1000 / DELAY
# if set to true, will scale up the fps after eating a food
INCREMENT_SPEED = False
SCALE = 1.0065

# dimensions
WN: int = 12
HN: int = 12
BLOCK_SIZE = 40
# some padding outside the walls of the game, lower values might not allow
# the score text to have enough space!
PD = 50
WIDTH = WN * BLOCK_SIZE + 2*PD
HEIGHT = HN * BLOCK_SIZE + 2*PD

# snake
# this will determine the shape of the pixels, either round or square-shaped
# uncomment the one you desire
SHAPE = 'square'
#SHAPE = 'circle'

INITIAL_SIZE = 4
# the snake's head roundness, 0 to disable
# only when SHAPE = 'square'
ROUNDNESS = BLOCK_SIZE


# colors, all in tuple format, (r, g, b)
BG_COLOR = (50, 50, 50)
SNAKE_HEAD_COLOR = (232, 200, 19)
SNAKE_COLOR = (4, 188, 136)
BOX_COLOR = (80, 80, 80)
WALL_COLOR = (220, 220, 240)
FOOD_COLOR = (232, 29, 73)

# fonts for texts
FONT_FILE = 'font.ttf'
FONT_SIZE = 22

# foods
# this will be the number of foods that will always be in the game map
NUM_FOODS = 1

# checking some parameters, to make the game more well-behaved
if NUM_FOODS >= WN * HN:
	raise ValueError(f'Number of foods should be less than {WN*HN}')
if DELAY <= 0 or FPS <= 0:
	raise ValueError('Delay and FPS should be positive numbers!')
if INITIAL_SIZE >= WN-1:
	raise ValueError('Snake\'s INITIAL_SIZE is too high!')

# comment this if your screen is big enough
if WIDTH > 1920 or HEIGHT > 1080:
	raise ValueError('Consider reducing WN and HN or BLOCK_SIZE! Too big for most screens!')

# comment this if you wanna get dizzy :)
if FPS > 25:
	raise ValueError('Consider using a higher value for DELAY. Or lower the FPS.')


class Position:
	"""
	Position class that acts as coordinates in a 2d plane
	"""
	def __init__(self, x: int, y: int) -> None:
		self.x = x
		self.y = y


	def __eq__(self, other: tuple | object) -> bool:
		if isinstance(other, tuple):
			return self.astuple == other

		elif isinstance(other, Position):
			return ((self.x == other.x) and (self.y == other.y))


	def __ne__(self, other: tuple | object) -> bool:
		if isinstance(other, tuple):
			return self.astuple != other

		elif isinstance(other, Position):
			return ((self.x != other.x) or (self.y != other.y))


	@property
	def astuple(self):
		return (self.x, self.y)


	def __repr__(self) -> str:
		return str(self.astuple)


class Snake:
	"""
	Snake class that handles all the logic of a snake
	"""
	def __init__(self, init_size: int = 3) -> None:
		self.direction: str = 'r'

		# first element will be the head
		self.body: list[Position] = [
			Position(i-1, 0)
			for i in range(init_size-1, -1, -1)
		]

		# useful when growing the snake
		self._left_over: Position = self.body[-1]


	@property
	def size(self):
		return len(self.body)


	@property
	def head(self) -> Position:
		return self.body[0]


	def turn(self, dir_to_turn: str) -> None:
		if self.direction == 'u':
			if dir_to_turn == 'd':
				return

		elif self.direction == 'd':
			if dir_to_turn == 'u':
				return

		elif self.direction == 'r':
			if dir_to_turn == 'l':
				return

		elif self.direction == 'l':
			if dir_to_turn == 'r':
				return

		self.direction = dir_to_turn


	def grow(self) -> None:
		self.body.append(self._left_over)


	def move(self) -> None:
		# find out the new position of the head
		new_head = Position(*self.head.astuple)

		# remove the last body part and save it
		self._left_over = self.body.pop()


		match self.direction:
			case 'r':
				new_head.x += 1
			case 'l':
				new_head.x -= 1
			case 'd':
				new_head.y += 1
			case 'u':
				new_head.y -= 1


		# all except the first and the last Position (head and tail)
		self.body.insert(0, new_head)


	def ate_food(self, food_pos: Position | tuple) -> bool:
		return (self.head == food_pos)


	def hit_position(self, pos: Position | tuple) -> bool:
		return (pos in self.body)


	def hit_self(self) -> bool:
		return (self.head in self.body[1:])


	def __repr__(self) -> str:
		return str(self.body)


class Block:
	"""
	Block class holds the information of each grid in the snake game
	Contains information of the positions as well as styles
	"""
	def __init__(
			self,
			left: int | float,
			top: int | float,
			border: int = 0,
			size: int = BLOCK_SIZE,
			color: tuple[int, int, int] = (255, 255, 255),
			kind: str = 'blank',
			border_radius: tuple[int, int, int, int] = (0, 0, 0, 0) # (tl, tr, br, bl)
	) -> None:


		self.block: pg.Rect = pg.Rect((left, top), (size, size))
		self.color: pg.Color = pg.Color(*color)
		self.border: int = border
		self.border_radius: tuple[int, int, int, int] = border_radius

		# kind could be: 'blank', 'snake', 'head', 'food'
		self.kind: str = kind


	def __repr__(self) -> str:
		return self.kind[0]


def calc_border_radiuses(direction: str) -> tuple[int, int, int, int]:
	tr = tl = br = bl = 0
	if direction == 'u':
		tr = tl = ROUNDNESS
	elif direction == 'd':
		br = bl = ROUNDNESS
	elif direction == 'r':
		tr = br = ROUNDNESS
	elif direction == 'l':
		tl = bl = ROUNDNESS

	return (tl, tr, br, bl)


def update_world(world: list[list[Block]], snake: Snake, foods: list[Position]) -> None:
	for r in range(HN):
		for c in range(WN):
			# calculating the coordinates of each pixel/block
			left = c * BLOCK_SIZE + PD
			top = r * BLOCK_SIZE + PD

			coordinate = (c, r)
			# this seems backwards but is actually the right way
			# because r, which is rows, goes up and down -> y coordinate
			# and c, which is cols, goes right and left -> x coordinate

			if SHAPE == 'circle':
				radiuses = tuple([BLOCK_SIZE for _ in range(4)])
			elif SHAPE == 'square':
						radiuses = tuple([0 for _ in range(4)])
			if snake.hit_position(pos=coordinate):
				# neat trick to use ate_food method to check collision with head
				if snake.ate_food(coordinate):
					# the snake's head, only if want different color for the head
					# rounding the head based on the direction of snake
					if SHAPE == 'square':
						radiuses = calc_border_radiuses(direction=snake.direction)
					world[r][c] = Block(left=left, top=top, color=SNAKE_HEAD_COLOR, kind='head', border_radius=radiuses)
				else: # snake body parts except the head

					world[r][c] = Block(left=left, top=top, color=SNAKE_COLOR, kind='snake', border_radius=radiuses)

			elif coordinate in foods:
				world[r][c] = Block(left=left, top=top, color=FOOD_COLOR, kind='food', border_radius=radiuses)

			else: # just the empty world block
				world[r][c] = Block(left=left, top=top, color=BOX_COLOR, border=1, kind='blank')


def draw_world(screen: pg.surface, world: list[list[Block]]) -> None:
	for r in range(HN):
		for c in range(WN):
			block = world[r][c].block
			block_color = world[r][c].color
			border = world[r][c].border
			radiuses = world[r][c].border_radius

			pg.draw.rect(
				screen,
				color=block_color,
				rect=block,
				width=border,
				border_top_left_radius=radiuses[0],
				border_top_right_radius=radiuses[1],
				border_bottom_right_radius=radiuses[2],
				border_bottom_left_radius=radiuses[3]
			)


def hit_wall(snake: Snake) -> bool:
	outofbound = (snake.head.x < 0 or snake.head.x >= WN) or (snake.head.y < 0 or snake.head.y >= HN)

	return outofbound


def generate_foods(foods: list[Position], snake: Snake, n: int = NUM_FOODS) -> None:
	while True:
		if len(foods) >= n: break

		x, y = randint(0, WN-1), randint(0, HN-1)
		p = Position(x, y)

		# this coordinate should not collide with other foods or the snake
		if snake.hit_position(pos=p) or (p in foods): continue

		foods.append(p)


def is_world_full(world: list[list[Block]]) -> bool:
	for row in world:
		for blk in row:
			if blk.kind == 'blank':
				return False
	return True


def is_world_snaked(world: list[list[Block]]) -> bool:
	for row in world:
		for blk in row:
			if blk.kind not in ['head', 'snake']:
				return False

	return True


def messg_on_game_over(screen, messg: str, color = 'white') -> None:
	pg.time.delay(1000)
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return
			if event.type == pg.KEYDOWN:
				if event.key in  [pg.K_RETURN, pg.K_KP_ENTER]:
					return


		font = pg.font.Font(FONT_FILE, int(FONT_SIZE*1.8))
		text = font.render(messg, True, color)

		screen.fill(BG_COLOR)
		screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//3))
		pg.display.update()


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Snake Game')
clock = pg.time.Clock()

font = pg.font.Font(FONT_FILE, FONT_SIZE)
score = font.render('', True, 'white')
#score_rect = score.get_rect(center=(PD, PD//2.2))

world: list[list[Block]] = [
	[None for col in range(WN)] for row in range(HN)
]

snake = Snake(init_size=INITIAL_SIZE)

foods: list[Position] = []
generate_foods(foods=foods, snake=snake)

update_world(world=world, snake=snake, foods=foods)

game_over = False
while not game_over:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			game_over = True
		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_UP:
				snake.turn('u')
			elif event.key == pg.K_DOWN:
				snake.turn('d')
			elif event.key == pg.K_LEFT:
				snake.turn('l')
			elif event.key == pg.K_RIGHT:
				snake.turn('r')

			if event.key == pg.K_KP_PLUS:
				if FPS + 1 <= 32:
					FPS += 1
			elif event.key == pg.K_KP_MINUS:
				if FPS - 1 > 0:
					FPS -= 1
			break

	snake.move()

	for i, food in enumerate(foods):
		if snake.ate_food(food_pos=food):
			if INCREMENT_SPEED: FPS *= SCALE

			snake.grow()
			foods.pop(i)
			if not is_world_full(world=world):
				generate_foods(foods=foods, snake=snake)

			break


	if snake.hit_self() or hit_wall(snake):
		game_over = True
		messg_on_game_over(screen, messg='Game Over!')


	update_world(world=world, snake=snake, foods=foods)

	if is_world_snaked(world=world):
		game_over = True
		messg_on_game_over(screen, messg='Well congrats! You won the snake game!')



	screen.fill(color=BG_COLOR)
	draw_world(screen, world)

	# to make the blocks near the edge of the wall the correct size
	adj = PD//10
	# the walls
	pg.draw.rect(
		screen,
		color=WALL_COLOR,
		width=6,
		rect=(PD-adj, PD-adj, WIDTH - 2*PD + 2*adj, HEIGHT - 2*PD + 2*adj) # very nasty!
	)

	score = font.render(f'Snake Size = {snake.size}\t ---- \tFPS = {FPS:.1f}', True, 'gray')
	#screen.blit(score, score_rect)
	screen.blit(score, (PD, 0))

	pg.display.update()

	clock.tick(FPS)

pg.quit()
sys.exit()