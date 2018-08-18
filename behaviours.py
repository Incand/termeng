from src.components import Component, Transform


class TestBehaviour(Component):
    def start(self):
        self._transform = self.get_component(Transform)

    def update(self):
        self._transform.translate(0.01, 0.02, -0.015)

