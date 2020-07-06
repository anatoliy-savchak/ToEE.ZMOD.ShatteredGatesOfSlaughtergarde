import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Immunity_Blindness"

print("Registering " + GetConditionName())
###################################################

def Immunity_Blindness_OnConditionAddPre(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjModifier)
	#print("Immunity_Blind_OnConditionAddPre")

	if (evt_obj.is_modifier("sp-Blindness")):
		attachee.float_text_line( "Blindess Immunity", toee.tf_red)
		evt_obj.return_val = 0
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnConditionAddPre, toee.EK_NONE, Immunity_Blindness_OnConditionAddPre, ())
#breakp("Registered " + GetConditionName())
