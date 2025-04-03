import pyassimp
import pyassimp.postprocess
import numpy as np
import ctypes
from OpenGL.GL import *
# Importar funciones específicas de VBO/VAO
from OpenGL.GL import glGenBuffers, glBindBuffer, glBufferData, glGenVertexArrays, glBindVertexArray, glEnableVertexAttribArray, glVertexAttribPointer, glDeleteBuffers, glDeleteVertexArrays, GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW, GL_FLOAT, GL_UNSIGNED_INT, GL_TRIANGLES, glDrawElements
from pyassimp.errors import AssimpError # Importar explícitamente

class ModelLoader:
    def __init__(self):
        # self.meshes ahora almacenará VAOs, VBOs, EBOs y conteo de índices
        self.meshes_gl = [] 
        # Mantener las transformaciones aquí, aunque se apliquen fuera en el renderer
        self.model_position = [0, 0, 0] 
        self.model_scale = [1, 1, 1]
        self.model_rotation = [0, 0, 0]

    def load_model(self, file_path):
        """Cargar un modelo 3D desde archivo FBX usando OpenGL moderno"""
        scene = None 
        try:
            with pyassimp.load(file_path, 
                             processing=pyassimp.postprocess.aiProcess_Triangulate | 
                                       pyassimp.postprocess.aiProcess_FlipUVs | 
                                       pyassimp.postprocess.aiProcess_GenSmoothNormals) as scene:
            
                if not scene or not scene.meshes:
                    print(f"Error: No se encontraron mallas en {file_path}")
                    return False

                for mesh in scene.meshes:
                    vertices_data = []
                    if not hasattr(mesh, 'vertices') or not mesh.vertices.size:
                         print(f"Advertencia: Malla sin vértices en {file_path}")
                         continue

                    has_normals = hasattr(mesh, 'normals') and mesh.normals.size > 0
                    if not has_normals:
                         print(f"Advertencia: Malla sin normales en {file_path}")

                    for i in range(len(mesh.vertices)):
                        vertex = mesh.vertices[i]
                        normal = mesh.normals[i] if has_normals else [0.0, 0.0, 1.0]
                        vertices_data.extend([vertex[0], vertex[1], vertex[2], 
                                              normal[0], normal[1], normal[2]])
                    
                    vertices_np = np.array(vertices_data, dtype=np.float32)
                    
                    indices = []
                    if hasattr(mesh, 'faces'):
                        for face in mesh.faces:
                             if len(face) == 3:
                                 indices.extend(face)
                             else:
                                 print(f"Advertencia: Cara no triangular en {file_path}")
                    
                    if not indices:
                        print(f"Advertencia: Malla sin índices válidos en {file_path}")
                        continue 

                    indices_np = np.array(indices, dtype=np.uint32)
                    
                    # --- Crear VAO, VBO, EBO con OpenGL Core Profile ---
                    vao = glGenVertexArrays(1)
                    vbo = glGenBuffers(1)
                    ebo = glGenBuffers(1)
                    
                    glBindVertexArray(vao)
                    
                    # Subir datos de vértices
                    glBindBuffer(GL_ARRAY_BUFFER, vbo)
                    glBufferData(GL_ARRAY_BUFFER, vertices_np.nbytes, vertices_np, GL_STATIC_DRAW)
                    
                    # Subir índices
                    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
                    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_np.nbytes, indices_np, GL_STATIC_DRAW)
                    
                    # Configurar atributos de vértice
                    stride = 6 * vertices_np.itemsize
                    
                    # Atributo de posición (location = 0 en el shader)
                    glEnableVertexAttribArray(0)
                    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
                    
                    # Atributo de normal (location = 1 en el shader)
                    glEnableVertexAttribArray(1)
                    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, 
                                         ctypes.c_void_p(3 * vertices_np.itemsize))
                    
                    # Desvincular VAO
                    glBindVertexArray(0)
                    
                    # Almacenar la información necesaria para dibujar
                    self.meshes_gl.append({
                        'vao': vao,
                        'vbo': vbo,
                        'ebo': ebo,
                        'index_count': len(indices_np)
                    })
            
            if not self.meshes_gl:
                 print(f"Error: No se procesaron mallas válidas desde {file_path}")
                 return False

            print(f"Modelo cargado correctamente: {len(self.meshes_gl)} mallas, {sum(mesh['index_count'] for mesh in self.meshes_gl)} vértices")
            return True
            
        except AssimpError as e: 
            print(f"Error de Assimp/PyAssimp: {e}")
            self.cleanup()
            return False
        except Exception as e:
            print(f"Error inesperado: {e}") 
            self.cleanup()
            return False

    def cleanup(self):
        """Liberar recursos OpenGL"""
        for mesh_gl in self.meshes_gl:
            if mesh_gl.get('vao'): glDeleteVertexArrays(1, [mesh_gl['vao']])
            if mesh_gl.get('vbo'): glDeleteBuffers(1, [mesh_gl['vbo']])
            if mesh_gl.get('ebo'): glDeleteBuffers(1, [mesh_gl['ebo']])
        self.meshes_gl = []
        print("Recursos de modelo liberados")

    # Las funciones set_position/scale/rotation no cambian, 
    # se usan externamente para calcular la matriz del modelo
    def set_position(self, x, y, z):
        self.model_position = [x, y, z]
    
    def set_scale(self, x, y, z):
        self.model_scale = [x, y, z]
        
    def set_rotation(self, x, y, z):
        self.model_rotation = [x, y, z]
    
    def draw(self):
        """Renderizar el modelo (el shader y las matrices ya deben estar configurados)"""
        if not self.meshes_gl:
            return
        
        # Con OpenGL Core Profile, las transformaciones se hacen vía uniforms en el shader
        # así que no necesitamos glPushMatrix/glTranslate/etc aquí
        
        for mesh_gl in self.meshes_gl:
            glBindVertexArray(mesh_gl['vao'])
            glDrawElements(GL_TRIANGLES, mesh_gl['index_count'], GL_UNSIGNED_INT, None)
            glBindVertexArray(0) 