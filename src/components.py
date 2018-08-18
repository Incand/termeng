"""Module containing basic components."""
import numpy as np

from src import engine


class Component():
    def __init__(self):
        engine.start_event.add(self.start)
        engine.update_event.add(self.update)
        engine.render_event.add(self.render)
        engine.stop_event.add(self.stop)

    @property
    def termobj(self):
        return self._termobj

    @termobj.setter
    def termobj(self, new_termobj):
        self._termobj = new_termobj

    def get_component(self, typ):
        if not self._termobj:
            return None
        for comp in self.termobj._components:
            if isinstance(comp, typ):
                return comp

    def start(self):
        pass

    def update(self):
        pass

    def render(self, scr):
        pass

    def stop(self):
        pass


class Transform(Component):
    def __init__(self, translation=None, rotation=None, scale=None):
        self._translation = translation if translation else np.array([0, 0, 0, 1])
        self._rotation = rotation if rotation else np.array([1, 0, 0, 0])
        self._scale = scale if scale else np.ones(4)
        self._update_obj2world()
        Component.__init__(self)

    @property
    def translation(self):
        return self._translation[:3]

    @translation.setter
    def translation(self, translation):
        _trans = np.concatenate((translation, [1])) \
            if len(translation) == 3 else \
            np.array(translation)
        self._translation = _trans
        self._update_obj2world()

    @property
    def _translation_matrix(self):
        transmat = np.identity(4)
        transmat[:, 3] = self._translation
        return transmat

    def translate(self, x, y, z):
        self.translation = self.translation + np.array([x, y, z])

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = np.array(rotation)
        self._update_obj2world()
   
    @property
    def _rotation_matrix(self):
        # TODO Use real rotation matrix
        return np.identity(4)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = np.array(scale)
        self._update_obj2world()

    @property
    def _scale_matrix(self):
        return np.diag(self.scale)

    def _update_obj2world(self):
        self._obj2world = np.dot(
            np.dot(self._scale_matrix,
                   self._rotation_matrix),
            self._translation_matrix)


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

        _w_verts = (np.dot(self._transform._obj2world, vert) for vert in
                self.vertices)

        sample = next(_w_verts)
        scr.move(10, 10)
        scr.addstr(str(sample))
        # TODO Render this mesh


class Camera(Component):
    def __init__(self):
        self.fov = 120
        Component.__init__(self)

