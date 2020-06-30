import toee, templeplus.pymod, tpdp, debug, sys

###################################################

def GetConditionName():
	return "Cast_Defensively_Ex"

print("Registering " + GetConditionName())
###################################################

def Cast_Defensively_Remove(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	debug.breakp("Cast_Defensively_Remove")
	print("Cast_Defensively_Remove {} {}".format(attachee, evt_obj.data1))
	args.condition_remove()
	return 0

#modObj = templeplus.pymod.PythonModifier()
#modObj.ExtendExisting("Cast_Defensively")
#modObj.AddHook(toee.ET_OnD20PythonSignal, "Cast_Defensively_Remove", Cast_Defensively_Remove, ())
#modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_Resurrection, Cast_Defensively_Remove, ())
#modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_SetCastDefensively, Cast_Defensively_Remove, ())