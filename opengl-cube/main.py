from src.game_renderer import GameRenderer
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import sys
import os

class SnakeGame:
    def __init__(self, width, height):
        pygame.init()
        self.game = GameRenderer(width, height)
        self.clock = pygame.time.Clock()
        
        # Cargar el modelo FBX
        model_path = os.path.join(os.path.dirname(__file__), 'src', 'movie_camera.fbx')
        self.has_camera_model = self.game.load_fbx_model('camera', model_path)
        if not self.has_camera_model:
            print("¡Advertencia! No se pudo cargar el modelo de cámara. Se usará un cubo por defecto.")
        
        self.reset_game()

    def reset_game(self):
        # Game state
        self.snake = [[10, 10], [9, 10], [8, 10]]  # Initial snake position
        self.direction = [1, 0]  # Moving right initially
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        
    def generate_food(self):
        while True:
            food = [random.randint(0, 19), random.randint(0, 19)]
            if food not in self.snake:
                return food

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                # Arrow key controls with inverted up/down movement
                if event.key == pygame.K_UP and self.direction != [0, -1]:
                    self.direction = [0, 1]   # Down movement (inverted)
                elif event.key == pygame.K_DOWN and self.direction != [0, 1]:
                    self.direction = [0, -1]  # Up movement (inverted)
                elif event.key == pygame.K_LEFT and self.direction != [1, 0]:
                    self.direction = [-1, 0]  # Left movement
                elif event.key == pygame.K_RIGHT and self.direction != [-1, 0]:
                    self.direction = [1, 0]   # Right movement
                # Quit with 'q'
                elif event.key == pygame.K_q:
                    return False
                # Restart with spacebar when game is over
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        return True

    def update(self):
        if self.game_over:
            return

        # Calculate new head position
        new_head = [
            (self.snake[0][0] + self.direction[0]) % 20,  # Wrap around horizontally
            (self.snake[0][1] + self.direction[1]) % 20   # Wrap around vertically
        ]

        # Check if snake hits itself
        if new_head in self.snake:
            self.game_over = True
            return

        # Move snake
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            if i == 0:
                # Head color (red)
                self.game.draw_cube(segment[0], segment[1], color=(1.0, 0.0, 0.0))
            else:
                # Body color (green)
                self.game.draw_cube(segment[0], segment[1], color=(0.0, 1.0, 0.0))
        
        # Draw food (using model or cube)
        if self.has_camera_model:
            # Usar el modelo de cámara para la comida con una rotación progresiva
            self.game.draw_model('camera', self.food[0], self.food[1], scale=0.005)
        else:
            # Usar un cubo azul si no se pudo cargar el modelo
            self.game.draw_cube(self.food[0], self.food[1], color=(0.0, 0.0, 1.0))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            if running:
                self.update()
                self.render()
                self.clock.tick(10)  # Game speed
                
                # Display score and game instructions
                caption = f"Snake Game - Score: {self.score}"
                if self.game_over:
                    caption += " - GAME OVER! Press SPACE to restart or Q to quit"
                pygame.display.set_caption(caption)
        
        pygame.quit()
        sys.exit()

def main():
    game = SnakeGame(800, 600)
    game.run()

if __name__ == "__main__":
    main()