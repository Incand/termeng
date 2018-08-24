import numpy as np
import quaternion

from src.components import Component


class Transform(Component):
    def __init__(self, translation=None, rotation=None, scale=None):
        self.translation = translation if translation is not None \
            else np.array([0, 0, 0, 1])
        self.rotation = rotation if rotation is not None \
            else np.array([0, 0, 0])
        self.scale = scale if scale is not None \
            else np.ones(4)
        Component.__init__(self)

    @property
    def translation(self):
        return self._translation[:3]

    @translation.setter
    def translation(self, translation):
        if len(translation) == 4:
            self._translation = translation
        elif len(translation) == 3:
            self._translation = np.concatenate((translation, [1]))
        else:
            raise ValueError('translation has to be np.array of len 3 or 4')
        self._trans_mat = np.identity(4)
        self._trans_mat[:, 3] = self._translation
        self._update_obj2world()

    def translate(self, x, y, z):
        self.translation = self.translation + np.array([x, y, z])

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        if isinstance(rotation, np.quaternion):
            self._rotation = rotation
        elif len(rotation) == 4:
            self._rotation = np.asarray(rotation, dtype=np.quaternion)
        elif len(rotation) == 3:
            self._rotation = quaternion.from_euler_angles(rotation)
        else:
            raise ValueError('rotation has to be quaternion (len 4) or ' +
                             'euler angles (len 3)')
        # TODO Use correct rotation matrix
        rot = np.identity(4)
        rot[:3, :3] = quaternion.as_rotation_matrix(self._rotation)
        self._rot_mat = rot
        self._update_obj2world()
   
    def rotate(self, x, y, z):
        self.rotation *= quaternion.from_euler_angles([x, y, z])

    @property
    def scale(self):
        return self._scale[:3]

    @scale.setter
    def scale(self, scale):
        if len(scale) == 4:
            self._scale = scale
        elif len(scale) == 3:
            self._scale = np.concatenate((scale, [1]))
        else:
            raise ValueError('scale param has to be np.array of len 3 or 4')
        self._scale_mat = np.diag(self._scale)
        self._update_obj2world()

    def scale_by(self, x, y, z):
        self.scale *= np.array([x, y, z])

    def _update_obj2world(self):
        try:
            self._obj2world = \
                (self._scale_mat @ \
                self._rot_mat) @ \
                self._trans_mat
        except:
            pass
    
    # TODO Make parenting work
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if not isinstance(parent, Transform):
            raise ValueError('Parent of Transform has to be Transform')
        self._parent = parent

