from bellum.common.smf import SMF
from bellum.common.smf.objects import Board, User, Group
from bellum.settings import SMF_GROUP_UNALLIED, SMF_GROUP_ALLIED, SMF_GROUP_LEADER, SMF_POST_GROUP
from bellum.settings import SMF_CAT_ALLIANCE, SMF_SECURITY_PROFILE, SMF_ENABLED

def registerAccount(username, password, email, empire):
    if SMF_ENABLED:
        smf = SMF()
        User.create(smf, username, password, email, empire)

def makeModerator(alliance, account):
    if SMF_ENABLED:
        smf = SMF()
        board = Board(smf, alliance.smf_board_id)
        user = User(smf, account.login)
        board.addModerator(user.id)

def removeModerator(alliance, account):
    if SMF_ENABLED:
        smf = SMF()
        board = Board(smf, alliance.smf_board_id)
        user = User(smf, account.login)
        board.delModerator(user.id)

def makeLeader(alliance, account):      # makes leader
    if SMF_ENABLED:
        smf = SMF()
        board = Board(smf, alliance.smf_board_id)
        user = User(smf, account.login)
                                        # first, make moderator
        board.addModerator(user.id)
                                        # set group
        user.setPersonalTextAndBaseGroup(u'', SMF_GROUP_LEADER)

def destroyAlliance(alliance):
    '''mark that disbanding an alliance is a series of bootFromAlliance and then destroyAlliance'''
    if SMF_ENABLED:
        smf = SMF()
        group = Group(smf, alliance.smf_group_id)
        board = Board(smf, alliance.smf_board_id)
        group.delete()
        board.delete()


def bootFromAlliance(alliance, account):
    '''remove user account from alliance'''
    if SMF_ENABLED:
        smf = SMF()
        user = User(smf, account.login)

        board = Board(smf, alliance.smf_board_id)       # just in case he was a moderator
        try:
            board.delModerator(user.id)
        except:
            pass

        user.groups.remove(alliance.smf_group_id)
        user.saveGroups()
        user.setPersonalTextAndBaseGroup(u'', SMF_GROUP_UNALLIED)

def acceptAlliance(alliance, account):
    '''accepts an Account to Alliance'''
    if SMF_ENABLED:
        smf = SMF()

        user = User(smf, account.login)

        user.groups += [alliance.smf_group_id]
        user.saveGroups()
        user.setPersonalTextAndBaseGroup(u'Sojusz '+alliance.name, SMF_GROUP_ALLIED)

def createAlliance(name, account):
    '''name is a Unicode name for the alliance
       account is leaders object'''
    if SMF_ENABLED:
        smf = SMF()
        user = User(smf, account.login)

        group = Group.create(smf, u'Sojusz '+name)
        board = Board.create(smf, u'Sojusz '+name, SMF_CAT_ALLIANCE, SMF_SECURITY_PROFILE)

        board.groups = [group.id]
        board.saveGroups()
        board.addModerator(user.id)

        user.groups += [group.id]
        user.saveGroups()

        # now modify user parameters
        user.setPersonalTextAndBaseGroup(u'Sojusz: '+name, SMF_GROUP_LEADER)

        return group.id, board.id