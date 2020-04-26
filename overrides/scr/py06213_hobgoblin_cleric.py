import toee, debugg, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlHobgoblinCleric.get_from_obj(attachee)
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlHobgoblinCleric.get_from_obj(attachee)
	if (ctrl):
		return ctrl.enter_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

class CtrlHobgoblinCleric(object):
	def __init__(self):
		self.spells = utils_npc_spells.NPCSpells()
		return

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = 6213
		npc.scripts[const_toee.sn_enter_combat] = 6213
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_CHAIN_SHIRT, npc)
		npc.item_wield_best_all()
		item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_MACE_HEAVY_MASTERWORK, npc)
		npc.item_wield(item, toee.item_wear_weapon_primary)
		utils_item.item_money_create_in_inventory(npc, 82, 355 + 200 + 3*50)
		utils_item.item_create_in_inventory_mass(npc, [const_proto_scrolls.PROTO_SCROLL_OF_DELAY_POISON, const_proto_scrolls.PROTO_SCROLL_OF_RESIST_ENERGY])
		return

	@classmethod
	def create_obj(cls, loc):
		PROTO_NPC_HOBGOBLIN_CLERIC = 14195
		npc = toee.game.obj_create(PROTO_NPC_HOBGOBLIN_CLERIC, loc)
		ctrl = cls()
		utils_storage.obj_storage(npc).data[cls.get_name()] = ctrl
		ctrl.created(npc)
		return npc

	@classmethod
	def get_name(cls):
		return "CtrlHobgoblinCleric"

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
		return

	def start_combat(self, attachee, triggerer):
		print("{}::{} (round: {})".format(type(self).__name__, "start_combat", toee.game.combat_turn))

		#debugg.breakp("start_combat")
		tac = utils_tactics.TacticsHelper(self.get_name())
		while (1):
			if (self.spells.get_spell_count(toee.spell_shield_of_faith)):
				tac.add_five_foot_step()
				tac.add_target_self()
				tac.add_cast_single_code(self.spells.prep_spell(triggerer, toee.spell_shield_of_faith))
				break
			if (self.spells.get_spell_count(toee.spell_hold_person)):
				tac.add_five_foot_step()
				tac.add_target_closest()
				tac.add_cast_single_code(self.spells.prep_spell(triggerer, toee.spell_hold_person))
				break
			if (self.spells.get_spell_count(toee.spell_cure_light_wounds) and triggerer.stat_level_get(toee.stat_hp_max) - 13 > triggerer.stat_level_get(toee.stat_hp_current)):
				tac.add_five_foot_step()
				tac.add_target_self()
				tac.add_cast_single_code(self.spells.prep_spell(triggerer, toee.spell_cure_light_wounds))
				break
			if (self.spells.get_spell_count(toee.spell_invisibility) and triggerer.stat_level_get(toee.stat_hp_current) <= 10):
				tac.add_five_foot_step()
				tac.add_target_self()
				tac.add_cast_single_code(self.spells.prep_spell(triggerer, toee.spell_invisibility))
				break
			tac.add_target_closest()
			tac.add_attack()
			break

		if (not attachee.item_worn_at(toee.item_wear_weapon_primary)):
			attachee.item_wield_best_all()
		print(tac.custom_tactics)
		if (tac.count > 0):
			tac.make_name()
			attachee.ai_strategy_set_custom(tac.custom_tactics)
		return toee.RUN_DEFAULT

	def enter_combat(self, attachee, triggerer):
		stat_class = toee.stat_level_cleric
		caster_level = 3
		# 2
		self.spells.add_spell(toee.spell_hold_person, stat_class, caster_level)
		self.spells.add_spell(toee.spell_invisibility, stat_class, caster_level)
		# 1
		self.spells.add_spell(toee.spell_cause_fear, stat_class, caster_level)
		self.spells.add_spell(toee.spell_cure_light_wounds, stat_class, caster_level)
		self.spells.add_spell(toee.spell_protection_from_good, stat_class, caster_level)
		self.spells.add_spell(toee.spell_shield_of_faith, stat_class, caster_level)

		# 0
		self.spells.add_spell(toee.spell_cure_minor_wounds, stat_class, caster_level)
		return toee.RUN_DEFAULT