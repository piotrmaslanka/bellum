from bellum.common.alliance import isAllied

'''0 - Heading back
   1 - Attack if not Allied on Arrival
                 else Reinforce
   2 - Attack
   3 - Fallback if not Allied on Arrival
                 else Reinforce
   4 - Reinforce
   5 - Debug - Fallback on Contact'''

def whatToDo(account, target_province, designation):

    if designation == 0: designation = 1    # because heading back for all intents counts as Attack/Reinforce

    try:
        target_province.presence
    except:
        is_occupied = False
    else:
        is_occupied = True


    if designation == 5:        # debug
        return 'FALLBACK'

    if not is_occupied:
        return 'ASSAULT'

    if designation == 4:
            return 'REINFORCE'

    if target_province.presence.owner == account:
        return 'REINFORCE'

    if designation == 2:
        return 'ASSAULT'

    if designation == 1:
        if isAllied(account, target_province.presence.owner):
            return 'REINFORCE'
        else:
            return 'ASSAULT'

    if designation == 3:
        if isAllied(account, target_province.presence.owner):
            return 'REINFORCE'
        else:
            return 'FALLBACK'

    raise Exception, 'Unexpected designation: '+str(designation)
    