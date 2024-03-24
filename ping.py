import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

PAD_WIDTH, PAD_HEIGHT = 10, 100
BALL_RADIUS = 10

BALL_SPEED_X = 7
BALL_SPEED_Y = 7

def quit_game():
    pygame.quit()
    sys.exit()

# Клас ракетки
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, PAD_WIDTH, PAD_HEIGHT)

    def draw(self):
        pygame.draw.rect(win, WHITE, self.rect)

# Клас м'яча
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.direction_x = BALL_SPEED_X
        self.direction_y = BALL_SPEED_Y

    def draw(self):
        pygame.draw.circle(win, WHITE, self.rect.center, BALL_RADIUS)

    def move(self):
        self.rect.x += self.direction_x
        self.rect.y += self.direction_y

# Оновлення позицій ракеток та м'яча
def update_positions():
    global score_left, score_right

    player_paddle.rect.y = pygame.mouse.get_pos()[1] - PAD_HEIGHT // 2

    keys = pygame.key.get_pressed()
    if play_vs_bot:
        ai_paddle.rect.y = ball.rect.y - PAD_HEIGHT // 2
    else:
        if keys[pygame.K_UP]:
            ai_paddle.rect.y -= 10
        if keys[pygame.K_DOWN]:
            ai_paddle.rect.y += 10

    if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(ai_paddle.rect):
        ball.direction_x *= -1

    if ball.rect.y <= 0 or ball.rect.y >= HEIGHT - BALL_RADIUS * 2:
        ball.direction_y *= -1

    if ball.rect.x < 0:
        score_right += 1
        ball.rect.x = WIDTH // 2 - BALL_RADIUS
        ball.rect.y = HEIGHT // 2 - BALL_RADIUS
    elif ball.rect.x > WIDTH - BALL_RADIUS * 2:
        score_left += 1
        ball.rect.x = WIDTH // 2 - BALL_RADIUS
        ball.rect.y = HEIGHT // 2 - BALL_RADIUS



# Відображення гравців та м'яча на екрані
def draw_menu():
    win.fill(BLACK)
    font = pygame.font.Font(None, 36)

    play_vs_bot_text = font.render("Грати проти бота", True, WHITE)
    play_vs_bot_rect = play_vs_bot_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    play_2_players_text = font.render("Грати у двох", True, WHITE)
    play_2_players_rect = play_2_players_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    rules_text = font.render("Правила гри", True, WHITE)
    rules_rect = rules_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    exit_text = font.render("Вихід", True, WHITE)
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))

    win.blit(play_vs_bot_text, play_vs_bot_rect)
    win.blit(play_2_players_text, play_2_players_rect)
    win.blit(rules_text, rules_rect)
    win.blit(exit_text, exit_rect)

    pygame.display.update()

    return play_vs_bot_rect, play_2_players_rect, rules_rect, exit_rect

def draw():
    win.fill(BLACK)
    player_paddle.draw()
    ai_paddle.draw()
    ball.draw()

    font = pygame.font.Font(None, 36)
    text_left = font.render(str(score_left), True, WHITE)
    text_right = font.render(str(score_right), True, WHITE)
    win.blit(text_left, (WIDTH // 2 - 50, 20))
    win.blit(text_right, (WIDTH // 2 + 30, 20))

    pygame.display.update()

player_paddle = Paddle(30, HEIGHT // 2 - PAD_HEIGHT // 2)
ai_paddle = Paddle(WIDTH - 40, HEIGHT // 2 - PAD_HEIGHT // 2)
ball = Ball(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS)

score_left = 0
score_right = 0


# Головний цикл гри
running = True
clock = pygame.time.Clock()
menu = True
play_vs_bot = False
play_2_players = False
rules = False

while running:
    while menu:
        play_vs_bot_rect, play_2_players_rect, rules_rect, exit_rect = draw_menu()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_vs_bot_rect.collidepoint(mouse_x, mouse_y):
                    menu = False
                    play_vs_bot = True
                elif play_2_players_rect.collidepoint(mouse_x, mouse_y):
                    menu = False
                    play_2_players = True
                elif rules_rect.collidepoint(mouse_x, mouse_y):
                    rules = True
                elif exit_rect.collidepoint(mouse_x, mouse_y):
                    running = False
                    menu = False

        while rules:
            # Виведення правил гри
            win.fill(BLACK)
            font = pygame.font.Font(None, 36)
            rules_text = "Правила гри:"
            rule1 = ("- Ви контролюєте ракетку, рухаючи мишкою, другий "
                     "гравець керує стрілочками.")
            rule2 = ("- Завдання - відбивати м'яч, щоб він не пролетів "
                     "за вашу ракетку.")
            rule3 = ("- Гравець, який пропустив м'яч, додає одне "
                     "очко суперникові.")
            rule4 = "- Гра триває до  безкінечності(поки що)."
            back_text = "Назад"
            rules_rect = font.render(rules_text, True, WHITE)
            rule1_rect = font.render(rule1, True, WHITE)
            rule2_rect = font.render(rule2, True, WHITE)
            rule3_rect = font.render(rule3, True, WHITE)
            rule4_rect = font.render(rule4, True, WHITE)
            back_text_rect = font.render(back_text, True, WHITE)

            win.blit(rules_rect, (50, 50))
            win.blit(rule1_rect, (50, 100))
            win.blit(rule2_rect, (50, 150))
            win.blit(rule3_rect, (50, 200))
            win.blit(rule4_rect, (50, 250))
            win.blit(back_text_rect, (50, 300))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if back_text_rect.get_rect().collidepoint(mouse_x, mouse_y):
                        rules = False
                        menu = True

        # Гра проти бота
        while play_vs_bot:
            game_over = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        play_vs_bot = False
                        menu = True
                        score_left = score_right = 0
                        ball.rect.x = WIDTH // 2 - BALL_RADIUS
                        ball.rect.y = HEIGHT // 2 - BALL_RADIUS
                        ball.direction_x = BALL_SPEED_X
                        ball.direction_y = BALL_SPEED_Y
                    elif event.key == pygame.K_ESCAPE:
                        quit_game()

            if not game_over:
                update_positions()
                ball.move()

            if score_right == 5:
                win.fill(BLACK)
                font = pygame.font.Font(None, 72)
                text = font.render("Програш:(", True, WHITE)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                win.blit(text, text_rect)
                pygame.display.update()
                game_over = True
                running = False
            elif score_left == 5:
                win.fill(BLACK)
                font = pygame.font.Font(None, 72)
                text = font.render("Перемога:)", True, WHITE)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                win.blit(text, text_rect)
                pygame.display.update()
                game_over = True
                running = False

            draw()
            clock.tick(60)


            # Гра у двох гравців
        while play_2_players:
            game_over = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        play_2_players = False
                        menu = True
                        score_left = score_right = 0
                        ball.rect.x = WIDTH // 2 - BALL_RADIUS
                        ball.rect.y = HEIGHT // 2 - BALL_RADIUS
                        ball.direction_x = BALL_SPEED_X
                        ball.direction_y = BALL_SPEED_Y

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_paddle.rect.y -= 7
            if keys[pygame.K_DOWN]:
                player_paddle.rect.y += 7

            if not game_over:
                update_positions()
                ball.move()
            draw()
            clock.tick(60)


