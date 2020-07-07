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
		#if (self.encounters_placed): return
		#debugg.breakp("place_encounters")

		self.monsters = dict()
		self.m2 = list()
		self.destroy_all_npc()

		self.encounters_placed = 1
		#self.place_encounter_t1()
		#self.place_encounter_t2()
		#self.place_encounter_t3()
		#self.place_encounter_t4()
		#self.place_encounter_t5()
		#self.place_encounter_t6()
		#self.place_encounter_t7()
		#self.place_encounter_t8()
		#self.place_encounter_t9()
		#self.place_encounter_t10()
		#self.place_encounter_t11()
		#self.place_encounter_t12()
		#self.place_encounter_t13()
		#self.place_encounter_t14()
		#self.place_encounter_t15()
		self.place_encounter_t16()
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
		toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_TEMPLE, 495, 449) #t16
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
		print("create_npc_at npc: {}, ctrl: {}, id: {}".format(npc, ctrl, npc.id))
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
			if (npc):
				ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(npc)
				if (ctrl and ("revealing" in dir(ctrl))):
					ctrl.revealing(npc)
				npc.object_flag_unset(toee.OF_DONTDRAW)
				if (ctrl and ("revealed" in dir(ctrl))):
					ctrl.revealed(npc)
		if (not npc and not no_error):
			print("Monster {} {} not found!".format(encounter_name, monster_code_name))
			debugg.breakp("Monster not found")
		return

	def activate_monster(self, encounter_name, monster_code_name, remove_no_attack = 1, remove_no_kos = 1, no_error = 0):
		npc = None
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc):
				ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(npc)
				if (ctrl and ("activating" in dir(ctrl))):
					ctrl.activating(npc)
				if (remove_no_attack):
					npc.npc_flag_unset(toee.ONF_NO_ATTACK)
				if (remove_no_kos):
					npc.npc_flag_set(toee.ONF_KOS)
				if (ctrl and ("activated" in dir(ctrl))):
					ctrl.activated(npc)
		if (not npc and not no_error):
			print("Monster {} {} not found!".format(encounter_name, monster_code_name))
			debugg.breakp("Monster not found")
		return npc, info

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
		return

	def create_promter_at(self, loc, dialog_script_id, line_id, radar_radius_ft, method, new_name):
		npc = py06122_cormyr_prompter.create_promter_at(loc, dialog_script_id, line_id, radar_radius_ft, method, new_name)
		return npc

	def destroy_all_npc(self):
		myself = toee.game.get_obj_by_id(self.id)
		for npc in toee.game.obj_list_range(myself.location, 200, toee.OLC_NPC):
			if (npc.id == self.id): continue
			npc.destroy()
		return
