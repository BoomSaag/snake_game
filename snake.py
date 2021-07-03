import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

windowWidth = 800
windowHeight = 800
border_width = 10

surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Ultra Snake")

pygame.init()
clock = pygame.time.Clock()
GameState = 0
fps = 60
red = [255, 0, 0]
green = [0, 255, 50]
border_colour = [255, 60, 60]

snake_width = 20
snake_colour = green
snake_tick = 0.1
snake_segments = 5
snake_trail = []


class Snake(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super(Snake, self).__init__()
        self.image = pygame.Surface([snake_width, snake_width])
        self.image.fill(snake_colour)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.type = type
        self.speed = snake_width
        self.move = 0
        self.counter = 1

    def update(self):
        keystate = pygame.key.get_pressed()

        # Left - 0
        if keystate[pygame.K_LEFT]:
            if not self.move == 1:
                self.move = 0

        # Right - 1
        if keystate[pygame.K_RIGHT]:
            if not self.move == 0:
                self.move = 1

        # Up - 2
        if keystate[pygame.K_UP]:
            if not self.move == 3:
                self.move = 2

        # Down - 3
        if keystate[pygame.K_DOWN]:
            if not self.move == 2:
                self.move = 3

        # movement
        if int(self.counter) >= 1:

            if self.move == 0:
                self.rect.move_ip([-self.speed, 0])
            elif self.move == 1:
                self.rect.move_ip([self.speed, 0])
            elif self.move == 2:
                self.rect.move_ip([0, -self.speed])
            elif self.move == 3:
                self.rect.move_ip([0, self.speed])
            self.counter = 0
            snake_trail.append([self.rect.center[0], self.rect.center[1]])
            if len(snake_trail) > snake_segments + 1:
                snake_trail.pop(0)

        else:
            self.counter += snake_tick


class Segment(pygame.sprite.Sprite):

    def __init__(self, pos, num):
        super(Segment, self).__init__()
        self.image = pygame.Surface([snake_width, snake_width])
        self.image.fill(snake_colour)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.num = num

    def update(self):
        if len(snake_trail) > self.num + 1:
            self.rect.center = snake_trail[self.num]


class Kossie(pygame.sprite.Sprite):

    def __init__(self, pos):
        super(Kossie, self).__init__()
        self.image = pygame.Surface([snake_width - 4, snake_width - 4])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = pos


player_group = pygame.sprite.Group()
segment_group = pygame.sprite.Group()
kossie_group = pygame.sprite.Group()
head = Snake(windowWidth/2, windowHeight/2)
player_group.add(head)

for i in range(0, snake_segments):
    snake_trail.append([int(windowWidth/2) + (snake_width * snake_segments) - ((i+1) * snake_width), int(windowHeight/2)])
    segment = Segment(snake_trail[i], i)
    segment_group.add(segment)


def Eat():

    global snake_segments, snake_tick

    pos = [random.randrange(snake_width, windowWidth - snake_width, snake_width), random.randrange(snake_width, windowHeight - snake_width, snake_width)]

    if pos == head.rect.center or len(kossie_group) > 0:
        pass
    else:
        food = Kossie(pos)
        kossie_group.add(food)

    if pygame.sprite.spritecollide(head, kossie_group, True):
        snake_segments += 3
        for i in range(1, 4):
            add = Segment(snake_trail[1], snake_segments-i)
            segment_group.add(add)
            print(i)
        snake_tick += 0.05
    pygame.sprite.groupcollide(segment_group, kossie_group, False, True)


def collide():

    if pygame.sprite.spritecollide(head, segment_group, False):
        for idx, part in enumerate(segment_group):
            if idx < snake_segments:
                if pygame.sprite.collide_mask(head, part):
                    QuitGame()
                else:
                    pass


def QuitGame():

    pygame.quit()
    sys.exit()


# Main loop
while True:

    surface.fill([20, 40, 20])
    pygame.draw.rect(surface, border_colour, [0, 0, windowWidth, windowHeight], border_width)
    for event in GAME_EVENTS.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                QuitGame()

        if event.type == GAME_GLOBALS.QUIT:
            QuitGame()
    if head.rect.left < 10 or head.rect.top < 10 or head.rect.right > windowWidth - 10 or head.rect.bottom > windowHeight - 10:
        QuitGame()
    Eat()
    kossie_group.draw(surface)
    player_group.draw(surface)
    segment_group.draw(surface)
    player_group.update()
    segment_group.update()
    collide()
    pygame.display.flip()
    clock.tick(fps)
