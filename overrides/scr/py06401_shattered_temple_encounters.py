import toee, debug, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour, const_proto_potions, utils_obj, const_proto_food, utils_npc, utils_target_list

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
		dagger = npc.item_find_by_proto(MONK_THROW_WEAPON)
		if (dagger): 
			npc.item_wield(dagger, toee.item_wear_weapon_primary)
			tac = utils_tactics.TacticsHelper(self.get_name())
			#tac.add_five_foot_step()
			tac.add_target_closest()
			tac.add_halt()
			tac.add_attack()
			tac.add_total_defence()
			tac.add_halt()
		else:
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_clear_target()
			tac.add_target_closest()
			tac.add_use_potion()
			tac.add_d20_action(toee.D20A_STUNNING_FIST, 0)
			tac.add_attack()
			tac.add_approach()
			tac.add_attack()
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

class CtrlArcaneGuard(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls):
		return 14920

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		# assign scripts
		utils_obj.obj_scripts_clear(npc)
		npc.scripts[const_toee.sn_start_combat] = shattered_temple_encounters
		npc.scripts[const_toee.sn_enter_combat] = shattered_temple_encounters
		# create inventory
		utils_item.item_create_in_inventory(const_proto_food.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, npc)
		#utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_FIREBALL, npc)

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_MITHRAL_SHIRT, npc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_SPIKED_CHAIN_MASTERWORK, npc)
		npc.item_wield_best_all()
		npc.condition_add_with_args("AI_Improved_Trip_Aoo", 0, 0)
		#npc.condition_add_with_args("Fighting_Defensively_Monster", 0, 0)
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

			if (self.spells.get_spell_count(toee.spell_fireball)): 
				tac = utils_tactics.TacticsHelper(self.get_name())
				#tac.add_five_foot_step()
				tac.add_target_closest()
				tac.add_halt()
				tac.add_cast_fireball_code(self.spells.prep_spell(npc, toee.spell_fireball))
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
				tac.add_use_item(healing_potion.id)
				tac.add_total_defence()
				break

			
			best_target = None
			d20Action = toee.D20A_DISARM
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
						if (atarget.measures.value_prone): d20Action = 0
						best_target = atarget.target
				#else: print("none found")

			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_clear_target()
			if (best_target):
				tac.add_target_obj(best_target.id)
			else:
				tac.add_target_closest()
				tac.add_target_threatened() # if not then closest
			if (d20Action):
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

		# special as scroll
		self.spells.add_spell(toee.spell_fireball, stat_class, 3)

		#attachee.item_worn_unwield(toee.item_wear_weapon_primary, 1)
		return toee.RUN_DEFAULT

	def revealed(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		#print("Wizard trying to cast shield...")
		utils_npc.npc_spell_ensure(npc, toee.spell_shield, toee.stat_level_wizard, 1)
		npc.cast_spell(toee.spell_shield, npc)
		return
