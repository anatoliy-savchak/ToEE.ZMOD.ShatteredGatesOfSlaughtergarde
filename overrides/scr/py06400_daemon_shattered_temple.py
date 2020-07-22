import toee, debugg, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee
import ctrl_behaviour, py06122_cormyr_prompter, shattered_consts, py06211_shuttered_monster, const_proto_scrolls, py06401_shattered_temple_encounters, const_proto_wands, utils_npc

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debugg.breakp("san_first_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_TEMPLE): toee.RUN_DEFAULT
	for pc in toee.game.party:
		pc.condition_add("Inspect")
	ctrl = CtrlShatteredTemple.ensure(attachee)
	ctrl.place_encounters()
	return toee.RUN_DEFAULT

NAMEID_DOOR_T7 = 907

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	if (attachee.name == NAMEID_DOOR_T7):
		utils_obj.obj_scripts_clear(attachee)
		#utils_obj.obj_timed_destroy(obj, 1000)
		#toee.game.timevent_add(_door_used, (attachee, triggerer), 1000, 0) # 1000 = 1 second
		toee.game.timevent_add(_door_used_interrupt, (attachee, triggerer), 100, 1) # 1000 = 1 second
		for pc in toee.game.party:
			pc.anim_goal_interrupt()

		
		#return toee.SKIP_DEFAULT
		#attachee.portal_toggle_open()
	return toee.RUN_DEFAULT

def _door_used(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	loc = attachee.location
	attachee.destroy()
	for npc in toee.game.obj_list_vicinity(loc, toee.OLC_NPC):
		if (npc.proto == 14830):
			py06122_cormyr_prompter.promter_talk(npc, triggerer)
			break
	return 1

def _door_used_interrupt(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#attachee.portal_toggle_open()
	triggerer.anim_goal_use_object(attachee, 12, attachee.location, 1)
	toee.game.timevent_add(_door_used, (attachee, triggerer), 1000, 0) # 1000 = 1 second
	#for pc in toee.game.party:
	#	pc.anim_goal_interrupt()
	return 1

def cst():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(shattered_consts.SHATERRED_TEMPLE_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlShatteredTemple.get_name() in o.data):
		result = o.data[CtrlShatteredTemple.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlShatteredTemple(object):
	def __init__(self):
		self.encounters_placed = 0
		self.monsters = dict()
		self.m2 = list()
		self.id = None
		self.haertbeats_since_sleep_status_update = 0
		return

	def created(self, npc):
		self.id = npc.id
		npc.scripts[const_toee.sn_dialog] = 6400
		return

	@staticmethod
	def get_name():
		return "CtrlShatteredTemple"

	@classmethod
	def ensure(cls, npc):
		data = utils_storage.obj_storage(npc).data
		ctrl = None
		if (cls.get_name() in data):
			ctrl = data[cls.get_name()]
		else:
			ctrl = cls()
			ctrl.created(npc)
			utils_storage.obj_storage(npc).data[cls.get_name()] = ctrl
		return ctrl

	@classmethod
	def get_from_obj(cls, npc):
		data = utils_storage.obj_storage(npc).data
		if (cls.get_name() in data):
			return data[cls.get_name()]
		return None

	def place_encounters(self):
		if (self.encounters_placed): return
		self.encounters_placed = 1
		#debugg.breakp("place_encounters")

		self.monsters = dict()
		self.m2 = list()
		#self.destroy_all_npc()

		self.encounters_placed = 1
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
		self.print_monsters()

		# debug
		#wizard = toee.game.party[4]
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_COLOR_SPRAY, wizard)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_OBSCURING_MIST, wizard)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_INVISIBILITY, wizard)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_BLUR, wizard)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_GLITTERDUST, wizard)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_FIREBALL, wizard)
		#utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_MAGIC_MISSILES_1ST, wizard)
		#utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_ACID_SPLASH, wizard)
		#wizard.identify_all()
		#utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GLAIVE_MASTERWORK, toee.game.party[1])
		#self.remove_trap_doors()
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 436, 496)
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 442, 475)
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 452, 460) #t11
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 495, 454) #t15
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 495, 449) #t16
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 511, 450) #t17
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 515, 471) #t18
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 530, 449) #t19
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 533, 462) #t21
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 514, 474) #t22
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 515, 499) #t23
		utils_obj.scroll_to_leader()
		return

	def place_encounter_t1(self):
		self.create_promter_at(utils_obj.sec2loc(484, 475), 6400, 10, 15, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Tapestry Hall")

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
		self.create_promter_at(utils_obj.sec2loc(487, 492), 6400, 20, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Spring")

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
		self.create_promter_at(utils_obj.sec2loc(485, 510), 6400, 30, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Storage")

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
		p2 = self.create_promter_at(utils_obj.sec2loc(459, 479), 6400, 40, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Stable")
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

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
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

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
		self.create_promter_at(utils_obj.sec2loc(430, 493), 6400, 70, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Northern Quarters")

		fire_epicenter = utils_obj.sec2loc(437, 494)
		npc, ctrl = self.create_arcane_guard_at(utils_obj.sec2loc(428, 493), const_toee.rotation_0800_oclock, "t7", "aguard1", 2)
		if (ctrl):
			ctrl.fire_epicenter = fire_epicenter
		npc, ctrl = self.create_arcane_guard_at(utils_obj.sec2loc(424, 493), const_toee.rotation_0800_oclock, "t7", "aguard2", 3)
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

	def create_arcane_guard_at(self, npc_loc, rot, encounter, code_name, guard_ai_type = 0):
		npc, ctrl = py06401_shattered_temple_encounters.CtrlArcaneGuard.create_obj_and_class(npc_loc, 0)
		if (ctrl):
			ctrl.guard_ai_type = guard_ai_type
			ctrl.created(npc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
		return npc, ctrl

	def create_quaggoth_at(self, npc_loc, rot, encounter, code_name):
		npc, ctrl = py06401_shattered_temple_encounters.CtrlQuaggoth.create_obj_and_class(npc_loc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
		return npc

	def create_npc_at(self, npc_loc, ctrl_class, rot, encounter, code_name):
		npc, ctrl = ctrl_class.create_obj_and_class(npc_loc)
		x, y = utils_obj.loc2sec(npc.location)
		print("create_npc_at npc: {}, ctrl: {}, id: {}, coord: {},{}".format(npc, ctrl, npc.id, x, y))
		if (npc):
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
		return npc, ctrl

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		assert isinstance(npc, toee.PyObjHandle)
		if (not faction): faction = shattered_consts.FACTION_SLAUGHTERGARDE_LABORATORY
		if (faction and faction != -1):
			npc.faction_add(faction)
		#npc.npc_flag_set(toee.ONF_NO_ATTACK)
		if (no_kos):
			npc.npc_flag_unset(toee.ONF_KOS)
		if (no_draw):
			npc.object_flag_set(toee.OF_DONTDRAW)
		if (monster_name):
			nameid = utils_toee.make_custom_name(monster_name)
			if (nameid):
				npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
				npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		info = py06211_shuttered_monster.MonsterInfo()
		info.id = npc.id
		info.proto = npc.proto
		info.cr = utils_npc.npc_get_cr(npc)
		info.name = "{}_{}_{}".format(shattered_consts.SHATERRED_TEMPLE, encounter_name, monster_code_name)
		self.m2.append(info)
		self.monsters[info.name] = info
		return

	def get_monsterinfo(self, encounter_name, monster_code_name):
		key = "{}_{}_{}".format(shattered_consts.SHATERRED_TEMPLE, encounter_name, monster_code_name)
		if (key in self.monsters):
			info = self.monsters[key]
			assert isinstance(info, py06211_shuttered_monster.MonsterInfo)
			return info
		return None

	def reveal_monster(self, encounter_name, monster_code_name, no_error = 0):
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

	def activate_monster(self, encounter_name, monster_code_name, remove_no_attack = 1, remove_no_kos = 1, no_error = 0):
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
			assert isinstance(info, py06211_shuttered_monster.MonsterInfo)
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
		if (type(ctrl) is py06401_shattered_temple_encounters.CtrlGaranaach and toee.game.combat_turn == 1):
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
				debugg.breakp("problem")
			else:
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
					assert isinstance(objinfo, py06211_shuttered_monster.MonsterInfo)
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

	def destroy_all_npc(self):
		myself = toee.game.get_obj_by_id(self.id)
		for npc in toee.game.obj_list_range(myself.location, 200, toee.OLC_NPC):
			if (npc.id == self.id): continue
			npc.destroy()
		return
