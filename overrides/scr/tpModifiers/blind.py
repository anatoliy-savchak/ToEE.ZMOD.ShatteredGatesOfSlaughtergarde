import toee, templeplus.pymod, sys, tpdp, math, traceback, debug

###################################################
def GetConditionName():
	return "Blind"

print("Registering " + GetConditionName())
###################################################

def OnQueryReturnTrue(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	
	evt_obj.return_val = 1
	return 0

def OnQueryReturnFalse(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	
	evt_obj.return_val = 0
	return 0

def OnGetMoveSpeed(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjMoveSpeed)
	
	if (not attachee.d20_query(toee.Q_Critter_Has_True_Seeing)):
		evt_obj.factor = evt_obj.factor * 0.5
	return 0

def OnGetAttackerConcealmentMissChance(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjObjectBonus)

	evt_obj.bonus_list.add(50, 0, 189) #{189}{~Blinded~[TAG_BLINDED]}
	return 0

def OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)

	evt_obj.append("Blind")
	return 0

def OnToHitBonusFromDefenderCondition(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)

	evt_obj.bonus_list.add(2, 0, 161) #{161}{Attacker is not Visible}
	return 0

def OnGetAC(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)

	evt_obj.bonus_list.add_cap(8, 0, 189)#{189}{~Blinded~[TAG_BLINDED]}
	evt_obj.bonus_list.add_cap(3, 0, 189)#{189}{~Blinded~[TAG_BLINDED]}
	return 0

#Condition_sp_Blindness
modObj = templeplus.pymod.PythonModifier(GetConditionName(), 3) # reserved
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_Critter_Is_Blinded, OnQueryReturnTrue, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_AOOPossible, OnQueryReturnFalse, ())
modObj.AddHook(toee.ET_OnGetMoveSpeed, toee.EK_NONE, OnGetMoveSpeed, ())
modObj.AddHook(toee.ET_OnGetAttackerConcealmentMissChance, toee.EK_NONE, OnGetAttackerConcealmentMissChance, ())
modObj.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, OnGetTooltip, ())
modObj.AddHook(toee.ET_OnToHitBonusFromDefenderCondition, toee.EK_NONE, OnToHitBonusFromDefenderCondition, ())
modObj.AddHook(toee.ET_OnGetAC, toee.EK_NONE, OnGetAC, ())