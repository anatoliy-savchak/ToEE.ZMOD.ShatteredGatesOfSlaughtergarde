import toee, templeplus.pymod, tpdp, debug

###################################################

def GetConditionName():
	return "Surprised2"

print("Registering " + GetConditionName())
###################################################

def TurnBasedStatusInitNoActions(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTurnBasedStatus)
	evt_obj.tb_status.hourglass_state = 0
	evt_obj.tb_status.flags |= 2
	print("TurnBasedStatusInitNoActions for {}".format(attachee))
	#debug.breakp("TurnBasedStatusInitNoActions")
	args.condition_remove()
	return 0

def Surprised2_OnBeginRound(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	print("Surprised2_OnBeginRound for {}".format(attachee))
	#args.condition_remove()
	return 0

def Surprised2_S_BeginTurn(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	print("Surprised2_S_BeginTurn for {}".format(attachee))
	#args.condition_remove()
	return 0

def Surprised2_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)
	evt_obj.append("Surprised")
	return 0

def Surprised2_OnGetEffectTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjEffectTooltip)
	#evt_obj.append(65, -1, "Surprised")
	evt_obj.append(tpdp.hash("SURPRISED2"), -1, "")
	return 0

modObj1 = templeplus.pymod.PythonModifier(GetConditionName(), 2) #
modObj1.AddHook(toee.ET_OnTurnBasedStatusInit, toee.EK_NONE, TurnBasedStatusInitNoActions, ())
modObj1.AddHook(toee.ET_OnBeginRound, toee.EK_NONE, Surprised2_OnBeginRound, ())
modObj1.AddHook(toee.ET_OnD20Signal, toee.EK_S_BeginTurn, Surprised2_S_BeginTurn, ())
modObj1.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, Surprised2_OnGetTooltip, ())
modObj1.AddHook(toee.ET_OnGetEffectTooltip, toee.EK_NONE, Surprised2_OnGetEffectTooltip, ())