import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Immunity_Poison"

print("Registering " + GetConditionName())
###################################################

def OnConditionAddPre(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjModifier)

	if (evt_obj.is_modifier("Poisoned")):
		attachee.float_text_line( "Poison Immunity", toee.tf_red)
		toee.game.create_history_from_pattern(66, attachee, toee.OBJ_HANDLE_NULL) # is immune to ~poison~[TAG_POISON]
		evt_obj.return_val = 0
	return 0

def OnD20QueryTrue(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	
	evt_obj.return_val = 1
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnConditionAddPre, toee.EK_NONE, OnConditionAddPre, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_Critter_Is_Immune_Poison, OnD20QueryTrue, ())
