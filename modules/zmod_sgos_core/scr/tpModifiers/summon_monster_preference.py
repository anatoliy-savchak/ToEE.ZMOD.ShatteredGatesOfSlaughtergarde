import toee, templeplus.pymod, tpdp, debug

###################################################

def GetConditionName():
	return "Summon_Monster_Preference"

print("Registering " + GetConditionName())
###################################################

def Summon_Monster_Preference_S_EndTurn(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	args.condition_remove()
	return 0

def Summon_Monster_Preference_OnD20PythonQuery(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Signal)
	#condition_level = args.get_param(0)
	#requested_level = evt_obj.data1
	#if (level == requested_level):
	evt_obj.return_val = args.get_arg(0)
	
	#print("Summon_Monster_Preference_OnD20PythonQuery :: evt_obj.return_val = {}, condition_level: {}, requested_level: {}".format(evt_obj.return_val, condition_level, requested_level))
	#debug.breakp("Summon_Monster_Preference_OnD20PythonQuery")
	return 0

modObj1 = templeplus.pymod.PythonModifier("Summon_Monster_Preference_1", 2) # 1 - option
modObj1.AddHook(toee.ET_OnD20Signal, toee.EK_S_EndTurn, Summon_Monster_Preference_S_EndTurn, ())
modObj1.AddHook(toee.ET_OnD20PythonQuery, "Summon_Monster_Preference_1", Summon_Monster_Preference_OnD20PythonQuery, ())

modObj2 = templeplus.pymod.PythonModifier("Summon_Monster_Preference_2", 2) # 1 - option
modObj2.AddHook(toee.ET_OnD20Signal, toee.EK_S_EndTurn, Summon_Monster_Preference_S_EndTurn, ())
modObj2.AddHook(toee.ET_OnD20PythonQuery, "Summon_Monster_Preference_2", Summon_Monster_Preference_OnD20PythonQuery, ())

modObj3 = templeplus.pymod.PythonModifier("Summon_Monster_Preference_3", 2) # 1 - option
modObj3.AddHook(toee.ET_OnD20Signal, toee.EK_S_EndTurn, Summon_Monster_Preference_S_EndTurn, ())
modObj3.AddHook(toee.ET_OnD20PythonQuery, "Summon_Monster_Preference_3", Summon_Monster_Preference_OnD20PythonQuery, ())
