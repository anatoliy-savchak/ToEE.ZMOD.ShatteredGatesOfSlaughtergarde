import toee, debug
import shattered_consts, ctrl_daemon, const_toee

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_CITY_SUMBERTON): toee.RUN_DEFAULT
	ctrl = CtrlShatteredCitySumberton.ensure(attachee)
	ctrl.check_sleep_status_update(1)
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_CITY_SUMBERTON): toee.RUN_DEFAULT
	ctrl = CtrlShatteredCitySumberton.ensure(attachee)
	ctrl.check_sleep_status_update(0)
	return toee.RUN_DEFAULT

class CtrlShatteredCitySumberton(ctrl_daemon.CtrlDaemon):
	def created(self, npc):
		super(CtrlShatteredCitySumberton, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = shattered_consts.SHATERRED_CITY_SUMBERTON_DAEMON_SCRIPT
		return

	@classmethod
	def get_name(cls):
		return shattered_consts.SHATERRED_CITY_SUMBERTON

	def get_map_default(self):
		return shattered_consts.MAP_ID_SHATERRED_CITY_SUMBERTON

	# Sleep interface
	def can_sleep(self):
		if (1):
			return toee.SLEEP_SAFE
		return toee.SLEEP_PASS_TIME_ONLY

