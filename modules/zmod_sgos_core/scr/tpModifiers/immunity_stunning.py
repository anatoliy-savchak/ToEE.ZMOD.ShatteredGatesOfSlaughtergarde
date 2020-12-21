import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Immunity_Stunning"

print("Registering " + GetConditionName())
###################################################

def OnConditionAddPre(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjModifier)

	if (evt_obj.is_modifier("Stunned")):
		attachee.float_text_line( "Stunning Immunity", toee.tf_red)
		toee.game.create_history_from_pattern(63, attachee, toee.OBJ_HANDLE_NULL) # is immune to ~stunned~[TAG_STUNNED]
		evt_obj.return_val = 0
	return 0
modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnConditionAddPre, toee.EK_NONE, OnConditionAddPre, ())