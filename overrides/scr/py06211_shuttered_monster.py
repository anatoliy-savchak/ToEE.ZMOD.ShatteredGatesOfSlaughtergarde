import toee, debugg, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_target_list

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlMonster.get_from_obj(attachee)
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlMonster.get_from_obj(attachee)
	if (ctrl):
		return ctrl.enter_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

class MonsterInfo:
	def __init__(self):
		self.proto = 0
		self.id = None
		self.cr = 0
		self.name = None
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

class CtrlMonster(object):
	def __init__(self):
		self.option_is_melee = 1
		self.option_first_javelin = 0
		self.option_starts_combat_sneaked = 0
		self.option_dont_move = 0
		self.wield_next_round_back_proto = 0
		self.option_5fs_prefer = 0
		self.option_prefer_low_ac = 0
		return

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = 6211
		npc.scripts[const_toee.sn_enter_combat] = 6211
		return

	@staticmethod
	def get_name():
		return "CtrlMonster"

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
		if (toee.game.combat_turn == 1 and self.option_starts_combat_sneaked):
			#debugg.breakp("option_starts_combat_sneaked")
			attachee.critter_flag_set(OCF_MOVING_SILENTLY)
			self.option_starts_combat_sneaked = 0

		#debugg.breakp("start_combat")
		tac = utils_tactics.TacticsHelper(self.get_name())
		while (1):
			if (self.wield_next_round_back_proto):
				weapon = attachee.item_find_by_proto(self.wield_next_round_back_proto)
				if (weapon):
					attachee.item_wield(weapon, toee.item_wear_weapon_primary)
				self.wield_next_round_back_proto = 0

			if (toee.game.combat_turn == 1 and self.option_first_javelin):
				weapon = attachee.item_find_by_proto(const_proto_weapon.PROTO_WEAPON_JAVELIN)
				if (weapon):
					prev_item = attachee.item_worn_at(toee.item_wear_weapon_primary)
					if (prev_item):
						self.wield_next_round_back_proto = prev_item.proto
					attachee.item_wield(weapon, toee.item_wear_weapon_primary)

			if (self.option_prefer_low_ac):
				tac.add_clear_target()

				is_ranged = 0
				curr_item = attachee.item_worn_at(toee.item_wear_weapon_primary)
				if (curr_item and toee.game.is_ranged_weapon(curr_item.obj_get_int(toee.obj_f_weapon_type))):
					is_ranged = 1

				target = None
				if (not is_ranged):
					measures = utils_target_list.AITargetMeasure.by_ac(0)
					measures.measure_can_path = 1
					measures.measure_range_is_within_melee = 1
					measures.measure_distance = 1
					#measures.mult_can_path = 10
					targs = utils_target_list.AITargetList(attachee, 1, 0, measures).rescan()
					print(targs)
					if (targs):
						for item in targs.list:
							assert isinstance(item, utils_target_list.AITarget)
							if (not item.measures.value_range_is_within_melee and (not item.measures.value_can_path or item.measures.value_can_path > 24)): continue
							target = item.target
							if (target): break

					print(target)

				if (target is None or not target):
					if (is_ranged):
						tac.add_five_foot_step()
						tac.add_target_low_ac()
						tac.add_attack()
					else: 
						#tac.add_target_closest()
						#tac.add_ready_vs_approach()
						tac.add_total_defence()
				else: 
					tac.add_target_obj(target.id)
					tac.add_approach();
					tac.add_attack()
					#tac.add_ready_vs_approach()
					tac.add_total_defence()
				break

			if (self.option_5fs_prefer):
				tac.add_five_foot_step()

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
		if (self.option_first_javelin):
			weapon = attachee.item_find_by_proto(const_proto_weapon.PROTO_WEAPON_JAVELIN)
			if (weapon):
				attachee.item_wield(weapon, toee.item_wear_weapon_primary)
		if (self.option_starts_combat_sneaked):
			#debugg.breakp("option_starts_combat_sneaked")
			attachee.critter_flag_set(OCF_MOVING_SILENTLY)
		return toee.RUN_DEFAULT