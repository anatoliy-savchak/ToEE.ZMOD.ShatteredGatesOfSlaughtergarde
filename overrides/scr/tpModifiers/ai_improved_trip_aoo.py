from templeplus.pymod import PythonModifier
from toee import *
from debugg import *

###################################################

def GetConditionName():
	return "AI_Improved_Trip_Aoo"

print("Registering " + GetConditionName())
###################################################

def Improved_Trip_Aoo_OnTripAoo(attachee, args, evt_obj):
	evt_obj.return_val = 1
	return 0

modObj = PythonModifier(GetConditionName(), 2)
modObj.AddHook(ET_OnD20Query, EK_Q_Trip_AOO, Improved_Trip_Aoo_OnTripAoo, ())
