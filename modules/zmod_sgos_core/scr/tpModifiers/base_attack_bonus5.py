import toee, templeplus.pymod

###################################################

def GetConditionName():
	return "Base_Attack_Bonus5"

print("Registering " + GetConditionName())
###################################################

def Base_Attack_Bonus_OnToHitBonusBase(attachee, args, evt_obj):
	val = args.get_param(0) # does not work
	if (not val): val = 5
	evt_obj.bonus_list.add(val, 0, 139) #{139}{Racial Bonus}
	#breakp("")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - base attack
modObj.AddHook(toee.ET_OnToHitBonusBase, toee.EK_NONE, Base_Attack_Bonus_OnToHitBonusBase, ())

