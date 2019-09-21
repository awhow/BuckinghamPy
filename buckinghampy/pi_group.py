from operator import itemgetter

from .helpers import tryInt

def pprint(PiGroupList):
    """Takes a PiGroupList and prints all the Pi Groups nicely to the
    screen."""

    i = 1
    for PiGroup in PiGroupList:
        print("Pi-Group " + str(i) + ":  ", end="")
        i+=1
        pprintPiGroup(PiGroup)
        print("")


def pprintPiGroup(PiGroup):
    """Takes Pi Group and prints output nicely to the screen."""

    PiGroup = sorted(PiGroup, key=itemgetter(1), reverse=True)
    for param, power in PiGroup:
        if ( tryInt(power) == 1 ):
            print("(" + param.name + ')', end=" ")
        elif ( tryInt(power) != 0):
            print("(" + param.name + ')^' + str(tryInt(power)), end=" ")
