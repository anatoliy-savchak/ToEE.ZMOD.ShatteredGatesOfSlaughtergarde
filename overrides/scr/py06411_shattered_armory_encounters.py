import toee, debug, tpdp, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour
import const_proto_potions, utils_obj, const_proto_food, utils_npc, utils_target_list, const_proto_wands, utils_sneak, const_deseases, utils_npc_spells, utils_npc

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
		#attachee.condition_add_with_args("Barbarian_Raged", 0, 0)
		#attachee.obj_set_int(toee.stat_hp_current, 15)
		if (utils_npc.npc_hp_current_percent(attachee) > 90):
			print("BOOOOOOOOOOOOOOOOOOOOM")
			attachee.damage(attachee, toee.D20DT_BLUDGEONING, toee.dice_new("5d10"), 0, 0)
		attachee.condition_add_with_args("Close_Door")
		return toee.RUN_DEFAULT


	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None
		is_raged = npc.d20_query(toee.Q_Barbarian_Raged)

		close_the_door = None
		#if (toee.game.combat_turn == 1):
		#	close_the_door = self.get_var("close_the_door")

		door = None
		for obj in toee.game.obj_list_vicinity(utils_obj.sec2loc(421, 522), toee.OLC_PORTAL):
			if (obj.name == 920): #{920}{Door A1}
				door = obj
				break
		isOpen = None
		isJammed = None
		isLocked = None
		if (door):
			isOpen = door.portal_flags_get() & toee.OPF_OPEN
			isJammed = door.portal_flags_get() & toee.OPF_JAMMED
			isLocked = door.portal_flags_get() & toee.OPF_LOCKED

		print("door: {}, open: {}, jammed: {}, locked: {}".format(door, isOpen, isJammed, isLocked))
		tag = self.get_var("tag")
		if (not tag): tag = 0
		hp = utils_npc.npc_hp_current(npc)
		locx, locy = utils_obj.loc2sec(npc.location)
		print("npc location ({}, {}), hp: {}, tag: {}".format(locx, locy, hp, tag))
		while (not tac):
			if (hp < 20 and locx < 422 and not isLocked):
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				tac.add_goto_loc(utils_obj.sec2loc(424, 519 + tag*2))
				tac.add_use_potion()
				tac.add_ready_vs_approach()
				tac.add_halt()
				break

			if (locx > 421 and door and not isLocked):
				print("closing the door")
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_obj(door.id)
				tac.add_approach_single()
				tac.add_halt()
				tac.add_python_action(3015)
				break

			if (locx > 421 and door and not isLocked):
				print("barricading the door")
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_obj(door.id)
				tac.add_approach_single()
				tac.add_halt()
				tac.add_python_action(3016)
				break

			if (locx > 445 and door and isLocked):
				print("ai_stop_attacking")
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				tac.add_halt()
				tac.add_total_defence()
				npc.ai_stop_attacking()
				npc.critter_flag_set(toee.OCF_FLEEING)
				break

			if (locx > 421 and door and isLocked):
				print("FLEE_COMBAT")
				tac = utils_tactics.TacticsHelper(self.get_name())
				beakon = utils_npc.npc_find_nearest_pc_loc(utils_obj.sec2loc(453, 521), 10)
				tac.add_clear_target()
				if (beakon):
					print("D20A_FLEE_COMBAT to beakon: {}".format(beakon))
					tac.add_target_obj(beakon.id)
					tac.add_d20_action(toee.D20A_FLEE_COMBAT, 0)
				else:
					#tac.add_goto_loc(utils_obj.sec2loc(458, 519 + tag*2))
					tac.add_d20_action(toee.D20A_FLEE_COMBAT, utils_obj.sec2loc(458, 519 + tag*2))
				break

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
