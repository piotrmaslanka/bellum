from django.db import models
from math import sqrt
from django.conf import settings
from datetime import datetime
from time import mktime

class BigIntegerField(models.IntegerField):
    '''Henrietta: Same ownership status as CSCharField'''
    empty_strings_allowed = False
    def get_internal_type(self):
        return "BigIntegerField"
    def db_type(self):
        if settings.DATABASE_ENGINE == 'oracle':
            return 'NUMBER(19)'
        else:
            return 'bigint'

class CSCharField(models.Field):
    '''A CharField which is stored internally using const-len char fields
    It is able to provide substantial optimizations, especially when we know fields are going to be exactly
    as long.
    Henrietta: I ripped it from some site, don't remember which though. Just for the record, this class is not mine.'''
    def __init__(self, max_length, *args, **kwargs):
        super(CSCharField, self).__init__(*args, **kwargs)
        self.max_length = max_length
    def db_type(self):
        return 'char(%s)' % self.max_length        
    
class Requirement(object):
    '''A class that can verify requirements - mothership constructs and technology levels'''
    def __init__(self, **kwargs):
        '''Possible:
            c category: construction
            t category: technology
        '''
        self.req_array = kwargs.keys()
        self.__dict__.update(kwargs)
                
    def checkConstructionByMotherSingle(self, mother, conid, lvl):
        if mother.getConstructionLevelById(conid) < lvl:
            return False
        return True
    def checkTechnologySingle(self, tech, conid, lvl):
        if tech.getTechnologyLevelById(conid) < lvl:
            return False
        return True

    def checkConstructionsByMother(self, mother):
        for entry in self.req_array:
            if entry[0] == 'c':
                lvl = self.__dict__[entry]
                id = int(entry[2:])
                if not self.checkConstructionByMotherSingle(mother, id, lvl):
                    return False
        return True
    
    def checkTechnology(self, tech):
        for entry in self.req_array:
            if entry[0] == 't':
                id = int(entry[2:])
                lvl = self.__dict__[entry]
                if not self.checkTechnologySingle(tech, id, lvl):
                    return False
        return True
        
    def validate(self, mother):
        if not self.checkConstructionsByMother(mother):
            return False
        if not self.checkTechnology(mother.owner.technology):
            return False
        return True        
        
        
class XYPosition(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    
    class Meta:
        abstract = True
    def distance(self, XY):
        '''Calculates distance between self and another XY instance'''
        return sqrt((self.x - XY.x) ** 2 + (self.y - XY.y) ** 2)
        
class ResourceIndex(models.Model):
    '''resource ratio is per second'''
    lastupdated = models.DateTimeField()
    titan = BigIntegerField(default=0)
    pluton = BigIntegerField(default=0)
    men = BigIntegerField(default=0)
    
    ratio_titan = models.FloatField(default=0)
    ratio_pluton = models.FloatField(default=0)
    ratio_men = models.FloatField(default=0)
    
    def setRatio(self, new_ratio_titan, new_ratio_pluton, new_ratio_men):
        '''Sets new ratio. Accepts a tuple of:
            (new_ration_titan, new_ration_pluton, new_ration_men)'''
        self.ratio_titan = new_ratio_titan
        self.ratio_pluton = new_ratio_pluton
        self.ratio_men = new_ratio_men
        return self
    
    def stateUpdate(self, to=None):
        '''Updates resource state internally to specified datetime in to field.
        If to is not specified, then current datetime is assumed.
        Does not sync anything'''
        
        if to == None:
            to = datetime.now()

        lastdone = mktime(self.lastupdated.timetuple())
        updateto = mktime(to.timetuple())
        
        assert updateto >= lastdone, 'update_resource_to(%s) < lastupdated(%s)' % (to, self.lastupdated)
        
        delta = updateto - lastdone
        
        self.titan = self.titan + self.ratio_titan * delta
        self.pluton = self.pluton + self.ratio_pluton * delta
        self.men = self.men + self.ratio_men * delta
        self.lastupdated = to
        return self
    
    def addRatio(self, resourceIndex):
        self.ratio_titan += resourceIndex.ratio_titan
        self.ratio_pluton += resourceIndex.ratio_pluton
        self.ratio_men += resourceIndex.ratio_men
        return self

    def __le__(self, resourceIndex):
        ''' Returns SELF <= ResourceIndex '''
        return (self.titan <= resourceIndex.titan) or (self.pluton <= resourceIndex.pluton) or (self.men <= resourceIndex.men)
    
    def __ge__(self, resourceIndex):
        ''' Returns SELF >= ResourceIndex '''
        return (self.titan >= resourceIndex.titan) or (self.pluton >= resourceIndex.pluton) or (self.men >= resourceIndex.men)
        
    def __lt__(self, resourceIndex):
        ''' Returns SELF < ResourceIndex '''
        return (self.titan < resourceIndex.titan) or (self.pluton < resourceIndex.pluton) or (self.men < resourceIndex.men)
        
    def __gt__(self, resourceIndex):
        ''' Returns SELF > ResourceIndex '''
        return (self.titan > resourceIndex.titan) or (self.pluton > resourceIndex.pluton) or (self.men > resourceIndex.men)

    def __add__(self, resourceIndex):
        ''' Returns SELF + ResourceIndex '''
        return ResourceIndex(titan=self.titan + resourceIndex.titan,
                             pluton=self.pluton + resourceIndex.pluton,
                             men=self.men + resourceIndex.men)
        
    def __mul__(self, factor):
        return ResourceIndex(titan=self.titan*factor,
                             pluton=self.pluton*factor,
                             men=self.men*factor)

    def __imul__(self, factor):
        self.titan = self.titan * factor
        self.pluton = self.pluton * factor
        self.men = self.men * factor
        return self
        
    def __iadd__(self, resourceIndex):
        ''' Sets the class if SELF += ResourceIndex '''
        self.titan = self.titan + resourceIndex.titan
        self.pluton = self.pluton + resourceIndex.pluton
        self.men = self.men + resourceIndex.men
        return self
    
    def __sub__(self, resourceIndex):
        ''' Returns SELF - ResourceIndex '''
        return ResourceIndex(titan=self.titan - resourceIndex.titan,
                             pluton=self.pluton - resourceIndex.pluton,
                             men=self.men - resourceIndex.men)
        
    def __isub__(self, resourceIndex):
        ''' Sets the class if SELF -= ResourceIndex '''
        self.titan = self.titan - resourceIndex.titan
        self.pluton = self.pluton - resourceIndex.pluton
        self.men = self.men - resourceIndex.men
        return self
        
    def __eq__(self, anotherObject):
        if anotherObject == None:
            return False
        elif type(anotherObject) == int:
            if anotherObject == 0:
                return (self.titan == 0) and (self.pluton == 0) and (self.men == 0)
        else:
            return (self.titan == anotherObject.titan) and (self.pluton == anotherObject.pluton) and (self.men == anotherObject.men)

    def __repr__(self):
        return 'ResourceIndex, titan='+str(self.titan)+' pluton='+str(self.pluton)+' men='+str(self.men)+' ratio_titan='+str(self.ratio_titan)+'ratio_pluton='+str(self.ratio_pluton)+'ratio_men='+str(self.ratio_men)