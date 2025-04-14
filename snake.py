import pygame
import random
import sys
import time

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 25  
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

snake_color = GREEN
food_color = RED
bomb_color = ORANGE
background_color = BLACK
difficulty = 1
game_speed = 10

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0)
        ])
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        if new_position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def render(self, surface):
        for position in self.positions:
            rect = pygame.Rect(
                position[0] * GRID_SIZE, 
                position[1] * GRID_SIZE, 
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, snake_color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
    
    def render(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, food_color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

class Bomb:
    def __init__(self):
        self.positions = []
        self.active = False
        
    def spawn_bombs(self, snake_positions, food_position, count=3):
        self.positions = []
        for _ in range(count):
            position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            while position in snake_positions or position == food_position or position in self.positions:
                position = (
                    random.randint(0, GRID_WIDTH - 1),
                    random.randint(0, GRID_HEIGHT - 1)
                )
            self.positions.append(position)
        self.active = True
        
    def render(self, surface):
        if self.active:
            for position in self.positions:
                rect = pygame.Rect(
                    position[0] * GRID_SIZE,
                    position[1] * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE
                )
                pygame.draw.rect(surface, bomb_color, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        self.big_font = pygame.font.SysFont('Arial', 40)
        self.snake = Snake()
        self.food = Food()
        self.bomb = Bomb()
        self.state = "MENU"
        self.update_count = 0
        self.move_speed = 6
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.state == "GAME":
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                        
                elif self.state == "MENU" or self.state == "GAME_OVER":
                    if event.key == pygame.K_RETURN:
                        self.snake.reset()
                        self.food.randomize_position()
                        self.bomb.active = False
                        self.state = "GAME"
                    elif event.key == pygame.K_s and self.state == "MENU":
                        self.state = "SETTINGS"
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                        
                elif self.state == "SETTINGS":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                    elif event.key == pygame.K_1:
                        global snake_color
                        snake_color = GREEN
                    elif event.key == pygame.K_2:
                        snake_color = BLUE
                    elif event.key == pygame.K_3:
                        snake_color = YELLOW
                    elif event.key == pygame.K_4:
                        snake_color = PURPLE
                    elif event.key == pygame.K_e:
                        global difficulty, game_speed
                        difficulty = 1
                        game_speed = 10
                        self.move_speed = 6
                    elif event.key == pygame.K_m:
                        difficulty = 2
                        game_speed = 15
                        self.move_speed = 4
                    elif event.key == pygame.K_h:
                        difficulty = 3
                        game_speed = 20
                        self.move_speed = 3
    
    def update(self):
        if self.state == "GAME":
            self.update_count += 1
            if self.update_count >= self.move_speed:
                self.update_count = 0
                self.snake.update()
                
                if self.snake.get_head_position() == self.food.position:
                    self.snake.length += 1
                    self.snake.score += difficulty * 10
                    self.food.randomize_position()
                    
                    while self.food.position in self.snake.positions or (self.bomb.active and self.food.position in self.bomb.positions):
                        self.food.randomize_position()
                    
                    if difficulty >= 2 and not self.bomb.active:
                        bomb_count = 3 if difficulty == 2 else 5
                        self.bomb.spawn_bombs(self.snake.positions, self.food.position, bomb_count)
                
                if self.bomb.active:
                    if self.snake.get_head_position() in self.bomb.positions:
                        self.snake.score = max(0, self.snake.score - 10)
                        self.bomb.positions.remove(self.snake.get_head_position())
                        if not self.bomb.positions:
                            self.bomb.active = False
    
    def render_menu(self):
        self.screen.fill(BLACK)
        
        title = self.big_font.render("SNAKE GAME", True, WHITE)
        play_text = self.font.render("Press ENTER to Play", True, WHITE)
        settings_text = self.font.render("Press S for Settings", True, WHITE)
        quit_text = self.font.render("Press Q to Quit", True, WHITE)
        
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        self.screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2))
        self.screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 2 + 40))
        self.screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 80))
        
    def render_settings(self):
        self.screen.fill(BLACK)
        
        title = self.big_font.render("SETTINGS", True, WHITE)
        back_text = self.font.render("Press ESC to go back", True, WHITE)
        
        color_title = self.font.render("Snake Color:", True, WHITE)
        color_1 = self.font.render("1: Green", True, GREEN)
        color_2 = self.font.render("2: Blue", True, BLUE)
        color_3 = self.font.render("3: Yellow", True, YELLOW)
        color_4 = self.font.render("4: Purple", True, PURPLE)
        
        diff_title = self.font.render("Difficulty:", True, WHITE)
        diff_1 = self.font.render("E: Easy (No bombs)", True, WHITE)
        diff_2 = self.font.render("M: Medium (3 bombs)", True, WHITE)
        diff_3 = self.font.render("H: Hard (5 bombs)", True, WHITE)
        
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        self.screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 50))
        
        self.screen.blit(color_title, (WIDTH // 4, 150))
        self.screen.blit(color_1, (WIDTH // 4, 180))
        self.screen.blit(color_2, (WIDTH // 4, 210))
        self.screen.blit(color_3, (WIDTH // 4, 240))
        self.screen.blit(color_4, (WIDTH // 4, 270))
        
        self.screen.blit(diff_title, (WIDTH // 4 * 3 - diff_title.get_width(), 150))
        self.screen.blit(diff_1, (WIDTH // 4 * 3 - diff_1.get_width(), 180))
        self.screen.blit(diff_2, (WIDTH // 4 * 3 - diff_2.get_width(), 210))
        self.screen.blit(diff_3, (WIDTH // 4 * 3 - diff_3.get_width(), 240))
        
        current_color = self.font.render(f"Current: {snake_color}", True, snake_color)
        current_diff = self.font.render(f"Current: {'Easy' if difficulty == 1 else 'Medium' if difficulty == 2 else 'Hard'}", True, WHITE)
        
        self.screen.blit(current_color, (WIDTH // 4, 320))
        self.screen.blit(current_diff, (WIDTH // 4 * 3 - current_diff.get_width(), 320))
        
        bomb_info = self.font.render("Bombs: -10 points when collected", True, bomb_color)
        self.screen.blit(bomb_info, (WIDTH // 2 - bomb_info.get_width() // 2, 380))
        
    def render_game_over(self):
        self.screen.fill(BLACK)
        
        title = self.big_font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Score: {self.snake.score}", True, WHITE)
        play_again = self.font.render("Press ENTER to Play Again", True, WHITE)
        menu_text = self.font.render("Press ESC for Menu", True, WHITE)
        
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        self.screen.blit(play_again, (WIDTH // 2 - play_again.get_width() // 2, HEIGHT // 2 + 40))
        self.screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 80))
        
    def render_game(self):
        self.screen.fill(background_color)
        
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (20, 20, 20), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (20, 20, 20), (0, y), (WIDTH, y))
            
        pygame.draw.rect(self.screen, WHITE, (0, 0, WIDTH, HEIGHT), 2)
        
        score_text = self.font.render(f"Score: {self.snake.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        diff_text = self.font.render(f"Difficulty: {'Easy' if difficulty == 1 else 'Medium' if difficulty == 2 else 'Hard'}", True, WHITE)
        self.screen.blit(diff_text, (WIDTH - diff_text.get_width() - 10, 10))
        
        self.snake.render(self.screen)
        self.food.render(self.screen)
        if self.bomb.active:
            self.bomb.render(self.screen)
        
    def render(self):
        if self.state == "MENU":
            self.render_menu()
        elif self.state == "SETTINGS":
            self.render_settings()
        elif self.state == "GAME":
            self.render_game()
        elif self.state == "GAME_OVER":
            self.render_game_over()
            
        pygame.display.update()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
