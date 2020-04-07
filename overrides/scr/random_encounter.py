import toee, const_toee, debugg

def can_sleep():
	print("sn_true_seeing: {}".format(toee.game.leader.scripts[const_toee.sn_true_seeing]))
	#debugg.breakp("can_sleep")
	result = toee.SLEEP_SAFE
	leader = toee.game.leader
	if (leader.scripts[const_toee.sn_true_seeing]):
		oldval = leader.obj_get_int(toee.obj_f_pad_i_7)
		print("obj_f_pad_i_7: {}".format(oldval))
		leader.obj_set_int(toee.obj_f_pad_i_7, 1)
		result = leader.object_script_execute(toee.OBJ_HANDLE_NULL, const_toee.sn_true_seeing)
		leader.obj_set_int(toee.obj_f_pad_i_7, oldval)

	print("can_sleep() = {}".format(result))
	return result

def encounter_create(encounter):
	assert isinstance(encounter, toee.PyRandomEncounter)
	return

def encounter_exists(setup, encounter):
	assert isinstance(encounter, toee.PyRandomEncounter)
	assert isinstance(setup, toee.PyRandomEncounterSetup)
	return 0
