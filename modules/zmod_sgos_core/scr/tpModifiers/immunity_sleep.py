import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Immunity_Sleep"

print("Registering " + GetConditionName())
###################################################

def OnConditionAddPre(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjModifier)

	if (evt_obj.is_modifier("sp-Sleep") or evt_obj.is_modifier("sp-Deep Slumber")):
		#attachee.float_text_line( "Sleep Immunity", toee.tf_red)
		evt_obj.return_val = 0
		attachee.float_mesfile_line("mes\\combat.mes", 5059, toee.tf_red ) # "Sleep Immunity"
		toee.game.create_history_from_pattern(31, attachee, toee.OBJ_HANDLE_NULL)
	return 0
modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnConditionAddPre, toee.EK_NONE, OnConditionAddPre, ())