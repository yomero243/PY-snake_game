# src/game_renderer.py
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from src.model_loader import ModelLoader

class GameRenderer:
    def __init__(self, width, height):
        pygame.init()
        self.display = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.setup_gl(width, height)
        self.rotation = 0
        self.models = {}  # Diccionario para almacenar modelos cargados
        
    def setup_gl(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width/height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        
    def draw_cube(self, x, y, color=(1.0, 1.0, 1.0)):
        glPushMatrix()
        glTranslatef(x * 0.1 - 1, y * 0.1 - 1, -5)
        glRotatef(self.rotation, 1, 1, 1)
        glScale(0.05, 0.05, 0.05)
        
        glBegin(GL_QUADS)
        # All faces use the same color
        glColor3f(*color)
        
        # Front face
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
        
        # Back face
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, -1, -1)
        
        # Top face
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 1, -1)
        
        # Bottom face
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, -1, 1)
        glVertex3f(-1, -1, 1)
        
        # Right face
        glVertex3f(1, -1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, -1, 1)
        
        # Left face
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, 1, -1)
        glEnd()
        
        glPopMatrix()
        self.rotation += 1
        
    def load_fbx_model(self, model_name, file_path):
        """Cargar un modelo FBX y almacenarlo con un nombre para referencia"""
        model = ModelLoader()
        if model.load_model(file_path):
            self.models[model_name] = model
            return True
        return False
    
    def draw_model(self, model_name, x, y, scale=0.01, rotation=None):
        """Dibujar un modelo cargado en una posición específica"""
        if model_name not in self.models:
            return False
            
        model = self.models[model_name]
        
        # Convertir coordenadas de juego a coordenadas 3D
        model_x = x * 0.1 - 1
        model_y = y * 0.1 - 1
        model_z = -5
        
        # Aplicar transformaciones
        model.set_position(model_x, model_y, model_z)
        model.set_scale(scale, scale, scale)
        
        # Aplicar rotación (usar la rotación global si no se especifica)
        if rotation is None:
            model.set_rotation(self.rotation, self.rotation, self.rotation)
        else:
            model.set_rotation(*rotation)
            
        # Dibujar el modelo
        glColor3f(1.0, 1.0, 1.0)  # Color blanco para el modelo
        model.draw()
        
        return True