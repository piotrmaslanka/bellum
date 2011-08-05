class Report(object):
    '''Battlefield report virtual class'''
    def startVolley(self, drop=False):
        '''Called when next volley is about to start'''
        pass
    def startTurn(self, drop=False):
        '''Called when next turn has began'''
        pass
    def endTurn(self):
        pass
    def endVolley(self):
        pass
    def startBattle(self):
        pass
    def endBattle(self):
        pass
    def momentumLost(self):
        pass
    def definitiveVictory(self):
        pass
    def finalize(self, report):
        '''report according to bellum.landarmy.defcon.objects.OUTCOME_*'''
        pass
    def initializeArmies(self, attacker_army, defender_army, is_drop):
        pass
    def initializeParties(self, attacker, root_defender):
        pass
    def initializeEnvironment(self, source, destination, occurred_on):
        '''source can either be a Mothership or a Province'''
        pass
        
    


