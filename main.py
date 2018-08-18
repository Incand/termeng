import src.engine as eng
import src.termobj as tobj
from src.components import Mesh, Transform

from behaviours import TestBehaviour

def main():
    # TODO setup
    cube = tobj.TermObj()
    cube.add_component(Transform())
    cube.add_component(Mesh.cube())
    cube.add_component(TestBehaviour())

    eng.start()


if __name__ == '__main__':
    main()
