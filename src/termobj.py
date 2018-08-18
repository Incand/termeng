"""Class for graphical terminal objects."""
from src.components import Component, Transform
import src.engine as eng


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


