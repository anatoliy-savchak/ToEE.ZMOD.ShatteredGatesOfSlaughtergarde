import toee, templeplus.pymod, sys, tpdp, math, traceback, debug

###################################################
def GetConditionName():
	return "Chained"

print("Registering " + GetConditionName())
###################################################

def Chained_OnAbilityScoreLevel_dex(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjBonusList)
	
	dex_bonus = args.get_arg(0)
	if (dex_bonus):
		evt_obj.bonus_list.add(dex_bonus, toee.EK_STAT_DEXTERITY, "Chained") 
	return 0

def OnGetMoveSpeed(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjMoveSpeed)
	
	evt_obj.factor = 0
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 3) # Dex penalty
modObj.AddHook(toee.ET_OnAbilityScoreLevel, toee.EK_STAT_DEXTERITY, Chained_OnAbilityScoreLevel_dex, ())
modObj.AddHook(toee.ET_OnGetMoveSpeed, toee.EK_NONE, OnGetMoveSpeed, ())
