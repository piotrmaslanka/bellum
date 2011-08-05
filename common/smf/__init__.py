'''The game uses Simple Machines Forum (SMF) as basis for it's communication platform'''

from bellum.settings import SMF_HOST, SMF_USER, SMF_PASS, SMF_NAME
from bellum.settings import SMF_GROUP_UNALLIED, SMF_GROUP_ALLIED, SMF_GROUP_LEADER, SMF_POST_GROUP
from MySQLdb import connect

class SMF(object):
    def __init__(self):
        dbc = connect(SMF_HOST, SMF_USER, SMF_PASS, SMF_NAME, use_unicode=True, charset="utf8")
        self.cur = dbc.cursor()

def username_taken(username):
    s = SMF()
    return s.cur.execute("SELECT id_member FROM members WHERE member_name=%s", (username, )) > 0

def empire_taken(username):
    s = SMF()
    return s.cur.execute("SELECT id_member FROM members WHERE real_name=%s", (username, )) > 0

def changepassword(username, newpasshash):
    s = SMF()
    return s.cur.execute("UPDATE members SET passwd=%s WHERE member_name=%s", (newpasshash, username))