import toee, debug
import shattered_consts, ctrl_daemon, const_toee

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_CITY_INN1): toee.RUN_DEFAULT
	ctrl = CtrlShatteredCityInn1.ensure(attachee)
	ctrl.check_sleep_status_update(1)
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_CITY_INN1): toee.RUN_DEFAULT
	ctrl = CtrlShatteredCityInn1.ensure(attachee)
	ctrl.check_sleep_status_update(0)
	return toee.RUN_DEFAULT

class CtrlShatteredCityInn1(ctrl_daemon.CtrlDaemon):
	def created(self, npc):
		super(CtrlShatteredCityInn1, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = shattered_consts.SHATERRED_CITY_SUMBERTON_INN1_DAEMON_SCRIPT
		return

	@classmethod
	def get_name(cls):
		return shattered_consts.SHATERRED_CITY_SUMBERTON_INN1

	def get_map_default(self):
		return shattered_consts.MAP_ID_SHATERRED_CITY_INN1

	# Sleep interface
	def can_sleep(self):
		if (toee.game.global_flags[shattered_consts.GLOBAL_FLAG_MAY_SLEEP_INN]):
			return toee.SLEEP_SAFE
		return toee.SLEEP_PASS_TIME_ONLY
