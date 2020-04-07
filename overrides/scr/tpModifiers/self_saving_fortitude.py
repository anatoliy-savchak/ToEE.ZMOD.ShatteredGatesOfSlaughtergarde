from templeplus.pymod import PythonModifier
from toee import *
from debugg import *

###################################################

def GetConditionName():
	return "Self_Saving_Fortitude"

print("Registering " + GetConditionName())
###################################################

def OnGetSaveThrowFort(attachee, args, evt_obj):
	print("Self_Saving_Fortitude attachee: {}, evt_obj.obj: {}".format(attachee, evt_obj.obj))
	if (evt_obj.obj == attachee):
		value = args.get_arg(0)
		evt_obj.bonus_list.add(value, 0, 137)
		print("added value: {}".format(value))
	#breakp("OnGetSaveThrowFort")
	return 0

modObj = PythonModifier(GetConditionName(), 2)
modObj.AddHook(ET_OnSaveThrowLevel, EK_SAVE_FORTITUDE, OnGetSaveThrowFort, ())

