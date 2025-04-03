#version 330 core

// Entradas desde VBOs
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

// Matrices de transformación
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Salidas hacia el fragment shader
out vec3 FragPos;
out vec3 Normal;

void main()
{
    // Calcular posición final del vértice
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    
    // Calcular posición del fragmento en espacio mundial (para iluminación)
    FragPos = vec3(model * vec4(aPos, 1.0));
    
    // Transformar normales (idealmente usaríamos la matriz inversa transpuesta)
    Normal = mat3(model) * aNormal;
}