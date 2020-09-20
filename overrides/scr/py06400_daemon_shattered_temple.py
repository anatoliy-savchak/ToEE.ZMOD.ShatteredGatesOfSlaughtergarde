import toee, debugg, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon, debug
import ctrl_behaviour, py06122_cormyr_prompter, shattered_consts, py06211_shuttered_monster, const_proto_scrolls, py06401_shattered_temple_encounters, const_proto_wands, utils_npc, monster_info
import py00677FarSouthDoor, startup_zmod, const_proto_containers, const_traps, const_proto_items, math, utils_locks

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	#debugg.breakp("san_new_map")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_TEMPLE): toee.RUN_DEFAULT
	ctrl = CtrlShatteredTemple.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debugg.breakp("san_first_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_TEMPLE): toee.RUN_DEFAULT
	ctrl = CtrlShatteredTemple.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	if (attachee.map == shattered_consts.MAP_ID_SHATERRED_TEMPLE):
		c = cst()
		if (c):
			c.check_sleep_status_update()
	return toee.RUN_DEFAULT

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	print("san_use name: {}, obj: {}".format(attachee.name, attachee))

	if (attachee.name == shattered_consts.NAMEID_DOOR_T7):
		toee.game.timevent_add(_t7_after, (attachee, triggerer), 300, 1) # 1000 = 1 second

	elif (attachee.name == shattered_consts.NAMEID_SHATTERED_TEMPLE_EXIT):
		cst().last_leave_shrs = toee.game.time.time_game_in_hours2(toee.game.time)
		total_seconds = py00677FarSouthDoor.distance_sumbertone_to_shattered_temple_sec()
		print("fade_and_teleport total_seconds: {}".format(total_seconds))
		toee.game.fade_and_teleport(total_seconds, 0, 0, 5122, 538, 510 ) #sumberton

	elif (attachee.name == shattered_consts.NAMEID_DOOR_T1_T2):
		print("NAMEID_DOOR_T1_T2 clicked: {}".format(attachee))
		loc = utils_obj.loc2sec(triggerer.location)
		flags = attachee.portal_flags_get()
		if (loc[1] >= 482): # is south of the door
			if (not flags & toee.OPF_BUSTED):
				attachee.portal_flag_set(toee.OPF_BUSTED)
				attachee.float_text_line("Unbarred the door!", toee.tf_green)
		elif(not flags & toee.OPF_BUSTED):
			attachee.float_text_line("Barred!", toee.tf_blue)
			return toee.SKIP_DEFAULT

	elif (attachee.proto == shattered_consts.PROTO_DEMON_ARCH_10FT):
		attachee.object_flag_set(toee.OF_DONTDRAW)
		utils_obj.obj_timed_destroy(attachee, 2000, 1)

	elif (attachee.name == shattered_consts.NAMEID_DOOR_T21):
		print("NAMEID_DOOR_T21 clicked: {}".format(attachee))
		if (not (attachee.object_flags_get() & toee.OF_DONTDRAW)):
			attachee.object_flag_set(toee.OF_DONTDRAW)
			utils_obj.obj_timed_destroy(attachee, 2000, 1)
			sibling = utils_obj.get_sibling_door(attachee)
			if (sibling and not (sibling.object_flags_get() & toee.OF_DONTDRAW)):
				sibling.object_flag_set(toee.OF_DONTDRAW)
				sibling.portal_toggle_open()
				utils_obj.obj_timed_destroy(sibling, 2000, 1)

	return toee.RUN_DEFAULT

def _t7_after(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	#obj.object_flag_set(toee.OF_OFF)
	attachee.destroy()
	for pc in toee.game.party:
		pc.anim_goal_interrupt()
	return 1

def san_dying(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	c = cst()
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

def cst():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(shattered_consts.SHATERRED_TEMPLE_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlShatteredTemple.get_name() in o.data):
		result = o.data[CtrlShatteredTemple.get_name()]
	else: return None
	assert isinstance(result, CtrlShatteredTemple)
	return result

class CtrlShatteredTemple(ctrl_daemon.CtrlDaemon):

	def created(self, npc):
		super(CtrlShatteredTemple, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = 6400
		return

	@staticmethod
	def get_name():
		return "CtrlShatteredTemple"

	def place_encounters(self, new_map):
		print("new_map: {}".format(new_map))
		print("place_encounters.encounters_placed == {}".format(self.encounters_placed))

		startup_zmod.zmod_templeplus_config_apply()

		if (self.encounters_placed and new_map == 0): return

		this_entrance_time = toee.game.time.time_game_in_hours2(toee.game.time)
		print("this_entrance_time == {}".format(this_entrance_time))
		if (not self.encounters_placed):
			self.first_entered_shrs = this_entrance_time
		self.last_entered_shrs = this_entrance_time
		if (not self.last_leave_shrs):
			self.last_leave_shrs = this_entrance_time

		if (not self.encounters_placed and 1):
			self.place_encounter_t1()
			self.place_encounter_t2()
			self.place_encounter_t3()
			self.place_encounter_t4()
			self.place_encounter_t5()
			self.place_encounter_t6()
			self.place_encounter_t7()
			self.place_encounter_t8()
			self.place_encounter_t9()
			self.place_encounter_t10()
			self.place_encounter_t11()
			self.place_encounter_t12()
			self.place_encounter_t13()
			self.place_encounter_t14()
			self.place_encounter_t15()
			self.place_encounter_t16()
			self.place_encounter_t17()
			self.place_encounter_t18()
			self.place_encounter_t19()
			self.place_encounter_t20()
			self.place_encounter_t21()
			self.place_encounter_t22()
			self.place_encounter_t23()
			self.place_encounter_t24()
			self.place_encounter_t25()
		
		if (not self.encounters_placed and 1):
			self.place_chests()
			self.place_demon_archs()

		self.encounters_placed += 1
		utils_npc.pc_turn_all(const_toee.rotation_0200_oclock)

		self.factions_existance_refresh()

		utils_obj.scroll_to_leader()

		self.check_sleep_status_update(1)
		self.check_entrance_patrol()

		return

	def place_encounter_patrol(self, near_pc):
		self.patrol_spawned_count += 1
		self.last_patrol_spawned_shrs = toee.game.time.time_game_in_hours2(toee.game.time)
		print("place_encounter_patrol {}".format(self.patrol_spawned_count))
		loc1 = utils_obj.sec2loc(480, 473)
		loc2 = utils_obj.sec2loc(480, 476)
		if (near_pc):
			loc1 = toee.game.leader.location - 2
			loc2 = loc1

		npc, ctrl = self.create_arcane_guard_at(loc1, const_toee.rotation_0800_oclock, "t0", "aguard1", 4, 0, 0)
		utils_npc.npc_unexploit(npc)

		npc, ctrl = self.create_arcane_guard_at(loc2, const_toee.rotation_0800_oclock, "t0", "aguard2", 5, 0, 0)
		utils_npc.npc_unexploit(npc)
		if (not near_pc):
			ctrl.fire_epicenter = utils_obj.sec2loc(483, 474)
		return

	def place_encounter_t1(self):
		self.create_promter_at(utils_obj.sec2loc(484, 475), 6400, 10, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Tapestry Hall").rotation = const_toee.rotation_0800_oclock

		self.create_surrinak_house_guard_at(utils_obj.sec2loc(481, 472), const_toee.rotation_0800_oclock, "t1", "guard1")
		self.create_surrinak_house_guard_at(utils_obj.sec2loc(481, 478), const_toee.rotation_0800_oclock, "t1", "guard2")
		return

	def display_encounter_t1(self):
		self.reveal_monster("t1", "guard1")
		self.reveal_monster("t1", "guard2")
		return

	def activate_encounter_t1(self):
		self.activate_monster("t1", "guard1")
		self.activate_monster("t1", "guard2")
		return

	def place_encounter_t2(self):
		self.create_promter_at(utils_obj.sec2loc(487, 492), 6400, 20, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Spring").rotation = const_toee.rotation_0200_oclock

		self.create_grimlock_at(utils_obj.sec2loc(484, 492), const_toee.rotation_1100_oclock, "t2", "grmilock1")
		self.create_grimlock_at(utils_obj.sec2loc(488, 492), const_toee.rotation_1100_oclock, "t2", "grmilock2")
		return

	def display_encounter_t2(self):
		self.reveal_monster("t2", "grmilock1")
		self.reveal_monster("t2", "grmilock2")
		return

	def activate_encounter_t2(self):
		self.activate_monster("t2", "grmilock1")
		self.activate_monster("t2", "grmilock2")
		return

	def place_encounter_t3(self):
		self.create_promter_at(utils_obj.sec2loc(485, 510), 6400, 30, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Storage").rotation = const_toee.rotation_1000_oclock

		self.create_surrinak_house_guard_at(utils_obj.sec2loc(492, 510), const_toee.rotation_1100_oclock, "t3", "guard1", 1)
		self.create_surrinak_house_guard_at(utils_obj.sec2loc(492, 514), const_toee.rotation_1100_oclock, "t3", "guard2", 1)
		return

	def display_encounter_t3(self):
		self.reveal_monster("t3", "guard1")
		self.reveal_monster("t3", "guard2")
		return

	def activate_encounter_t3(self):
		self.activate_monster("t3", "guard1")
		self.activate_monster("t3", "guard2")
		return

	def place_encounter_t4(self):
		p1 = self.create_promter_at(utils_obj.sec2loc(470, 475), 6400, 40, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Stable")
		p2 = self.create_promter_at(utils_obj.sec2loc(462, 479), 6400, 40, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Stable")
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p1.rotation = const_toee.rotation_0800_oclock
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)
		p2.rotation = const_toee.rotation_0300_oclock

		self.create_riding_lizard_at(utils_obj.sec2loc(469, 470), const_toee.rotation_0800_oclock, "t4", "lizard1")
		self.create_riding_lizard_at(utils_obj.sec2loc(464, 470), const_toee.rotation_0800_oclock, "t4", "lizard2")
		self.create_riding_lizard_at(utils_obj.sec2loc(459, 470), const_toee.rotation_0800_oclock, "t4", "lizard3")
		self.create_riding_lizard_at(utils_obj.sec2loc(464, 477), const_toee.rotation_0800_oclock, "t4", "lizard4")
		self.create_drow_rider_at(utils_obj.sec2loc(465, 481), const_toee.rotation_0800_oclock, "t4", "rider")
		return

	def display_encounter_t4(self):
		self.reveal_monster("t4", "lizard1")
		self.reveal_monster("t4", "lizard2")
		self.reveal_monster("t4", "lizard3")
		self.reveal_monster("t4", "lizard4")
		self.reveal_monster("t4", "rider")
		return

	def activate_encounter_t4(self):
		self.activate_monster("t4", "lizard1")
		self.activate_monster("t4", "lizard2")
		self.activate_monster("t4", "lizard3")
		self.activate_monster("t4", "lizard4")
		self.activate_monster("t4", "rider")
		return

	def place_encounter_t5(self):
		p1 = self.create_promter_at(utils_obj.sec2loc(449, 479), 6400, 50, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Eastern Intersection")
		p2 = self.create_promter_at(utils_obj.sec2loc(441, 486), 6400, 50, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Eastern Intersection")
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p1.rotation = const_toee.rotation_0800_oclock
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)
		p2.rotation = const_toee.rotation_0400_oclock

		leader, ctrl = self.create_arcane_guard_at(utils_obj.sec2loc(438, 476), const_toee.rotation_0800_oclock, "t5", "aguard")
		if (ctrl):
			ctrl.fire_epicenter = utils_obj.sec2loc(453, 480)
		minion = self.create_doom_fist_monk_at(utils_obj.sec2loc(442, 476), const_toee.rotation_0800_oclock, "t5", "monk1")
		minion.obj_set_obj(toee.obj_f_npc_leader, leader)
		minion = self.create_doom_fist_monk_at(utils_obj.sec2loc(442, 482), const_toee.rotation_0800_oclock, "t5", "monk2")
		minion.obj_set_obj(toee.obj_f_npc_leader, leader)
		return

	def display_encounter_t5(self):
		self.reveal_monster("t5", "monk1")
		self.reveal_monster("t5", "monk2")
		self.reveal_monster("t5", "aguard")
		return

	def activate_encounter_t5(self):
		self.activate_monster("t5", "monk1")
		self.activate_monster("t5", "monk2")
		self.activate_monster("t5", "aguard")
		return

	def place_encounter_t6(self):
		p1 = self.create_promter_at(utils_obj.sec2loc(463, 495), 6400, 60, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shrine of the Sinuous Serpent")
		p2 = self.create_promter_at(utils_obj.sec2loc(470, 498), 6400, 60, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shrine of the Sinuous Serpent")
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

		self.create_quaggoth_at(utils_obj.sec2loc(458, 498), const_toee.rotation_0200_oclock, "t6", "quaggoth")
		return

	def display_encounter_t6(self):
		self.reveal_monster("t6", "quaggoth")
		return

	def activate_encounter_t6(self):
		self.activate_monster("t6", "quaggoth")
		return

	def place_encounter_t7(self):
		self.create_promter_at(utils_obj.sec2loc(430, 493), 6400, 70, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Northern Quarters").rotation = const_toee.rotation_0800_oclock

		fire_epicenter = utils_obj.sec2loc(437, 494)
		npc, ctrl = self.create_arcane_guard_at(utils_obj.sec2loc(430, 493), const_toee.rotation_0800_oclock, "t7", "aguard1", 2)
		if (ctrl):
			ctrl.fire_epicenter = fire_epicenter
		npc, ctrl = self.create_arcane_guard_at(utils_obj.sec2loc(427, 493), const_toee.rotation_0800_oclock, "t7", "aguard2", 3)
		if (ctrl):
			ctrl.fire_epicenter = fire_epicenter
		return

	def display_encounter_t7(self):
		self.reveal_monster("t7", "aguard1")
		self.reveal_monster("t7", "aguard2")
		return

	def activate_encounter_t7(self):
		self.activate_monster("t7", "aguard1")
		self.activate_monster("t7", "aguard2")
		return

	def place_encounter_t8(self):
		self.create_promter_at(utils_obj.sec2loc(428, 506), 6400, 80, 15, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Southern Quarters")

		self.create_npc_at(utils_obj.sec2loc(422, 503), py06401_shattered_temple_encounters.CtrlGargoyle, const_toee.rotation_0800_oclock, "t8", "gargoyle")
		return

	def display_encounter_t8(self):
		self.reveal_monster("t8", "gargoyle")
		return

	def activate_encounter_t8(self):
		self.activate_monster("t8", "gargoyle")
		return

	def place_encounter_t9(self):
		self.create_promter_at(utils_obj.sec2loc(438, 511), 6400, 90, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Priest Quarters")

		self.create_npc_at(utils_obj.sec2loc(441, 511), py06401_shattered_temple_encounters.CtrlDrowZombie, const_toee.rotation_0800_oclock, "t9", "dzombie1")
		self.create_npc_at(utils_obj.sec2loc(438, 514), py06401_shattered_temple_encounters.CtrlDrowZombieDesicrate, const_toee.rotation_0800_oclock, "t9", "dzombie2")
		return

	def display_encounter_t9(self):
		self.reveal_monster("t9", "dzombie1")
		self.reveal_monster("t9", "dzombie2")
		return

	def activate_encounter_t9(self):
		self.activate_monster("t9", "dzombie1")
		self.activate_monster("t9", "dzombie2")
		return

	def place_encounter_t10(self):
		self.create_promter_at(utils_obj.sec2loc(434, 460), 6400, 100, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Bat Lair")

		self.create_npc_at(utils_obj.sec2loc(423, 462), py06401_shattered_temple_encounters.CtrlDireBat, const_toee.rotation_0800_oclock, "t10", "bat1")
		self.create_npc_at(utils_obj.sec2loc(423, 466), py06401_shattered_temple_encounters.CtrlDireBat, const_toee.rotation_0800_oclock, "t10", "bat2")
		return

	def display_encounter_t10(self):
		self.reveal_monster("t10", "bat1")
		self.reveal_monster("t10", "bat2")
		return

	def activate_encounter_t10(self):
		self.activate_monster("t10", "bat1")
		self.activate_monster("t10", "bat2")
		return

	def place_encounter_t11(self):
		self.create_promter_at(utils_obj.sec2loc(447, 461), 6400, 110, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shrine of the Fout Arms")

		self.create_npc_at(utils_obj.sec2loc(453, 459), py06401_shattered_temple_encounters.CtrlWererat, const_toee.rotation_1100_oclock, "t11", "warerat1")
		self.create_npc_at(utils_obj.sec2loc(449, 459), py06401_shattered_temple_encounters.CtrlWererat, const_toee.rotation_1100_oclock, "t11", "warerat2")
		return

	def display_encounter_t11(self):
		self.reveal_monster("t11", "warerat1")
		self.reveal_monster("t11", "warerat2")

		for obj in toee.game.obj_list_range(utils_obj.sec2loc(449, 459), 20, toee.OLC_PORTAL):
			utils_obj.obj_timed_destroy(obj, 100, 1)
		return

	def activate_encounter_t11(self):
		self.activate_monster("t11", "warerat1")
		self.activate_monster("t11", "warerat2")
		return

	def place_encounter_t12(self):
		self.create_promter_at(utils_obj.sec2loc(450, 449), 6400, 120, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Dragon's Lair")

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(448, 442), py06401_shattered_temple_encounters.CtrlGaranaach, const_toee.rotation_0600_oclock, "t12", "dragon")
		ctrl.notify_start_combat_npcid = self.id
		ctrl.notify_start_combat_ctrlname = self.get_name()
		return

	def display_encounter_t12(self):
		self.reveal_monster("t12", "dragon")
		return

	def activate_encounter_t12(self):
		self.activate_monster("t12", "dragon")
		return

	def place_encounter_t13(self):
		self.create_promter_at(utils_obj.sec2loc(440, 445), 6400, 132, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Yuan-Ti Lair")

		self.create_npc_at(utils_obj.sec2loc(436, 443), py06401_shattered_temple_encounters.CtrlShenn, const_toee.rotation_0900_oclock, "t13", "shenn")
		return

	def display_encounter_t13(self):
		self.reveal_monster("t13", "shenn", 1)
		return

	def activate_encounter_t13(self):
		npc, info = self.activate_monster("t13", "shenn", 1, 1, 1)
		return npc, info

	def place_encounter_t14(self):
		self.create_promter_at(utils_obj.sec2loc(478, 455), 6400, 140, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Bell Chamber")

		self.create_npc_at(utils_obj.sec2loc(478, 442), py06401_shattered_temple_encounters.CtrlWererat, const_toee.rotation_0200_oclock, "t14", "warerat1")
		self.create_npc_at(utils_obj.sec2loc(475, 442), py06401_shattered_temple_encounters.CtrlWererat, const_toee.rotation_0800_oclock, "t14", "warerat2")
		return

	def display_encounter_t14(self):
		self.reveal_monster("t14", "warerat1")
		self.reveal_monster("t14", "warerat2")
		return

	def activate_encounter_t14(self):
		self.activate_monster("t14", "warerat1")
		self.activate_monster("t14", "warerat2")
		return

	def place_encounter_t15(self):
		self.create_promter_at(utils_obj.sec2loc(495, 451), 6400, 150, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Baptismal Font")

		self.create_npc_at(utils_obj.sec2loc(498, 450), py06401_shattered_temple_encounters.CtrlLolthSting, const_toee.rotation_0200_oclock, "t15", "sting1")
		self.create_npc_at(utils_obj.sec2loc(498, 448), py06401_shattered_temple_encounters.CtrlLolthSting, const_toee.rotation_0200_oclock, "t15", "sting2")
		return

	def display_encounter_t15(self):
		self.reveal_monster("t15", "sting1")
		self.reveal_monster("t15", "sting2")
		return

	def activate_encounter_t15(self):
		self.activate_monster("t15", "sting1")
		self.activate_monster("t15", "sting2")
		return

	def place_encounter_t16(self):
		self.create_promter_at(utils_obj.sec2loc(506, 449), 6400, 160, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shrine of the Crone")

		leader, ctrl = self.create_npc_at(utils_obj.sec2loc(512, 450), py06401_shattered_temple_encounters.CtrlLanthurrae, const_toee.rotation_0200_oclock, "t16", "priestess")
		minion = self.create_npc_at(utils_obj.sec2loc(510, 448), py06401_shattered_temple_encounters.CtrlGrimlock, const_toee.rotation_0200_oclock, "t16", "grimlock1")[0]
		minion.obj_set_obj(toee.obj_f_npc_leader, leader)
		minion = self.create_npc_at(utils_obj.sec2loc(510, 452), py06401_shattered_temple_encounters.CtrlGrimlock, const_toee.rotation_0200_oclock, "t16", "grimlock2")[0]
		minion.obj_set_obj(toee.obj_f_npc_leader, leader)
		return

	def display_encounter_t16(self):
		self.reveal_monster("t16", "priestess")
		self.reveal_monster("t16", "grimlock1")
		self.reveal_monster("t16", "grimlock2")
		return

	def activate_encounter_t16(self):
		self.activate_monster("t16", "priestess")
		self.activate_monster("t16", "grimlock1")
		self.activate_monster("t16", "grimlock2")
		return

	def place_encounter_t17(self):
		self.create_promter_at(utils_obj.sec2loc(512, 466), 6400, 170, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Living Pictures")

		self.create_npc_at(utils_obj.sec2loc(517, 469), py06401_shattered_temple_encounters.CtrlWight, const_toee.rotation_0000_oclock, "t17", "wight")
		return

	def display_encounter_t17(self):
		self.reveal_monster("t17", "wight")
		return

	def activate_encounter_t17(self):
		self.activate_monster("t17", "wight")
		return

	def place_encounter_t18(self):
		self.create_promter_at(utils_obj.sec2loc(507, 475), 6400, 180, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Audience Hall", const_toee.rotation_0800_oclock)

		self.create_npc_at(utils_obj.sec2loc(504, 471), py06401_shattered_temple_encounters.CtrlDrowAcolyte, const_toee.rotation_0600_oclock, "t18", "acolyte1")
		self.create_npc_at(utils_obj.sec2loc(504, 478), py06401_shattered_temple_encounters.CtrlDrowAcolyte, const_toee.rotation_0900_oclock, "t18", "acolyte2")
		self.create_npc_at(utils_obj.sec2loc(500, 478), py06401_shattered_temple_encounters.CtrlDrowAcolyte, const_toee.rotation_0900_oclock, "t18", "acolyte3")
		return

	def display_encounter_t18(self, step = None):
		self.reveal_monster("t18", "acolyte1")
		self.reveal_monster("t18", "acolyte2")
		self.reveal_monster("t18", "acolyte3")
		return

	def trigger_monster_step_t18(self, step):
		self.trigger_monster_step("t18", "acolyte1", step)
		self.trigger_monster_step("t18", "acolyte2", step)
		self.trigger_monster_step("t18", "acolyte3", step)
		return

	def activate_encounter_t18(self):
		self.activate_monster("t18", "acolyte1")
		self.activate_monster("t18", "acolyte2")
		self.activate_monster("t18", "acolyte3")
		return

	def place_encounter_t19(self):
		self.create_promter_at(utils_obj.sec2loc(532, 441), 6400, 190, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Collapsed Room", const_toee.rotation_0800_oclock)

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(538, 438), py06401_shattered_temple_encounters.CtrlHuntingSpider, const_toee.rotation_0300_oclock, "t19", "hunting_spider1")
		ctrl.notify_start_combat_npcid = self.id
		ctrl.notify_start_combat_ctrlname = self.get_name()

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(536, 440), py06401_shattered_temple_encounters.CtrlHuntingSpider, const_toee.rotation_0300_oclock, "t19", "hunting_spider2")
		ctrl.notify_start_combat_npcid = self.id
		ctrl.notify_start_combat_ctrlname = self.get_name()

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(527, 439), py06401_shattered_temple_encounters.CtrlHuntingSpider, const_toee.rotation_0800_oclock, "t19", "hunting_spider3")
		ctrl.notify_start_combat_npcid = self.id
		ctrl.notify_start_combat_ctrlname = self.get_name()
		return

	def display_encounter_t19(self):
		self.reveal_monster("t19", "hunting_spider1")
		self.reveal_monster("t19", "hunting_spider2")
		self.reveal_monster("t19", "hunting_spider3")
		return

	def activate_encounter_t19(self):
		result = list()
		monster = self.activate_monster("t19", "hunting_spider1")
		result.append(monster)
		monster = self.activate_monster("t19", "hunting_spider2")
		result.append(monster)
		monster = self.activate_monster("t19", "hunting_spider3")
		result.append(monster)
		return tuple(result)

	def place_encounter_t20(self):
		self.create_promter_at(utils_obj.sec2loc(533, 461), 6400, 200, 15, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Sanctuary", const_toee.rotation_1100_oclock)

		self.create_npc_at(utils_obj.sec2loc(528, 459), py06401_shattered_temple_encounters.CtrlWebSpinningSpider, const_toee.rotation_0900_oclock, "t20", "spinning_spider1")
		self.create_npc_at(utils_obj.sec2loc(539, 459), py06401_shattered_temple_encounters.CtrlWebSpinningSpider, const_toee.rotation_0100_oclock, "t20", "spinning_spider2")
		self.create_npc_at(utils_obj.sec2loc(530, 467), py06401_shattered_temple_encounters.CtrlWebSpinningSpider, const_toee.rotation_1000_oclock, "t20", "spinning_spider3")
		return

	def display_encounter_t20(self):
		self.reveal_monster("t20", "spinning_spider1", 1)
		self.reveal_monster("t20", "spinning_spider2", 1)
		self.reveal_monster("t20", "spinning_spider3", 1)
		return

	def activate_encounter_t20(self):
		result = list()
		monster = self.activate_monster("t20", "spinning_spider1", 1, 1, 1)
		result.append(monster)
		monster = self.activate_monster("t20", "spinning_spider2", 1, 1, 1)
		result.append(monster)
		monster = self.activate_monster("t20", "spinning_spider3", 1, 1, 1)
		result.append(monster)
		return tuple(result)

	def place_encounter_t21(self):
		self.create_promter_at(utils_obj.sec2loc(533, 476), 6400, 210, 15, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shrine of the Death-Dealer", const_toee.rotation_1100_oclock)

		self.create_npc_at(utils_obj.sec2loc(529, 487), py06401_shattered_temple_encounters.CtrlHugeFiendishSpider, const_toee.rotation_0900_oclock, "t21", "fiendish_spider")
		return

	def display_encounter_t21(self):
		self.reveal_monster("t21", "fiendish_spider")
		return

	def activate_encounter_t21(self):
		print("activate_encounter_t21")
		self.activate_monster("t21", "fiendish_spider")
		return

	def place_encounter_t22(self):
		p1 = self.create_promter_at(utils_obj.sec2loc(512, 485), 6400, 220, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Statue Hall", const_toee.rotation_1100_oclock)
		p2 = self.create_promter_at(utils_obj.sec2loc(506, 492), 6400, 220, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Statue Hall", const_toee.rotation_1100_oclock)
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

		self.create_npc_at(utils_obj.sec2loc(515, 497), py06401_shattered_temple_encounters.CtrlAdvancedMagmaHurler, const_toee.rotation_0000_oclock, "t22", "hurler")
		return

	def display_encounter_t22(self):
		self.reveal_monster("t22", "hurler")
		return

	def activate_encounter_t22(self):
		print("activate_encounter_t22")
		self.activate_monster("t22", "hurler")
		return

	def place_encounter_t23(self):
		self.create_promter_at(utils_obj.sec2loc(532, 502), 6400, 230, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Sacrifice Quarters", const_toee.rotation_0200_oclock)

		self.create_npc_at(utils_obj.sec2loc(540, 497), py06401_shattered_temple_encounters.CtrlStirge, const_toee.rotation_0100_oclock, "t23", "stirge1")
		self.create_npc_at(utils_obj.sec2loc(540, 499), py06401_shattered_temple_encounters.CtrlStirge, const_toee.rotation_0100_oclock, "t23", "stirge2")
		self.create_npc_at(utils_obj.sec2loc(540, 501), py06401_shattered_temple_encounters.CtrlStirge, const_toee.rotation_0100_oclock, "t23", "stirge3")
		self.create_npc_at(utils_obj.sec2loc(540, 503), py06401_shattered_temple_encounters.CtrlStirge, const_toee.rotation_0100_oclock, "t23", "stirge4")
		self.create_npc_at(utils_obj.sec2loc(540, 505), py06401_shattered_temple_encounters.CtrlStirge, const_toee.rotation_0100_oclock, "t23", "stirge5")
		self.create_npc_at(utils_obj.sec2loc(540, 507), py06401_shattered_temple_encounters.CtrlStirge, const_toee.rotation_0100_oclock, "t23", "stirge6")
		return

	def display_encounter_t23(self):
		self.reveal_monster("t23", "stirge1")
		self.reveal_monster("t23", "stirge2")
		self.reveal_monster("t23", "stirge3")
		self.reveal_monster("t23", "stirge4")
		self.reveal_monster("t23", "stirge5")
		self.reveal_monster("t23", "stirge6")
		return

	def activate_encounter_t23(self):
		print("activate_encounter_t23")
		self.activate_monster("t23", "stirge1")
		self.activate_monster("t23", "stirge2")
		self.activate_monster("t23", "stirge3")
		self.activate_monster("t23", "stirge4")
		self.activate_monster("t23", "stirge5")
		self.activate_monster("t23", "stirge6")
		return

	def place_encounter_t24(self):
		self.create_promter_at(utils_obj.sec2loc(531, 515), 6400, 240, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Sacrifice Quarters", const_toee.rotation_0200_oclock)

		dy = 2
		self.create_npc_at(utils_obj.sec2loc(541, 512), py06401_shattered_temple_encounters.CtrlWhitespawnHordeling, const_toee.rotation_0100_oclock, "t24", "whitespawn1")
		self.create_npc_at(utils_obj.sec2loc(541, 512 + dy), py06401_shattered_temple_encounters.CtrlWhitespawnHordeling, const_toee.rotation_0100_oclock, "t24", "whitespawn2")
		self.create_npc_at(utils_obj.sec2loc(541, 512 + dy*2), py06401_shattered_temple_encounters.CtrlWhitespawnHordeling, const_toee.rotation_0100_oclock, "t24", "whitespawn3")
		self.create_npc_at(utils_obj.sec2loc(541, 512 + dy*3), py06401_shattered_temple_encounters.CtrlWhitespawnHordeling, const_toee.rotation_0100_oclock, "t24", "whitespawn4")
		return

	def display_encounter_t24(self):
		self.reveal_monster("t24", "whitespawn1")
		self.reveal_monster("t24", "whitespawn2")
		self.reveal_monster("t24", "whitespawn3")
		self.reveal_monster("t24", "whitespawn4")
		return

	def activate_encounter_t24(self):
		print("activate_encounter_t24")
		self.activate_monster("t24", "whitespawn1")
		self.activate_monster("t24", "whitespawn2")
		self.activate_monster("t24", "whitespawn3")
		self.activate_monster("t24", "whitespawn4")
		return

	def place_encounter_t25(self):
		self.create_promter_at(utils_obj.sec2loc(513, 511), 6400, 250, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Mirror Hall", const_toee.rotation_1100_oclock)

		self.create_npc_at(utils_obj.sec2loc(513, 517), py06401_shattered_temple_encounters.CtrlElectrumClockworkHorror, const_toee.rotation_1100_oclock, "t25", "clockwork")
		return

	def display_encounter_t25(self):
		self.reveal_monster("t25", "clockwork")
		return

	def activate_encounter_t25(self):
		print("activate_encounter_t25")
		self.activate_monster("t25", "clockwork")
		return

	def create_surrinak_house_guard_at(self, npc_loc, rot, encounter, code_name, skip_longbow = 0):
		PROTO_NPC_SURRINAK_HOUSE_GUARD = 14900
		npc = toee.game.obj_create(PROTO_NPC_SURRINAK_HOUSE_GUARD, npc_loc)
		if (npc):
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_BREASTPLATE_MASTERWORK, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
			#utils_item.item_create_in_inventory(const_proto_armor.PROTO_CLOAK_BLACK, npc)
			if (not skip_longbow):
				utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_LONGBOW_COMPOSITE_14, npc)
				utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_ARROW_QUIVER, npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD_MASTERWORK, npc)
			npc.item_wield_best_all()
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			ctrl.option_prefer_low_ac = 1
			if (skip_longbow):
				npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)
		return npc

	def create_grimlock_at(self, npc_loc, rot, encounter, code_name):
		PROTO_NPC_GRIMLOCK = 14916
		npc = toee.game.obj_create(PROTO_NPC_GRIMLOCK, npc_loc)
		if (npc):
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GREATAXE, npc)
			npc.item_wield_best_all()
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			ctrl.option_prefer_low_ac = 1
			npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)
		return npc

	def create_riding_lizard_at(self, npc_loc, rot, encounter, code_name):
		PROTO_NPC_RIDING_LIZARD = 14917
		npc = toee.game.obj_create(PROTO_NPC_RIDING_LIZARD, npc_loc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
			#ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			#ctrl.option_5fs_prefer = 1
			#npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)
		return npc

	def create_drow_rider_at(self, npc_loc, rot, encounter, code_name):
		PROTO_NPC_DROW_RIDER = 14918
		npc = toee.game.obj_create(PROTO_NPC_DROW_RIDER, npc_loc)
		if (npc):
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE_MASTERWORK, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GLAIVE_MASTERWORK, npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD_MASTERWORK, npc)
			npc.feat_add(toee.feat_weapon_focus_glaive, 1)
			npc.item_wield_best_all()
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
			#ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			#ctrl.option_prefer_low_ac = 1
			npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)
		return npc

	def create_doom_fist_monk_at(self, npc_loc, rot, encounter, code_name):
		npc, ctrl = py06401_shattered_temple_encounters.CtrlDoomFistMonk.create_obj_and_class(npc_loc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
		return npc

	def create_arcane_guard_at(self, npc_loc, rot, encounter, code_name, guard_ai_type = 0, no_draw = 1, no_kos = 1):
		npc, ctrl = py06401_shattered_temple_encounters.CtrlArcaneGuard.create_obj_and_class(npc_loc, 0)
		if (ctrl):
			ctrl.guard_ai_type = guard_ai_type
			ctrl.created(npc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, no_draw, no_kos)
		return npc, ctrl

	def create_quaggoth_at(self, npc_loc, rot, encounter, code_name):
		npc, ctrl = py06401_shattered_temple_encounters.CtrlQuaggoth.create_obj_and_class(npc_loc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
		return npc

	def reveal_monster1(self, encounter_name, monster_code_name, no_error = 0):
		npc = None
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc and not info.revealed):
				ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(npc)
				if (ctrl and ("revealing" in dir(ctrl))):
					ctrl.revealing(npc)
				info.revealed = 1
				npc.object_flag_unset(toee.OF_DONTDRAW)
				if (ctrl and ("revealed" in dir(ctrl))):
					ctrl.revealed(npc)
		if (not npc and not no_error and (not info or not info.revealed)):
			print("Monster {} {} not found!".format(encounter_name, monster_code_name))
			debugg.breakp("Monster not found")
		return npc, info

	def activate_monster1(self, encounter_name, monster_code_name, remove_no_attack = 1, remove_no_kos = 1, no_error = 0):
		npc = None
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc):
				if (not info.activated):
					ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(npc)
					if (ctrl and ("activating" in dir(ctrl))):
						ctrl.activating(npc)
					if (remove_no_attack):
						npc.npc_flag_unset(toee.ONF_NO_ATTACK)
					info.activated = 1
					print("ACTIVATED: {}".format(npc))
					if (remove_no_kos):
						npc.npc_flag_set(toee.ONF_KOS)
					if (ctrl and ("activated" in dir(ctrl))):
						ctrl.activated(npc)
				else: info.activated +=1
		if (not npc and not no_error):
			print("Monster {} {} not found!".format(encounter_name, monster_code_name))
			debugg.breakp("Monster not found")
		return npc, info

	def trigger_monster_step(self, encounter_name, monster_code_name, step):
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc):
				ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(npc)
				if (ctrl and ("trigger_step" in dir(ctrl))):
					result = ctrl.trigger_step(npc, step)
					return result
		return

	def print_monsters(self):
		exptotal = 0
		exptotal1 = 0
		per = len(toee.game.party)
		for info in self.m2:
			assert isinstance(info, monster_info.MonsterInfo)
			#npc = toee.game.get_obj_by_id(info.id)
			exp = utils_npc.npc_get_cr_exp(toee.game.leader, info.cr)
			exptotal1 += exp // per
			exptotal += exp
			print("{}, cr: {}, exp: {}, total: {}, total per one: {}, id: {}".format(info.name, info.cr, exp, exptotal, exptotal1, info.id))
		return

	def on_notify_combat_start(self, ctrl, npc):
		assert isinstance(ctrl, ctrl_behaviour.CtrlBehaviour)
		assert isinstance(npc, toee.PyObjHandle)
		print("on_notify_combat_start: {}, {}, {}".format(ctrl, npc, toee.game.combat_turn))
		#debugg.breakp("on_notify_combat_start")
		if (type(ctrl) is py06401_shattered_temple_encounters.CtrlGaranaach and toee.game.combat_turn == 2):
			#debugg.breakp("on_notify_combat_start2")
			self.display_encounter_t13()
			npc2, info = self.activate_encounter_t13()
			print("npc2, info: {}, {}".format(npc2, info))
			closest = None
			closest_dist = 0
			for pc in toee.game.party:
				if (not npc2.can_see(pc)): continue
				dist = npc2.distance_to(pc)
				if (not closest):
					closest = pc
					closest_dist = dist
					continue
				if (dist < closest_dist):
					closest = pc
			print("closest: {}".format(closest))
			if (not closest):
				closest = toee.game.party[0]
				#debugg.breakp("problem")
			npc2.attack(closest)
			npc2.add_to_initiative()
		elif (type(ctrl) is py06401_shattered_temple_encounters.CtrlHuntingSpider and toee.game.combat_turn == 3):
			#debugg.breakp("on_notify_combat_start3")
			self.display_encounter_t20()
			monsters = self.activate_encounter_t20()
			print("monsters: {}".format(monsters))
			closest_pc_tuple = utils_npc.find_pc_closest_to_origin(utils_obj.sec2loc(533, 442))
			print("closest_pc: {}".format(closest_pc_tuple))
			if (monsters):
				startx = 534
				for m in monsters:
					obj = m[0]
					objinfo = m[1]
					assert isinstance(objinfo, monster_info.MonsterInfo)
					assert isinstance(obj, toee.PyObjHandle)
					if (objinfo.activated > 1):
						print("already activated: {}".format(objinfo.activated))
						break
					alive = utils_npc.npc_is_alive(obj, 0)
					print("obj: {}, alive: {}".format(obj, alive))
					if (not alive): continue
					print("moving to: {}, 448".format(startx))
					obj.move(utils_obj.sec2loc(startx, 448))
					obj.rotation = const_toee.rotation_1100_oclock
					startx -= 2
					if (closest_pc_tuple):
						obj.attack(closest_pc_tuple[0])
		return

	def create_promter_at(self, loc, dialog_script_id, line_id, radar_radius_ft, method, new_name, rotation = None):
		npc = py06122_cormyr_prompter.create_promter_at(loc, dialog_script_id, line_id, radar_radius_ft, method, new_name)
		if (rotation):
			npc.rotation = rotation
		return npc

	def get_monster_prefix_default(self):
		return shattered_consts.SHATERRED_TEMPLE

	def get_map_default(self):
		return shattered_consts.MAP_ID_SHATERRED_TEMPLE

	def place_chests(self):
		#return
		# import utils_obj, const_proto_containers, math
		#T4
		#Ironbound Chest
		if (1):
			loc = utils_obj.sec2loc(494, 517)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_GENERIC, loc)
			chest.move(loc)

			chest.scripts[const_toee.sn_trap] = const_traps.TRAP_SCRIPT_CR4_GLYPH_OF_WARDING_BLAST
			if ("counter_set" in dir(chest.scripts)):
				chest.scripts.counter_set(const_toee.sn_trap, 0, const_traps.TRAP_SPEC_GLYPH_SDC28_DDC_28_CR4)

			nameid = utils_toee.make_custom_name("Ironbound Chest")
			if (nameid):
				chest.obj_set_int(const_toee.obj_f_description_correct, nameid)

			utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_RESTORATION, chest)
			utils_item.item_create_in_inventory(const_proto_items.PROTO_ARMOR_NECKLACE_SCARAB, chest) # 750 gp
			utils_item.item_money_create_in_inventory(chest, 20)

		#T6
		#Altar
		if (1):
			loc = utils_obj.sec2loc(467, 502)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_ALTAR, loc)
			chest.move(loc, 7, 12)

			utils_item.item_create_in_inventory(const_proto_items.PROTO_GENERIC_PEARL_BLACK, chest) # 500 gp

		#T7
		#Altar
		if (1):
			loc = utils_obj.sec2loc(421, 491)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_FOOTLOCKER, loc)
			chest.move(loc, 0, 0)
			chest.rotation = math.radians(45)

			utils_item.item_money_create_in_inventory(chest, 0, 200)

		#T9
		#Jewelry Box
		if (1):
			loc = utils_obj.sec2loc(442, 513)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_JEWELRY_BOX, loc)
			chest.move(loc, 0, 0)
			chest.rotation = math.radians(45)

			utils_item.item_money_create_in_inventory(chest, 0, 200)
			utils_locks.container_setup_dc(chest, 20, 0, 10, 5, utils_locks.BREAK_DC_CHEST_SMALL)

		#T16
		#Altar left
		if (1):
			loc = utils_obj.sec2loc(517,444)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_ALTAR, loc)
			chest.move(loc, 0, 0)
			chest.rotation = math.radians(90) # pointing east

			# Northwestern Altar: The crone is holding her right arm out with her palm up. Her eyes are closed. The bowl holds 25 pp.
			utils_item.item_money_create_in_inventory(chest, 25)
		#Altar top
		if (1):
			loc = utils_obj.sec2loc(507,444)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_ALTAR, loc)
			chest.move(loc, 0, 0)
			chest.rotation = math.radians(180) # pointing south

			# Northeastern Altar: The crone is holding her right arm out with her palm out and fingers curled in a clawing pose. Her 
			# fanged mouth is open. The bowl holds a gold necklace worth (400 gp).
			utils_item.item_money_create_in_inventory(chest, 0, 400)
		#Altar bottom 
		if (1):
			loc = utils_obj.sec2loc(517,456)
			chestt = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_ALTAR, loc)
			chestt.move(loc, 0, 0)
			chestt.rotation = math.radians(360) # pointing north

			chestt.scripts[const_toee.sn_trap] = const_traps.TRAP_SCRIPT_POISON_GAS_PRESSURIZED_UNGOL_DUST
			if ("counter_set" in dir(chestt.scripts)):
				chestt.scripts.counter_set(const_toee.sn_trap, 0, const_traps.TRAP_SPEC_POISON_GAS_SDC15_DDC_15_CR1)

		#Altar right
		if (1):
			loc = utils_obj.sec2loc(507,456)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_ALTAR, loc)
			chest.move(loc, 0, 0)
			chest.rotation = math.radians(270) # pointing west

			utils_item.item_create_in_inventory(const_proto_items.PROTO_GENERIC_PEARL_BLACK, chest) # 500 gp

		#T21
		if (1):
			loc = utils_obj.sec2loc(537,493)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_ALTAR, loc)
			chest.move(loc, 0, 0)
			chest.rotation = math.radians(90+45) # pointing north

			utils_item.item_create_in_inventory(const_proto_items.PROTO_GENERIC_PEARL_BLACK, chest) # 500 gp

		#T22
		if (1):
			loc = utils_obj.sec2loc(506,487)
			chest = toee.game.obj_create(const_proto_containers.PROTO_CONTAINER_CHEST_GIANT, loc)
			chest.move(loc, 8.485282, -14.1421356)
			chest.rotation = math.radians(45) # pointing bottom left

			nameid = utils_toee.make_custom_name("Sarcophagus")
			if (nameid):
				chest.obj_set_int(const_toee.obj_f_description_correct, nameid)

			utils_locks.container_setup_dc(chest, -30, 0, 120, 8, 30)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD_PLUS_1, chest)
			utils_item.item_create_in_inventory(shattered_consts.PROTO_ARMOR_SHIELD_OF_DRAGONRIDER, chest)
		return

	def place_demon_archs(self):
		#T10
		if (1):
			loc = utils_obj.sec2loc(435, 460)
			arch = toee.game.obj_create(shattered_consts.PROTO_DEMON_ARCH_10FT, loc)
			arch.move(loc, 0, 0)
			arch.rotation = 2.3561945

			arch.scripts[const_toee.sn_use] = shattered_consts.SHATERRED_TEMPLE_DAEMON_SCRIPT
			arch.scripts[const_toee.sn_trap] = const_traps.TRAP_SCRIPT_FIERY_DEMON_ARCH
			if ("counter_set" in dir(arch.scripts)):
				arch.scripts.counter_set(const_toee.sn_trap, 0, const_traps.TRAP_SPEC_FIRE_SDC16_DDC_16_CR3)

		#T14
		if (1):
			loc = utils_obj.sec2loc(478,457)
			arch = toee.game.obj_create(shattered_consts.PROTO_DEMON_ARCH_10FT, loc)
			arch.move(loc, 0, 0)
			arch.rotation = math.radians(180+45) #3.926991

			arch.scripts[const_toee.sn_use] = shattered_consts.SHATERRED_TEMPLE_DAEMON_SCRIPT
			arch.scripts[const_toee.sn_trap] = const_traps.TRAP_SCRIPT_FIERY_DEMON_ARCH
			if ("counter_set" in dir(arch.scripts)):
				arch.scripts.counter_set(const_toee.sn_trap, 0, const_traps.TRAP_SPEC_FIRE_SDC16_DDC_16_CR3)

		#T15
		if (1):
			loc = utils_obj.sec2loc(504,449)
			arch = toee.game.obj_create(shattered_consts.PROTO_DEMON_ARCH_10FT, loc)
			arch.move(loc, 0, 0)
			arch.rotation = math.radians(90+45) #2.3561945 poiting top-right

			arch.scripts[const_toee.sn_use] = shattered_consts.SHATERRED_TEMPLE_DAEMON_SCRIPT
			arch.scripts[const_toee.sn_trap] = const_traps.TRAP_SCRIPT_FIERY_DEMON_ARCH
			if ("counter_set" in dir(arch.scripts)):
				arch.scripts.counter_set(const_toee.sn_trap, 0, const_traps.TRAP_SPEC_FIRE_SDC16_DDC_16_CR3)

		#T22
		if (1): # to T23
			loc = utils_obj.sec2loc(522,503)
			arch = toee.game.obj_create(shattered_consts.PROTO_DEMON_ARCH_10FT, loc)
			arch.move(loc, 0, 0)
			arch.rotation = math.radians(90+45) #2.3561945 poiting top-right

			arch.scripts[const_toee.sn_use] = shattered_consts.SHATERRED_TEMPLE_DAEMON_SCRIPT
			arch.scripts[const_toee.sn_trap] = const_traps.TRAP_SCRIPT_FIERY_DEMON_ARCH
			if ("counter_set" in dir(arch.scripts)):
				arch.scripts.counter_set(const_toee.sn_trap, 0, const_traps.TRAP_SPEC_FIRE_SDC16_DDC_16_CR3)

		if (1): # to T25
			loc = utils_obj.sec2loc(514,508)
			arch = toee.game.obj_create(shattered_consts.PROTO_DEMON_ARCH_10FT, loc)
			arch.move(loc, 0, 0)
			arch.rotation = math.radians(180+45) #3.926991 poiting top-left

			arch.scripts[const_toee.sn_use] = shattered_consts.SHATERRED_TEMPLE_DAEMON_SCRIPT
			arch.scripts[const_toee.sn_trap] = const_traps.TRAP_SCRIPT_FIERY_DEMON_ARCH
			if ("counter_set" in dir(arch.scripts)):
				arch.scripts.counter_set(const_toee.sn_trap, 0, const_traps.TRAP_SPEC_FIRE_SDC16_DDC_16_CR3)
		return

	def critter_dying(self, attachee, triggerer):
		#debug.breakp("critter_dying")
		self.factions_existance_refresh()

		if (not toee.game.global_flags[shattered_consts.GLOBAL_FLAG_TEMPLE_COMPLETED]):
			spawn_left = 0
			if (self.factions_existance and (shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN in self.factions_existance)): 
				spawn_left = self.factions_existance[shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN][0]

			print("spawn_left: {}".format(spawn_left))
			if (spawn_left == 0):
				toee.game.global_flags[shattered_consts.GLOBAL_FLAG_TEMPLE_COMPLETED] = 1
				print("toee.game.global_flags[shattered_consts.GLOBAL_FLAG_TEMPLE_COMPLETED] = 1")

		self.check_sleep_status_update(1)
		return

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		super(CtrlShatteredTemple, self).monster_setup(npc, encounter_name, monster_code_name, monster_name, no_draw, no_kos, faction)
		npc.scripts[const_toee.sn_dying] = shattered_consts.SHATERRED_TEMPLE_DAEMON_SCRIPT
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
