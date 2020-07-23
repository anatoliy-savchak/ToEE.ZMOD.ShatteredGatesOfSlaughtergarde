import toee, debug, tpdp, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour
import const_proto_potions, utils_obj, const_proto_food, utils_npc, utils_target_list, const_proto_wands, utils_sneak, const_deseases, utils_npc_spells, utils_npc
import py06401_shattered_temple_encounters

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
		utils_item.item_create_in_inventory(const_proto_food.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, npc)
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
			tac = utils_tactics.TacticsHelper(self.get_name())
			if (not is_raged):
				tac.add_rage()
			tac.add_clear_target()
			tac.add_target_closest()
			tac.add_target_damaged()
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

		# create inventory
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_FLIND_PLUS1, npc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_WOODEN_LARGE_PLUS_1, npc)
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
		utils_item.item_create_in_inventory(4090, npc) # Hill Giant Club
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_HIDE_MASTERWORK, npc)
		npc.item_wield_best_all()

		npc.feat_add(toee.feat_sunder, 1)
		return

class CtrlHalfFiendOgre(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14941

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_armory_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_armory_encounters
		#npc.scripts[const_toee.sn_will_kos] = shattered_armory_encounters

		## create inventory
		#utils_item.item_create_in_inventory(4090, npc) # Hill Giant Club
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE_PLUS_1_BLACK, npc)
		npc.item_wield_best_all()
		return
