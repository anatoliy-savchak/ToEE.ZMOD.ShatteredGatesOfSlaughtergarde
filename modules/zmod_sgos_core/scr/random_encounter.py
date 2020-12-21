import toee, const_toee, debug, utils_storage, ctrl_daemon, traceback, sys

# Sleep interface
def can_sleep():
	daemon_ctrl = ctrl_daemon.CtrlDaemon.get_current_daemon()
	if (not daemon_ctrl): return toee.SLEEP_SAFE
	result = daemon_ctrl.can_sleep()
	return result

# See Camp@1010EF00
# During Sleep, if (can_sleep() == toee.SLEEP_DANGEROUS) it will check,
#	once per hour of whether encounter should be created using encounter_exists() == 1.
#	If success then encounter_create will be called with same encounter variable.

# Sleep interface
def encounter_exists(setup, encounter):
	assert isinstance(setup, toee.PyRandomEncounterSetup)
	assert isinstance(encounter, toee.PyRandomEncounter)
	#print("encounter_exists setup: {}, encounter: {}".format(setup, encounter))

	if (setup.flags & toee.ES_F_SLEEP_ENCOUNTER):
		daemon_ctrl = ctrl_daemon.CtrlDaemon.get_current_daemon()
		if (daemon_ctrl and ("encounter_exists" in dir(daemon_ctrl))):
			result = daemon_ctrl.encounter_exists(setup, encounter)
			return result

	return 0

# Sleep interface
def encounter_create(encounter):
	assert isinstance(encounter, toee.PyRandomEncounter)
	print("encounter_create encounter.flags: {}".format(encounter.flags))
	try:
		if (encounter.flags & toee.ES_F_SLEEP_ENCOUNTER):
			daemon_ctrl = ctrl_daemon.CtrlDaemon.get_current_daemon()
			if (daemon_ctrl and ("encounter_create" in dir(daemon_ctrl))):
				daemon_ctrl.encounter_create(encounter)
	except Exception, e:
		print "!!!!!!!!!!!!! encounter_create error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debug.breakp("error")
	return