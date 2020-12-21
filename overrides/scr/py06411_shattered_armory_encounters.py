import toee, debug, tpdp, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour
import const_proto_potions, utils_obj, utils_npc, utils_target_list, const_proto_wands, utils_sneak, const_deseases, utils_npc_spells, utils_npc
import py06401_shattered_temple_encounters, const_proto_items, const_proto_rings, const_proto_cloth, const_proto_wondrous, shattered_consts

shattered_armory_encounters = 6411

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.enter_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_end_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.end_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_exit_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.exit_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_will_kos(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	print("will_kos({}, {})".format(attachee, triggerer))
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.will_kos(attachee, triggerer)
	else: print("san_will_kos ctrl not found")
	return toee.RUN_DEFAULT

class CtrlGnollBarbarian2(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14937

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters

		# create inventory
		utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, npc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GREATAXE_MASTERWORK, npc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_BREASTPLATE_PLUS_1_BLACK, npc)
		npc.item_wield_best_all()
		return

	def enter_combat(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		return toee.RUN_DEFAULT


	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None
		is_raged = npc.d20_query(toee.Q_Barbarian_Raged)
		while (not tac):
			tac = self.tactic_coup_de_grace(npc)
			if (tac):
				return tac

			tac = utils_tactics.TacticsHelper(self.get_name())
			if (not is_raged):
				tac.add_rage()
			tac.add_clear_target()
			tac.add_target_closest()
			#tac.add_target_damaged()
			tac.add_flank()
			tac.add_attack()
			tac.add_approach_single()
			tac.add_attack()
			tac.add_ready_vs_approach()
			tac.add_total_defence()
			tac.add_halt()
			break
		return tac

class CtrlGnollArcher(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14938

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_will_kos] = shattered_armory_encounters

		# create inventory
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD_MASTERWORK, npc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_LONGBOW_COMPOSITE_16_MASTERWORK, npc)
		item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(toee.obj_f_ammo_quantity, 40)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_MITHRAL_SHIRT, npc)
		npc.item_wield_best_all()

		npc.feat_add(toee.feat_improved_precise_shot, 1)
		return

	def enter_combat(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		return toee.RUN_DEFAULT

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None
		while (not tac):
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_clear_target()
			tac.add_target_damaged()
			tac.add_attack()
			tac.add_target_low_ac()
			tac.add_attack()
			tac.add_target_closest()
			tac.add_attack()
			tac.add_total_defence()
			tac.add_halt()
			break
		return tac

	def will_kos(self, attachee, triggerer):
		#print("will_kos({}, {})".format(attachee, triggerer))
		if (triggerer.proto == 14939): #troll
			return 0
		return toee.RUN_DEFAULT

class CtrlBlindTroll(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14939

class CtrlFlindSoldier(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14940

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		#npc.scripts[const_toee.sn_will_kos] = shattered_armory_encounters
		npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)

		# create inventory
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_FLIND_PLUS1, npc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_LARGE_PLUS_1_STEEL, npc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR_MASTERWORK, npc)
		npc.item_wield_best_all()
		return

	def enter_combat(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		return toee.RUN_DEFAULT

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None

		primary_weapon = npc.item_worn_at(toee.item_wear_weapon_primary)
		skip_disarm = 0
		while (not tac):
			if (not skip_disarm and primary_weapon and utils_npc.npc_hp_current_percent(npc) <= 50):
				skip_disarm = 1
				melees = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_melee()).rescan()
				if (not melees.list): continue
				list2 = sorted(melees.list, cmp = py06401_shattered_temple_encounters.CtrlArcaneGuard_measures_cmp, reverse = True)
				if (not list2): continue
				atarget = list2[0]
				assert isinstance(atarget, utils_target_list.AITarget)
				print("found atarget: {}".format(atarget))
				print("found target: {}".format(atarget.target))

				if (not atarget.measures.value_weapon_melee): continue
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				#tac.add_target_closest()
				tac.add_target_obj(atarget.target.id)
				#tac.add_approach_single()
				tac.add_d20_action(toee.D20A_DISARM, 0)
				tac.add_attack()
				tac.add_total_defence()
				tac.add_halt()
				break

			tac = self.tactic_coup_de_grace(npc)
			if (tac):
				return tac

			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_target_closest()
			tac.add_approach_single()
			tac.add_attack()
			tac.add_ready_vs_approach()
			tac.add_total_defence()
			tac.add_halt()
			break
		return tac

class CtrlHillGiant(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14942

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		#npc.scripts[const_toee.sn_will_kos] = shattered_armory_encounters

		# create inventory
		utils_item.item_create_in_inventory(4099, npc) # Hill Giant Club
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_HIDE_MASTERWORK, npc)
		npc.item_wield_best_all()

		npc.feat_add(toee.feat_sunder, 1)
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None
		while (toee.game.combat_turn == 1 and not tac):
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_clear_target()
			tac.add_target_closest()
			tac.add_charge()
			tac.add_halt()
			tac.add_total_defence()
			break
		return tac

	def debug_replace1(self):
		npc = self.npc_get()
		if (not npc): return
		item = npc.item_find_by_proto(4090)
		if (item):
			item.destroy()
		utils_item.item_create_in_inventory(4099, npc) # Hill Giant Club
		npc.item_wield_best_all()
		return

class CtrlHalfFiendOgre(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14941

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlHalfFiendOgre, self).created(npc)
		#npc.condition_add_with_args("Initiative_Bonus", 30, 0)
		#npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)
		return

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		#npc.scripts[const_toee.sn_will_kos] = shattered_armory_encounters

		## create inventory
		#utils_item.item_create_in_inventory(4090, npc) # Hill Giant Club
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE_PLUS_1_BLACK, npc)
		utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, npc)
		npc.item_wield_best_all()
		fog_potion = utils_item.item_create_in_inventory(8601, npc)
		fog_potion.item_flag_set(toee.OIF_NO_NPC_PICKUP)
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		fog_potion = npc.item_find_by_proto(8601)
		print("Find fog_potion {}, self: {} ".format(fog_potion, npc))
		if (fog_potion):
			#debug.breakp("desecrate")
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_clear_target()
			tac.add_target_self()
			tac.add_use_item(fog_potion.id)
			tac.add_total_defence()
			return tac

		hp = npc.stat_level_get(toee.stat_hp_current)
		if (hp <= 50):
			#{939}{A6 Door}
			print("looking for a door")
			door = utils_obj.find_nearest_obj_by_nameid(npc, 30, 939, toee.OLC_PORTAL)
			if (door):
				print("door found")
				#if (not door.portal_flags_get() & toee.OPF_OPEN)
				if (not (door.object_flags_get() & toee.OF_DONTDRAW)):
					tac = utils_tactics.TacticsHelper(self.get_name())
					tac.add_clear_target()
					tac.add_target_obj(door.id)
					#tac.add_approach_single()
					tac.add_goto_loc(utils_obj.sec2loc(449, 508))
					tac.add_python_action(3018) # open_door
					tac.add_clear_target()
					tac.add_target_closest()
					tac.add_attack()
					return tac

			healing_potion = npc.item_find_by_proto(const_proto_potions.PROTO_POTION_OF_CURE_MODERATE_WOUNDS)
			if (healing_potion):
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				tac.add_target_self()
				tac.add_use_item(healing_potion.id)
				tac.add_clear_target()
				tac.add_target_closest()
				tac.add_attack()

		return None

	def trigger_step(self, npc, step):
		assert isinstance(npc, toee.PyObjHandle)
		assert isinstance(step, int)

		npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)
		fog_potion = npc.item_find_by_proto(8601)
		if (fog_potion):
			npc.use_item(fog_potion)
		return

class CtrlRedspwawnFirebelcher(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14943

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None
		do_ball = 1

		while (not tac):
			tac = self.tactic_coup_de_grace(npc)
			if (tac):
				return tac

			if (do_ball): 
				m = utils_target_list.AITargetMeasure.by_all()
				m.measure_affected_range = 5
				m.measure_has_los = 1
				foes = utils_target_list.AITargetList(npc, 1, 0, m).rescan()
				target = foes.find_affected_best(1, 1)
				if (target):
					print("target.measures.value_affected_range_count_foes: {}".format(target.measures.value_affected_range_count_foes))
				else: print("no target")
				if (not target or target.measures.value_affected_range_count_foes <= 1): 
					do_ball = 0
					print("skip ball")
					continue

				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				tac.add_target_obj(target.target.id)
				tac.add_python_action(3019) # belch_fire
				tac.add_clear_target()
				tac.add_target_closest()
				tac.add_attack()
				tac.add_total_defence()
				break
			break
		return tac

class CtrlTroglodyteBarbarians(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14944

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		#debug.breakp("condition_add_with_args")
		npc.condition_add_with_args("Stench_Of_Troglodyte", 0, 10, 17, 30)

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR_PLUS_1, npc)
		utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, npc, 2)
		npc.item_wield_best_all()
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		is_raged = npc.d20_query(toee.Q_Barbarian_Raged)
		if (not is_raged):
			print("go rage")
			#npc.condition_add_with_args("Barbarian_Raged", 0, 0)
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_rage()
			tac.add_target_closest()
			tac.add_charge()
			tac.add_attack()
			tac.add_ready_vs_approach()
			tac.add_attack()
			tac.add_total_defence()
			tac.add_halt()
			return tac

		stenched = self.get_var("stenched")
		if (not stenched):
			self.vars["stenched"] = 1
			#npc.condition_add_with_args("Barbarian_Raged", 0, 0)
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_target_closest()
			tac.add_approach_single()
			tac.add_python_action(3020) # produce stench
			tac.add_attack()
			tac.add_total_defence()
			tac.add_halt()
			return tac

		tac = self.tactic_coup_de_grace(npc)
		if (tac):
			return tac

		return

class CtrlTroglodyteThug(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14945

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		npc.condition_add_with_args("Stench_Of_Troglodyte", 0, 10, 17, 30)
		npc.condition_add("Sneak_Attack_Ex")
		npc.condition_add("Hide_Ex")
		
		utils_npc.npc_skill_ensure(npc, toee.skill_tumble, 8)

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR_PLUS_1, npc)
		utils_item.item_create_in_inventory(const_proto_items.PROTO_WONDROUS_AMULET_OF_NATURAL_ARMOR_1, npc)
		utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, npc)
		
		npc.item_wield_best_all()
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		if (1):
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_target_closest()
			tac.add_target_low_ac()
			tac.add_flank()
			tac.add_attack()
			tac.add_total_defence()
			tac.add_halt()
			return tac
		return

class CtrlTroglodyteSoldier(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14946


	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		npc.condition_add_with_args("Stench_Of_Troglodyte", 0, 10, 17, 30)
		npc.condition_add_with_args("Bonus_Attack", 1)

		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_HALBERD_MASTERWORK, npc)
		#utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_LONGSPEAR, npc)
		#utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GLAIVE_MASTERWORK, npc)
		
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE_MASTERWORK, npc)
		case = toee.game.random_range(1, 5)
		if (case == 1):
			utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_CLOAK_OF_RESISTANCE_1_BLUE, npc)
		elif (case == 2):
			utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_CLOAK_OF_RESISTANCE_1_ORANGE, npc)
		elif (case == 3):
			utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_CLOAK_OF_RESISTANCE_1_WHITE, npc)
		elif (case == 4):
			utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_CLOAK_OF_RESISTANCE_1_GREEN, npc)
		elif (case == 5):
			utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_CLOAK_OF_RESISTANCE_1_BLACK, npc)
		
		utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, npc)
		
		npc.item_wield_best_all()
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)

		stenched = self.get_var("stenched")
		if (not stenched):
			self.vars["stenched"] = 1
			#npc.condition_add_with_args("Barbarian_Raged", 0, 0)
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_target_closest()
			tac.add_approach_single()
			tac.add_python_action(3020) # produce stench
			tac.add_attack()
			tac.add_total_defence()
			tac.add_halt()
			return tac

		tac = self.tactic_coup_de_grace(npc)
		if (tac):
			return tac

		return

class CtrlTroglodyteCleric(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14947

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlTroglodyteCleric, self).created(npc)
		#utils_obj.obj_scripts_clear(npc)
		#npc.condition_add_with_args("Caster_Level_Add", 5, 0)
		npc.condition_add_with_args("Stench_Of_Troglodyte", 0, 10, 17, 30)
		utils_npc.npc_skill_ensure(npc, toee.skill_concentration, 6)
		npc.condition_add_with_args("Bonus_Attack", 1)
		
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR_PLUS_1, npc)
		utils_item.item_create_in_inventory(const_proto_rings.PROTO_RING_OF_PROTECTION_PLUS_1, npc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SPEAR_PLUS_1, npc)
		npc.item_wield_best_all()
		return

	def revealed(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_npc.npc_spell_ensure(npc, toee.spell_magic_circle_against_good, toee.stat_level_cleric, 5, 1)
		npc.cast_spell(toee.spell_magic_circle_against_good, npc)
		return

	def trigger_step(self, npc, step):
		assert isinstance(npc, toee.PyObjHandle)
		assert isinstance(step, int)

		if (step == 2):
			utils_npc.npc_spell_ensure(npc, toee.spell_shield_of_faith, toee.stat_level_cleric, 5, 1)
			npc.cast_spell(toee.spell_shield_of_faith, npc)
		elif (step == 3):
			utils_npc.npc_spell_ensure(npc, toee.spell_protection_from_law, toee.stat_level_cleric, 5, 1)
			npc.cast_spell(toee.spell_protection_from_law, npc)
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None

		foes = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_all()).rescan()
		threats = foes.get_threats()
		print("threats: {}".format(threats))

		while (not tac):
			hp_perc = utils_npc.npc_hp_current_percent(npc)
			print("hp_perc: {}".format(hp_perc))

			tac = self.tactic_coup_de_grace(npc)
			if (tac):
				return tac

			stenched = self.get_var("stenched")
			if (not stenched):
				self.vars["stenched"] = 1
				#npc.condition_add_with_args("Barbarian_Raged", 0, 0)
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_self()
				tac.add_python_action(3020) # produce stench
				tac.add_attack()
				tac.add_total_defence()
				tac.add_halt()
				return tac

			if (hp_perc <= 30):
				if (self.spells.get_spell_count(toee.spell_sanctuary)): 
					tac = utils_tactics.TacticsHelper(self.get_name())
					tac.add_target_self()
					tac.add_five_foot_step()
					tac.add_halt()
					tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_sanctuary))
					tac.add_total_defence()
					break

				if (self.spells.get_spell_count(toee.spell_cure_light_wounds)): 
					tac = utils_tactics.TacticsHelper(self.get_name())
					tac.add_target_self()
					tac.add_five_foot_step()
					tac.add_halt()
					tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_cure_light_wounds))
					tac.add_total_defence()
					break

			if (self.spells.get_spell_count(toee.spell_hold_person)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_hold_person))
				tac.add_halt()
				tac.add_total_defence()
				break

			if (self.spells.get_spell_count(toee.spell_bestow_curse)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				if (threats):
					#tac.add_five_foot_step() NO TOUCH!!
					tac.add_target_obj(threats[0].target.id)
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_bestow_curse))
				tac.add_halt()
				tac.add_total_defence()
				break

			if (self.spells.get_spell_count(toee.spell_inflict_light_wounds)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				if (threats):
					#tac.add_five_foot_step() NO TOUCH!!
					tac.add_target_obj(threats[0].target.id)
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_inflict_light_wounds))
				tac.add_halt()
				tac.add_total_defence()
				break

			break
		return tac

	def enter_combat(self, attachee, triggerer):
		self.spells = utils_npc_spells.NPCSpells()
		caster_level_cleric = attachee.highest_divine_caster_level
		print("caster_level_cleric: {}".format(caster_level_cleric))
		self.spells.add_spell(toee.spell_bestow_curse, toee.stat_level_cleric, caster_level_cleric)
		#self.spells.add_spell(toee.spell_contagion, toee.stat_level_cleric, caster_level_cleric)
		#self.spells.add_spell(toee.spell_dispel_magic, toee.stat_level_cleric, caster_level_cleric)
		#self.spells.add_spell(toee.spell_inflict_serious_wounds, toee.stat_level_cleric, caster_level_cleric, 1)
		self.spells.add_spell(toee.spell_sanctuary, toee.stat_level_cleric, caster_level_cleric)

		self.spells.add_spell(toee.spell_hold_person, toee.stat_level_cleric, caster_level_cleric, 2)
		self.spells.add_spell(toee.spell_cure_light_wounds, toee.stat_level_cleric, caster_level_cleric)

		#self.spells.add_spell(toee.spell_inflict_light_wounds, toee.stat_level_cleric, caster_level_cleric, 2) # due to supposed pearl of power
		return toee.RUN_DEFAULT

class CtrlOrcharix(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14948


	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlOrcharix, self).created(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters

		# 1 - Bite plus ability drain
		# 2, 3 - Claws plus trip
		# 4, 5 - Wings
		# 6 - Tail slap plus trip
		attacks_with_trip = (1 << 1) + (1 << 2) + (1 << 5)
		mode = 2 # 0 any, 1 any natural, 2 specific natural
		npc.condition_add_with_args("Monster_Trip_Ex", mode, attacks_with_trip)

		dc = 16
		save = toee.D20_Save_Fortitude
		ability = toee.stat_constitution
		dice_packed = toee.dice_new("1d4").packed
		attacks_with_drain = 1
		npc.condition_add_with_args("Monster_Ability_Drain_Su", dc, save, ability, dice_packed, attacks_with_drain)

		return

	def dying(self, attachee, triggerer):
		utils_item.item_create_in_inventory(const_proto_items.PROTO_WONDROUS_AMULET_OF_HEALTH_1, attachee)
		return toee.RUN_DEFAULT

class CtrlTieflingBlademaster(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14949

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlTieflingBlademaster, self).created(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR_PLUS_1, npc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD_MASTERWORK, npc)
		shortsword = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SHORTSWORD_MASTERWORK, npc)
		npc.item_wield_best_all()
		npc.item_wield(shortsword, toee.item_wear_weapon_secondary)
		return

	def enter_combat(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)

		weapon = attachee.item_find_by_proto(const_proto_weapon.PROTO_LONGSWORD_MASTERWORK)
		if (weapon):
			print("equipping toee.item_wear_weapon_primary: {}".format(weapon))
			attachee.item_wield(weapon, toee.item_wear_weapon_primary)
		else: print("PROTO_LONGSWORD_MASTERWORK not found!")

		weapon = attachee.item_find_by_proto(const_proto_weapon.PROTO_WEAPON_SHORTSWORD_MASTERWORK)
		if (weapon):
			print("equipping toee.item_wear_weapon_secondary: {}".format(weapon))
			attachee.item_wield(weapon, toee.item_wear_weapon_secondary)
		else: print("PROTO_WEAPON_SHORTSWORD_MASTERWORK not found!")

		utils_npc.npc_print_wears(utils_npc.npc_get_wears(attachee))

		return toee.RUN_DEFAULT

class CtrlTieflingWizard(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14950

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlTieflingWizard, self).created(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters

		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_ROBES_BROWN, npc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT_MASTERWORK, npc)
		item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(toee.obj_f_ammo_quantity, 20)
		utils_item.item_create_in_inventory(const_proto_items.PROTO_WONDROUS_BRACES_OF_ARMOR_1, npc)
		npc.item_wield_best_all()
		return

	def revealed(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_npc.npc_spell_ensure(npc, toee.spell_shield, toee.stat_level_wizard, 3, 1)
		npc.cast_spell(toee.spell_shield, npc)
		return

	def trigger_step(self, npc, step):
		assert isinstance(npc, toee.PyObjHandle)
		assert isinstance(step, int)

		if (step == 2):
			utils_npc.npc_spell_ensure(npc, toee.spell_mage_armor, toee.stat_level_wizard, 3, 1)
			npc.cast_spell(toee.spell_mage_armor, npc)
		elif (step == 3):
			utils_npc.npc_spell_ensure(npc, toee.spell_protection_from_good, toee.stat_level_wizard, 3, 1)
			npc.cast_spell(toee.spell_protection_from_good, npc)
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None

		foes = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_all()).rescan()
		threats = foes.get_threats()
		print("threats: {}".format(threats))

		while (not tac):
			hp_perc = utils_npc.npc_hp_current_percent(npc)
			print("hp_perc: {}".format(hp_perc))

			if (self.spells.get_spell_count(toee.spell_scorching_ray)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				if (threats):
					tac.add_target_obj(threats[0].target.id)
					tac.add_five_foot_step()
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_scorching_ray))
				tac.add_halt()
				tac.add_total_defence()
				break

			if (self.spells.get_spell_count(toee.spell_magic_missile)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				if (threats):
					tac.add_target_obj(threats[0].target.id)
					tac.add_five_foot_step()
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_magic_missile))
				tac.add_halt()
				tac.add_total_defence()
				break

			if (self.spells.get_spell_count(toee.spell_color_spray)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				if (threats):
					tac.add_target_obj(threats[0].target.id)
					tac.add_five_foot_step()
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_color_spray))
				tac.add_halt()
				tac.add_total_defence()
				break

			break
		return tac

	def enter_combat(self, attachee, triggerer):
		#debug.breakp("enter_combat")
		self.spells = utils_npc_spells.NPCSpells()
		caster_level = attachee.highest_arcane_caster_level
		self.spells.add_spell(const_toee.spell_scorching_ray, toee.stat_level_wizard, caster_level, 2)
		self.spells.add_spell(toee.spell_magic_missile, toee.stat_level_wizard, caster_level)
		self.spells.add_spell(toee.spell_color_spray, toee.stat_level_wizard, caster_level)
		return toee.RUN_DEFAULT

class CtrlGnollPriestess(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14951

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlGnollPriestess, self).created(npc)
		#utils_obj.obj_scripts_clear(npc)
		#npc.condition_add_with_args("Caster_Level_Add", 5, 0)
		utils_npc.npc_skill_ensure(npc, toee.skill_concentration, 6)
		npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)
		
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_STUDDED_LEATHER_ARMOR_PLUS_1, npc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_LARGE_WOODEN, npc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_FLAIL_MASTERWORK, npc)
		utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_BULLS_STRENGTH, npc)
		npc.item_wield_best_all()
		return

	def revealed(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_npc.npc_spell_ensure(npc, toee.spell_shield_of_faith, toee.stat_level_cleric, 5, 1)
		npc.cast_spell(toee.spell_shield_of_faith, npc)
		return

	def trigger_step(self, npc, step):
		assert isinstance(npc, toee.PyObjHandle)
		assert isinstance(step, int)

		if (step == 2):
			utils_npc.npc_spell_ensure(npc, toee.spell_divine_favor, toee.stat_level_cleric, npc.highest_divine_caster_level, 1)
			npc.cast_spell(toee.spell_divine_favor, npc)
		elif (step == 3):
			utils_npc.npc_spell_ensure(npc, toee.spell_endurance, toee.stat_level_cleric, npc.highest_divine_caster_level, 1)
			npc.cast_spell(toee.spell_endurance, npc)
		elif (step == 4):
			scroll = npc.item_find_by_proto(const_proto_scrolls.PROTO_SCROLL_OF_BULLS_STRENGTH)
			if (not scroll):
				print("scroll PROTO_SCROLL_OF_BULLS_STRENGTH not found!")
				return
			flind = npc
			if (self.get_var("a12") or self.get_var("a14") == 1):
				flind = utils_npc.npc_find_nearest_npc_by_proto(npc, 15, CtrlFlindSoldier.get_proto_id())
			if (not flind):
				print("flind not found!")
				flind = npc

			npc.use_item(scroll, flind)
		elif (step == 5):
			utils_npc.npc_spell_ensure(npc, toee.spell_protection_from_good, toee.stat_level_cleric, npc.highest_divine_caster_level, 1)
			npc.cast_spell(toee.spell_protection_from_good, npc)
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None

		foes = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_all()).rescan()
		threats = foes.get_threats()
		print("threats: {}".format(threats))

		invisibility_potion = None
		if (not self.get_var("invisibility_potion used")):
			invisibility_potion = npc.item_find_by_proto(const_proto_potions.PROTO_POTION_OF_INVISIBILITY)
		cure_wand = npc.item_find_by_proto(const_proto_wands.PROTO_WAND_OF_CURE_MODERATE_WOUNDS)
		while (not tac):
			hp_perc = utils_npc.npc_hp_current_percent(npc)
			print("hp_perc: {}".format(hp_perc))

			tac = self.tactic_coup_de_grace(npc, foes)
			if (tac):
				break

			if (invisibility_potion):
				self.vars["invisibility_potion used"] = 1
				#debug.breakp("invisibility_potion")
				#is_dentified = invisibility_potion.item_flags_get() & toee.OIF_IDENTIFIED
				#print("is_dentified: {} of {}".format(is_dentified, invisibility_potion))
				#invisibility_potion.item_flag_set(toee.OIF_IDENTIFIED)

				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				tac.add_target_self()
				tac.add_use_item(invisibility_potion.id)
				tac.add_halt()
				break

			if (0 and self.spells.get_spell_count(toee.spell_invisibility)): 
				debug.breakp("spell_invisibility")
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				tac.add_target_self()
				tac.add_halt()
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_invisibility))
				tac.add_total_defence()
				break

			if (cure_wand):
				#foes = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_all()).rescan()
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				tac.add_target_self()
				tac.add_target_friend_hurt()
				tac.add_approach_single()
				tac.add_use_item(cure_wand.id)
				tac.add_halt()
				break

			if (0 and self.spells.get_spell_count(toee.spell_protection_from_good)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				tac.add_halt()
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_protection_from_good))
				tac.add_total_defence()
				break

			if (self.spells.get_spell_count(toee.spell_spiritual_weapon)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				tac.add_halt()
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_spiritual_weapon))
				tac.add_total_defence()
				break
			
			if (self.spells.get_spell_count(toee.spell_doom)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				tac.add_halt()
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_doom))
				tac.add_total_defence()
				break

			if (self.spells.get_spell_count(toee.spell_hold_person)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				tac.add_target_high_ac()
				tac.add_halt()
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_hold_person))
				tac.add_total_defence()
				break

			if (self.spells.get_spell_count(toee.spell_inflict_light_wounds)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				if (threats):
					#tac.add_five_foot_step() NO TOUCH!!
					tac.add_target_obj(threats[0].target.id)
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_inflict_light_wounds))
				tac.add_halt()
				tac.add_total_defence()
				break

			break
		return tac

	def enter_combat(self, attachee, triggerer):
		self.spells = utils_npc_spells.NPCSpells()
		caster_level_cleric = attachee.highest_divine_caster_level
		print("caster_level_cleric: {}".format(caster_level_cleric))

		if (self.get_var("a12")):
			self.spells.add_spell(toee.spell_hold_person, toee.stat_level_cleric, caster_level_cleric)
			self.spells.add_spell(toee.spell_spiritual_weapon, toee.stat_level_cleric, caster_level_cleric)
			self.spells.add_spell(toee.spell_doom, toee.stat_level_cleric, caster_level_cleric)
			self.spells.add_spell(toee.spell_protection_from_good, toee.stat_level_cleric, caster_level_cleric)

		if (self.get_var("a14")):
			self.spells.add_spell(toee.spell_inflict_light_wounds, toee.stat_level_cleric, caster_level_cleric)
			self.spells.add_spell(toee.spell_inflict_moderate_wounds, toee.stat_level_cleric, caster_level_cleric)
			self.spells.add_spell(toee.spell_doom, toee.stat_level_cleric, caster_level_cleric)
			self.spells.add_spell(toee.spell_protection_from_good, toee.stat_level_cleric, caster_level_cleric)

		if (self.get_var("a14") == 1):
			utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_CURE_MODERATE_WOUNDS, attachee)
			utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OF_INVISIBILITY, attachee)
			attachee.item_worn_unwield(toee.item_wear_weapon_primary, 0)
		elif (self.get_var("a14") == 2):
			self.spells.add_spell(toee.spell_hold_person, toee.stat_level_cleric, caster_level_cleric)
		elif (self.get_var("a14") == 3):
			self.spells.add_spell(toee.spell_spiritual_weapon, toee.stat_level_cleric, caster_level_cleric)
		return toee.RUN_DEFAULT

class CtrlTrollMercenary(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14952

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters

		dice_packed = toee.dice_new("3d6").packed
		weapon_proto_filter = const_proto_weapon.PROTO_WEAPON_GREATSWORD_PLUS_1
		npc.condition_add_with_args("Weapon_Damage_Dice", dice_packed, weapon_proto_filter)

		# create inventory
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GREATSWORD_PLUS_1, npc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_BREASTPLATE_PLUS_1_BLACK, npc)
		utils_item.item_create_in_inventory(const_proto_items.PROTO_WONDROUS_AMULET_OF_HEALTH_1, npc)
		npc.item_wield_best_all()
		return

class CtrlElementalFireHuge(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14510

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None

		while (not tac):
			went_to_1 = self.get_var("went_to_1")
			if (not went_to_1):
				self.vars["went_to_1"] = 1
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				tac.add_goto(521, 445)
				tac.add_halt()
				tac.add_attack_threatened()
				break
			break
		return tac

class CtrlDerroArtisan(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14953

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters

		# create inventory
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_BOLT_QUIVER, npc)

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_LEATHER_ARMOR_GREY, npc)
		npc.item_wield_best_all()
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None

		foes = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_all()).rescan()
		threats = foes.get_threats()
		print("threats: {}".format(threats))

		sound_burst_skip = 0
		while (not tac):
			hp_perc = utils_npc.npc_hp_current_percent(npc)
			print("hp_perc: {}".format(hp_perc))

			sound_bursted = self.get_var("sound_bursted")
			if (not sound_bursted and not sound_burst_skip): 
				scroll = utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_SOUND_BURST, npc)
				if (not scroll): continue

				foes.measures.measure_affected_range = 25-5
				foes.rescan()
				targ = foes.find_affected_best(0, 1)
				if (not targ or targ.measures.value_affected_range_count_foes <=1):
					sound_burst_skip = 1
					print("find_affected_best NONE!!")
					continue

				self.vars["sound_bursted"] = 1
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				print("sound burst target {}".format(targ.target))
				tac.add_target_obj(targ.target.id)
				tac.add_halt()
				tac.add_use_item(scroll.id)
				break
			break
		return tac

class CtrlDerroArtisanBoss(CtrlDerroArtisan):
	def dying(self, attachee, triggerer):
		utils_item.item_create_in_inventory(12881, attachee)
		return toee.RUN_DEFAULT

class CtrlSuccubus(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14954

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		npc.condition_add_with_args("Spell_DC_Mod", toee.spell_charm_monster, 10) # should yield 22
		npc.condition_add_with_args("Spell_DC_Mod", toee.spell_suggestion, 9) # should yield 21

		# create inventory
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_LEATHER_CLOTHING, npc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_BOOTS_PADDED_RED, npc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_GLOVES_PADDED_RED, npc)
		npc.item_wield_best_all()
		return

	def enter_combat(self, attachee, triggerer):
		self.spells = utils_npc_spells.NPCSpells()
		self.spells.add_spell(toee.spell_charm_monster, toee.domain_special, 4, 2)
		#self.spells.add_spell(toee.spell_suggestion, toee.domain_special, 4) problem - 466 is replaced by dominate monster. leave it be for now
		self.spells.add_spell(const_toee.spell_summon_vrock, toee.domain_special, 4)
		return toee.RUN_DEFAULT

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None

		foes = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_all())
		foes.measures.measure_stat_save_willpower = 1
		foes.rescan()
		threats = foes.get_threats()
		print("threats: {}".format(threats))

		while (not tac):
			if (self.spells.get_spell_count(toee.spell_charm_monster)): 
				targets = foes.get_charm_candidates()
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				if (threats):
					tac.add_five_foot_step()
				if (targets):
					tac.add_target_obj(targets[0].target.id)
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_charm_monster))
				tac.add_halt()
				tac.add_total_defence()
				break

			if (self.spells.get_spell_count(toee.spell_suggestion)): 
				targets = foes.get_charm_candidates()
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				if (threats):
					tac.add_five_foot_step()
				if (targets):
					tac.add_target_obj(targets[0].target.id)
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_suggestion))
				tac.add_halt()
				tac.add_total_defence()
				break

			if (self.spells.get_spell_count(const_toee.spell_summon_vrock)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				if (threats):
					tac.add_five_foot_step()
				
				self.spells.prep_spell(npc, const_toee.spell_summon_vrock)
				tac.add_cast_single_code("'Summon Vrock (INTERNAL)' domain_special 4")
				tac.add_halt()
				tac.add_total_defence()
				break

			break
		return tac

class CtrlMezzoloth(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14955

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		npc.condition_add_with_args("Spell_DC_Mod", toee.spell_cloudkill, 7) # should yield 17

		# create inventory
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_TRIDENT_PLUS_1, npc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_LARGE_STEEL, npc)
		npc.item_wield_best_all()
		return

	def enter_combat(self, attachee, triggerer):
		self.spells = utils_npc_spells.NPCSpells()
		self.spells.add_spell(toee.spell_cloudkill, toee.domain_special, 4)
		return toee.RUN_DEFAULT

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None

		foes = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_all())
		foes.measures.measure_stat_save_willpower = 1
		foes.rescan()
		threats = foes.get_threats()
		print("threats: {}".format(threats))

		while (not tac):
			if (self.spells.get_spell_count(toee.spell_cloudkill)): 
				targets = foes.get_charm_candidates()
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_self()
				if (threats):
					tac.add_five_foot_step()
				if (targets):
					tac.add_target_obj(targets[0].target.id)
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_cloudkill))
				tac.add_halt()
				tac.add_total_defence()
				break
			break
		return tac

class CtrlGnollWarchief(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14956

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters

		#npc.condition_add_with_args("Rapid_Shot", 1)
		#npc.condition_add_with_args("Rapid_Shot_Ranger", 1)
		npc.obj_set_idx_int(toee.obj_f_critter_level_idx, 0, toee.stat_level_ranger)
		npc.obj_set_idx_int(toee.obj_f_critter_level_idx, 1, toee.stat_level_ranger)
		npc.obj_set_idx_int(toee.obj_f_critter_level_idx, 2, toee.stat_level_ranger)
		npc.obj_set_idx_int(toee.obj_f_critter_level_idx, 3, toee.stat_level_ranger)
		npc.obj_set_idx_int(toee.obj_f_critter_level_idx, 4, toee.stat_level_ranger)
		npc.obj_set_idx_int(toee.obj_f_critter_level_idx, 5, toee.stat_level_blackguard)
		npc.obj_set_idx_int(toee.obj_f_critter_level_idx, 6, toee.stat_level_blackguard)
		npc.obj_set_idx_int(toee.obj_f_critter_level_idx, 7, toee.stat_level_blackguard)

		npc.feat_add(toee.feat_favored_enemy_humanoid_elf, 1)
		utils_npc.npc_generate_hp(npc)

		Monster_Ranged_Poison_poison_id = 5 # Large Scorpion
		Monster_Ranged_Poison_duration = 10
		Monster_Ranged_Poison_dc = 10
		Monster_Ranged_Poison_arrows = 12
		npc.condition_add_with_args("Monster_Ranged_Poison", Monster_Ranged_Poison_poison_id, Monster_Ranged_Poison_duration, Monster_Ranged_Poison_dc, Monster_Ranged_Poison_arrows) 

		# create inventory
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_LONGBOW_COMPOSITE_16_PLUS1, npc)
		item = utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(toee.obj_f_ammo_quantity, 40)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_FALCHION_PLUS_1, npc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_CHAINMAIL_MITHRAL_PLUS_1, npc)
		utils_item.item_create_in_inventory(const_proto_items.PROTO_WONDROUS_GAUNTLETS_OF_OGRE_POWER, npc)
		npc.item_wield_best_all()
		return

class CtrlGnollHezrou(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14259

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		npc.condition_add_with_args("Spell_DC_Mod", toee.spell_chaos_hammer, 6) # should yield 18

		npc.condition_add_with_args("No_Move", -1, 0)
		return
	
	def enter_combat(self, attachee, triggerer):
		self.spells = utils_npc_spells.NPCSpells()
		self.spells.add_spell(toee.spell_chaos_hammer, toee.domain_special, 5, 10)
		self.spells.add_spell(const_toee.spell_hezrou_stench, toee.domain_special, 5)

		#script A20
		attachee.condition_add_with_args("sp-Summoned", 0, 4)
		attachee.condition_add_with_args("Timed-Disappear", 0, 4)
		return toee.RUN_DEFAULT

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None

		foes = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_all())
		foes.rescan()
		threats = foes.get_threats()
		print("threats: {}".format(threats))

		while (not tac):
			if (self.spells.get_spell_count(const_toee.spell_hezrou_stench)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				#tac.add_target_self()
				if (threats):
					tac.add_five_foot_step()
				if (threats):
					tac.add_target_obj(threats[0].target.id)
				tac.add_cast_single_code(self.spells.prep_spell(npc, const_toee.spell_hezrou_stench))
				tac.add_halt()
				tac.add_total_defence()
				break

			if (threats):
				break # do default

			if (self.spells.get_spell_count(toee.spell_chaos_hammer)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				#tac.add_target_self()
				if (threats):
					tac.add_five_foot_step()
				if (threats):
					tac.add_target_obj(threats[0].target.id)
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_chaos_hammer))
				tac.add_halt()
				tac.add_total_defence()
				break
			break
		return tac

	def dying(self, attachee, triggerer):
		toee.game.global_flags[shattered_consts.GLOBAL_FLAG_WARCHIEF_KILLED] = 1
		utils_item.item_create_in_inventory(12882, attachee)
		return toee.RUN_DEFAULT
