from src import engine
from src.components import Component, Transform

import numpy as np


class TestBehaviour(Component):
    def start(self):
        self._transform = self.get_component(Transform)

    def update(self):
        self._transform.scale = np.ones(3) + \
            (1 + np.sin(2 * np.pi * engine.TIME / 10)) / 2

