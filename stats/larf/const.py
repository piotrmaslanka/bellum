#   Rules are as follow. Something that accepts an object
#   ID MUST as well accept it as instance, if instance
#   object is passed instead of an integer

# LA - Larf Alliance
# must: name, shname, aid
# acronyms: accid - account ID, aid - alliance ID
LA_DISBAND_ALLIANCE = 'disbandAlliance'
LA_CREATE_ALLIANCE = 'createAlliance'
LA_LEAVE_ALLIANCE = 'leaveAlliance'
    # accid
LA_APPLIED_TO_ALLIANCE = 'appliedToAlliance'
    # accid, message
LA_DECLINED_APPLICATION_TO_ALLIANCE = 'decApptoAlliance'
    # accid, playername, message
LA_ACCEPTED_APPLICATION_TO_ALLIANCE = 23423423
    # accid, playername, message
LA_KICKED_FROM_ALLIANCE = 'fuck'
    # kicker, kickee
LA_MODIFIED_TEAMSITE = 'tsmod'
    # old, current
LA_MADE_LEADER = 'mldr'
    # newleader, oldleader [database IDs]
LA_ALLIANCE_BROADCAST = 'broadcast'
    # accid, title, body - Larf Alliance



# LM - Larf Mothership
# required: mid - mother ID
# acronyms: accid - accountID
LM_CONSTRUCTION_ORDERED = 'orderedConstructionOnMothership'
    # what, levelfrom
LM_CONSTRUCTION_CANCELLED = 'cancelledConstructionOnMothership'
    # what, levelcurrent
LM_LANDARMY_TRAINING = 'startedTrainingArmyOnMothership'
    # what, amount
LM_NAMECHANGE = 'namechangems234'
    # old, new
LM_RESEARCH_ORDERED = 1243234342
    # what, levelfrom
LM_RESEARCH_CANCELLED = 1.33432234
    # what, levelcurrent
LM_DEPLOY_LAND_GROUND = 'deployLandforceGarrisonOntoProvince'
    # garrison - a Garrison object reference, provinceid
LM_SENT_RESOURCE = 'sent some resources'
    # resources - a ResourceIndex object, target - target mothership id
LM_RCVD_RESOURCE = 'received some resources'
    # resources - a ResourceIndex object, from - from mothership id, target - target mothership id
        # message is written to target player

LM_RELOCATION = 'is relocating mothership'
    # source, target - planet IDs

# LP - Larf Province
# required: pid - province ID

LP_BUILD_ORDERED = 'ordered building on a province'
    # what, levelfrom
LP_BUILD_CANCELLED = 'cancelled building on a province'
    # what, levelcurrent
LP_DEPLOY_LAND_GROUND = 'deploylandforcefromprovinceontoprovince'
    # garrison, target(pid), designation, orders
LP_MOTHER_PICKUP_LAND = 'motherpickuplandfromprovince'
    # garrison, mid

# LX - Larf Combat

LX_DROP_COMBAT_LAND = 'land combat by drop'
    # attacker_id, defender_id, province_id, attacker_won
LX_PROVINCE_COMBAT_LAND = 'land combat by airstrike'
    # attacker_id, defender_id, source_pid, target_pid, attacker_won