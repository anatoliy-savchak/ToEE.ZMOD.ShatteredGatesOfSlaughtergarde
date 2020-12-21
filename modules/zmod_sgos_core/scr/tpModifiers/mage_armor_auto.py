import toee, templeplus.pymod, sys, tpdp, traceback, debug

###################################################
def GetConditionName():
	return "Mage_Armor_Auto"

print("Registering " + GetConditionName())
###################################################

def OnNewDay(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)

	print("OnNewDay")
	attachee.cast_spell(toee.spell_mage_armor, attachee)
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 3) # reserved
modObj.AddHook(toee.ET_OnNewDay, toee.EK_NONE, OnNewDay, ())
