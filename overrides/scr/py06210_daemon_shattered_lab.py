import toee, debugg, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee
import py06122_cormyr_prompter, py06211_shuttered_monster, utils_sneak, utils_npc, const_proto_items, tpdp, const_proto_scrolls, py06213_hobgoblin_cleric, const_proto_rings, shattered_consts
import py00677FarSouthDoor, monster_info, ctrl_daemon

DEBUG_WRITE_MONSTERS_PATH = None #"d:\\temp\\monsters.txt"

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	#debugg.breakp("san_first_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_LAB): toee.RUN_DEFAULT
	ctrl = CtrlShatteredLab.ensure(attachee)
	ctrl.place_encounters()
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	leader = toee.game.leader
	lscripts = leader.scripts
	if (leader.map == shattered_consts.MAP_ID_SHATERRED_LAB):
		c = csl()
		if (c):
			c.check_sleep_status_update()
	return toee.RUN_DEFAULT

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)

	if (attachee.name == 1641): #{1641}{Shattered Lab Exit}
		csl().last_leave_shrs = toee.game.time.time_game_in_hours2(toee.game.time)
		total_seconds = py00677FarSouthDoor.distance_sumbertone_to_shattered_lab_sec()
		print("fade_and_teleport total_seconds: {}".format(total_seconds))
		toee.game.fade_and_teleport(total_seconds, 0, 0, 5122, 538, 510 ) #sumberton
	#else:
	#	attachee.object_flag_set(toee.OF_DONTDRAW)
	#debug.breakp("san_use")
	return toee.RUN_DEFAULT

def san_dying(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print("san_dying: {}".format(attachee.id))
	c = csl()
	if (c):
		c.critter_dying(attachee, triggerer)
	return toee.RUN_DEFAULT

def csl():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(shattered_consts.SHATERRED_LAB_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlShatteredLab.get_name() in o.data):
		result = o.data[CtrlShatteredLab.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlShatteredLab(object):
	def __init__(self):
		self.encounters_placed = 0
		self.monsters = dict()
		self.m2 = list()
		self.id = None
		self.haertbeats_since_sleep_status_update = -1
		self.first_entered_shrs = 0
		self.last_entered_shrs = 0
		self.last_leave_shrs = 0
		self.last_patrol_spawned_shrs = 0
		self.patrol_spawned_count = 0
		self.factions_existance = dict()
		return

	def created(self, npc):
		self.id = npc.id
		npc.scripts[const_toee.sn_dialog] = 6210
		npc.origin = shattered_consts.MAP_ID_SHATERRED_LAB
		nameid = utils_toee.make_custom_name("Daemon-{}".format(shattered_consts.SHATERRED_LAB))
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		return

	@staticmethod
	def get_name():
		return "CtrlShatteredLab"

	@classmethod
	def ensure(cls, npc):
		data = utils_storage.obj_storage(npc).data
		ctrl = None
		if (cls.get_name() in data):
			ctrl = data[cls.get_name()]
		else:
			ctrl = cls()
			utils_storage.obj_storage(npc).data[cls.get_name()] = ctrl
			ctrl_daemon.CtrlDaemon.set_daemon(npc.id, shattered_consts.MAP_ID_SHATERRED_LAB)
			ctrl.created(npc)
		return ctrl

	@classmethod
	def get_from_obj(cls, npc):
		data = utils_storage.obj_storage(npc).data
		if (cls.get_name() in data):
			return data[cls.get_name()]
		return None

	def place_encounters(self):
		print("place_encounters.encounters_placed == {}".format(self.encounters_placed))

		if (toee.game.quests[shattered_consts.QUEST_SPICY_CHICANERY].state == toee.qs_unknown):
			print("QUEST_SPICY_CHICANERY => qs_mentioned")
			toee.game.quests[shattered_consts.QUEST_SPICY_CHICANERY].state = toee.qs_mentioned

		this_entrance_time = toee.game.time.time_game_in_hours2(toee.game.time)
		print("this_entrance_time == {}".format(this_entrance_time))
		if (not self.encounters_placed):
			self.first_entered_shrs = this_entrance_time
		self.last_entered_shrs = this_entrance_time
		if (not self.last_leave_shrs):
			self.last_leave_shrs = this_entrance_time

		if (not self.encounters_placed and 1):
			#self.place_encounter_l1()
			self.place_encounter_l2()
			#self.place_encounter_l3()
			#self.place_encounter_l4()
			#self.place_encounter_l5()
			#self.place_encounter_l6()
			#self.place_encounter_l7()
			#self.place_encounter_l8()
			#self.place_encounter_l9()
			#self.place_encounter_l10()
			#self.place_encounter_l11()
			#self.place_encounter_l12()
			#self.place_encounter_l13()
			#self.place_encounter_l15()
			#self.place_encounter_l16()
			#self.place_encounter_l17()
			#self.place_encounter_l18()

		if (not self.encounters_placed and 1):
			self.place_chests()

		self.encounters_placed += 1
		utils_npc.pc_turn_all(const_toee.rotation_0400_oclock)
		#self.print_monsters()
		self.factions_existance_refresh()
		# debug
		self.remove_trap_doors()
		#toee.game.fade_and_teleport(0, 0, 0, 5121, 475, 510)
		#toee.game.fade_and_teleport(0, 0, 0, 5121, 466, 476) # Balcony
		#toee.game.fade_and_teleport(0, 0, 0, 5121, 508, 511) # Library
		#toee.game.fade_and_teleport(0, 0, 0, 5121, 461, 449) # Maug
		utils_obj.scroll_to_leader()

		self.check_sleep_status_update(1)
		self.check_entrance_patrol()
		return

	def place_encounter_patrol(self, near_pc):
		self.patrol_spawned_count += 1
		self.last_patrol_spawned_shrs = toee.game.time.time_game_in_hours2(toee.game.time)
		print("place_encounter_patrol {}".format(self.patrol_spawned_count))
		loc1 = utils_obj.sec2loc(519, 467)
		loc2 = utils_obj.sec2loc(517, 467)
		loc3 = utils_obj.sec2loc(519, 470)
		if (near_pc):
			loc1 = toee.game.leader.location - 6
			loc2 = loc1 - 6
			loc4 = loc2 - 6

		self.create_goblin_scrounger_at(loc1, const_toee.rotation_1100_oclock, "l_patrol", "goblin1", 0, 1)
		self.create_goblin_scrounger_at(loc2, const_toee.rotation_1100_oclock, "l_patrol", "goblin2", 0, 1)
		self.create_goblin_scrounger_at(loc3, const_toee.rotation_1100_oclock, "l_patrol", "goblin3", 0, 1)
		return

	def place_encounter_l1(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(518, 461), 6210, 1, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Treacherous Tunnel")
		return

	def place_encounter_l2(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(513, 473), 6210, 20, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Lab Entrance")

		self.create_hobgoblin_impaler_at(utils_obj.sec2loc(504, 469), const_toee.rotation_0800_oclock, "l2", "hobgoblin1", 1)
		self.create_hobgoblin_impaler_at(utils_obj.sec2loc(505, 477), const_toee.rotation_0800_oclock, "l2", "hobgoblin2", 1)
		self.create_hobgoblin_archer_at(utils_obj.sec2loc(510, 465), const_toee.rotation_0500_oclock, "l2", "hobgoblin_archer", 1)
		return

	def create_hobgoblin_impaler_at(self, npc_loc, rot, encounter, code_name, no_draw):
		npc = toee.game.obj_create(14188, npc_loc)
		if (npc):
			#utils_obj.obj_scripts_clear(npc)
			#utils_item.item_clear_all(npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_PICK_HEAVY, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_HALF_PLATE, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_WOODEN_LARGE, npc)
			npc.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
			npc.item_wield_best_all()
			npc.obj_set_int(toee.obj_f_npc_challenge_rating, -1)
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, no_draw)
			#self.monster_setup(npc, encounter, code_name, code_name, no_draw)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
		return


	def create_hobgoblin_archer_at(self, npc_loc, rot, encounter, code_name, no_draw):
		npc = toee.game.obj_create(14189, npc_loc)
		if (npc):
			#utils_obj.obj_scripts_clear(npc)
			#utils_item.item_clear_all(npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SHORTBOW, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_BREASTPLATE, npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_ARROW_QUIVER, npc)
			npc.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
			npc.item_wield_best_all()
			npc.obj_set_int(toee.obj_f_npc_challenge_rating, -1)
			npc.condition_add_with_args("Hide_Ex", 0, 0)
			npc.move(npc_loc)
			npc.rotation = const_toee.rotation_0500_oclock
			self.monster_setup(npc, "l2", "hobgoblin_archer", None)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			ctrl.option_stay = 1
			hidden = utils_sneak.npc_make_hide(npc, 1)
			if (hidden):
				ctrl.option_starts_combat_sneaked = 1
		return

	def place_encounter_l3(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(495, 473), 6210, 30, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Gaol").rotation = const_toee.rotation_0800_oclock

		npc = self.create_goblin_scrounger_at(utils_obj.sec2loc(498, 468), const_toee.rotation_0500_oclock, "l3", "goblin1", 0)
		if (npc):
			key = utils_item.item_create_in_inventory(10001, npc)
			if (key):
				key.obj_set_int(toee.obj_f_key_key_id, 32)
		self.create_goblin_scrounger_at(utils_obj.sec2loc(498, 478), const_toee.rotation_1000_oclock, "l3", "goblin2", 0)
		self.create_goblin_scrounger_at(utils_obj.sec2loc(490, 477), const_toee.rotation_0800_oclock, "l3", "goblin3", 0)
		return

	def place_encounter_l4(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(484, 472), 6210, 40, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Skythe Room")
		return

	def place_encounter_l5(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(493, 456), 6210, 50, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Barracks")

		self.create_goblin_trooper_at(utils_obj.sec2loc(496, 447), const_toee.rotation_0400_oclock, "l5", "trooper1", 1, 1)
		self.create_goblin_trooper_at(utils_obj.sec2loc(492, 444), const_toee.rotation_0400_oclock, "l5", "trooper2", 1, 1)
		return

	def create_goblin_trooper_at(self, npc_loc, rot, encounter, code_name, no_draw, no_kos):
		PROTO_NPC_GOBLIN_TROOPER = 14190
		npc = toee.game.obj_create(PROTO_NPC_GOBLIN_TROOPER, npc_loc)
		if (npc):
			#utils_obj.obj_scripts_clear(npc)
			utils_item.item_clear_all(npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_BATTLEAXE, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_HALF_PLATE, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_STEEL_SMALL, npc)
			npc.item_wield_best_all()
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, no_draw, no_kos)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			utils_npc.npc_skill_ensure(npc, toee.skill_spot, 4)
		return npc

	def place_encounter_l6(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(477, 478), 6210, 60, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Operating Room")

		self.create_hobgoblin_impaler_at(utils_obj.sec2loc(479, 482), const_toee.rotation_1100_oclock, "l6", "hobgoblin1", 0)
		self.create_hobgoblin_impaler_at(utils_obj.sec2loc(475, 482), const_toee.rotation_0800_oclock, "l6", "hobgoblin2", 0)
		return

	def create_goblin_scrounger_at(self, npc_loc, rot, encounter, code_name, is_napping, activated = None):
		PROTO_NPC_GOBLIN_SCROUNGER = 14191
		npc = toee.game.obj_create(PROTO_NPC_GOBLIN_SCROUNGER, npc_loc)
		if (npc):
			#utils_obj.obj_scripts_clear(npc)
			utils_item.item_clear_all(npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SHORTSWORD, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_JAVELIN, npc)
			npc.item_wield_best_all()
			npc.move(npc_loc)
			npc.rotation = rot
			if (is_napping):
				npc.condition_add_with_args("Napping", 1, 0)

			if (is_napping or activated):
				self.monster_setup(npc, encounter, code_name, None, 0, 0)
			else:
				self.monster_setup(npc, encounter, code_name, None)

			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			ctrl.option_first_javelin = 1
			utils_npc.npc_skill_ensure(npc, toee.skill_spot, 2)
			utils_npc.npc_skill_ensure(npc, toee.skill_listen, 2)
			utils_npc.npc_skill_ensure(npc, toee.skill_hide, 5)
			npc.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
			npc.condition_add_with_args("Hide_Ex", 0, 0)
		return npc

	def place_encounter_l7(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(465, 478), 6210, 70, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_FLOAT_DIALOG_LINE, "Balcony")

		npc = self.create_goblin_scrounger_at(utils_obj.sec2loc(468, 479), const_toee.rotation_1100_oclock, "l7", "goblin1", 1)
		key = utils_item.item_create_in_inventory(10001, npc)
		if (key):
			key.obj_set_int(toee.obj_f_key_key_id, 31)
		self.create_goblin_scrounger_at(utils_obj.sec2loc(466, 474), const_toee.rotation_1100_oclock, "l7", "goblin2", 1)
		self.create_goblin_scrounger_at(utils_obj.sec2loc(463, 477), const_toee.rotation_1100_oclock, "l7", "goblin3", 1)
		return

	def place_encounter_l8(self):
		p1 = py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(457, 481), 6210, 80, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Howler Trap")
		p1.rotation = const_toee.rotation_0600_oclock
		p2 = py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(454, 458), 6210, 80, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Howler Trap")
		p2.rotation = const_toee.rotation_1100_oclock
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

		PROTO_NPC_HOWLER = 14893
		npc_loc = utils_obj.sec2loc(459, 466)
		npc = toee.game.obj_create(PROTO_NPC_HOWLER, npc_loc)
		if (npc):
			npc.move(npc_loc)
			npc.condition_add_with_args("Quills_Ex", 1, 0)
			npc.rotation = const_toee.rotation_0600_oclock
			self.monster_setup(npc, "l8", "howler", None, 1, 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			npc.npc_flag_set(toee.ONF_NO_ATTACK)
		return

	def place_encounter_l9(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(491, 437), 6210, 90, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_FLOAT_DIALOG_LINE, "Rift")

		self.create_dire_rat_at(utils_obj.sec2loc(473, 438), const_toee.rotation_0200_oclock, "l9", "dire_rat_1")
		self.create_dire_rat_at(utils_obj.sec2loc(475, 439), const_toee.rotation_0200_oclock, "l9", "dire_rat_2")
		self.create_dire_rat_at(utils_obj.sec2loc(477, 440), const_toee.rotation_0200_oclock, "l9", "dire_rat_3")
		return

	def place_encounter_l10(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(507, 436), 6210, 100, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Midden Heap")

		PROTO_NPC_ANKHEG = 14894
		npc_loc = utils_obj.sec2loc(514, 443)
		npc = toee.game.obj_create(PROTO_NPC_ANKHEG, npc_loc)
		if (npc):
			npc.move(npc_loc)
			#dice_packed = toee.dice_new("1d4").dice_packed()
			#print("PROTO_NPC_ANKHEG dice_packed: {}".format(dice_packed))
			dice_packed = 513
			npc.condition_add_with_args("Monster Bonus Damage", toee.D20DT_ACID, dice_packed)
			npc.rotation = const_toee.rotation_0600_oclock
			self.monster_setup(npc, "l10", "ankheg", None, 1, 1, shattered_consts.FACTION_WILDERNESS_HOSTILE)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
		return

	def place_encounter_l11(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(464, 438), 6210, 110, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Mirror Hall")

		self.create_goblin_trooper_at(utils_obj.sec2loc(462, 434), const_toee.rotation_0800_oclock, "l11", "trooper1", 1, 1)
		npc = self.create_goblin_trooper_at(utils_obj.sec2loc(459, 438), const_toee.rotation_0400_oclock, "l11", "trooper2", 1, 1)
		key = utils_item.item_create_in_inventory(10001, npc)
		if (key):
			key.obj_set_int(toee.obj_f_key_key_id, 33)

		return

	def place_encounter_l12(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(462, 445), 6210, 120, 15, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_FLOAT_DIALOG_LINE, "Summoning Pit")

		PROTO_NPC_MAUG = 14895
		npc_loc = utils_obj.sec2loc(461, 451)
		npc = toee.game.obj_create(PROTO_NPC_MAUG, npc_loc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = const_toee.rotation_0900_oclock
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD_MASTERWORK, npc, 2)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE_MASTERWORK, npc)
			self.monster_setup(npc, "l12", "maug", None, 0, 1, shattered_consts.FACTION_CELESTIAL_ARMY)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
		return

	def place_encounter_l13(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(502, 499), 6210, 130, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Lizard Lair")

		PROTO_NPC_LIZARD_MONITOR = 14896
		npc_loc = utils_obj.sec2loc(504, 493)
		npc = toee.game.obj_create(PROTO_NPC_LIZARD_MONITOR, npc_loc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = const_toee.rotation_0500_oclock
			info = self.monster_setup(npc, "l13", "lizard", None, 0, 1, shattered_consts.FACTION_WILDERNESS_HOSTILE)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
		return

	def place_encounter_l15(self):
		p1 = py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(508, 510), 6210, 150, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Library")
		p2 = py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(502, 513), 6210, 150, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Library")
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

		PROTO_NPC_GOBLIN_UNDERBOSS = 14192
		npc_loc = utils_obj.sec2loc(508, 514)
		npc = toee.game.obj_create(PROTO_NPC_GOBLIN_UNDERBOSS, npc_loc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = const_toee.rotation_1100_oclock
			item = utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT_MASTERWORK, npc)
			item = utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_STEEL_SMALL, npc)
			npc.item_wield(item, toee.item_wear_shield)
			item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_SCIMITAR_MASTERWORK, npc)
			npc.item_wield(item, toee.item_wear_weapon_primary)
			self.monster_setup(npc, "l15", "goblin_underboss", None, 1, 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)

		PROTO_NPC_HYENA = 14193
		npc_loc = utils_obj.sec2loc(508, 512)
		npc = toee.game.obj_create(PROTO_NPC_HYENA, npc_loc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = const_toee.rotation_1100_oclock
			self.monster_setup(npc, "l15", "hyena", None, 1, 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
		return

	def place_encounter_l16(self):
		p1 = py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(480, 509), 6210, 160, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shrine")
		p2 = py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(467, 509), 6210, 160, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shrine")
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

		self.create_hobgoblin_skeleton_at(utils_obj.sec2loc(476, 511), const_toee.rotation_1100_oclock, "l16", "skeleton1")
		self.create_hobgoblin_skeleton_at(utils_obj.sec2loc(474, 510), const_toee.rotation_1100_oclock, "l16", "skeleton2")
		self.create_hobgoblin_skeleton_at(utils_obj.sec2loc(472, 511), const_toee.rotation_0100_oclock, "l16", "skeleton3")

		npc = py06213_hobgoblin_cleric.CtrlHobgoblinCleric.create_obj(utils_obj.sec2loc(474, 513))
		npc.rotation = const_toee.rotation_1100_oclock
		self.monster_setup(npc, "l16", "cleric", None, 1, 1)
		return

	def place_encounter_l17(self):
		p1 = py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(461, 510), 6210, 170, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shattered Gate")
		p2 = py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(459, 498), 6210, 170, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Shattered Gate")
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

		self.create_hobgoblin_zombie_at(utils_obj.sec2loc(458, 501), const_toee.rotation_1100_oclock, "l17", "zombie1")
		self.create_hobgoblin_zombie_at(utils_obj.sec2loc(456, 499), const_toee.rotation_1100_oclock, "l17", "zombie2")
		self.create_hobgoblin_zombie_at(utils_obj.sec2loc(457, 507), const_toee.rotation_0600_oclock, "l17", "zombie3")
		self.create_hobgoblin_zombie_at(utils_obj.sec2loc(455, 505), const_toee.rotation_0600_oclock, "l17", "zombie4")
		return

	def place_encounter_l18(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(474, 501), 6210, 180, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Emissary's Room")

		self.create_dark_creeper_at(utils_obj.sec2loc(472, 500), const_toee.rotation_0500_oclock, "l18", "creeper1")
		self.create_dark_creeper_at(utils_obj.sec2loc(474, 497), const_toee.rotation_0500_oclock, "l18", "creeper2")
		return

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		assert isinstance(npc, toee.PyObjHandle)
		if (not faction): faction = shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN
		if (faction and faction != -1):
			npc.faction_add(faction)
		#npc.npc_flag_set(toee.ONF_NO_ATTACK)
		if (no_kos):
			npc.npc_flag_unset(toee.ONF_KOS)
		if (no_draw):
			npc.object_flag_set(toee.OF_DONTDRAW)
			#npc.object_flag_set(toee.OF_OFF)
		if (monster_name):
			nameid = utils_toee.make_custom_name(monster_name)
			if (nameid):
				npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
				npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		info = monster_info.MonsterInfo()
		info.id = npc.id
		info.proto = npc.proto
		info.cr = utils_npc.npc_get_cr(npc)
		info.name = "{}_{}_{}".format(shattered_consts.SHATERRED_LAB, encounter_name, monster_code_name)
		self.m2.append(info)
		self.monsters[info.name] = info
		npc.scripts[const_toee.sn_dying] = shattered_consts.SHATERRED_LAB_DAEMON_SCRIPT
		npc.origin = shattered_consts.MAP_ID_SHATERRED_LAB
		return info

	def create_dire_rat_at(self, npc_loc, rot, encounter, code_name):
		PROTO_NPC_DIRE_RAT = 14765
		npc = toee.game.obj_create(PROTO_NPC_DIRE_RAT, npc_loc)
		if (npc):
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 0, 0)
		return npc
	
	def create_hobgoblin_skeleton_at(self, npc_loc, rot, encounter, code_name):
		PROTO_NPC_SKELETON_HOBGOBLIN = 14194
		npc = toee.game.obj_create(PROTO_NPC_SKELETON_HOBGOBLIN, npc_loc)
		if (npc):
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT, npc)
			npc.item_wield_best_all()
			item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SPEAR, npc)
			npc.item_wield(item, toee.item_wear_weapon_primary)
			item = utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_STEEL_SMALL, npc)
			npc.item_wield(item, toee.item_wear_shield)
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
		return npc

	def create_hobgoblin_zombie_at(self, npc_loc, rot, encounter, code_name):
		PROTO_NPC_ZOMBIE_HOBGOBLIN = 14898
		npc = toee.game.obj_create(PROTO_NPC_ZOMBIE_HOBGOBLIN, npc_loc)
		if (npc):
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
			item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_BATTLEAXE, npc)
			npc.item_wield_best_all()
			#npc.item_wield(item, toee.item_wear_weapon_primary)
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
		return npc

	def create_dark_creeper_at(self, npc_loc, rot, encounter, code_name):
		PROTO_NPC_DARK_CREEPER = 14897
		npc = toee.game.obj_create(PROTO_NPC_DARK_CREEPER, npc_loc)
		if (npc):
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_LEATHER_ARMOR_BLACK, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_CLOAK_BLACK, npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_DAGGER, npc)
			#utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_DAGGER_THROWING, npc, 5)
			utils_item.item_create_in_inventory(const_proto_rings.PROTO_RING_PLAIN_COPPER, npc)
			npc.item_wield_best_all()
			npc.move(npc_loc)
			npc.rotation = rot
			npc.critter_flag_set(toee.OCF_MOVING_SILENTLY)
			npc.condition_add_with_args("Hide_Ex", 0, 0)
			self.monster_setup(npc, encounter, code_name, None, 1, 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			#ctrl.option_5fs_prefer = 1
		return npc

	def print_monsters2(self):
		f = None
		if (DEBUG_WRITE_MONSTERS_PATH):
			f = open(DEBUG_WRITE_MONSTERS_PATH, "w")
		for key, value in self.monsters.items():
			assert isinstance(value, monster_info.MonsterInfo)
			#print("{}={}".format(key, value.id))
			obj = toee.game.get_obj_by_id(value.id)
			if (obj):
				#s = "{}\t{}".format(obj.obj_get_int(toee.obj_f_npc_challenge_rating), obj.description)
				s = "{} = {}".format(key, obj.description)
				print(s)
				#print("{}={}".format(key, value.id))
				if (f):
					f.write(s + "\n")
		if (f):
			f.close()
		return

	def get_monsterinfo(self, encounter_name, monster_code_name):
		key = "{}_{}_{}".format(shattered_consts.SHATERRED_LAB, encounter_name, monster_code_name)
		if (key in self.monsters):
			info = self.monsters[key]
			assert isinstance(info, monster_info.MonsterInfo)
			return info
		return None

	def reveal_monster(self, encounter_name, monster_code_name):
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc):
				npc.object_flag_unset(toee.OF_DONTDRAW)
				#npc.object_flag_unset(toee.OF_OFF)
		return

	def display_encounter_l2(self):
		self.reveal_monster("l2", "hobgoblin1")
		self.reveal_monster("l2", "hobgoblin2")
		self.reveal_monster("l2", "hobgoblin_archer")
		return

	def display_encounter_l5(self):
		self.reveal_monster("l5", "trooper1")
		self.reveal_monster("l5", "trooper2")
		return
	
	def display_encounter_l10(self):
		self.reveal_monster("l10", "ankheg")
		return

	def get_monster_info_npc(self, encounter_name, monster_code_name):
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			return npc, info
		return None

	def activate_monster(self, encounter_name, monster_code_name):
		npc = None
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc):
				npc.npc_flag_unset(toee.ONF_NO_ATTACK)
				npc.npc_flag_set(toee.ONF_KOS)
		if (not npc):
			print("Monster {} {} not found!".format(encounter_name, monster_code_name))
			debugg.breakp("Monster not found")
		return npc, info

	def activate_encounter_l2(self):
		self.activate_monster("l2", "hobgoblin1")
		self.activate_monster("l2", "hobgoblin2")
		self.activate_monster("l2", "hobgoblin_archer")
		return

	def display_encounter_l3(self):
		self.reveal_monster("l3", "goblin1")
		self.reveal_monster("l3", "goblin2")
		self.reveal_monster("l3", "goblin3")
		return

	def display_encounter_l8(self):
		self.reveal_monster("l8", "howler")
		return

	def display_encounter_l11(self):
		self.reveal_monster("l11", "trooper1")
		self.reveal_monster("l11", "trooper2")
		return

	def display_encounter_l13(self):
		self.reveal_monster("l13", "lizard")
		return

	def display_encounter_l15(self):
		self.reveal_monster("l15", "goblin_underboss")
		self.reveal_monster("l15", "hyena")
		return

	def display_encounter_l16(self):
		self.reveal_monster("l16", "skeleton1")
		self.reveal_monster("l16", "skeleton2")
		self.reveal_monster("l16", "skeleton3")
		self.reveal_monster("l16", "cleric")
		return

	def display_encounter_l17(self):
		self.reveal_monster("l17", "zombie1")
		self.reveal_monster("l17", "zombie2")
		self.reveal_monster("l17", "zombie3")
		self.reveal_monster("l17", "zombie4")
		return

	def display_encounter_l18(self):
		self.reveal_monster("l18", "creeper1")
		self.reveal_monster("l18", "creeper2")
		return

	def activate_encounter_l3(self):
		#debugg.breakp("activate_encounter_l3")
		npc, info = self.activate_monster("l3", "goblin1")
		if (npc):
			hidden = utils_sneak.npc_make_hide(npc, 1)
			if (hidden):
				ctrl = py06211_shuttered_monster.CtrlMonster.get_from_obj(npc)
				if (ctrl):
					ctrl.option_starts_combat_sneaked = 1
		npc, info = self.activate_monster("l3", "goblin2")
		if (npc):
			hidden = utils_sneak.npc_make_hide(npc, 1)
			if (hidden):
				ctrl = py06211_shuttered_monster.CtrlMonster.get_from_obj(npc)
				if (ctrl):
					ctrl.option_starts_combat_sneaked = 1
		npc, info = self.activate_monster("l3", "goblin3")
		if (npc):
			hidden = utils_sneak.npc_make_hide(npc, 1)
			if (hidden):
				ctrl = py06211_shuttered_monster.CtrlMonster.get_from_obj(npc)
				if (ctrl):
					ctrl.option_starts_combat_sneaked = 1
		return

	def activate_encounter_l5(self):
		self.activate_monster("l5", "trooper1")
		self.activate_monster("l5", "trooper2")
		return

	def activate_encounter_l6(self):
		self.activate_monster("l6", "hobgoblin1")
		self.activate_monster("l6", "hobgoblin2")
		return

	def activate_encounter_l8(self):
		self.activate_monster("l8", "howler")
		return

	def activate_encounter_l10(self):
		self.activate_monster("l10", "ankheg")
		return

	def activate_encounter_l11(self):
		self.activate_monster("l11", "trooper1")
		self.activate_monster("l11", "trooper2")
		return

	def activate_encounter_l13(self):
		self.activate_monster("l13", "lizard")
		return

	def activate_encounter_l15(self):
		self.activate_monster("l15", "goblin_underboss")
		self.activate_monster("l15", "hyena")
		return

	def activate_encounter_l16(self):
		self.activate_monster("l16", "skeleton1")
		self.activate_monster("l16", "skeleton2")
		self.activate_monster("l16", "skeleton3")
		self.activate_monster("l16", "cleric")
		return

	def activate_encounter_l17(self):
		self.activate_monster("l17", "zombie1")
		self.activate_monster("l17", "zombie2")
		self.activate_monster("l17", "zombie3")
		self.activate_monster("l17", "zombie4")
		return

	def activate_encounter_l18(self):
		self.activate_monster("l18", "creeper1")
		self.activate_monster("l18", "creeper2")
		return

	def remove_trap_doors(self):
		for obj in toee.game.obj_list_range(toee.game.party[0].location, 200, toee.OLC_PORTAL):
			assert isinstance(obj, toee.PyObjHandle)
			no = obj.obj_get_int(toee.obj_f_hp_pts) 
			if ( not (no == 61 or no == 62)): continue
			utils_obj.obj_timed_destroy(obj, 1000, 1)
		return

	def place_chests(self):
		# fill static chests
		for obj in toee.game.obj_list_range(toee.game.party[0].location, 200, toee.OLC_CONTAINER):
			assert isinstance(obj, toee.PyObjHandle)
			no = obj.obj_get_int(toee.obj_f_hp_pts) 
			nameid = obj.name
			if (nameid == 1301):
				obj.container_flag_set(toee.OCOF_LOCKED)
				obj.obj_set_int(toee.obj_f_container_lock_dc, 15) 
				obj.obj_set_int(toee.obj_f_container_key_id, 31)
				obj.obj_set_int(toee.obj_f_container_pad_i_1, 17) # Break DC
				obj.obj_set_int(toee.obj_f_secretdoor_dc, 17) # Break DC 2
				obj.obj_set_int(toee.obj_f_hp_pts, 20) # Smash HP
				obj.obj_set_int(toee.obj_f_hp_adj, 5) # Smash Hardeness
				utils_item.item_create_in_inventory(const_proto_items.PROTO_GENERIC_JASPER_BLUE, obj) # Originally ivory figurine
			elif (nameid == 1302):
				obj.container_flag_set(toee.OCOF_LOCKED)
				obj.obj_set_int(toee.obj_f_container_lock_dc, 15) 
				obj.obj_set_int(toee.obj_f_container_key_id, 32)
				obj.obj_set_int(toee.obj_f_container_pad_i_1, 17) # Break DC
				obj.obj_set_int(toee.obj_f_secretdoor_dc, 17) # Break DC 2
				obj.obj_set_int(toee.obj_f_hp_pts, 20) # Smash HP
				obj.obj_set_int(toee.obj_f_hp_adj, 5) # Smash Hardeness
				utils_item.item_create_in_inventory(const_proto_items.PROTO_GENERIC_PEARL_WHITE, obj) # Originally opal earrings
				utils_item.item_money_create_in_inventory(obj, 0, 12)
			elif (nameid == 1303):
				obj.container_flag_set(toee.OCOF_LOCKED)
				obj.obj_set_int(toee.obj_f_container_lock_dc, 15) 
				obj.obj_set_int(toee.obj_f_container_key_id, 33)
				obj.obj_set_int(toee.obj_f_container_pad_i_1, 17) # Break DC
				obj.obj_set_int(toee.obj_f_secretdoor_dc, 17) # Break DC 2
				obj.obj_set_int(toee.obj_f_hp_pts, 20) # Smash HP
				obj.obj_set_int(toee.obj_f_hp_adj, 5) # Smash Hardeness
				utils_item.item_money_create_in_inventory(obj, 0, 350) # Originally porcelain plate
			elif (nameid == 1304):
				obj.container_flag_set(toee.OCOF_LOCKED)
				obj.obj_set_int(toee.obj_f_container_lock_dc, 15) 
				obj.obj_set_int(toee.obj_f_container_pad_i_1, 17) # Break DC
				obj.obj_set_int(toee.obj_f_secretdoor_dc, 17) # Break DC 2
				obj.obj_set_int(toee.obj_f_hp_pts, 20) # Smash HP
				obj.obj_set_int(toee.obj_f_hp_adj, 5) # Smash Hardeness
				utils_item.item_money_create_in_inventory(obj, 0, 33)
			elif (no == 151):
				obj.obj_set_int(toee.obj_f_container_pad_i_1, 17) # Break DC
				utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SHORTBOW_MASTERWORK, obj)
				utils_item.item_create_in_inventory_mass(obj \
					, [const_proto_scrolls.PROTO_SCROLL_OF_BURNING_HANDS \
					, const_proto_scrolls.PROTO_SCROLL_OF_REDUCE_PERSON \
					, const_proto_scrolls.PROTO_SCROLL_OF_CHILL_TOUCH \
					, const_proto_scrolls.PROTO_SCROLL_OF_ENDURE_ELEMENTS \
					, const_proto_scrolls.PROTO_SCROLL_OF_MAGIC_WEAPON \
					, const_proto_scrolls.PROTO_SCROLL_OF_PROTECTION_FROM_GOOD \
					, const_proto_scrolls.PROTO_SCROLL_OF_PROTECTION_FROM_LAW \
					, const_proto_scrolls.PROTO_SCROLL_OF_RAY_OF_ENFEEBLEMENT \
					, const_proto_scrolls.PROTO_SCROLL_OF_SUMMON_MONSTER_I \
					, const_proto_scrolls.PROTO_SCROLL_OF_CHARM_PERSON])

				utils_item.item_create_in_inventory(shattered_consts.PROTO_QUEST_ITEM_BARREL_OF_SPICE, obj)
				#item.scripts[const_toee.sn_insert_item] = shattered_consts.SHATERRED_LAB_DAEMON_SCRIPT
				#item.scripts[const_toee.sn_remove_item] = shattered_consts.SHATERRED_LAB_DAEMON_SCRIPT
		return

	def can_sleep(self):

		return toee.SLEEP_DANGEROUS

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

	def kill_monsters(self):
		sm = 0.0
		killer = toee.game.leader
		for info in self.m2:
			assert isinstance(info, monster_info.MonsterInfo)
			npc = toee.game.get_obj_by_id(info.id)
			if (not npc): continue
			villian = npc.faction_has(shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN)
			if (not villian): continue
			if (not sm):
				sm = utils_item.acquire_sell_modifier_once()
			print("Killing {}, {}".format(info.name, npc))
			utils_item.autosell(sm, utils_item.items_get(npc, 1))
			npc.critter_kill_by_effect(killer)
		return

	def check_entrance_patrol(self):
		threshhold_hours_passed = 4*24 + 16 + 1
		left_for = self.last_entered_shrs - self.last_leave_shrs
		print("check_entrance_patrol left_for: {}, last_leave_shrs: {}, last_entered_shrs: {}".format(left_for, self.last_leave_shrs, self.last_entered_shrs))
		if (left_for < threshhold_hours_passed): return 0

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
		self.factions_existance = monster_info.MonsterInfo.get_factions_existance(self.m2)
		return

	def critter_dying(self, attachee, triggerer):
		self.factions_existance_refresh()
		return

	def check_sleep_status_update(self, force = 0):
		self.haertbeats_since_sleep_status_update +=1
		if (force or self.haertbeats_since_sleep_status_update > 5):
			self.haertbeats_since_sleep_status_update = 0
			toee.game.sleep_status_update()
		return

	# Sleep interface
	def can_sleep(self):
		for npc in toee.game.obj_list_vicinity(toee.game.leader.location, toee.OLC_NPC):
			if (utils_npc.npc_is_alive(npc, 1) and (npc.faction_has(shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN) or npc.faction_has(shattered_consts.FACTION_WILDERNESS_HOSTILE))): 
				return toee.SLEEP_IMPOSSIBLE

		if (toee.game.leader.distance_to(utils_obj.sec2loc(484, 436)) <= 40):
			return toee.SLEEP_SAFE

		spawn_left = 0
		if (self.factions_existance and (shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN in self.factions_existance)): 
			spawn_left = self.factions_existance[shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN][0]

		if (spawn_left):
			return toee.SLEEP_DANGEROUS

		return toee.SLEEP_SAFE

	# Sleep interface
	def encounter_exists(self, setup, encounter):
		assert isinstance(setup, toee.PyRandomEncounterSetup)
		assert isinstance(encounter, toee.PyRandomEncounter)

		will_not_happen = toee.game.random_range(0, 9)
		if (will_not_happen): return 0

		if (self.last_patrol_spawned_shrs):
			current = toee.game.time.time_game_in_hours2(toee.game.time)
			past_since = current - self.last_patrol_spawned_shrs
			if (past_since < 20): return 0

		encounter.id = 6210
		return 1

	# Sleep interface
	def encounter_create(self, encounter):
		assert isinstance(encounter, toee.PyRandomEncounter)
		if (encounter.id != 6210): return
		self.place_encounter_patrol(1)
		return

	def storage_skip_load(self, key, val):
		if (key == "m2"): return 1
		return 0

	def storage_data_loaded(self):
		self.m2 = list()
		if (self.monsters):
			for val in self.monsters.itervalues():
				if (val and not val in self.m2):
					self.m2.append(val)
		return

	def storage_data_loaded_all(self):
		print("storage_data_loaded_all map: {}".format(toee.game.leader.map))
		if (toee.game.leader.map != shattered_consts.MAP_ID_SHATERRED_LAB): return
		to_del = list()
		objs = utils_storage.Storage().objs
		assert isinstance(objs, dict)
		for o in objs.itervalues():
			assert isinstance(o, utils_storage.ObjectStorage)
			if (o.name.startswith("G_") and o.origin == shattered_consts.MAP_ID_SHATERRED_LAB):
				npc = toee.game.get_obj_by_id(o.name)
				if (npc):
					print("npc hp: {}, npc: {}".format(utils_npc.npc_hp_current(npc), npc))
				if (not npc or (npc.object_flags_get() & toee.OF_DESTROYED) or utils_npc.npc_hp_current(npc) < 0):
					to_del.append(o)
		print("drop objects, count: {}, list: {}".format(len(to_del), to_del))
		for o in to_del:
			del objs[o.name]
		return
