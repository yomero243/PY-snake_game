from src.game_renderer import GameRenderer
import pygame
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

def main():
    # Inicializar el juego con una ventana de 800x600
    game = GameRenderer(800, 600)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Limpiar la pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Dibujar un cubo de ejemplo en la posición (5, 5)
        game.draw_cube(5, 5)
        
        # Actualizar la pantalla
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()