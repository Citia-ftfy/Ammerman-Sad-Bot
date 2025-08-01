import numpy as np
from OpenGL.GL import *

class CubeVBO:
    def __init__(self, vertices, indices):
        self.vertex_vbo = glGenBuffers(1)
        self.index_vbo = glGenBuffers(1)
        self.vertex_count = len(indices)

        # Vertices
        vertex_data = np.array(vertices, dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

        # Indices
        index_data = np.array(indices, dtype=np.uint32)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_vbo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_vbo)
        glDrawElements(GL_QUADS, self.vertex_count, GL_UNSIGNED_INT, None)
        glDisableClientState(GL_VERTEX_ARRAY)