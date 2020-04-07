from templeplus.pymod import PythonModifier
from toee import *
from debugg import *

###################################################

def GetConditionName():
	return "Base_Movement"

print("Registering " + GetConditionName())
###################################################

def Base_Movement_OnGetBaseMoveSpeed(attachee, args, evt_obj):
	val = args.get_param(0)
	evt_obj.bonus_list.add( val, 1, 139)
	return 0

modObj = PythonModifier(GetConditionName(), 2) # 0 - base movement in feet
modObj.AddHook(ET_OnGetMoveSpeedBase, EK_NONE, Base_Movement_OnGetBaseMoveSpeed, ())

