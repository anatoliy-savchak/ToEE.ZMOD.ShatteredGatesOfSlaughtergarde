import toee, templeplus.pymod, tpdp, debug, sys

###################################################

def GetConditionName():
	return "Bonus_Attack"

print("Registering " + GetConditionName())
###################################################

def Bonus_Attack_OnGetBonusAttacks(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	
	if (evt_obj.bonus_list and args.get_arg(0)):
		evt_obj.bonus_list.add(args.get_arg(0), 34, "Multiattack")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - number of bonus attacks
modObj.AddHook(toee.ET_OnGetBonusAttacks, toee.EK_NONE, Bonus_Attack_OnGetBonusAttacks, ())

