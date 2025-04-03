# Contents of `README.md`

# 3D Cube with OpenGL

This project implements a simple 3D cube using OpenGL in Python. It demonstrates the use of shaders, camera manipulation, and basic rendering techniques.

## Requirements

To run this project, you need to have the following Python packages installed:

- PyOpenGL
- pygame

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Running the Application

To run the application, execute the following command in your terminal:

```
python src/main.py
```

Make sure your terminal window is large enough to accommodate the OpenGL context.

## Project Structure

- `src/main.py`: Entry point of the application.
- `src/shaders/fragment.glsl`: Fragment shader code for coloring the cube.
- `src/shaders/vertex.glsl`: Vertex shader code for transforming vertex data.
- `src/cube.py`: Class for creating and rendering the 3D cube.
- `src/camera.py`: Class for managing camera position and orientation.

## Controls

- Use the arrow keys to move the camera.
- Press `Q` to quit the application.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.