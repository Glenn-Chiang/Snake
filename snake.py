import pygame
from sys import exit
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

small_font = pygame.font.SysFont('consolas', 20)
large_font = pygame.font.SysFont('consolas', 50)

title_text = large_font.render('S N A K E', 1, WHITE)
game_over_text = large_font.render('GAME OVER', 1, WHITE)
start_prompt = small_font.render('Press [SPACE] to start', 1, WHITE)
restart_prompt = small_font.render('Press [SPACE] to restart', 1, WHITE)


class Snake():

    def __init__(self):
        self.seg_size = 20
        self.num_segs = 8
        self.direction = 'RIGHT'
        self.start_pos = (20, SCREEN_HEIGHT//2)

        self.positions = [(self.start_pos[0] + seg_num * self.seg_size, self.start_pos[1])
                          for seg_num in range(self.num_segs)]  # list of tuples(coordinates) of each of the snake's body segments

        self.segments = [pygame.Rect(pos[0], pos[1], self.seg_size, self.seg_size)
                         for pos in self.positions]  # list of rects which are the snake's body segments
        self.head = self.segments[-1]

    def grow(self):
        tail = self.segments[0]
        adj_seg = self.segments[1]

        # Tail is moving right
        if tail.x < adj_seg.x:
            new_seg = pygame.Rect(tail.x - self.seg_size,
                                  tail.y, self.seg_size, self.seg_size)
        # Tail is moving left
        if tail.x > adj_seg.x:
            new_seg = pygame.Rect(tail.x + self.seg_size,
                                  tail.y, self.seg_size, self.seg_size)
        # Tail is moving up
        if tail.y < adj_seg.y:
            new_seg = pygame.Rect(
                tail.x, tail.y + self.seg_size, self.seg_size, self.seg_size)
        # Tail is moving down
        if tail.y > adj_seg.y:
            new_seg = pygame.Rect(
                tail.x, tail.y - self.seg_size, self.seg_size, self.seg_size)

        self.segments.insert(0, new_seg)
        self.positions.insert(0, (new_seg.x, new_seg.y))

    def move(self):

        # Move head first
        head = self.segments[-1]
        cur_head = head.copy()
        cur_head_pos = (head.x, head.y)

        if self.direction == 'RIGHT':
            self.positions[-1] = (head.x + self.seg_size, head.y)
            head.x += self.seg_size

        if self.direction == 'LEFT':
            self.positions[-1] = (head.x - self.seg_size, head.y)
            head.x -= self.seg_size

        if self.direction == 'UP':
            self.positions[-1] = (head.x, head.y - self.seg_size)
            head.y -= self.seg_size

        if self.direction == 'DOWN':
            self.positions[-1] = (head.x, head.y + self.seg_size)
            head.y += self.seg_size

        # Rest of body
        for idx, seg in enumerate(self.segments[:len(self.segments)-1]):
            if idx < len(self.segments) - 2:
                self.segments[idx] = self.segments[idx+1].copy()
                new_pos = (self.segments[idx].x, self.segments[idx].y)
            else:
                self.segments[idx] = cur_head
                new_pos = cur_head_pos

            self.positions[idx] = new_pos

    def check_wall_collision(self):
        head = self.segments[-1]

        if head.x + self.seg_size >= SCREEN_WIDTH and self.direction == 'RIGHT':
            return True

        if head.x <= 0 and self.direction == 'LEFT':
            return True

        if head.y <= 0 and self.direction == 'UP':
            return True

        if head.y + self.seg_size >= SCREEN_HEIGHT and self.direction == 'DOWN':
            return True

        return False

    def check_self_collision(self):
        head = self.segments[-1]

        for i, seg in enumerate(self.segments):
            if i < len(self.segments) - 2 and head.colliderect(seg):
                return True

        return False


def spawn_apple(snake, all_positions):
    # Ensure apple does not spawn inside snake
    available_positions = [
        pos for pos in all_positions if pos not in snake.positions]
    spawn_pos = random.choice(available_positions)
    apple = pygame.Rect(spawn_pos[0], spawn_pos[1],
                        snake.seg_size, snake.seg_size)
    return apple


def draw_snake(snake):
    for i, seg in enumerate(snake.segments):
        if i < len(snake.segments) - 1:
            pygame.draw.rect(screen, RED, seg)
        else:  # head
            pygame.draw.rect(screen, WHITE, seg)


def draw_entities(snake, apple, score):

    draw_snake(snake)
    pygame.draw.rect(screen, GREEN, apple)

    score_text = small_font.render(f'Score: {score}', 1, WHITE)
    screen.blit(score_text, (20, 20))


def draw_start_screen_text():
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width() //
                2, SCREEN_HEIGHT//2 - title_text.get_height()//2))
    screen.blit(start_prompt, (SCREEN_WIDTH//2 - start_prompt.get_width() //
                2, SCREEN_HEIGHT//2 + title_text.get_height()//2))


def draw_game_over_screen_text():
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width() //
                2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
    screen.blit(restart_prompt, (SCREEN_WIDTH//2 - restart_prompt.get_width() //
                2, SCREEN_HEIGHT//2 + game_over_text.get_height()//2))


def main():
    game_state = 1
    snake = Snake()
    score = 0

    all_positions = []
    for y_pos in range(0, SCREEN_HEIGHT, snake.seg_size):
        for x_pos in range(0, SCREEN_WIDTH, snake.seg_size):
            all_positions.append((x_pos, y_pos))

    apple_exists = True
    apple = spawn_apple(snake, all_positions)

    while True:
        screen.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Pre-game
        if game_state == 0:

            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state = 1

            draw_start_screen_text()

        # In-game
        if game_state == 1:

            if not apple_exists:
                apple = spawn_apple(snake, all_positions)
                apple_exists = True

            for event in events:
                if event.type == pygame.KEYDOWN:
                    # Get player input to change direction
                    if snake.direction == 'RIGHT' or snake.direction == 'LEFT':
                        if event.key == pygame.K_UP:
                            snake.direction = 'UP'
                        elif event.key == pygame.K_DOWN:
                            snake.direction = 'DOWN'

                    if snake.direction == 'UP' or snake.direction == 'DOWN':
                        if event.key == pygame.K_LEFT:
                            snake.direction = 'LEFT'
                        elif event.key == pygame.K_RIGHT:
                            snake.direction = 'RIGHT'
                    break

            if snake.check_wall_collision() or snake.check_self_collision():
                game_state = 2
            else:
                snake.move()

            if snake.head.colliderect(apple):
                score += 1
                snake.grow()
                apple_exists = False

        draw_entities(snake, apple, score)

        # Post-game / Game over
        if game_state == 2:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    main()

            draw_game_over_screen_text()

        pygame.display.update()
        clock.tick(15)


main()
