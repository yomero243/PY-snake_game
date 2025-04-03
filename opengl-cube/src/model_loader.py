import pyassimp
import pyassimp.postprocess
import numpy as np
from OpenGL.GL import *

class ModelLoader:
    def __init__(self):
        self.meshes = []
        self.model_position = [0, 0, 0]
        self.model_scale = [1, 1, 1]
        self.model_rotation = [0, 0, 0]

    def load_model(self, file_path):
        """Cargar un modelo 3D desde un archivo FBX"""
        try:
            # Importar la escena usando PyAssimp
            scene = pyassimp.load(file_path, 
                                 processing=pyassimp.postprocess.aiProcess_Triangulate | 
                                           pyassimp.postprocess.aiProcess_FlipUVs)
            
            # Procesar cada malla en la escena
            for mesh in scene.meshes:
                vertices = []
                for i in range(len(mesh.vertices)):
                    vertex = mesh.vertices[i]
                    if mesh.normals.any():
                        normal = mesh.normals[i]
                    else:
                        normal = [0.0, 0.0, 1.0]  # Default normal
                    
                    vertices.extend([vertex[0], vertex[1], vertex[2], 
                                     normal[0], normal[1], normal[2]])
                
                # Convertir a numpy array para mejor rendimiento
                vertices = np.array(vertices, dtype=np.float32)
                
                # Crear indices para los triangulos
                indices = []
                for face in mesh.faces:
                    indices.extend(face)
                indices = np.array(indices, dtype=np.uint32)
                
                # Almacenar malla procesada
                self.meshes.append({
                    'vertices': vertices,
                    'indices': indices,
                    'material_index': mesh.materialindex
                })
            
            # Liberar recursos
            pyassimp.release(scene)
            return True
            
        except Exception as e:
            print(f"Error al cargar modelo: {e}")
            return False
    
    def set_position(self, x, y, z):
        """Establecer posición del modelo"""
        self.model_position = [x, y, z]
    
    def set_scale(self, x, y, z):
        """Establecer escala del modelo"""
        self.model_scale = [x, y, z]
        
    def set_rotation(self, x, y, z):
        """Establecer rotación del modelo en grados"""
        self.model_rotation = [x, y, z]
    
    def draw(self):
        """Renderizar el modelo"""
        if not self.meshes:
            return
            
        glPushMatrix()
        # Aplicar transformaciones
        glTranslatef(*self.model_position)
        glRotatef(self.model_rotation[0], 1, 0, 0)
        glRotatef(self.model_rotation[1], 0, 1, 0)
        glRotatef(self.model_rotation[2], 0, 0, 1)
        glScalef(*self.model_scale)
        
        # Renderizar cada malla
        for mesh in self.meshes:
            vertices = mesh['vertices']
            indices = mesh['indices']
            
            glBegin(GL_TRIANGLES)
            # Renderizar cada triángulo
            for i in range(0, len(indices), 3):
                for j in range(3):
                    idx = indices[i + j] * 6  # 6 valores por vértice (3 pos + 3 normal)
                    
                    # Aplicar normal
                    glNormal3f(vertices[idx + 3], vertices[idx + 4], vertices[idx + 5])
                    
                    # Aplicar vértice
                    glVertex3f(vertices[idx], vertices[idx + 1], vertices[idx + 2])
            glEnd()
            
        glPopMatrix() 