"""Module containing base component class."""
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

