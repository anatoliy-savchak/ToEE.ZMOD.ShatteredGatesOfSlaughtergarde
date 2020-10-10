import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon
import ctrl_behaviour, py06122_cormyr_prompter, barovia_consts, py06211_shuttered_monster, const_proto_scrolls, const_proto_wands, utils_npc
import py06501_barovia_encounters, startup_zmod, utils_sneak, py00677FarSouthDoor

# import py06500_daemon_barovia
# py06500_daemon_barovia.cs()
# game.fade_and_teleport(0, 0, 0, 5125, 429, 478)
# game.fade_and_teleport(0, 0, 0, 5125, 467, 478)

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	#debug.breakp("san_new_map")
	if (attachee.map != barovia_consts.MAP_ID_BAROVIA): toee.RUN_DEFAULT
	ctrl = CtrlBarovia.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	startup_zmod.zmod_templeplus_config_apply()
	if (attachee.map != barovia_consts.MAP_ID_BAROVIA): toee.RUN_DEFAULT
	ctrl = CtrlBarovia.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#debug.breakp("san_heartbeat")
	if (attachee.map != barovia_consts.MAP_ID_BAROVIA): toee.RUN_DEFAULT
	startup_zmod.zmod_templeplus_config_apply()
	ctrl = cs()
	if (not ctrl):
		ctrl = CtrlBarovia.ensure(attachee)
		ctrl.place_encounters(1)
	if (ctrl):
		ctrl.heartbeat()
	return toee.RUN_DEFAULT

def san_dying(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	c = cs()
	if (c):
		c.critter_dying(attachee, triggerer)
	storage = utils_storage.obj_storage_by_id(attachee.id)
	if (storage):
		cb = storage.get_data(ctrl_behaviour.CtrlBehaviour.get_name())
		if (not cb):
			cb = storage.get_data(py06211_shuttered_monster.CtrlMonster.get_name())
		if ("dying" in dir(cb)):
			cb.dying(attachee, triggerer)
	return toee.RUN_DEFAULT


def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))
	return toee.RUN_DEFAULT

def cs():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(barovia_consts.BAROVIA_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlBarovia.get_name() in o.data):
		result = o.data[CtrlBarovia.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlBarovia(ctrl_daemon.CtrlDaemon):
	def __init__(self):
		super(CtrlBarovia, self).__init__()
		return

	def created(self, npc):
		super(CtrlBarovia, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = barovia_consts.BAROVIA_DAEMON_SCRIPT
		return

	@staticmethod
	def get_name():
		return "CtrlBarovia"

	def get_map_default(self):
		return barovia_consts.MAP_ID_BAROVIA

	def place_encounters(self, new_map):
		print("new_map: {}".format(new_map))
		print("place_encounters.encounters_placed == {}".format(self.encounters_placed))
		startup_zmod.zmod_templeplus_config_apply()
		startup_zmod.zmod_conditions_apply_pc()

		if (self.encounters_placed and new_map == 0): return

		this_entrance_time = toee.game.time.time_game_in_hours2(toee.game.time)
		print("this_entrance_time == {}".format(this_entrance_time))
		if (not self.encounters_placed):
			self.first_entered_shrs = this_entrance_time
		self.last_entered_shrs = this_entrance_time
		if (not self.last_leave_shrs):
			self.last_leave_shrs = this_entrance_time

		#todo - remember destroyed doors
		#self.remove_door_by_name(921) #{921}{Portcullis A2}
		if (not self.encounters_placed):
			#self.place_encounter_e1()
			self.place_encounter_e2()

		self.encounters_placed += 1
		self.factions_existance_refresh()
		self.check_sleep_status_update(1)
		#toee.game.fade_and_teleport(0, 0, 0, 5125, 429, 478)

		utils_obj.scroll_to_leader()
		return

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		super(CtrlBarovia, self).monster_setup(npc, encounter_name, monster_code_name, monster_name, no_draw, no_kos, faction)
		npc.scripts[const_toee.sn_dying] = barovia_consts.MAP_ID_BAROVIA
		return
	
	def heartbeat(self):
		#self.remove_door_by_name(921) #{921}{Portcullis A2}
		return

	def debug_fix(self):
		toee.game.get_obj_by_id(self.id).scripts[const_toee.sn_heartbeat] = barovia_consts.BAROVIA_DAEMON_SCRIPT
		return

	def get_dialogid_default(self):
		return barovia_consts.BAROVIA_DAEMON_DIALOG

	def place_encounter_e1(self):
		self.create_promter_at(utils_obj.sec2loc(436, 478), self.get_dialogid_default(), 10, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Zobmie Street Ambush", const_toee.rotation_0200_oclock)

		self.create_npc_at(utils_obj.sec2loc(450, 473), py06501_barovia_encounters.CtrlZombieInfected, const_toee.rotation_0300_oclock, "e1", "zombie1")
		self.create_npc_at(utils_obj.sec2loc(453, 478), py06501_barovia_encounters.CtrlZombieInfected, const_toee.rotation_0100_oclock, "e1", "zombie2")
		self.create_npc_at(utils_obj.sec2loc(453, 480), py06501_barovia_encounters.CtrlZombieInfected, const_toee.rotation_0100_oclock, "e1", "zombie3")
		self.create_npc_at(utils_obj.sec2loc(455, 485), py06501_barovia_encounters.CtrlZombieInfected, const_toee.rotation_0100_oclock, "e1", "zombie4")
		self.create_npc_at(utils_obj.sec2loc(458, 486), py06501_barovia_encounters.CtrlZombieInfected, const_toee.rotation_0100_oclock, "e1", "zombie5")
		self.create_npc_at(utils_obj.sec2loc(458, 473), py06501_barovia_encounters.CtrlZombieInfected, const_toee.rotation_0100_oclock, "e1", "zombie6")

		self.create_npc_at(utils_obj.sec2loc(450, 485), py06501_barovia_encounters.CtrlCarcassEater, const_toee.rotation_0100_oclock, "e1", "eater1")
		self.create_npc_at(utils_obj.sec2loc(450, 487), py06501_barovia_encounters.CtrlCarcassEater, const_toee.rotation_0100_oclock, "e1", "eater2")
		return

	def display_encounter_e1(self):
		print("display_encounter_e1")
		self.reveal_monster("e1", "zombie1")
		self.reveal_monster("e1", "zombie2")
		self.reveal_monster("e1", "zombie3")
		self.reveal_monster("e1", "zombie4")
		self.reveal_monster("e1", "zombie5")
		self.reveal_monster("e1", "zombie6")

		self.reveal_monster("e1", "eater1")
		self.reveal_monster("e1", "eater2")
		return

	def activate_encounter_e1(self):
		print("activate_encounter_e1")
		self.activate_monster("e1", "zombie1")
		self.activate_monster("e1", "zombie2")
		self.activate_monster("e1", "zombie3")
		self.activate_monster("e1", "zombie4")
		self.activate_monster("e1", "zombie5")
		self.activate_monster("e1", "zombie6")

		self.activate_monster("e1", "eater1")
		self.activate_monster("e1", "eater2")
		return

	def place_encounter_e2(self):
		self.create_promter_at(utils_obj.sec2loc(476, 478), self.get_dialogid_default(), 20, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Zobmie Street Ambush", const_toee.rotation_0200_oclock)

		self.create_npc_at(utils_obj.sec2loc(476, 486), py06501_barovia_encounters.CtrlZombieInfected, const_toee.rotation_1100_oclock, "e2", "zombie1")
		self.create_npc_at(utils_obj.sec2loc(485, 484), py06501_barovia_encounters.CtrlZombieInfected, const_toee.rotation_1100_oclock, "e2", "zombie2")
		self.create_npc_at(utils_obj.sec2loc(481, 474), py06501_barovia_encounters.CtrlZombieInfected, const_toee.rotation_0300_oclock, "e2", "zombie3")
		self.create_npc_at(utils_obj.sec2loc(489, 472), py06501_barovia_encounters.CtrlZombieInfected, const_toee.rotation_0100_oclock, "e2", "zombie4")

		self.create_npc_at(utils_obj.sec2loc(492, 477), py06501_barovia_encounters.CtrlDireMaggot, const_toee.rotation_0100_oclock, "e2", "maggot1")
		self.create_npc_at(utils_obj.sec2loc(492, 480), py06501_barovia_encounters.CtrlDireMaggot, const_toee.rotation_0100_oclock, "e2", "maggot2")

		self.create_npc_at(utils_obj.sec2loc(478, 473), py06501_barovia_encounters.CtrlVargouilleLesser, const_toee.rotation_0100_oclock, "e2", "varg1")
		self.create_npc_at(utils_obj.sec2loc(476, 473), py06501_barovia_encounters.CtrlVargouilleLesser, const_toee.rotation_0500_oclock, "e2", "varg2")
		return

	def display_encounter_e2(self):
		print("display_encounter_e2")
		self.reveal_monster("e2", "zombie2")
		self.reveal_monster("e2", "zombie2")
		self.reveal_monster("e2", "zombie3")
		self.reveal_monster("e2", "zombie4")

		self.reveal_monster("e2", "maggot1")
		self.reveal_monster("e2", "maggot2")

		self.reveal_monster("e2", "varg1")
		self.reveal_monster("e2", "varg2")
		return

	def activate_encounter_e2(self):
		print("activate_encounter_e2")
		self.activate_monster("e2", "zombie2")
		self.activate_monster("e2", "zombie2")
		self.activate_monster("e2", "zombie3")
		self.activate_monster("e2", "zombie4")

		self.activate_monster("e2", "maggot1")
		self.activate_monster("e2", "maggot2")

		self.activate_monster("e2", "varg1")
		self.activate_monster("e2", "varg2")
		return

