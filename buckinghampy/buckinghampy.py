from __future__ import print_function
from operator import itemgetter
import warnings
import numpy as np

__version__ = "0.3"

knownParamDict = {
'mass': [1],                  # Basic types
'length': [0,1],
'time': [0,0,1],
'temperature': [0,0,0,1],
'velocity': [0,1,-1],         # Derived types
'acceleration': [0,1,-2],
'force': [1,1,-2],
'energy': [1,2,-2],
'pressure': [1,-1,-2],
'density': [1,-3],            # Fluid Properties
'viscosity': [1,-1,-1],
'conductivity': [1,1,-3,-1],
'specificheat': [0,2,-2,-1]
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


def numOfTerms(paramList):
    """Takes list of dimensional vectors, returns number of Pi Terms and
    Repeating Terms.

    """
    sum = np.array([0,0,0,0,0,0,0])
    for param in paramList:
        sum += param.dim**2

    numOfParams = len(paramList)
    numOfDims = len(sum.nonzero()[0])
    numOfRepeat = numOfDims
    numOfPiTerms = numOfParams - numOfDims
    return numOfPiTerms, numOfRepeat


def run(paramList, repeatingList):
    """Takes list of parameters and returns set of Pi groups.

    """

    numOfPiTerms, numOfRepeat = numOfTerms(paramList)
    nonRepeatList = list(set(paramList) - set(repeatingList))
    if len(repeatingList) != numOfRepeat:
        warnings.warn("repeatinglist should be of length " 
                      + str(numOfRepeat) + ".")

    PiGroupList = []        
    for obj in nonRepeatList:
        PiGroup = calcPiGroup(obj, repeatingList)
        PiGroupList.append(PiGroup)
        
    return PiGroupList
    
        
def calcPiGroup(nonRepeatVar, repeatingList, eps=1e-16):
    """Given a non--repeating variable and a list of repeating variables,
    calculate the exponents to create a non--dimensional term.

    """
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


def isWholeNum(arr, crit=6):
    """Requires numpy array input
    """
    return (np.round(arr, crit) % 1 == 0)


def tryInt(num, crit=6):
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
