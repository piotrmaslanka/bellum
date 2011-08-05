from time import time    # unixtime
from bellum.settings import SMF_GROUP_UNALLIED, SMF_POST_GROUP

class Group(object):
    def __init__(self, smf, id_group):
        self.smf = smf
        self.id = id_group
        if self.smf.cur.execute("SELECT * FROM membergroups WHERE id_group="+str(id_group)) == 0:
            raise Exception, 'Group does not exist'
        id_group, group_name, description, online_color, min_posts, max_messages, stars, group_type, hidden, id_parent = self.smf.cur.fetchone()
        self.name = group_name

    def delete(self):
        '''assumes all users have been removed from this group'''
        self.smf.cur.execute("DELETE FROM membergroups WHERE id_group="+str(self.id))

    @staticmethod
    def create(smf, name):
        smf.cur.execute("INSERT INTO membergroups VALUES (null, %s, '', '', -1, 0, '', 0, 0, 0)", (name,))
        return Group(smf, smf.cur.lastrowid)

class Board(object):
    def __init__(self, smf, brd):
        self.smf = smf

        if type(brd) in (int, long):        # is an ID
            r = self.smf.cur.execute("SELECT * FROM boards WHERE id_board="+str(brd))
        else:
            r = self.smf.cur.execute("SELECT * FROM boards WHERE name=%s", (brd, ))

        if r == 0:
            raise Exception, 'Board does not exist'

        x = self.smf.cur.fetchone()
        self.id = x[0]
        self.name = x[9]
        try:
            self.groups = map(int, x[7].split(','))
        except:
            self.groups = []

    def saveGroups(self):
        gs = ','.join(map(str, self.groups))
        self.smf.cur.execute("UPDATE boards SET member_groups=%s WHERE id_board="+str(self.id), (gs,))

    def addModerator(self, user_id):
        self.smf.cur.execute("INSERT INTO moderators VALUES ("+str(self.id)+", "+str(user_id)+")")

    def delModerator(self, user_id):
        self.smf.cur.execute("DELETE FROM moderators WHERE id_member="+str(user_id))

    def delete(self):       # doesnt delete the board, because it's too complicated. Just mark it pending deletion. Assumes moderators are already gone
        self.smf.cur.execute("UPDATE boards SET name=%s, member_groups='' WHERE id_board="+str(self.id), ('DERELICT '+str(self.id), ))

    @staticmethod
    def create(smf, name, id_cat, id_profile):
        q = "INSERT INTO boards VALUES (null, "+str(id_cat)+", 0, 0, 1, 0, 0, '', "+str(id_profile)+", %s, '', 0, 0, 1, 0, 0, 0, 0, '')"
        smf.cur.execute(q, (name, ))
        return Board(smf, smf.cur.lastrowid)

class User(object):
    def __init__(self, smf, usr):
        self.smf = smf

        if type(usr) in (int, long):        # is an ID
            r = self.smf.cur.execute("SELECT * FROM members WHERE id_member="+str(usr))
        else:
            r = self.smf.cur.execute("SELECT * FROM members WHERE member_name=%s", (usr, ))

        if r == 0:
            raise Exception, 'User does not exist'
        x = self.smf.cur.fetchone()
        self.id = x[0]
        self.login = x[1]
        try:
            self.groups = map(int, x[51].split(','))
        except:
            self.groups = []

    def saveGroups(self):
        gs = ','.join(map(str, self.groups))
        self.smf.cur.execute("UPDATE members SET additional_groups=%s WHERE id_member="+str(self.id), (gs,))
    def setMainGroup(self, id_group):
        self.smf.cur.execute("UPDATE members SET id_group="+str(id_group)+" WHERE id_member="+str(self.id))

    @staticmethod
    def create(smf, username, password, email, empire):
        q = "INSERT INTO members VALUES(null, %s, "
        q += str(int(time()))+", "      # date_registered
        q += "0, "+str(SMF_GROUP_UNALLIED)+", "   # posts, id_group
        q += "'polish-utf8', "        # lngfile
        q += str(int(time()))+", "      # last_login
        q += "%s, 0, 0, 0, '', '', 0, '', '', %s, '', "      # real_name
        q += "%s, '', 0, '0001-01-01', '', '', '', '', '', '', '', 1, 1, '', '', 0, '', 0, 0, 0, '', 0, 0, 0, 0, '', '', '', '', 0, 1, '', 0, '', '', "
        q += str(SMF_POST_GROUP)+", 0, '0000', '', 0, '', 1)" # id_post_group

        smf.cur.execute(q, (username, empire, password, email))
        return User(smf, smf.cur.lastrowid)

    def setPersonalTextAndBaseGroup(self, text, id_group):
        self.smf.cur.execute("UPDATE members SET personal_text=%s, id_group="+str(id_group)+" WHERE id_member="+str(self.id), (text, ))
        