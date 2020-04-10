import toee, debugg, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee
import py06122_cormyr_prompter, py06211_shuttered_monster, utils_sneak, utils_npc

MAP_ID_SHATERRED_LAB = 5121
SHATERRED_LAB = "shattered_lab"
FACTION_SLAUGHTERGARDE_LABORATORY = 73
SHATERRED_LAB_DAEMON_ID = "G_E5ABE70D_F211_42B3_9822_DA440143228C"

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	#debugg.breakp("san_first_heartbeat")
	if (attachee.map != MAP_ID_SHATERRED_LAB): toee.RUN_DEFAULT
	ctrl = CtrlShatteredLab.ensure(attachee)
	ctrl.place_encounters()
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#ctrl = CtrlShatteredLab.get_from_obj(attachee)
	#if (ctrl):
	#	ctrl.process_promters()
	return toee.RUN_DEFAULT

def csl():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(SHATERRED_LAB_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	result = o.data[CtrlShatteredLab.get_name()]
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlShatteredLab(object):
	def __init__(self):
		self.encounters_placed = 0
		self.monsters = dict()
		self.promters = []
		self.id = None
		return

	def created(self, npc):
		self.id = npc.id
		npc.scripts[const_toee.sn_dialog] = 6210
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
		self.place_encounter_l1()
		self.place_encounter_l2()
		self.place_encounter_l3()
		self.print_monsters()
		return

	def place_encounter_l1(self):
		#self.promters.append(PromterInfo.create(518, 461, 1, 20))
		#self.promters.append(PromterInfo.create(518, 471, 1, 20))
		#py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(518, 461), 6210, 1, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Treacherous Tunnel")
		return

	def place_encounter_l2(self):
		if (1==1): return
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(513, 473), 6210, 20, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Lab Entrance")

		PROTO_NPC_HOBGOBLIN_1 = 14188
		npc = toee.game.obj_create(PROTO_NPC_HOBGOBLIN_1, utils_obj.sec2loc(504, 469))
		if (npc):
			utils_obj.obj_scripts_clear(npc)
			utils_item.item_clear_all(npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_PICK_HEAVY, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_HALF_PLATE, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_WOODEN_LARGE, npc)
			npc.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
			npc.item_wield_best_all()
			npc.obj_set_int(toee.obj_f_npc_challenge_rating, -1)
			npc.rotation = const_toee.rotation_0800_oclock
			self.monster_setup(npc, "l2", "hobgoblin1", "Hobgoblin Impaler")
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)

		PROTO_NPC_HOBGOBLIN_2 = 14188
		npc_loc = utils_obj.sec2loc(505, 477)
		npc = toee.game.obj_create(PROTO_NPC_HOBGOBLIN_2, npc_loc)
		if (npc):
			utils_obj.obj_scripts_clear(npc)
			utils_item.item_clear_all(npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_PICK_HEAVY, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_HALF_PLATE, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_WOODEN_LARGE, npc)
			npc.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
			npc.item_wield_best_all()
			npc.obj_set_int(toee.obj_f_npc_challenge_rating, -1)
			npc.move(npc_loc)
			npc.rotation = const_toee.rotation_0800_oclock
			self.monster_setup(npc, "l2", "hobgoblin2", "Hobgoblin Impaler")
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)

		npc_loc = utils_obj.sec2loc(510, 465)
		npc = toee.game.obj_create(PROTO_NPC_HOBGOBLIN_1, npc_loc)
		if (npc):
			utils_obj.obj_scripts_clear(npc)
			utils_item.item_clear_all(npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SHORTBOW, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_BREASTPLATE, npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_ARROW_QUIVER, npc)
			npc.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
			npc.item_wield_best_all()
			npc.obj_set_int(toee.obj_f_npc_challenge_rating, -1)
			npc.move(npc_loc)
			npc.rotation = const_toee.rotation_0500_oclock
			self.monster_setup(npc, "l2", "hobgoblin_archer", "Hobgoblin Archer")
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			ctrl.option_stay = 1
		return

	def place_encounter_l3(self):
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(495, 473), 6210, 30, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Gaol")
		PROTO_NPC_HOBGOBLIN_1 = 14188
		npc_loc = utils_obj.sec2loc(498, 468)
		npc = toee.game.obj_create(PROTO_NPC_HOBGOBLIN_1, npc_loc)
		if (npc):
			utils_obj.obj_scripts_clear(npc)
			utils_item.item_clear_all(npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SHORTSWORD, npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_JAVELIN, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
			npc.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
			npc.condition_add_with_args("Hidden_Attack", 0, 0)
			npc.item_wield_best_all()
			npc.obj_set_int(toee.obj_f_npc_challenge_rating, -1)
			npc.move(npc_loc)
			npc.rotation = const_toee.rotation_0500_oclock
			self.monster_setup(npc, "l3", "hobgoblin1", "Hobgoblin Scrounger", 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			ctrl.option_first_javelin = 1
			npc.condition_add_with_args("Sneak_Attack_Ex", 0, 0)
			utils_npc.npc_skill_ensure(npc, skill_hide, 5)

		PROTO_NPC_HOBGOBLIN_2 = 14188
		npc_loc = utils_obj.sec2loc(498, 478)
		npc = toee.game.obj_create(PROTO_NPC_HOBGOBLIN_2, npc_loc)
		if (npc):
			utils_obj.obj_scripts_clear(npc)
			utils_item.item_clear_all(npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SHORTSWORD, npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_JAVELIN, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
			npc.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
			npc.condition_add_with_args("Hidden_Attack", 0, 0)
			npc.item_wield_best_all()
			npc.obj_set_int(toee.obj_f_npc_challenge_rating, -1)
			npc.move(npc_loc)
			npc.rotation = const_toee.rotation_1000_oclock
			self.monster_setup(npc, "l3", "hobgoblin2", "Hobgoblin Scrounger", 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			ctrl.option_first_javelin = 1
			utils_npc.npc_skill_ensure(npc, skill_hide, 5)

		npc_loc = utils_obj.sec2loc(490, 477)
		npc = toee.game.obj_create(PROTO_NPC_HOBGOBLIN_2, npc_loc)
		if (npc):
			utils_obj.obj_scripts_clear(npc)
			utils_item.item_clear_all(npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SHORTSWORD, npc)
			utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_JAVELIN, npc)
			utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
			npc.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
			npc.condition_add_with_args("Hidden_Attack", 0, 0)
			npc.item_wield_best_all()
			npc.obj_set_int(toee.obj_f_npc_challenge_rating, -1)
			npc.move(npc_loc)
			npc.rotation = const_toee.rotation_0800_oclock
			self.monster_setup(npc, "l3", "hobgoblin3", "Hobgoblin Scrounger", 1)
			ctrl = py06211_shuttered_monster.CtrlMonster.ensure(npc)
			ctrl.option_first_javelin = 1
			utils_npc.npc_skill_ensure(npc, skill_hide, 5)
		return

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1):
		assert isinstance(npc, toee.PyObjHandle)
		npc.faction_add(FACTION_SLAUGHTERGARDE_LABORATORY)
		npc.npc_flag_set(toee.ONF_NO_ATTACK)
		npc.npc_flag_unset(toee.ONF_KOS)
		if (no_draw):
			npc.object_flag_set(toee.OF_DONTDRAW)
		nameid = utils_toee.make_custom_name(monster_name)
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		info = MonsterInfo()
		info.id = npc.id
		info.proto = npc.proto
		self.monsters["{}_{}_{}".format(SHATERRED_LAB, encounter_name, monster_code_name)] = info
		return

	def print_monsters(self):
		for key, value in self.monsters.items():
			assert isinstance(value, MonsterInfo)
			print("{}={}".format(key, value.id))
		return

	def process_promters(self):
		#debugg.breakp("process_promters")
		party = None
		found = None
		found_pc = None
		for info in self.promters:
			assert isinstance(info, PromterInfo)
			if (info.displayed_times): continue
			if (not party): party = toee.game.party
			for pc in party:
				dist = pc.distance_to(info.loc)
				if (dist <= info.distance_trigger):
					found = info
					found_pc = pc
					break
		if (found):
			print("found found_pc:{}, with:{}, dialog_line:{}".format(found_pc, toee.game.get_obj_by_id(self.id), found.dialog_line))
			debugg.breakp("process_promters")
			found_pc.begin_dialog(toee.game.get_obj_by_id(self.id), found.dialog_line)
			found.displayed_times += 1
		return

	def get_monsterinfo(self, encounter_name, monster_code_name):
		key = "{}_{}_{}".format(SHATERRED_LAB, encounter_name, monster_code_name)
		if (key in self.monsters):
			info = self.monsters[key]
			assert isinstance(info, MonsterInfo)
			return info
		return None

	def reveal_monster(self, encounter_name, monster_code_name):
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc):
				npc.object_flag_unset(toee.OF_DONTDRAW)
		return

	def display_encounter_l2(self):
		self.reveal_monster("l2", "hobgoblin1")
		self.reveal_monster("l2", "hobgoblin2")
		self.reveal_monster("l2", "hobgoblin_archer")
		return

	def activate_monster(self, encounter_name, monster_code_name):
		npc = None
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc):
				npc.npc_flag_unset(toee.ONF_NO_ATTACK)
				npc.npc_flag_set(toee.ONF_KOS)
		return npc, info

	def activate_encounter_l2(self):
		self.activate_monster("l2", "hobgoblin1")
		self.activate_monster("l2", "hobgoblin2")
		self.activate_monster("l2", "hobgoblin_archer")
		return

	def display_encounter_l3(self):
		self.reveal_monster("l3", "hobgoblin1")
		self.reveal_monster("l3", "hobgoblin2")
		self.reveal_monster("l3", "hobgoblin3")
		return

	def activate_encounter_l3(self):
		#debugg.breakp("activate_encounter_l3")
		npc, info = self.activate_monster("l3", "hobgoblin1")
		if (npc):
			hidden = utils_sneak.npc_make_hide(npc, 1)
			if (hidden):
				ctrl = py06211_shuttered_monster.CtrlMonster.get_from_obj(npc)
				if (ctrl):
					ctrl.option_starts_combat_sneaked = 1
		npc, info = self.activate_monster("l3", "hobgoblin2")
		if (npc):
			hidden = utils_sneak.npc_make_hide(npc, 1)
			if (hidden):
				ctrl = py06211_shuttered_monster.CtrlMonster.get_from_obj(npc)
				if (ctrl):
					ctrl.option_starts_combat_sneaked = 1
		npc, info = self.activate_monster("l3", "hobgoblin3")
		if (npc):
			hidden = utils_sneak.npc_make_hide(npc, 1)
			if (hidden):
				ctrl = py06211_shuttered_monster.CtrlMonster.get_from_obj(npc)
				if (ctrl):
					ctrl.option_starts_combat_sneaked = 1
		return

class MonsterInfo:
	def __init__(self):
		self.proto = 0
		self.id = None
		return

class PromterInfo:
	def __init__(self):
		self.locx = 0
		self.locy = 0
		self.loc = 0
		self.dialog_line = None
		self.displayed_times = 0
		self.distance_trigger = 0
		return

	@classmethod
	def create(cls, locx, locy, dialog_line, distance_trigger):
		obj = cls()
		obj.locx = locx
		obj.locy = locy
		obj.loc = utils_obj.sec2loc(locx, locy)
		obj.dialog_line = dialog_line
		obj.distance_trigger = distance_trigger
		return obj