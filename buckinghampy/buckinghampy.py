from __future__ import print_function
from operator import itemgetter
import warnings
from itertools import combinations
import numpy as np

__version__ = "0.4"

knownParamDict = {
'mass': [1],                   # Basic types
'length': [0,1],
'time': [0,0,1],
'temperature': [0,0,0,1],
'area': [0,2],                 # Geometry
'volumne': [0,3],
'secondMomentOfArea': [0,4],
'velocity': [0,1,-1],          # Kinematics
'acceleration': [0,1,-2],
'angle': [0],
'angularVelocity': [0,0,-1],
'volumneFlowRate': [0,3,-1],
'massFlowRate': [1,0,-1],
'force': [1,1,-2],             # Dynamics
'torque': [1,2,-2],
'moment': [1,2,-2],
'energy': [1,2,-2],
'power': [1,2,-3],
'pressure': [1,-1,-2],
'stress': [1,-1,-2],
'density': [1,-3],             # Fluid Properties
'viscosity': [1,-1,-1],
'kinematicViscosity': [0,2,-1],
'conductivity': [1,1,-3,-1],
'specificHeat': [0,2,-2,-1]
}


class param:
    """Define dimensions vector of a parameter.

    dimensional vector: 
    [ M L t T N I J ]

    1 Mass (kilogram, k)
    2 Length (metre, m)
    3 Time (second, s)
    4 Temperature (Kelvin, K)
    5 Quantity (moles, mol)
    6 Current (ampere, A)
    7 Luminous intensity (candela, cd)"""


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


def numOfTerms(paramList):
    """Takes list of dimensional vectors, returns number of Pi Terms and
    Repeating Terms."""

    A = np.vstack([i.dim for i in paramList]).T
    u, s, vh = np.linalg.svd(A)
    rank = np.sum( s > 1e-10 )

    numOfDims = rank
    numOfParams = len(paramList)

    numOfRepeat = numOfDims
    numOfPiTerms = numOfParams - numOfDims
    return numOfPiTerms, numOfRepeat


def checkRepeatingList(paramList, repeatingList):
    """Test repeatingList to see if it meets BuckinghamPi requirements."""

    # Test length of list
    numOfPiTerms, numOfRepeat = numOfTerms(paramList)

    if (len(repeatingList) != numOfRepeat):
        warning = "repeatingList should be of length " + str(numOfRepeat) + "."
        return (False, warning)

    # Test that params are linearly independent
    A = np.vstack([i.dim for i in repeatingList]).T

    u, s, vh = np.linalg.svd(A)
    rank = np.sum( s > 1e-10 )

    if (rank != numOfRepeat):
        warning = "Params are not dimensionally independent"
        return (False, warning)

    return (True,None)


def run(paramList, repeatingList=[], depParam=None):
    """Takes list of parameters and returns set of Pi groups."""

    # If no repeatingList is given, create a list of all possible repeatingList's.
    # Use the first repeatingList that satisifies the BuckinghamPi requirements.
    if (repeatingList == []):
        numOfPiTerms, numOfRepeat = numOfTerms(paramList)
        subParamList = list(set(paramList) - set([depParam]))
        repeatingListList = [list(i) for i in combinations(subParamList, numOfRepeat)]
        for rList in repeatingListList:
            test, message = checkRepeatingList(paramList, rList)
            if test:
                repeatingList = rList
                break

    # If a repeatingList is given check to make sure it is valid.
    else:
        warntype = "always"
        warnings.simplefilter(warntype)

        test, message = checkRepeatingList(paramList, repeatingList)
        if not test:
            warnings.warn(message)

    nonRepeatList = list(set(paramList) - set(repeatingList))

    PiGroupList = []        
    for obj in nonRepeatList:
        PiGroup = calcPiGroup(obj, repeatingList)
        PiGroupList.append(PiGroup)
        
    return PiGroupList
    
        
def calcPiGroup(nonRepeatVar, repeatingList, eps=1e-15):
    """Given a non--repeating variable and a list of repeating variables,
    calculate the exponents to create a non--dimensional term."""

    A = nonRepeatVar.dim
    for obj in repeatingList:
        A = np.vstack([A,obj.dim])

    A = A.T

    u, s, vh = np.linalg.svd(A)
    null_mask = (s <= eps)
    null_space = np.compress(null_mask, vh, axis=0)
    null_space = null_space[0]
    null_space = null_space*(abs(null_space) >= 1e-8)

    factor = bestFactor(null_space)

    powers = factor*null_space
    params = [nonRepeatVar] + repeatingList
    return (zip(params,powers))


def tryInt(num, crit=6):
    """Take float, and cast it as an int if it is very close to a whole
    number value."""
    if (np.round(num, crit) % 1 == 0):
        return int(np.round(num,crit))
    else:
        return num


def bestFactor(powers):
    fslist = []

    factor = 1/max(abs(powers))
    score = scoreFactor(factor,powers)
    fslist.append((factor,score))

    factor = -1/max(abs(powers))
    score = scoreFactor(factor,powers)
    fslist.append((factor,score))

    factor = 1/min(abs(powers[powers != 0]))
    score = scoreFactor(factor,powers)
    fslist.append((factor,score))

    factor = -1/min(abs(powers[powers != 0]))
    score = scoreFactor(factor,powers)
    fslist.append((factor,score))

    return max(fslist,key=itemgetter(1))[0]


def scoreFactor(factor,powers):
    trial = factor*powers
    numWhole = sum(isWholeNum(trial))
    numPos = sum(trial > 0)
    score = numWhole + numPos
    return score


def isWholeNum(arr, crit=6):
    """Requires numpy array input."""
    return (np.round(arr, crit) % 1 == 0)


def pprint(PiGroupList):
    i = 1
    for PiGroup in PiGroupList:
        print("Pi-Group " + str(i) + ":  ", end="")
        i+=1
        pprintPiGroup(PiGroup)
        print("")


def pprintPiGroup(PiGroup):
    """Takes Pi Group and prints output nicely to screen.

    """
    PiGroup = sorted(PiGroup, key=itemgetter(1), reverse=True)
    for param, power in PiGroup:
        if ( tryInt(power) == 1 ):
            print("(" + param.name + ')', end=" ")
        elif ( tryInt(power) != 0):
            print("(" + param.name + ')^' + str(tryInt(power)), end=" ")


