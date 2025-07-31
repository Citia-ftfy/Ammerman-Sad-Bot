class TDObject:
    """
    A class to represent a 3D object with vertices, edges, and faces.
    Defaults to a cube if not initialized with custom data.
    """

    def __init__(self, vertices=None, edges=None, faces=None, position=(0, 0, 0),cf=(0.5, 0.7, 1.0),cl=(0, 0, 0)):
        # Default to a cube if nothing is provided
        self.vertices = vertices if vertices is not None else (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1)
        )
        self.edges = edges if edges is not None else (
            (0,1),(1,2),(2,3),(3,0),
            (4,5),(5,7),(7,6),(6,4),
            (0,4),(1,5),(2,7),(3,6)
        )
        self.faces = faces if faces is not None else (
            (0,1,2,3),
            (4,5,7,6),
            (0,1,5,4),
            (2,3,6,7),
            (1,2,7,5),
            (0,3,6,4)
        )
        self.cf = cf # (r, g, b) for color fill
        self.cl = cl # (r, g, b) for color line
        self.position = position  # (x, y, z)

    #setters
    def set_vertices(self, verts):
        self.vertices = verts

    def set_edges(self, edgs):
        self.edges = edgs

    def set_faces(self, face):
        self.faces = face

    def set_position(self, pos):
        self.position = pos

    def set_color_fill(self, color):
        self.cf = color

    def set_color_line(self, color):
        self.cl = color

    #getters
    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_faces(self):
        return self.faces

    def get_position(self):
        return self.position
    
    def get_color_fill(self):
        return self.cf
    
    def get_color_line(self):
        return self.cl