import toee, templeplus.pymod, tpdp, debug

###################################################

def GetConditionName():
	return "No_Move"

print("Registering " + GetConditionName())
###################################################

def No_Move_OnTurnBasedStatusInit(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTurnBasedStatus)

	evt_obj.tb_status.hourglass_state = 2
	return 0

def No_Move_OnBeginRound(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	print("No_Move_OnBeginRound for {}".format(attachee))
	#args.condition_remove()
	return 0

def No_Move_OnGetMoveSpeed(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjMoveSpeed)

	evt_obj.bonus_list.set_overall_cap(1, 0, 0, 0)
	evt_obj.bonus_list.set_overall_cap(2, 0, 0, 0)
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) #
#modObj.AddHook(toee.ET_OnTurnBasedStatusInit, toee.EK_NONE, No_Move_OnTurnBasedStatusInit, ())
modObj.AddHook(toee.ET_OnGetMoveSpeed, toee.EK_NONE, No_Move_OnGetMoveSpeed, ())
#modObj1.AddHook(toee.ET_OnBeginRound, toee.EK_NONE, Surprised2_OnBeginRound, ())
