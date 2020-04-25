import toee, templeplus.pymod

###################################################

def GetConditionName():
	return "Caster_Level_Add"

print("Registering " + GetConditionName())
###################################################

def Caster_Level_Add_OnGetBaseCasterLevel(attachee, args, evt_obj):
	classEnum = args.get_arg(1)
	if classEnum != 0 and evt_obj.arg0 != classEnum:
		return 0
	classLvl = args.get_arg(0)
	evt_obj.bonus_list.add(classLvl, 0, 137)
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - add Class Level, classEnum (0 any)
modObj.AddHook(toee.ET_OnGetBaseCasterLevel, toee.EK_NONE, Caster_Level_Add_OnGetBaseCasterLevel, ())
#breakp("Registered " + GetConditionName())
