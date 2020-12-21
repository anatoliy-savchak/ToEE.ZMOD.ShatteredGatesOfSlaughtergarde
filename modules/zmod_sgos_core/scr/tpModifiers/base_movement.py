import toee, templeplus.pymod

###################################################

def GetConditionName():
	return "Base_Movement"

print("Registering " + GetConditionName())
###################################################

def Base_Movement_OnGetBaseMoveSpeed(attachee, args, evt_obj):
	val = args.get_param(0)
	evt_obj.bonus_list.add(val, 1, 139)
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - base movement in feet
modObj.AddHook(toee.ET_OnGetMoveSpeedBase, toee.EK_NONE, Base_Movement_OnGetBaseMoveSpeed, ())