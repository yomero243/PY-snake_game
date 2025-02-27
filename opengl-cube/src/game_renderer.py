# src/game_renderer.py
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class GameRenderer:
    def __init__(self, width, height):
        pygame.init()
        self.display = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.setup_gl(width, height)
        self.rotation = 0
        
    def setup_gl(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (width/height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        
    def draw_cube(self, x, y):
        glPushMatrix()
        # Convert 2D coordinates to 3D space
        glTranslatef(x * 0.1 - 1, y * 0.1 - 1, -5)
        glRotatef(self.rotation, 1, 1, 1)
        glScale(0.05, 0.05, 0.05)  # Make cube smaller
        
        # Draw cube
        glBegin(GL_QUADS)
        # Front face (red)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
        # Back face (green)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, -1, -1)
        glEnd()
        glPopMatrix()
        
        self.rotation += 1