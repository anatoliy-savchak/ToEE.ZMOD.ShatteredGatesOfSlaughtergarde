import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon
import ctrl_behaviour, py06122_cormyr_prompter, shattered_consts, py06211_shuttered_monster, const_proto_scrolls, const_proto_wands, utils_npc
import py06411_shattered_armory_encounters

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_ARMORY): toee.RUN_DEFAULT
	for pc in toee.game.party:
		pc.condition_add("Inspect")
		pc.condition_add("Smash_Object")
	ctrl = CtrlShatteredArmory.ensure(attachee)
	ctrl.place_encounters()
	return toee.RUN_DEFAULT

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	#debug.breakp("san_use")
	return toee.RUN_DEFAULT

def csa():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(shattered_consts.SHATERRED_ARMORY_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlShatteredArmory.get_name() in o.data):
		result = o.data[CtrlShatteredArmory.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlShatteredArmory(ctrl_daemon.CtrlDaemon):
	def __init__(self):
		super(CtrlShatteredArmory, self).__init__()
		return

	def created(self, npc):
		super(CtrlShatteredArmory, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = shattered_consts.SHATERRED_ARMORY_DAEMON_SCRIPT
		return

	@staticmethod
	def get_name():
		return "CtrlShatteredArmory"

	def place_encounters(self):
		#if (self.encounters_placed): return
		#debugg.breakp("place_encounters")
		if (not self.encounters_placed):
			#self.place_encounter_a1()
			self.place_encounter_a2()

		self.encounters_placed = 1
		#self.print_monsters()

		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 481, 499)
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 450, 445)
		toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 437, 522) #a2
		utils_obj.scroll_to_leader()
		return

	def get_dialogid_default(self):
		return shattered_consts.SHATERRED_ARMORY_DAEMON_DIALOG

	def place_encounter_a1(self):
		self.create_promter_at(utils_obj.sec2loc(415, 520), self.get_dialogid_default(), 10, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Audience Hall", const_toee.rotation_0000_oclock)

		ctrl = self.create_npc_at(utils_obj.sec2loc(419, 518), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0100_oclock, "a1", "gnoll1")[1]
		ctrl.vars["tag"] = 1
		ctrl = self.create_npc_at(utils_obj.sec2loc(419, 521), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0100_oclock, "a1", "gnoll2")[1]
		ctrl.vars["tag"] = 2
		ctrl = self.create_npc_at(utils_obj.sec2loc(419, 525), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0000_oclock, "a1", "gnoll3")[1]
		ctrl.vars["tag"] = 3
		return

	def display_encounter_a1(self):
		print("display_encounter_a1")
		self.reveal_monster("a1", "gnoll1")
		self.reveal_monster("a1", "gnoll2")
		self.reveal_monster("a1", "gnoll3")
		return

	def activate_encounter_a1(self):
		print("activate_encounter_a1")
		self.activate_monster("a1", "gnoll1")
		self.activate_monster("a1", "gnoll2")
		self.activate_monster("a1", "gnoll3")
		return

	def place_encounter_a2(self):
		self.create_promter_at(utils_obj.sec2loc(453, 521), self.get_dialogid_default(), 20, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Audience Hall", const_toee.rotation_0000_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(463, 518), py06411_shattered_armory_encounters.CtrlGnollArcher, const_toee.rotation_0100_oclock, "a2", "gnoll1")
		self.create_npc_at(utils_obj.sec2loc(463, 525), py06411_shattered_armory_encounters.CtrlGnollArcher, const_toee.rotation_0100_oclock, "a2", "gnoll2")
		return


	def display_encounter_a2(self):
		print("display_encounter_a2")
		self.reveal_monster("a2", "gnoll1")
		self.reveal_monster("a2", "gnoll2")
		return

	def activate_encounter_a2(self):
		print("activate_encounter_a2")
		#self.activate_monster("a2", "gnoll1")
		#self.activate_monster("a2", "gnoll2")
		return
