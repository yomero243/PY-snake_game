# src/game_renderer.py
import pygame
import os
import ctypes
import numpy as np
from OpenGL.GL import *
import glm
from src.shader_loader import ShaderLoader
from src.model_loader import ModelLoader

class GameRenderer:
    def __init__(self, width, height):
        pygame.init()
        
        # Configurar atributos OpenGL para Core Profile (necesario en macOS)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, 
                                      pygame.GL_CONTEXT_PROFILE_CORE)
        
        # Crear ventana con contexto OpenGL
        self.display = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.width = width
        self.height = height
        
        # Inicializar shaders y configuración GL
        self.setup_gl()
        
        # Variables para rotación
        self.background_rotation_z = 0
        self.models = {}  # Diccionario para almacenar modelos cargados
        
        # Inicializar VBO/VAO para el cubo
        self.setup_cube_buffers()
    
    def setup_gl(self):
        """Configuración moderna de OpenGL con shaders"""
        # Cargar shaders
        current_dir = os.path.dirname(os.path.abspath(__file__))
        vertex_path = os.path.join(current_dir, 'shaders', 'vertex.glsl')
        fragment_path = os.path.join(current_dir, 'shaders', 'fragment.glsl')
        
        self.shader = ShaderLoader()
        self.shader.load_shader(vertex_path, fragment_path)
        
        # Configuración de OpenGL
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.05, 0.05, 0.05, 1.0)  # Fondo gris oscuro
        
        # Crear matrices de proyección y vista
        self.update_matrices()
    
    def update_matrices(self):
        """Actualizar matrices de proyección y vista"""
        # Matriz de proyección (perspectiva)
        self.projection = glm.perspective(glm.radians(45.0), self.width / self.height, 0.1, 50.0)
        
        # Matriz de vista (posición de cámara)
        self.view = glm.lookAt(
            glm.vec3(0.0, 0.0, 3.0),  # Posición de la cámara
            glm.vec3(0.0, 0.0, 0.0),  # Punto hacia donde mira
            glm.vec3(0.0, 1.0, 0.0)   # Vector "arriba"
        )
        
        # Posición de la luz y del observador (para shading)
        self.light_pos = glm.vec3(5.0, 5.0, 5.0)
        self.view_pos = glm.vec3(0.0, 0.0, 3.0)
    
    def setup_cube_buffers(self):
        """Configuración de VBO y VAO para el cubo"""
        # Vértices del cubo (posición, normales)
        cube_vertices = np.array([
            # Cara frontal
            -1.0, -1.0,  1.0,  0.0,  0.0,  1.0, # Abajo-izq
             1.0, -1.0,  1.0,  0.0,  0.0,  1.0, # Abajo-der
             1.0,  1.0,  1.0,  0.0,  0.0,  1.0, # Arriba-der
            -1.0,  1.0,  1.0,  0.0,  0.0,  1.0, # Arriba-izq
            
            # Cara trasera
            -1.0, -1.0, -1.0,  0.0,  0.0, -1.0, # Abajo-izq
            -1.0,  1.0, -1.0,  0.0,  0.0, -1.0, # Arriba-izq
             1.0,  1.0, -1.0,  0.0,  0.0, -1.0, # Arriba-der
             1.0, -1.0, -1.0,  0.0,  0.0, -1.0, # Abajo-der
            
            # Cara superior
            -1.0,  1.0, -1.0,  0.0,  1.0,  0.0, # Atrás-izq
            -1.0,  1.0,  1.0,  0.0,  1.0,  0.0, # Frente-izq
             1.0,  1.0,  1.0,  0.0,  1.0,  0.0, # Frente-der
             1.0,  1.0, -1.0,  0.0,  1.0,  0.0, # Atrás-der
            
            # Cara inferior
            -1.0, -1.0, -1.0,  0.0, -1.0,  0.0, # Atrás-izq
             1.0, -1.0, -1.0,  0.0, -1.0,  0.0, # Atrás-der
             1.0, -1.0,  1.0,  0.0, -1.0,  0.0, # Frente-der
            -1.0, -1.0,  1.0,  0.0, -1.0,  0.0, # Frente-izq
            
            # Cara derecha
             1.0, -1.0, -1.0,  1.0,  0.0,  0.0, # Abajo-atrás
             1.0,  1.0, -1.0,  1.0,  0.0,  0.0, # Arriba-atrás
             1.0,  1.0,  1.0,  1.0,  0.0,  0.0, # Arriba-frente
             1.0, -1.0,  1.0,  1.0,  0.0,  0.0, # Abajo-frente
            
            # Cara izquierda
            -1.0, -1.0, -1.0, -1.0,  0.0,  0.0, # Abajo-atrás
            -1.0, -1.0,  1.0, -1.0,  0.0,  0.0, # Abajo-frente
            -1.0,  1.0,  1.0, -1.0,  0.0,  0.0, # Arriba-frente
            -1.0,  1.0, -1.0, -1.0,  0.0,  0.0  # Arriba-atrás
        ], dtype=np.float32)
        
        # Índices para dibujar las 6 caras del cubo (2 triángulos por cara)
        cube_indices = np.array([
            0, 1, 2, 2, 3, 0,       # Cara frontal
            4, 5, 6, 6, 7, 4,       # Cara trasera
            8, 9, 10, 10, 11, 8,    # Cara superior
            12, 13, 14, 14, 15, 12, # Cara inferior
            16, 17, 18, 18, 19, 16, # Cara derecha
            20, 21, 22, 22, 23, 20  # Cara izquierda
        ], dtype=np.uint32)
        
        # Crear VAO, VBO y EBO
        self.cube_vao = glGenVertexArrays(1)
        self.cube_vbo = glGenBuffers(1)
        self.cube_ebo = glGenBuffers(1)
        
        # Vincular VAO
        glBindVertexArray(self.cube_vao)
        
        # Configurar VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.cube_vbo)
        glBufferData(GL_ARRAY_BUFFER, cube_vertices.nbytes, cube_vertices, GL_STATIC_DRAW)
        
        # Configurar EBO
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.cube_ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, cube_indices.nbytes, cube_indices, GL_STATIC_DRAW)
        
        # Configurar atributos de vértice
        # Posición (location 0)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 
                             6 * np.dtype(np.float32).itemsize, 
                             ctypes.c_void_p(0))
        
        # Normal (location 1)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 
                             6 * np.dtype(np.float32).itemsize, 
                             ctypes.c_void_p(3 * np.dtype(np.float32).itemsize))
        
        # Desvincular
        glBindVertexArray(0)
    
    def draw_cube(self, x, y, color=(1.0, 1.0, 1.0)):
        """Dibujar cubo usando shaders y transformaciones modernas"""
        # Matriz de modelo para este cubo específico
        model = glm.mat4(1.0)  # Matriz identidad
        model = glm.translate(model, glm.vec3(x * 0.1 - 1, y * 0.1 - 1, -5.0))
        model = glm.scale(model, glm.vec3(0.05, 0.05, 0.05))
        
        # Usar shader y configurar uniforms
        self.shader.use()
        self.shader.set_mat4("model", model)
        self.shader.set_mat4("view", self.view)
        self.shader.set_mat4("projection", self.projection)
        self.shader.set_vec3("lightPos", self.light_pos)
        self.shader.set_vec3("viewPos", self.view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        self.shader.set_vec3("objectColor", color)
        
        # Dibujar
        glBindVertexArray(self.cube_vao)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
    
    def load_fbx_model(self, model_name, file_path):
        """Crea una instancia de ModelLoader para un modelo FBX"""
        model = ModelLoader() 
        self.models[model_name] = model
        print(f"Instancia de ModelLoader creada para '{model_name}'.")
        return model
    
    def draw_background_model(self, model_name, scale=1.0, z_distance=10.0):
        """Dibujar un modelo FBX como fondo, rotando en Z"""
        if model_name not in self.models:
            return False
            
        model_loader = self.models[model_name]
        
        # Crear matriz de modelo para el fondo
        model_matrix = glm.mat4(1.0)
        model_matrix = glm.translate(model_matrix, glm.vec3(0.0, 0.0, -z_distance))
        model_matrix = glm.rotate(model_matrix, glm.radians(self.background_rotation_z), glm.vec3(0.0, 0.0, 1.0))
        model_matrix = glm.scale(model_matrix, glm.vec3(scale, scale, scale))
        
        # Configurar shader
        self.shader.use()
        self.shader.set_mat4("model", model_matrix)
        self.shader.set_mat4("view", self.view)
        self.shader.set_mat4("projection", self.projection)
        self.shader.set_vec3("lightPos", self.light_pos)
        self.shader.set_vec3("viewPos", self.view_pos)
        self.shader.set_vec3("lightColor", (1.0, 1.0, 1.0))
        self.shader.set_vec3("objectColor", (0.8, 0.8, 0.8))  # Color gris claro
        
        # Dibujar el modelo
        model_loader.draw()
        
        # Incrementar rotación
        self.background_rotation_z = (self.background_rotation_z + 0.5) % 360
        return True
    
    def cleanup(self):
        """Limpia todos los recursos OpenGL"""
        print("Limpiando GameRenderer...")
        
        # Limpiar modelos
        for model_name, model in self.models.items():
            print(f"Limpiando modelo: {model_name}")
            model.cleanup()
        self.models = {}
        
        # Limpiar recursos del cubo
        if hasattr(self, 'cube_vao'):
            glDeleteVertexArrays(1, [self.cube_vao])
        if hasattr(self, 'cube_vbo'):
            glDeleteBuffers(1, [self.cube_vbo])
        if hasattr(self, 'cube_ebo'):
            glDeleteBuffers(1, [self.cube_ebo])
            
        # Limpiar shader
        if hasattr(self, 'shader'):
            self.shader.cleanup()