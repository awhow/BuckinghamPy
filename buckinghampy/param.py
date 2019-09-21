import numpy as np

from .predefined_param import knownParamDict

class Param:
    """
    Defines a name and dimensional vector for a paramter.

    The name is a string that will be used as the parameter's symbol,
    and the dimensional vector is defined as [ M L t T N I J ]. Where

    1 Mass (kilogram, k)
    2 Length (metre, m)
    3 Time (second, s)
    4 Temperature (Kelvin, K)
    5 Quantity (moles, mol)
    6 Current (ampere, A)
    7 Luminous intensity (candela, cd)

    """


    def __init__(self, name, ptype=None, dim=[0,0,0,0,0,0,0]):
        self.name = name

        if ptype is not None:
            dim = knownParamDict[ptype]

        dim += [0]*(7-len(dim)) # Pad dim with zeros.
        self.dim = np.array(dim)

    def __repr__(self):
        return '(%s)' % self.name

    def __str__(self):
        return str(self.name) + ': ' + str(self.dim)
