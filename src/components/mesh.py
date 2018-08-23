import numpy as np

from src import engine
from src.components import Component, Transform


class Mesh(Component):
    @classmethod
    def from_file(cls, termobj, path):
        # TODO 3D File loading
        vertices = []
        triangles = []
        return Mesh(termobj, vertices, triangles)

    @classmethod
    def cube(cls):
        vertices = [
            # Front face
            [-0.5, -0.5, -0.5, 1], #  0
            [ 0.5, -0.5, -0.5, 1], #  1
            [ 0.5,  0.5, -0.5, 1], #  2
            [-0.5,  0.5, -0.5, 1], #  3
            # Right
            [ 0.5, -0.5, -0.5, 1], #  4
            [ 0.5, -0.5,  0.5, 1], #  5
            [ 0.5,  0.5,  0.5, 1], #  6
            [ 0.5,  0.5, -0.5, 1], #  7
            # Back
            [ 0.5, -0.5,  0.5, 1], #  8
            [-0.5, -0.5,  0.5, 1], #  9
            [-0.5,  0.5,  0.5, 1], # 10
            [ 0.5,  0.5,  0.5, 1], # 11
            # Left
            [-0.5, -0.5,  0.5, 1], # 12
            [-0.5, -0.5, -0.5, 1], # 13
            [-0.5,  0.5, -0.5, 1], # 14
            [-0.5,  0.5,  0.5, 1], # 15
            # Bottom
            [-0.5, -0.5,  0.5, 1], # 16
            [ 0.5, -0.5,  0.5, 1], # 17
            [ 0.5, -0.5, -0.5, 1], # 18
            [-0.5, -0.5, -0.5, 1], # 19
            # Top
            [-0.5,  0.5, -0.5, 1], # 20
            [ 0.5,  0.5, -0.5, 1], # 21
            [ 0.5,  0.5,  0.5, 1], # 22
            [-0.5,  0.5,  0.5, 1]  # 23
        ]
        triangles = [
             0,  1,  2,   2,  3,  0, # Front face
             4,  5,  6,   6,  7,  4, # Right
             8,  9, 10,  10, 11,  8, # Back
            12, 13, 14,  14, 15, 12, # Left
            16, 17, 18,  18, 19, 16, # Bottom
            20, 21, 22,  22, 23, 20  # Top
        ]
        return Mesh(vertices, triangles)

    def __init__(self, vertices, triangles):
        self.vertices = vertices
        self.triangles = triangles
        Component.__init__(self)

    def start(self):
        self._transform = self.get_component(Transform)

    def render(self, scr):
        if not self._transform:
            return

        obj2view = np.dot(
            engine.MAIN_CAMERA.get_world2view_matrix(),
            self._transform._obj2world
        )

        engine.debug('World vert: ' + str(np.dot(self._transform._obj2world,
            self.vertices[0])))

        _w_verts = (np.dot(obj2view, vert) for vert in self.vertices)
        engine.debug('Window vert: ' + str(next(_w_verts)))

        height, width = scr.getmaxyx()

        _v_verts = [
            np.array([
                (1 + vert[0]) * width / 2,
                (1 - vert[1]) * height / 2,
                vert[2]
            ]) for vert in _w_verts
        ]
        engine.debug('View vert: ' + str(_v_verts[0]))
        engine.debug('Scrdim: ' + str(engine.scr.getmaxyx()))

        for _v in _v_verts: 
            x, y = np.asarray(np.round(_v[:2]), dtype=int)
            if 0 <= x < width and 0 <= y < height:
                scr.move(y, x)
                scr.addch('X')
        # TODO Render this mesh

