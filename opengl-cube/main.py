from src.game_renderer import GameRenderer
import pygame
from OpenGL.GL import *
import random
import sys
import os

class SnakeGame:
    def __init__(self, width, height):
        pygame.init()
        self.game = GameRenderer(width, height) # Inicializa Pygame y contexto GL
        self.clock = pygame.time.Clock()
        
        # Crear instancia del cargador para el fondo
        model_path = os.path.join(os.path.dirname(__file__), 'src', 'movie_camera.fbx')
        background_model_loader = self.game.load_fbx_model('background_camera', model_path)
        
        # Ahora que el contexto GL está activo, cargar el modelo
        self.has_background_model = False
        if background_model_loader:
            print(f"Intentando cargar datos GL para el modelo: background_camera")
            if background_model_loader.load_model(model_path):
                self.has_background_model = True
                print("Modelo cargado exitosamente!")
            else:
                print(f"Fallo al cargar datos GL para el modelo")
        
        if not self.has_background_model:
            print("¡Advertencia! No se pudo cargar el modelo de cámara para el fondo.")
        
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
        
        # Dibujar el modelo de fondo si está cargado
        if self.has_background_model:
            # Ajusta scale y z_distance según necesites
            self.game.draw_background_model('background_camera', scale=0.02, z_distance=15.0) 
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            if i == 0:
                # Head color (red)
                self.game.draw_cube(segment[0], segment[1], color=(1.0, 0.0, 0.0))
            else:
                # Body color (green)
                self.game.draw_cube(segment[0], segment[1], color=(0.0, 1.0, 0.0))
        
        # Draw food (blue cube)
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
        
        # Limpiar recursos antes de salir
        self.game.cleanup() 
        pygame.quit()
        sys.exit()

def main():
    game = SnakeGame(800, 600)
    game.run()

if __name__ == "__main__":
    main()