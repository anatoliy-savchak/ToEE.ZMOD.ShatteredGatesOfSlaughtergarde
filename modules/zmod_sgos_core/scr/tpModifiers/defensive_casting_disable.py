import toee, templeplus.pymod, tpdp, debug, sys

###################################################

def GetConditionName():
	return "Defensive_Casting_Disble"

print("Registering " + GetConditionName())
###################################################

def Defensive_Casting_Disble_S_SetCastDefensively(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	print("Defensive_Casting_Disble_S_SetCastDefensively {} {}".format(attachee, evt_obj.data1))
	if (evt_obj.data1 == 1):
		print("defensive casting turn off send signal {}".format(attachee))
		attachee.d20_send_signal(toee.EK_S_SetCastDefensively, 0)
	return 0


modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2, 0) # 0 - number of quills lodged
modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_SetCastDefensively, Defensive_Casting_Disble_S_SetCastDefensively, ())