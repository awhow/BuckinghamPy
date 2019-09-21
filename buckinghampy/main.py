from operator import itemgetter
import warnings
from itertools import combinations
import numpy as np

from .helpers import isWholeNum


def numOfTerms(paramList):
    """
    Calculate the number of Pi Groups to be determine and the number
    of Repeating Terms.

    Args:
      paramList: list of params types
    Returns:
      numOfPiTerms (int): number of Pi Groups
      numOfRepeat (int): number of repeating terms

    """

    A = np.vstack([i.dim for i in paramList]).T
    u, s, vh = np.linalg.svd(A)
    rank = np.sum( s > 1e-10 )

    numOfDims = rank
    numOfParams = len(paramList)

    numOfRepeat = numOfDims
    numOfPiTerms = numOfParams - numOfDims
    return numOfPiTerms, numOfRepeat


def checkRepeatingList(paramList, repeatingList):
    """Test repeatingList to see if it meets BuckinghamPi requirements.

    If repeatingList is found to NOT be valid return tuple
    (False,warning). Where False indicates the validity of
    repeatingList and warning is a text string stating why
    repeatingList failed.

    If repeatingList is found to be valid return tuple with
    (True,None).

    """

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
    """Take list of parameters and returns set of Pi groups.

    Args:
      paramList (list of param): List of parameters important to the
                                 dimensional analysis problem.
      repeatingList (list of param): List of parameters to use as the
                                     repeating variables. If default
                                     empty list, calculate a reasonable list.
      depParam (param): If present, depParam is the dependent parameter.
                        Do not include depParam as a possible selection for
                        repeatingList.
    Returns:
      List of Pi Groups. Where Pi Groups are represents by a list of params.

    """

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


def bestFactor(powers):
    """Determine best factor to use to scale the Pi Group parameters."""

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
    """Score the factor based on number of whole number powers and number
    of positive powers."""

    trial = factor*powers
    numWhole = sum(isWholeNum(trial))
    numPos = sum(trial > 0)
    score = numWhole + numPos
    return score


