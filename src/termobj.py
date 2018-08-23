"""Class for graphical terminal objects."""
import numpy as np

from src.components import Component, Transform
from src import engine


class TermObj():
    @classmethod
    def empty(cls):
        empty = TermObj()
        empty.add_component(Transform())
        return empty

    def __init__(self):
        self._components = []

    def add_component(self, comp):
        if not isinstance(comp, Component):
            raise ValueError('Expected a component')
        self._components.append(comp)
        comp.termobj = self
        return comp


class Camera(TermObj):
    def __init__(self, fov=120, near=0.1, far=1000):
        self.fov = fov
        self.near = near
        self.far = far

        TermObj.__init__(self)
        self._tranform = \
            self.add_component(Transform(translation=np.array([0, 0, -50])))

    def get_world2view_matrix(self):
        h = 1 / np.tan(np.deg2rad(self.fov) / 2)
        # times 2 because of terminal char width to height ratio
        w = 2 * h / engine.get_aspect_ratio()

        f = self.far / (self.near - self.far)
        n = self.near * f
        
        projection_matrix = np.array([
            [w, 0,  0, 0],
            [0, h,  0, 0],
            [0, 0,  f, n],
            [0, 0, -1, 0]
        ])
        
        return np.dot(self._tranform._obj2world, projection_matrix)
        
