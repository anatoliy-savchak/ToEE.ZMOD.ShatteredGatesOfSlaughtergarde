import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName2():
	return "SurpriseRound2"

print("Registering " + GetConditionName2())
###################################################

def TurnBasedStatusInitSingleActions(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTurnBasedStatus)
	if (evt_obj.tb_status.hourglass_state > 3):
		evt_obj.tb_status.hourglass_state = 3
	print("TurnBasedStatusInitSingleActions for {}".format(attachee))
	args.condition_remove()
	return 0

def SurpriseRound2_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)
	evt_obj.append("Surprise Round")
	return 0

def SurpriseRound2_OnGetEffectTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjEffectTooltip)
	#evt_obj.append(65, -1, "Surprised")
	evt_obj.append(tpdp.hash("SURPRISEROUND2"), -1, "")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName2(), 2) #
modObj.AddHook(toee.ET_OnTurnBasedStatusInit, toee.EK_NONE, TurnBasedStatusInitSingleActions, ())
modObj.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, SurpriseRound2_OnGetTooltip, ())
modObj.AddHook(toee.ET_OnGetEffectTooltip, toee.EK_NONE, SurpriseRound2_OnGetEffectTooltip, ())
#modObj.AddHook(toee.ET_OnConditionAdd, toee.EK_NONE, SurpriseRound2_OnConditionAdd, ())
#modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_BeginTurn, SurpriseRound2_S_BeginTurn, ())
#modObj.AddHook(toee.ET_OnConditionAddFromD20StatusInit, toee.EK_NONE, SurpriseRound2_OnConditionAddFromD20StatusInit, ())