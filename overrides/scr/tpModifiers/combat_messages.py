import toee, templeplus.pymod, tpdp

###################################################

# still todo
def GetConditionName():
	return "Combat_Messages"

print("Registering " + GetConditionName())
###################################################

def Combat_Messages_Hit(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)

	attachee.float_text_line("critter_hits", toee.tf_yellow)
	return 0

def Combat_Messages_Hit_Critical(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	return 0

def Combat_Messages_Missed(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)

	attachee.float_text_line("Amateur", toee.tf_yellow)
	return 0

def Combat_Messages_Been_Hit(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)
	return 0

def Combat_Messages_Been_Hit_Critical(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)

	attachee.float_text_line("Ow! I'm gonna kill you for that!", toee.tf_yellow)
	return 0

def Combat_Messages_Been_Missed(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Query)

	attachee.float_text_line("Amateur", toee.tf_yellow)
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - style
modObj.AddHook(toee.ET_OnD20PythonSignal, "hit", Combat_Messages_Hit, ())
modObj.AddHook(toee.ET_OnD20PythonSignal, "hit critical", Combat_Messages_Hit_Critical, ())
modObj.AddHook(toee.ET_OnD20PythonSignal, "missed", Combat_Messages_Missed, ())
modObj.AddHook(toee.ET_OnD20PythonSignal, "been hit", Combat_Messages_Been_Hit, ())
modObj.AddHook(toee.ET_OnD20PythonSignal, "been hit critical", Combat_Messages_Been_Hit_Critical, ())
modObj.AddHook(toee.ET_OnD20PythonSignal, "been missed", Combat_Messages_Been_Missed, ())
