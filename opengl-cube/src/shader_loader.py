import os
import numpy as np
from OpenGL.GL import *
import glm

class ShaderLoader:
    """Clase para cargar y gestionar programas de shader OpenGL"""
    
    def __init__(self):
        self.program = None
        
    def load_shader(self, vertex_file_path, fragment_file_path):
        """Cargar y compilar shaders desde archivos"""
        # Leer códigos fuente
        with open(vertex_file_path, 'r') as file:
            vertex_source = file.read()
            
        with open(fragment_file_path, 'r') as file:
            fragment_source = file.read()
        
        # Crear y compilar el shader de vértice
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_source)
        glCompileShader(vertex_shader)
        self._check_compile_errors(vertex_shader, "VERTEX")
        
        # Crear y compilar el shader de fragmento
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_source)
        glCompileShader(fragment_shader)
        self._check_compile_errors(fragment_shader, "FRAGMENT")
        
        # Crear programa de shader
        self.program = glCreateProgram()
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)
        self._check_compile_errors(self.program, "PROGRAM")
        
        # Eliminar shaders ya que ya están vinculados
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        
        return self.program
    
    def _check_compile_errors(self, shader, shader_type):
        """Verificar errores de compilación o enlace"""
        if shader_type != "PROGRAM":
            success = glGetShaderiv(shader, GL_COMPILE_STATUS)
            if not success:
                info_log = glGetShaderInfoLog(shader).decode('utf-8')
                print(f"ERROR::SHADER_COMPILATION::{shader_type}\n{info_log}")
        else:
            success = glGetProgramiv(shader, GL_LINK_STATUS)
            if not success:
                info_log = glGetProgramInfoLog(shader).decode('utf-8')
                print(f"ERROR::PROGRAM_LINKING::{shader_type}\n{info_log}")
    
    def use(self):
        """Activar programa de shader"""
        glUseProgram(self.program)
    
    def set_bool(self, name, value):
        """Establecer uniform boolean"""
        glUniform1i(glGetUniformLocation(self.program, name), int(value))
    
    def set_int(self, name, value):
        """Establecer uniform int"""
        glUniform1i(glGetUniformLocation(self.program, name), value)
    
    def set_float(self, name, value):
        """Establecer uniform float"""
        glUniform1f(glGetUniformLocation(self.program, name), value)
    
    def set_vec3(self, name, value):
        """Establecer uniform vec3"""
        if isinstance(value, (list, tuple)):
            glUniform3f(glGetUniformLocation(self.program, name), value[0], value[1], value[2])
        else:  # Asumimos que es un glm.vec3
            glUniform3f(glGetUniformLocation(self.program, name), value.x, value.y, value.z)
    
    def set_mat4(self, name, mat):
        """Establecer uniform mat4"""
        # Flatten para convertir a array 1D y transponerla para OpenGL (column-major)
        loc = glGetUniformLocation(self.program, name)
        if isinstance(mat, list):  # Handle Python lists
            flat_mat = []
            for col in range(4):
                for row in range(4):
                    flat_mat.append(mat[row][col])
            glUniformMatrix4fv(loc, 1, GL_FALSE, flat_mat)
        else:  # Asumimos que es una matriz de glm
            glUniformMatrix4fv(loc, 1, GL_FALSE, glm.value_ptr(mat))
    
    def cleanup(self):
        """Liberar recursos del programa de shader"""
        if self.program:
            glDeleteProgram(self.program)
            self.program = None 