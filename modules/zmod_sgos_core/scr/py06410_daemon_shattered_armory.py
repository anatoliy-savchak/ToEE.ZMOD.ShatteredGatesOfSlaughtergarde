import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon
import ctrl_behaviour, py06122_cormyr_prompter, shattered_consts, py06211_shuttered_monster, const_proto_scrolls, const_proto_wands, utils_npc
import py06411_shattered_armory_encounters, startup_zmod, utils_sneak, py00677FarSouthDoor
import sys, traceback, monster_info

# import py06410_daemon_shattered_armory
# py06410_daemon_shattered_armory.csa()

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	#debug.breakp("san_new_map")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_ARMORY): toee.RUN_DEFAULT
	ctrl = CtrlShatteredArmory.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	startup_zmod.zmod_templeplus_config_apply()
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_ARMORY): toee.RUN_DEFAULT
	ctrl = CtrlShatteredArmory.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#debug.breakp("san_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_ARMORY): toee.RUN_DEFAULT
	ctrl = csa()
	if (not ctrl):
		ctrl = CtrlShatteredArmory.ensure(attachee)
		ctrl.place_encounters(1)
	if (ctrl):
		ctrl.heartbeat()
	return toee.RUN_DEFAULT

def san_dying(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print("Critter DYING: {}".format(attachee))
	try:
		c = csa()
		if (c):
			c.critter_dying(attachee, triggerer)
		storage = utils_storage.obj_storage_by_id(attachee.id)
		if (storage):
			cb = storage.get_data(ctrl_behaviour.CtrlBehaviour.get_name())
			if (not cb):
				cb = storage.get_data(py06211_shuttered_monster.CtrlMonster.get_name())
			if ("dying" in dir(cb)):
				cb.dying(attachee, triggerer)
	except Exception, e:
		print "Close_Door_Perform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debug.breakp("error")
	return toee.RUN_DEFAULT


def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))

	if (attachee.name == shattered_consts.NAMEID_SHATTERED_ARMORY_EXIT): #{1643}{Shattered Armory Exit}
		csa().last_leave_shrs = toee.game.time.time_game_in_hours2(toee.game.time)
		total_seconds = py00677FarSouthDoor.distance_sumbertone_to_shattered_armory_sec()
		print("fade_and_teleport total_seconds: {}".format(total_seconds))
		toee.game.fade_and_teleport(total_seconds, 0, 0, 5122, 538, 510 ) #sumberton
	elif (attachee.name == 939): #{939}{A6 Door}
		print("A6 Door")
		attachee.object_flag_set(toee.OF_DONTDRAW)
		if (toee.game.combat_turn):
			csa().encounter_a6_premature(attachee, triggerer)
	else:
		attachee.object_flag_set(toee.OF_DONTDRAW)
		if (attachee.name == 938): #{938}{A5 Fiery Demon Arch}
			promter = utils_npc.npc_find_nearest_npc_by_proto(attachee, 15, py06122_cormyr_prompter.PROTO_NPC_PROMPTER)
			if (promter):
				py06122_cormyr_prompter.promter_talk(promter, triggerer)
			else:
				print("promter not found!")
				#debug.breakp("promter not found!")
		elif (attachee.name == 942): #{942}{A10 Fiery Demon Arch}
			print("A10 Door")
			promter = utils_npc.npc_find_nearest_npc_by_proto(attachee, 15, py06122_cormyr_prompter.PROTO_NPC_PROMPTER)
			if (promter):
				py06122_cormyr_prompter.promter_talk(promter, triggerer)
			else:
				print("promter not found!")
		elif (attachee.name == 944): #{944}{A12 Fiery Demon Arch}
			print("A12 Door")
			promter = utils_npc.npc_find_nearest_npc_by_proto(attachee, 10, py06122_cormyr_prompter.PROTO_NPC_PROMPTER)
			if (promter):
				py06122_cormyr_prompter.promter_talk(promter, triggerer)
			else:
				print("promter not found!")
		elif (attachee.name == 946): #{946}{A16 Door}
			print("A16 Door")
			sibling = utils_obj.get_sibling_door(attachee)
			if (sibling and not (sibling.object_flags_get() & toee.OF_DONTDRAW)):
				sibling.object_flag_set(toee.OF_DONTDRAW)
				sibling.portal_toggle_open()
			promter = utils_npc.npc_find_nearest_npc_by_proto(attachee, 10, py06122_cormyr_prompter.PROTO_NPC_PROMPTER)
			if (promter):
				py06122_cormyr_prompter.promter_talk(promter, triggerer)
			else:
				print("promter not found!")
		elif (attachee.name == 947): #{947}{A19 Door}
			print("A16 Door")
			sibling = utils_obj.get_sibling_door(attachee)
			if (sibling and not (sibling.object_flags_get() & toee.OF_DONTDRAW)):
				sibling.object_flag_set(toee.OF_DONTDRAW)
				sibling.portal_toggle_open()
			promter = utils_npc.npc_find_nearest_npc_by_proto(attachee, 15, py06122_cormyr_prompter.PROTO_NPC_PROMPTER)
			if (promter):
				py06122_cormyr_prompter.promter_talk(promter, triggerer)
			else:
				print("promter not found!")
				
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

	def get_map_default(self):
		return shattered_consts.MAP_ID_SHATERRED_ARMORY

	def place_encounters(self, new_map):
		print("new_map: {}".format(new_map))
		print("place_encounters.encounters_placed == {}".format(self.encounters_placed))
		startup_zmod.zmod_templeplus_config_apply()

		self.factions_existance_refresh()
		self.check_sleep_status_update(1)
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
			self.place_encounter_a1()
			self.place_encounter_a2()
			self.place_encounter_a3()
			self.place_encounter_a4()
			self.place_encounter_a5()
			self.place_encounter_a6()
			self.place_encounter_a7()
			self.place_encounter_a9()
			self.place_encounter_a10()
			self.place_encounter_a11()
			self.place_encounter_a12()
			self.place_encounter_a14()
			self.place_encounter_a15()
			self.place_encounter_a16()
			self.place_encounter_a18()
			self.place_encounter_a19()
			self.place_encounter_a20()

		#self.place_ark()
		self.encounters_placed += 1
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 464, 522) #a3
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 541, 472) #a5
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 460, 499) #a5
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 429, 481) #a7
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 496, 498) #a10
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 528, 481) #a11
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 496, 457) #a15
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 508, 445) #a15

		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 460, 456)
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 433, 481)

		# test debug
		#toee.game.fade_and_teleport(0, 0, 0, 5124, 460, 456) #a18
		#toee.game.fade_and_teleport(0, 0, 0, 5124, 452, 445) #a19
		#print("test debug")
		#if (self.encounters_placed == 5):
		#	print("self.encounters_placed == 5")
		#	self.place_encounter_a20()

		self.check_entrance_patrol()
		utils_obj.scroll_to_leader()
		return

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		super(CtrlShatteredArmory, self).monster_setup(npc, encounter_name, monster_code_name, monster_name, no_draw, no_kos, faction)
		npc.scripts[const_toee.sn_dying] = shattered_consts.SHATERRED_ARMORY_DAEMON_SCRIPT
		return

	def create_promter_at(self, loc, dialog_script_id, line_id, radar_radius_ft, method, new_name, rotation = None):
		npc = super(CtrlShatteredArmory, self).create_promter_at(loc, dialog_script_id, line_id, radar_radius_ft, method, new_name, rotation)
		# this is to sleep check only
		npc.faction_add(shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN)
		return npc
	
	def heartbeat(self):
		#self.remove_door_by_name(921) #{921}{Portcullis A2}
		return

	def debug_fix(self):
		toee.game.get_obj_by_id(self.id).scripts[const_toee.sn_heartbeat] = shattered_consts.SHATERRED_ARMORY_DAEMON_SCRIPT
		return

	def get_dialogid_default(self):
		return shattered_consts.SHATERRED_ARMORY_DAEMON_DIALOG

	def skip_delayed(self, delayed, is_promter):
		if (delayed is None and is_promter): return 1 # allow promter
		if (delayed is None and not is_promter): return 1 # skip monsters
		if (delayed and is_promter): return 0 # skip promter
		if (delayed and not is_promter): return 0 # allow monsters
		return 0

	def place_encounter_patrol(self, near_pc):
		self.patrol_spawned_count += 1
		self.last_patrol_spawned_shrs = toee.game.time.time_game_in_hours2(toee.game.time)
		print("place_encounter_patrol {}".format(self.patrol_spawned_count))
		loc1 = utils_obj.sec2loc(419, 518)
		loc2 = utils_obj.sec2loc(419, 521)
		loc3 = utils_obj.sec2loc(419, 525)
		if (near_pc):
			loc1 = toee.game.leader.location - 2
			loc2 = loc1
			loc3 = loc1

		if (1): # check if previous patrol already present
			for obj in toee.game.obj_list_range(loc1, 20, toee.OLC_NPC):
				if (not utils_npc.npc_is_alive(obj)): continue
				if (obj.is_friendly(toee.game.leader)): continue
				print("Found previous patrol: {}".format(obj))
				print("Skip spawning new patrol")
				return

		npc, ctrl = self.create_npc_at(loc1, py06411_shattered_armory_encounters.CtrlFlindSoldier, const_toee.rotation_0100_oclock, "a0", "flind")
		utils_npc.npc_unexploit(npc)
		self.reveal_monster("a0", "flind")
		self.activate_monster("a0", "flind")

		if (1):
			npc, ctrl = self.create_npc_at(loc2, py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0100_oclock, "a0", "gnoll1")
			utils_npc.npc_unexploit(npc)
			self.reveal_monster("a0", "gnoll1")
			self.activate_monster("a0", "gnoll1")

			npc, ctrl = self.create_npc_at(loc3, py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0000_oclock, "a0", "gnoll2")
			utils_npc.npc_unexploit(npc)
			self.reveal_monster("a0", "gnoll2")
			self.activate_monster("a0", "gnoll2")
		return

	def place_encounter_a1(self, delayed = None):
		print("place_encounter_a1 self.skip_delayed(delayed, 1): {}".format(self.skip_delayed(delayed, 1)))
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(415, 520), self.get_dialogid_default(), 10, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Outer Stockade", const_toee.rotation_0000_oclock)

		if (self.skip_delayed(delayed, 0)): return

		ctrl = self.create_npc_at(utils_obj.sec2loc(419, 518), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0100_oclock, "a1", "gnoll1")[1]
		ctrl.vars["tag"] = 1
		ctrl = self.create_npc_at(utils_obj.sec2loc(419, 521), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0100_oclock, "a1", "gnoll2")[1]
		ctrl.vars["tag"] = 2
		ctrl = self.create_npc_at(utils_obj.sec2loc(419, 525), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0000_oclock, "a1", "gnoll3")[1]
		ctrl.vars["tag"] = 3
		return

	def display_encounter_a1(self):
		self.place_encounter_a1(1)
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

	def place_encounter_a2(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(448, 521), self.get_dialogid_default(), 20, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Inner Stockade", const_toee.rotation_0000_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(463, 518), py06411_shattered_armory_encounters.CtrlGnollArcher, const_toee.rotation_0100_oclock, "a2", "gnoll1")
		self.create_npc_at(utils_obj.sec2loc(463, 525), py06411_shattered_armory_encounters.CtrlGnollArcher, const_toee.rotation_0100_oclock, "a2", "gnoll2")
		return

	def display_encounter_a2(self):
		self.place_encounter_a2(1)
		print("display_encounter_a2")
		self.reveal_monster("a2", "gnoll1")
		self.reveal_monster("a2", "gnoll2")

		self.reveal_monster("a3", "troll", 1)
		return

	def activate_encounter_a2(self):
		print("activate_encounter_a2")
		self.activate_monster("a2", "gnoll1")
		self.activate_monster("a2", "gnoll2")
		return

	def place_encounter_a3(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(469, 520), self.get_dialogid_default(), 30, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Blind Troll", const_toee.rotation_0000_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		npc = self.create_npc_at(utils_obj.sec2loc(475, 517), py06411_shattered_armory_encounters.CtrlBlindTroll, const_toee.rotation_0200_oclock, "a3", "troll", 75)[0]
		npc.scripts[const_toee.sn_dialog] = 682
		return

	def display_encounter_a3(self):
		self.place_encounter_a3(1)
		print("display_encounter_a3")
		self.reveal_monster("a3", "troll")
		return

	def activate_encounter_a3(self):
		print("activate_encounter_a3")
		npc = self.activate_monster("a3", "troll", 1, 0)[0]
		#npc.begin_dialog(toee.game.leader, 1)
		toee.game.leader.begin_dialog(npc, 1)
		return

	def troll_kill(self):
		info, npc, ctrl = self.get_monsterinfo_and_npc_and_ctrl("a3", "troll")
		if (npc and utils_npc.npc_is_alive(npc, 1)):
			npc.critter_kill_by_effect(toee.game.leader)
		return

	def place_encounter_a4(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(479, 490), self.get_dialogid_default(), 40, 15, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Elevator Room", const_toee.rotation_0600_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(485, 476), py06411_shattered_armory_encounters.CtrlHillGiant, const_toee.rotation_0500_oclock, "a4", "giant")
		return

	def display_encounter_a4(self):
		self.place_encounter_a4(1)
		print("display_encounter_a4")
		self.reveal_monster("a4", "giant")
		return

	def activate_encounter_a4(self):
		print("activate_encounter_a4")
		self.activate_monster("a4", "giant")
		return

	def place_encounter_a5(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(453, 503), self.get_dialogid_default(), 50, 15, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Eastern Room", const_toee.rotation_0800_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(450, 503), py06411_shattered_armory_encounters.CtrlHalfFiendOgre, const_toee.rotation_0800_oclock, "a5", "ogre")
		return

	def display_encounter_a5(self):
		self.place_encounter_a5(1)
		print("display_encounter_a5")
		self.reveal_monster("a5", "ogre")
		return

	def activate_encounter_a5(self):
		print("activate_encounter_a5")
		self.activate_monster("a5", "ogre")
		return

	def trigger_monster_step_a5(self, step):
		self.trigger_monster_step("a5", "ogre", step)
		return

	def place_encounter_a6(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(443, 509), self.get_dialogid_default(), 60, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Redspwan Prison", const_toee.rotation_0800_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(443, 500), py06411_shattered_armory_encounters.CtrlRedspwawnFirebelcher, const_toee.rotation_0400_oclock, "a6", "firebelcher")
		return

	def display_encounter_a6(self):
		self.place_encounter_a6(1)
		print("display_encounter_a6")
		self.reveal_monster("a6", "firebelcher", 1)
		return

	def activate_encounter_a6(self):
		print("activate_encounter_a6")
		self.activate_monster("a6", "firebelcher", 1)
		return

	def encounter_a6_get_alive_monster(self):
		info = self.get_monsterinfo("a6", "firebelcher")
		if (not info): return 1
		npc = toee.game.get_obj_by_id(info.id)
		if (not npc): return None
		if (not utils_npc.npc_is_alive(npc, 1)): return None
		return npc

	def encounter_a6_is_monster_alive(self):
		npc = self.encounter_a6_get_alive_monster()
		if (not npc): return 0
		return 1

	def encounter_a6_premature(self, door, triggerer):
		print("encounter_a6_premature ({}, {})".format(door, triggerer))
		assert isinstance(triggerer, toee.PyObjHandle)
		if (triggerer and triggerer.type == toee.obj_t_pc):
			# only when npc is doing that
			return 0

		npc = self.encounter_a6_get_alive_monster()
		if (not npc): return 0
		assert isinstance(npc, toee.PyObjHandle)

		self.display_encounter_a6()
		self.activate_encounter_a6()
		promter = utils_npc.npc_find_nearest_npc_by_proto(door, 15, py06122_cormyr_prompter.PROTO_NPC_PROMPTER)
		if (promter):
			promter.destroy()

		npc = self.encounter_a6_get_alive_monster()
		# move it before the door
		npc.move(utils_obj.sec2loc(444, 508))
		npc.rotation = const_toee.rotation_0800_oclock

		npc.d20_status_init()
		npc.set_initiative(triggerer.get_initiative())
		return

	def place_encounter_a7(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			p1 = self.create_promter_at(utils_obj.sec2loc(420, 481), self.get_dialogid_default(), 70, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Southeastern Arsenal", const_toee.rotation_0800_oclock)
			p2 = self.create_promter_at(utils_obj.sec2loc(416, 479), self.get_dialogid_default(), 70, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Southeastern Arsenal", const_toee.rotation_1100_oclock)
			p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
			p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(419, 484), py06411_shattered_armory_encounters.CtrlTroglodyteBarbarians, const_toee.rotation_0900_oclock, "a7", "troglodyte_barb1")
		self.create_npc_at(utils_obj.sec2loc(418, 489), py06411_shattered_armory_encounters.CtrlTroglodyteBarbarians, const_toee.rotation_0900_oclock, "a7", "troglodyte_barb2")
		self.create_npc_at(utils_obj.sec2loc(415, 489), py06411_shattered_armory_encounters.CtrlTroglodyteBarbarians, const_toee.rotation_0900_oclock, "a7", "troglodyte_barb3")
		return

	def display_encounter_a7(self):
		self.place_encounter_a7(1)
		print("display_encounter_a7")
		self.reveal_monster("a7", "troglodyte_barb1")
		self.reveal_monster("a7", "troglodyte_barb2")
		self.reveal_monster("a7", "troglodyte_barb3")
		return

	def activate_encounter_a7(self):
		print("activate_encounter_a7")
		self.activate_monster("a7", "troglodyte_barb1")
		self.activate_monster("a7", "troglodyte_barb2")
		self.activate_monster("a7", "troglodyte_barb3")
		return

	def place_encounter_a9(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			p1 = self.create_promter_at(utils_obj.sec2loc(416, 475), self.get_dialogid_default(), 90, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Northeastern Arsenal", const_toee.rotation_0800_oclock)
			p2 = self.create_promter_at(utils_obj.sec2loc(419, 473), self.get_dialogid_default(), 90, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Northeastern Arsenal", const_toee.rotation_0800_oclock)
			p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
			p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

		if (self.skip_delayed(delayed, 0)): return

		self.create_npc_at(utils_obj.sec2loc(420, 475), py06411_shattered_armory_encounters.CtrlTroglodyteThug, const_toee.rotation_0300_oclock, "a9", "troglodyte_thug1")
		self.create_npc_at(utils_obj.sec2loc(413, 475), py06411_shattered_armory_encounters.CtrlTroglodyteThug, const_toee.rotation_0600_oclock, "a9", "troglodyte_thug2")

		self.create_npc_at(utils_obj.sec2loc(420, 468), py06411_shattered_armory_encounters.CtrlTroglodyteSoldier, const_toee.rotation_0400_oclock, "a9", "troglodyte_sold1")
		self.create_npc_at(utils_obj.sec2loc(413, 468), py06411_shattered_armory_encounters.CtrlTroglodyteSoldier, const_toee.rotation_0400_oclock, "a9", "troglodyte_sold2")

		self.create_npc_at(utils_obj.sec2loc(416, 471), py06411_shattered_armory_encounters.CtrlTroglodyteCleric, const_toee.rotation_0600_oclock, "a9", "troglodyte_cleric")
		return

	def display_encounter_a9(self):
		self.place_encounter_a9(1)
		print("display_encounter_a9")
		self.reveal_monster("a9", "troglodyte_thug1")
		self.reveal_monster("a9", "troglodyte_thug2")

		self.reveal_monster("a9", "troglodyte_sold1")
		self.reveal_monster("a9", "troglodyte_sold2")

		self.reveal_monster("a9", "troglodyte_cleric")
		return

	def activate_encounter_a9(self):
		print("activate_encounter_a9")
		npc, info = self.activate_monster("a9", "troglodyte_thug1")
		utils_sneak.npc_make_hide(npc, 1)

		npc, info = self.activate_monster("a9", "troglodyte_thug2")
		utils_sneak.npc_make_hide(npc, 1)

		self.activate_monster("a9", "troglodyte_sold1")
		self.activate_monster("a9", "troglodyte_sold2")

		self.activate_monster("a9", "troglodyte_cleric")
		return

	def trigger_monster_step_a9(self, step):
		self.trigger_monster_step("a9", "troglodyte_cleric", step)
		return

	def place_encounter_a10(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(496, 509), self.get_dialogid_default(), 100, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Western Tower", const_toee.rotation_1000_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(495, 512), py06411_shattered_armory_encounters.CtrlOrcharix, const_toee.rotation_0900_oclock, "a10", "orcharix")
		return

	def display_encounter_a10(self):
		self.place_encounter_a10(1)
		print("display_encounter_a10")
		self.reveal_monster("a10", "orcharix")
		return

	def activate_encounter_a10(self):
		print("activate_encounter_a10")
		self.activate_monster("a10", "orcharix")
		return

	def place_encounter_a11(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(501, 517), self.get_dialogid_default(), 110, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Tiefling Quarters", const_toee.rotation_1000_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(496, 516), py06411_shattered_armory_encounters.CtrlTieflingBlademaster, const_toee.rotation_0900_oclock, "a11", "tiefling_blade1")
		self.create_npc_at(utils_obj.sec2loc(496, 520), py06411_shattered_armory_encounters.CtrlTieflingBlademaster, const_toee.rotation_0900_oclock, "a11", "tiefling_blade2")

		self.create_npc_at(utils_obj.sec2loc(492, 517), py06411_shattered_armory_encounters.CtrlTieflingWizard, const_toee.rotation_0900_oclock, "a11", "tiefling_wiz")
		return

	def display_encounter_a11(self):
		self.place_encounter_a11(1)
		print("display_encounter_a11")
		self.reveal_monster("a11", "tiefling_blade1")
		self.reveal_monster("a11", "tiefling_blade2")
		self.reveal_monster("a11", "tiefling_wiz")
		return

	def activate_encounter_a11(self):
		print("activate_encounter_a11")
		self.activate_monster("a11", "tiefling_blade1")
		self.activate_monster("a11", "tiefling_blade2")
		self.activate_monster("a11", "tiefling_wiz")
		return

	def trigger_monster_step_a11(self, step):
		self.trigger_monster_step("a11", "tiefling_wiz", step)
		return

	def place_encounter_a12(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(538, 481), self.get_dialogid_default(), 120, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Southwestern Arsenal", const_toee.rotation_1000_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(537, 484), py06411_shattered_armory_encounters.CtrlFlindSoldier, const_toee.rotation_0200_oclock, "a12", "flind_soldier1")
		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(541, 487), py06411_shattered_armory_encounters.CtrlGnollPriestess, const_toee.rotation_0200_oclock, "a12", "priestess1")
		ctrl.vars["a12"] = 1
		return

	def display_encounter_a12(self):
		self.place_encounter_a12(1)
		print("display_encounter_a12")
		self.reveal_monster("a12", "flind_soldier1")
		self.reveal_monster("a12", "priestess1")
		return

	def activate_encounter_a12(self):
		print("activate_encounter_a12")
		self.activate_monster("a12", "flind_soldier1")
		self.activate_monster("a12", "priestess1")
		return

	def trigger_monster_step_a12(self, step):
		self.trigger_monster_step("a12", "priestess1", step)
		return

	def place_encounter_a14(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(542, 475), self.get_dialogid_default(), 140, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Northwestern Arsenal", const_toee.rotation_0500_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(542, 472), py06411_shattered_armory_encounters.CtrlFlindSoldier, const_toee.rotation_0500_oclock, "a14", "flind_soldier2")
		self.create_npc_at(utils_obj.sec2loc(547, 472), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0300_oclock, "a14", "barb1")
		self.create_npc_at(utils_obj.sec2loc(538, 472), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0600_oclock, "a14", "barb2")

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(544, 467), py06411_shattered_armory_encounters.CtrlGnollPriestess, const_toee.rotation_0500_oclock, "a14", "priestess2")
		ctrl.vars["a14"] = 1
		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(542, 467), py06411_shattered_armory_encounters.CtrlGnollPriestess, const_toee.rotation_0500_oclock, "a14", "priestess3")
		ctrl.vars["a14"] = 2
		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(540, 467), py06411_shattered_armory_encounters.CtrlGnollPriestess, const_toee.rotation_0500_oclock, "a14", "priestess4")
		ctrl.vars["a14"] = 3
		return

	def display_encounter_a14(self):
		self.place_encounter_a14(1)
		print("display_encounter_a14")
		self.reveal_monster("a14", "flind_soldier2")
		self.reveal_monster("a14", "barb1")
		self.reveal_monster("a14", "barb2")

		self.reveal_monster("a14", "priestess2")
		self.reveal_monster("a14", "priestess3")
		self.reveal_monster("a14", "priestess4")
		return

	def activate_encounter_a14(self):
		print("activate_encounter_a14")
		self.activate_monster("a14", "flind_soldier2")
		self.activate_monster("a14", "barb1")
		self.activate_monster("a14", "barb2")

		self.activate_monster("a14", "priestess2")
		self.activate_monster("a14", "priestess3")
		self.activate_monster("a14", "priestess4")
		return

	def trigger_monster_step_a14(self, step):
		self.trigger_monster_step("a14", "priestess2", step)
		self.trigger_monster_step("a14", "priestess3", step)
		self.trigger_monster_step("a14", "priestess4", step)
		return

	def place_encounter_a15(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(500, 444), self.get_dialogid_default(), 150, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Foundry Foyer", const_toee.rotation_0300_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(509, 445), py06411_shattered_armory_encounters.CtrlTrollMercenary, const_toee.rotation_0400_oclock, "a15", "troll")
		return

	def display_encounter_a15(self):
		self.place_encounter_a15(1)
		print("display_encounter_a15")
		self.reveal_monster("a15", "troll")
		return

	def activate_encounter_a15(self):
		print("activate_encounter_a15")
		self.activate_monster("a15", "troll")
		return

	def place_encounter_a16(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(519, 445), self.get_dialogid_default(), 160, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Foundry", const_toee.rotation_0300_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(533, 438), py06411_shattered_armory_encounters.CtrlElementalFireHuge, const_toee.rotation_0400_oclock, "a16", "fire_elemental")

		self.create_npc_at(utils_obj.sec2loc(520, 442), py06411_shattered_armory_encounters.CtrlDerroArtisan, const_toee.rotation_0200_oclock, "a16", "derro1")
		self.create_npc_at(utils_obj.sec2loc(520, 448), py06411_shattered_armory_encounters.CtrlDerroArtisan, const_toee.rotation_0200_oclock, "a16", "derro2")
		self.create_npc_at(utils_obj.sec2loc(525, 445), py06411_shattered_armory_encounters.CtrlDerroArtisanBoss, const_toee.rotation_0200_oclock, "a16", "derro3")
		return

	def display_encounter_a16(self):
		self.place_encounter_a16(1)
		print("display_encounter_a16")
		self.reveal_monster("a16", "fire_elemental")
		self.reveal_monster("a16", "derro1")
		self.reveal_monster("a16", "derro2")
		self.reveal_monster("a16", "derro3")
		return

	def activate_encounter_a16(self):
		print("activate_encounter_a16")
		self.activate_monster("a16", "fire_elemental")
		self.activate_monster("a16", "derro1")
		self.activate_monster("a16", "derro2")
		self.activate_monster("a16", "derro3")
		return

	def place_encounter_a18(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(454, 445), self.get_dialogid_default(), 180, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Gate Antechamber", const_toee.rotation_0700_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(461, 440), py06411_shattered_armory_encounters.CtrlSuccubus, const_toee.rotation_0500_oclock, "a18", "succubus")
		npc.scripts[const_toee.sn_dialog] = 681
		return

	def display_encounter_a18(self):
		self.place_encounter_a18(1)
		print("display_encounter_a18")
		self.reveal_monster("a18", "succubus")
		return

	def activate_encounter_a18(self):
		print("activate_encounter_a18")
		self.activate_monster("a18", "succubus", 1, 0)
		return

	def place_encounter_a19(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(436, 445), self.get_dialogid_default(), 190, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shattered Gates", const_toee.rotation_0700_oclock)

		if (self.skip_delayed(delayed, 0)): return
		
		self.create_npc_at(utils_obj.sec2loc(430, 445), py06411_shattered_armory_encounters.CtrlMezzoloth, const_toee.rotation_0800_oclock, "a19", "mezzoloth")
		return

	def display_encounter_a19(self):
		self.place_encounter_a19(1)
		print("display_encounter_a19")
		self.reveal_monster("a19", "mezzoloth")
		return

	def activate_encounter_a19(self):
		print("activate_encounter_a19")
		self.activate_monster("a19", "mezzoloth")
		return

	def place_encounter_a20(self, delayed = None):
		if (self.skip_delayed(delayed, 1)): 
			self.create_promter_at(utils_obj.sec2loc(420, 445), self.get_dialogid_default(), 200, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "The Warchief", const_toee.rotation_0700_oclock)

		if (self.skip_delayed(delayed, 0)): return

		self.create_npc_at(utils_obj.sec2loc(412, 444), py06411_shattered_armory_encounters.CtrlGnollWarchief, const_toee.rotation_0800_oclock, "a20", "warchief")
		self.create_npc_at(utils_obj.sec2loc(423, 438), py06411_shattered_armory_encounters.CtrlGnollHezrou, const_toee.rotation_0500_oclock, "a20", "hezrou")
		return

	def display_encounter_a20(self):
		self.place_encounter_a20(1)
		print("display_encounter_a20")
		self.reveal_monster("a20", "warchief")
		return

	def activate_encounter_a20(self):
		print("activate_encounter_a20")
		self.activate_monster("a20", "warchief")
		self.activate_monster("a20", "hezrou")
		return

	def trigger_monster_step_a20(self, step):
		self.reveal_monster("a20", "hezrou")
		return

	def place_ark(self):
		pole1 = toee.game.obj_create(12884, utils_obj.sec2loc(544, 466), 1.4142139, -9.899495)
		pole1.rotation = 0.7853982

		pole2 = toee.game.obj_create(12884, utils_obj.sec2loc(544,465), -1.41421306, -4.242641)
		pole2.rotation = 0.7853982

		ark = toee.game.obj_create(12883, utils_obj.sec2loc(543,465), -2.82842684, 5.65685368)
		ark.rotation = 2.3561945

		return

	def check_entrance_patrol(self):
		threshhold_hours_passed = 4*24 + 16 + 1
		left_for = self.last_entered_shrs - self.last_leave_shrs
		passed = left_for >= threshhold_hours_passed
		print("check_entrance_patrol left_for: {} hrs, passed: {}, treshhold: {}, last_leave_shrs: {}, last_entered_shrs: {}".format(left_for, passed, threshhold_hours_passed, self.last_leave_shrs, self.last_entered_shrs))
		if (not passed): return 0

		#print(self.factions_existance)
		spawn_left = 0
		if (self.factions_existance and (shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN in self.factions_existance)): 
			spawn_left = self.factions_existance[shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN][0]

		print("spawn_left: {}".format(spawn_left))
		if (spawn_left == 0): 
			return 0

		self.place_encounter_patrol(0)
		return 1

	def factions_existance_refresh(self):
		print("factions_existance_refresh")
		self.factions_existance = None
		self.factions_existance = monster_info.MonsterInfo.get_factions_existance(self.m2, 0)
		self.factions_existance = monster_info.MonsterInfo.get_factions_existance(self.promters_info, 0, self.factions_existance)
		print(self.factions_existance)
		return

	# Sleep interface
	def encounter_exists(self, setup, encounter):
		assert isinstance(setup, toee.PyRandomEncounterSetup)
		assert isinstance(encounter, toee.PyRandomEncounter)

		will_not_happen = toee.game.random_range(0, 9)
		print("Sleep random: {}".format(will_not_happen))
		if (will_not_happen): return 0

		print("Checking since spawned: {} < 20".format(self.last_patrol_spawned_shrs))
		if (self.last_patrol_spawned_shrs):
			current = toee.game.time.time_game_in_hours2(toee.game.time)
			past_since = current - self.last_patrol_spawned_shrs
			if (past_since < 20): 
				print("Too soon, returning")
				return 0

		encounter.id = 6410
		encounter.flags |= toee.ES_F_SLEEP_ENCOUNTER
		return 1

	# Sleep interface
	def encounter_create(self, encounter):
		assert isinstance(encounter, toee.PyRandomEncounter)
		if (encounter.id != 6410): return
		self.place_encounter_patrol(1)
		return

	def critter_dying(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		#debug.breakp("critter_dying")
		self.factions_existance_refresh()

		if (attachee and attachee.proto == py06411_shattered_armory_encounters.CtrlGnollWarchief.get_proto_id()):
			toee.game.global_flags[shattered_consts.GLOBAL_FLAG_WARCHIEF_KILLED] = 1
			attachee.obj_set_obj(toee.obj_f_npc_combat_focus, toee.OBJ_HANDLE_NULL)

		self.check_sleep_status_update(1)
		return
