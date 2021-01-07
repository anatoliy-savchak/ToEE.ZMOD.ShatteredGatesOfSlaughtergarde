import toee, templeplus.pymod

###################################################

def GetConditionName():
	return "AI_Improved_Trip_Aoo"

print("Registering " + GetConditionName())
###################################################

def Improved_Trip_Aoo_OnTripAoo(attachee, args, evt_obj):
	evt_obj.return_val = 1
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2)
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_Trip_AOO, Improved_Trip_Aoo_OnTripAoo, ())
