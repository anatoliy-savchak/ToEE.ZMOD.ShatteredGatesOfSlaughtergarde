import toee, templeplus.pymod, tpdp

###################################################

def GetConditionName():
	return "Fighting_Defensively_Monster"

print("Registering " + GetConditionName())
###################################################

def Fighting_Defensively_Monster_OnGetAC(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	#print("Fighting_Defensively_Monster_OnGetAC")
	evt_obj.bonus_list.add(2, 8, 116)
	return 0

def Fighting_Defensively_Monster_OnToHitBonus2(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	#print("Fighting_Defensively_Monster_OnGetAC")
	evt_obj.bonus_list.add(-4, 0, 116)
	return 0

def Fighting_Defensively_Monster_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)
	evt_obj.append("Fighting Defensively")
	return 0

def Fighting_Defensively_Monster_Q_FightingDefensively(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	evt_obj.return_val = 1
	return 0

def Fighting_Defensively_Monster_S_SetCastDefensively(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	args.condition_remove()
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnGetAC, toee.EK_NONE, Fighting_Defensively_Monster_OnGetAC, ())
modObj.AddHook(toee.ET_OnToHitBonus2, toee.EK_NONE, Fighting_Defensively_Monster_OnToHitBonus2, ())
modObj.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, Fighting_Defensively_Monster_OnGetTooltip, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_FightingDefensively, Fighting_Defensively_Monster_Q_FightingDefensively, ())
#modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_SetCastDefensively, Fighting_Defensively_Monster_S_SetCastDefensively, ()) CRASHES on Exit Combat!!!!
#breakp("Registered " + GetConditionName())
