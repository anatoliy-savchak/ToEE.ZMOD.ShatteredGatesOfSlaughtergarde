import toee, debug, tpdp, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour, const_proto_potions, utils_obj, const_proto_food, utils_npc, utils_target_list, const_proto_wands

shattered_temple_encounters = 6401

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

MONK_THROW_WEAPON = const_proto_weapon.PROTO_WEAPON_JAVELIN
MONK_THROW_WEAPON = const_proto_weapon.PROTO_WEAPON_DAGGER_THROWING
class CtrlDoomFistMonk(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls):
		return 14919

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		# assign scripts
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_temple_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_temple_encounters
		# create inventory
		utils_item.item_create_in_inventory(const_proto_food.PROTO_POTION_OF_MAGE_ARMOR, npc)
		utils_item.item_create_in_inventory(const_proto_food.PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		utils_item.item_create_in_inventory(MONK_THROW_WEAPON, npc)
		npc.item_wield_best_all()
		#npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)
		return

	def enter_combat(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("CtrlDoomFistMonk::enter_combat {}".format(attachee))
		opt = toee.game.random_range(1, 2)
		message = None
		if (opt == 1):
			message = "You just made a big mistake!"
		elif (opt == 2):
			message = "We don't like your kind around here!"

		if (message):
			attachee.float_text_line(message, toee.tf_red)
		return toee.RUN_DEFAULT

	def UsePotion(self, attachee):
		potion = attachee.item_find_by_proto(const_proto_food.PROTO_POTION_OF_MAGE_ARMOR)
		print("potion: {}".format(potion))
		if (potion):
			attachee.use_item(potion)
			potion.destroy()
		return

	def revealed(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		if (npc):
			self.UsePotion(npc)
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None
		melees = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_melee()).rescan()
		dagger = npc.item_find_by_proto(MONK_THROW_WEAPON)
		healing_potion = npc.item_find_by_proto(const_proto_food.PROTO_POTION_OF_CURE_LIGHT_WOUNDS)
		while (1):
			if (dagger): 
				print("dagger option, value_range_is_within_melee: {}".format(melees.aggr.value_range_is_within_melee))
				if (melees.aggr.value_range_is_within_melee == 0): 
					npc.item_wield(dagger, toee.item_wear_weapon_primary)
					tac = utils_tactics.TacticsHelper(self.get_name())
					#tac.add_five_foot_step()
					tac.add_target_closest()
					tac.add_halt()
					tac.add_attack()
					tac.add_total_defence()
					tac.add_halt()
					break

			leader = None
			if (healing_potion and utils_npc.npc_hp_current_percent(npc) <= 50):
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				tac.add_target_self()
				tac.add_use_item(healing_potion.id)
				#leader = utils_npc.find_npc_by_proto(14920)
				if (leader is None): leader = npc.leader_get()
				if (leader):
					tac.add_target_obj(leader.id)
				tac.add_d20_action(toee.D20A_FLEE_COMBAT, 0)
				#tac.add_total_defence()
				break

			if (healing_potion):
				if (leader is None): leader = npc.leader_get()
				print("checking leader to be healed. Leader: {}".format(leader))
				if (leader):
					leader_hp_perc = utils_npc.npc_hp_current_percent(leader)
					hp = leader.stat_level_get(toee.stat_hp_current)
					print("Leader hp%: {}, hp: {}".format(leader_hp_perc, hp))
					if (leader_hp_perc <= 50 and hp > -10):
					#if (1):
						print("go and heal")
						tac = utils_tactics.TacticsHelper(self.get_name())
						tac.add_target_obj(leader.id)
						tac.add_approach()
						tac.add_use_item(healing_potion.id)
						tac.add_total_defence()
						tac.add_halt()
				break

			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_clear_target()
			tac.add_target_closest()
			tac.add_use_potion()
			tac.add_d20_action(toee.D20A_STUNNING_FIST, 0)
			tac.add_attack()
			tac.add_approach()
			tac.add_attack()
			break
		return tac

def CtrlArcaneGuard_measures_cmp(x, y):
	assert isinstance(x, utils_target_list.AITarget)
	assert isinstance(y, utils_target_list.AITarget)
	#print("Comparing x: {} vs y: {}".format(x.target, y.target))
	#print("Comparing x: {}".format(x))
	#print("Comparing y: {}".format(y))
	if (x.measures.value_stat_hp < 0): 
		#print("return -1, as x.measures.value_stat_hp < 0 :: {}".format(x.measures.value_stat_hp))
		return -1 # skip dying dude
	if (y.measures.value_stat_hp < 0): 
		#print("return 1, as y.measures.value_stat_hp < 0 :: {}".format(y.measures.value_stat_hp))
		return 1 # skip dying dude

	if (not x.measures.value_weapon_melee and y.measures.value_weapon_melee): 
		#print("-1 skip weaponless dude (value_weapon_melee), x: {} vs y: {}".format(x.measures.value_weapon_melee, y.measures.value_weapon_melee))
		return -1 # skip weaponless dude
	if (x.measures.value_weapon_melee and not y.measures.value_weapon_melee): 
		#print("1 skip weaponless right dude (value_weapon_melee), x: {} vs y: {}".format(x.measures.value_weapon_melee, y.measures.value_weapon_melee))
		return 1 # skip weaponless right dude

	if (x.measures.value_prone and not x.measures.value_weapon_melee and not y.measures.value_weapon_melee):
		return 1
	if (y.measures.value_prone and not y.measures.value_weapon_melee and not x.measures.value_weapon_melee):
		return -1

	result = y.measures.value_stat_ac - x.measures.value_stat_ac
	#print("result: {}".format(result))
	return result

ARCANE_GUARD_SLEEP = toee.spell_deep_slumber
ARCANE_GUARD_SLEEP_SCROLL_PROTO = const_proto_scrolls.PROTO_SCROLL_OF_DEEP_SLUMBER
#ARCANE_GUARD_SLEEP_SCROLL_PROTO = const_proto_scrolls.PROTO_SCROLL_OF_SLEEP
class CtrlArcaneGuard(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls):
		return 14920

	def __init__(self):
		super(CtrlArcaneGuard, self).__init__()
		self.guard_ai_type = 0
		self.fire_epicenter = 0
		return

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		# assign scripts
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_temple_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_temple_encounters
		# create inventory
		utils_item.item_create_in_inventory(const_proto_food.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, npc)

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_MITHRAL_SHIRT, npc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SPIKED_CHAIN_MASTERWORK, npc)
		if (self.guard_ai_type == 0):
			utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_FIREBALL, npc)
		elif (self.guard_ai_type == 2):
			utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_FIREBALL, npc)
			pass
		elif (self.guard_ai_type == 3):
			#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_FIREBALL, npc)
			utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_MAGIC_MISSILES_1ST, npc)
			#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_DEEP_SLUMBER, npc)
			#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_SLEEP, npc)
			utils_item.item_create_in_inventory(ARCANE_GUARD_SLEEP_SCROLL_PROTO, npc)

		npc.item_wield_best_all()
		npc.condition_add_with_args("AI_Improved_Trip_Aoo", 0, 0)

		# attempt to disable combat casting, unsuccessful
		npc.d20_send_signal("Cast_Defensively_Remove")
		npc.d20_send_signal(toee.EK_S_Resurrection-toee.EK_S_HP_Changed, npc)
		npc.d20_send_signal(toee.EK_S_SetCastDefensively-toee.EK_S_HP_Changed, 1)
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None
		healing_potion = npc.item_find_by_proto(const_proto_food.PROTO_POTION_OF_CURE_MODERATE_WOUNDS)
		primary_weapon = npc.item_worn_at(toee.item_wear_weapon_primary)
		while (not tac):
			if (not primary_weapon):
				for obj in toee.game.obj_list_vicinity(npc.location, toee.OLC_WEAPON):
					if (obj.proto == const_proto_weapon.PROTO_WEAPON_SPIKED_CHAIN_MASTERWORK):
						primary_weapon = obj
						break
				if (primary_weapon):
					tac = utils_tactics.TacticsHelper(self.get_name())
					tac.add_clear_target()
					tac.add_target_obj(primary_weapon.id)
					tac.add_d20_action(toee.D20A_DISARMED_WEAPON_RETRIEVE, 0)
					tac.add_total_defence()
					break

			if (self.spells.get_spell_count(ARCANE_GUARD_SLEEP)): 
				#debug.breakp("spell_deep_slumber")
				tac = utils_tactics.TacticsHelper(self.get_name())
				#tac.add_five_foot_step()
				tac.add_target_closest()
				#tac.add_halt()
				tac.add_cast_area_code(self.spells.prep_spell(npc, ARCANE_GUARD_SLEEP))
				break

			if (self.spells.get_spell_count(toee.spell_fireball)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				#tac.add_five_foot_step()
				tac.add_target_closest()
				if (self.guard_ai_type == 2):
					trg, dist = utils_target_list.find_pc_closest_to_origin(utils_obj.sec2loc(434, 493))
					if (trg and dist <= 15):
						tac.add_target_obj(trg.id)
				tac.add_halt()
				#tac.add_cast_fireball_code(self.spells.prep_spell(npc, toee.spell_fireball))
				tac.add_cast_area_code(self.spells.prep_spell(npc, toee.spell_fireball))
				print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!CAST FIREBALL")
				break

			if (1): 
				scroll = npc.item_find_by_proto(const_proto_scrolls.PROTO_SCROLL_OF_FIREBALL)
				if (scroll):
					tac = utils_tactics.TacticsHelper(self.get_name())
					#tac.add_five_foot_step()
					tac.add_target_closest()
					print("self.fire_epicenter: {}".format(self.fire_epicenter))
					if (self.fire_epicenter):
						trg, dist = utils_target_list.find_pc_closest_to_origin(self.fire_epicenter)
						print("find_pc_closest_to_origin: {}, {}".format(trg, dist))
						if (trg and dist <= 15):
							tac.add_target_obj(trg.id)
					tac.add_halt()
					tac.add_use_item(scroll.id)
					break
			
			if (1): 
				scroll = npc.item_find_by_proto(ARCANE_GUARD_SLEEP_SCROLL_PROTO)
				if (scroll):
					tac = utils_tactics.TacticsHelper(self.get_name())
					#tac.add_five_foot_step()
					tac.add_target_closest()
					print("looking for good target for sleep")
					print("self.fire_epicenter: {}".format(self.fire_epicenter))
					if (self.fire_epicenter):
						trg, dist = utils_target_list.find_pc_closest_to_origin(self.fire_epicenter)
						print("find_pc_closest_to_origin: {}, {}".format(trg, dist))
						if (trg and dist <= 15):
							tac.add_target_obj(trg.id)
					#tac.add_halt()
					tac.add_use_item(scroll.id)
					break

			if (self.spells.get_spell_count(toee.spell_ray_of_enfeeblement)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				#tac.add_five_foot_step()
				tac.add_target_closest()
				tac.add_halt()
				tac.add_cast_single_code(self.spells.prep_spell(npc, toee.spell_ray_of_enfeeblement))
				break

			if (healing_potion and utils_npc.npc_hp_current_percent(npc) <= 50):
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_clear_target()
				tac.add_target_self()
				tac.add_use_item(healing_potion.id)
				tac.add_total_defence()
				break

			
			best_target = None
			d20Action = toee.D20A_DISARM
			melees = None
			if (1):
				#print("checking AITargetList...")
				melees = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_melee()).rescan()
				if (melees and melees.list and len(melees.list)):
					#print("found {}, sorting".format(len(melees.list)))
					print(melees)
					list2 = sorted(melees.list, cmp = CtrlArcaneGuard_measures_cmp, reverse = True)
					if (list2):
						for i in list2: print(i)
						atarget = list2[0]
						print("found atarget: {}".format(atarget))
						print("found target: {}".format(atarget.target))
						assert isinstance(atarget, utils_target_list.AITarget)
						if (atarget.measures.value_prone): 
							d20Action = 0
						elif (not melees.aggr.value_weapon_melee):
							d20Action = 0
						best_target = atarget.target
				#else: print("none found")

			wand = None
			if (self.guard_ai_type == 3 and not best_target):
				wand = npc.item_find_by_proto(const_proto_wands.PROTO_WAND_OF_MAGIC_MISSILES_1ST)

			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_clear_target()
			if (best_target):
				tac.add_target_obj(best_target.id)
			else:
				#tac.add_target_threatened() # if not then closest
				tac.add_target_closest()
			if (wand and (melees and not melees.aggr.value_range_is_within_melee)):
				tac.add_halt()
				tac.add_use_item(wand.id)
			elif (d20Action):
				tac.add_d20_action(d20Action, 0)
			tac.add_attack()
			tac.add_approach()
			tac.add_attack()
			tac.add_total_defence()
			break
		#debug.breakp("create_tactics2")
		return tac

	def enter_combat(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		stat_class = toee.stat_level_wizard
		caster_level = 1
		# 1
		#self.spells.add_spell(toee.spell_shield, stat_class, caster_level)
		self.spells.add_spell(toee.spell_ray_of_enfeeblement, stat_class, caster_level)

		print("{}.guard_ai_type: {}".format(attachee, self.guard_ai_type))
		#debug.breakp("enter_combat")
		# special as scroll
		if (self.guard_ai_type == 0):
			pass
			#self.spells.add_spell(toee.spell_fireball, stat_class, 3)
		elif (self.guard_ai_type == 2):
			pass
			#self.spells.add_spell(toee.spell_fireball, stat_class, 3)
		elif (self.guard_ai_type == 3):
			#self.spells.add_spell(ARCANE_GUARD_SLEEP, stat_class, 3)
			pass

		if (self.guard_ai_type == 2):
			attachee.move(utils_obj.sec2loc(428, 493))

		#attachee.item_worn_unwield(toee.item_wear_weapon_primary, 1)
		return toee.RUN_DEFAULT

	def revealed(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		#print("Wizard trying to cast shield...")
		utils_npc.npc_spell_ensure(npc, toee.spell_shield, toee.stat_level_wizard, 1)
		npc.cast_spell(toee.spell_shield, npc)
		return

class CtrlQuaggoth(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14921

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		# assign scripts
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_temple_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_temple_encounters
		#npc.scripts[const_toee.sn_hit] = shattered_temple_encounters
		#npc.scripts[const_toee.sn_miss] = shattered_temple_encounters
		#npc.scripts[const_toee.sn_critter_hits] = shattered_temple_encounters
		#npc.scripts[const_toee.sn_critical_hit] = shattered_temple_encounters
		# create inventory
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GREATCLUB, npc)
		npc.item_wield_best_all()
		#npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)
		return

	def enter_combat(self, attachee, triggerer):
		assert isinstance(attachee, toee.PyObjHandle)
		print("{}::enter_combat {}".format(type(self).__name__, attachee))

		attachee.turn_towards(toee.game.leader)
		messages = ("I'm gonna pin your ears back!", "Fresh meat!", "You just made my day!", "You're gonna be my bitch!", "I'm gonna pin your ears back!", "I'm gonna settle your hash!")
		opt = toee.game.random_range(0, len(messages)-1)
		message = messages[opt]
		if (message):
			attachee.float_text_line(message, toee.tf_yellow)
		return toee.RUN_DEFAULT

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None
		is_raged = npc.d20_query(toee.EK_Q_Barbarian_Raged - toee.EK_Q_Helpless)
		go_rage = 0
		if (not is_raged):
			if (toee.game.random_range(1, 6) == 1):
				go_rage = 1
		#go_rage = 1
		if (go_rage):
			npc.condition_add_with_args("Barbarian_Raged", 0, 0)

		tac = utils_tactics.TacticsHelper(self.get_name())
		tac.add_clear_target()
		tac.add_target_closest()
		#tac.add_target_damaged()
		tac.add_attack()
		tac.add_ready_vs_approach()
		tac.add_approach()
		tac.add_attack()
		tac.add_total_defence()
		tac.add_halt()
		return tac

class CtrlGargoyle(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14239

class CtrlDrowZombie(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14922

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		# assign scripts
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_temple_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_temple_encounters
		# create inventory
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD, npc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_HALF_PLATE, npc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_STEEL_SMALL, npc)
		npc.item_wield_best_all()
		return

class CtrlDrowZombieDesicrate(CtrlDrowZombie):
	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlDrowZombieDesicrate, self).created(npc)
		npc.condition_add_with_args("Initiative_Bonus", 30, 0)
		return

	def activated(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		desecrate_potion = utils_item.item_create_in_inventory(8600, npc)
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		desecrate_potion = npc.item_find_by_proto(8600)
		print("Find desecrate potion {}, self.desicrate: {} ".format(desecrate_potion, npc))
		if (desecrate_potion):
			#debug.breakp("desecrate")
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_clear_target()
			tac.add_target_self()
			tac.add_use_item(desecrate_potion.id)
			tac.add_total_defence()
			return tac
		return None

class CtrlDireBat(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14923

class CtrlWererat(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14924

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlWererat, self).created(npc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_RAPIER, npc)
		#utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		npc.item_wield_best_all()
		return

class CtrlGaranaach(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14925

	def __init__(self):
		super(CtrlGaranaach, self).__init__()
		self.next_breath_weapon_2_skip = 0
		return

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		super(CtrlGaranaach, self).created(npc)
		# assign scripts
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_temple_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_temple_encounters

		npc.condition_add_with_args("Line_Of_Acid", 40, 4, 16)
		return

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None
		self.next_breath_weapon_2_skip -= 1
		if (self.next_breath_weapon_2_skip <= 0):
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_clear_target()
			tac.add_target_closest()
			tac.add_halt()
			tac.add_python_action(3010)
			tac.add_ready_vs_approach()
			self.next_breath_weapon_2_skip = toee.game.random_range(1, 4)
			print("next_breath_weapon_2_skip: {}".format(self.next_breath_weapon_2_skip))
		return tac

	def start_combat1(self, attachee, triggerer):
		super(CtrlGaranaach, self).start_combat(attachee, triggerer)
		#for pc in toee.game.party:
		#	pc.condition_add("Surprised")
		return