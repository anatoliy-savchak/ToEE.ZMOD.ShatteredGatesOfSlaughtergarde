import toee, templeplus.pymod

###################################################

def GetConditionName():
	return "Initiative_Bonus"

print("Registering " + GetConditionName())
###################################################

def Initiative_Bonus_OnGetInitiativeMod(attachee, args, evt_obj):
	val = args.get_param(0) # does not work
	if (not val): val = 30
	evt_obj.bonus_list.add(val, 0, 139) #{139}{Racial Bonus}
	#breakp("")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - bonus, 1 - type
modObj.AddHook(toee.ET_OnGetInitiativeMod, toee.EK_NONE, Initiative_Bonus_OnGetInitiativeMod, ())

