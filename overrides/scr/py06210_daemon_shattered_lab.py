import toee, debugg, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee
import py06122_cormyr_prompter

MAP_ID_SHATERRED_LAB = 5121
SHATERRED_LAB = "shattered_lab"
FACTION_SLAUGHTERGARDE_LABORATORY = 73

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
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
		self.print_monsters()
		return

	def place_encounter_l1(self):
		#self.promters.append(PromterInfo.create(518, 461, 1, 20))
		#self.promters.append(PromterInfo.create(518, 471, 1, 20))
		py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(518, 471), 6210, 1, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Treacherous Tunnel")
		return

	def place_encounter_l2(self):
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
		return

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name):
		assert isinstance(npc, toee.PyObjHandle)
		npc.faction_add(FACTION_SLAUGHTERGARDE_LABORATORY)
		npc.npc_flag_set(toee.ONF_NO_ATTACK)
		npc.npc_flag_unset(toee.ONF_KOS)
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