import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Caster_Level_Mod"

print("Registering " + GetConditionName())
###################################################

def Caster_Level_Mod_OnGetCasterLevelMod(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)

	print("Caster_Level_Mod_OnGetCasterLevelMod {}".format(attachee))
	classEnum = args.get_arg(1)
	if classEnum != 0 and evt_obj.arg0 != classEnum:
		return 0
	spell_level = args.get_arg(0)
	evt_obj.return_val = spell_level
	print("Caster_Level_Mod_OnGetCasterLevelMod evt_obj.return_val: {}".format(evt_obj.return_val))
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 4) # 0 - 0 - return Class Level, 1 - classEnum (0 any), 2 - spell_enum
modObj.AddHook(toee.ET_OnGetCasterLevelMod, toee.EK_NONE, Caster_Level_Mod_OnGetCasterLevelMod, ())
#breakp("Registered " + GetConditionName())
