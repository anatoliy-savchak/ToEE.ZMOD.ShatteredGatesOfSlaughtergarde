class PyObjHandle(object):
	"""Mobile object"""

	def __init__(self, dummy = 0):
		self.area = 1	#	Gets the id of the current area, which is based on the current map.
		self.char_classes = (stat_level_barbarian, stat_level_wizard)	#	a tuple containing the character classes array
		self.highest_arcane_class = 1	#	Highest Arcane spell casting class
		self.highest_divine_class = 1	#	Highest Divine spell casting class
		self.highest_arcane_caster_level = 1	#	Highest Arcane caster level
		self.highest_divine_caster_level = 1	#	Highest Divine caster level
		self.description = ""	#	Gets description display name
		self.name = 1	#	GetNameId
		self.location = 9223372036854775807	#	Gets location LongLong
		self.location_full	= object()	#	Gets location tpdp.LocAndOffsets
		self.type = obj_t_npc	#	Gets obj_f type like obj_t_npc
		self.radius = 1.1	#	Gets and Sets radius
		self.height = 1.1	#	Gets and Sets RenderHeight double
		self.rotation = 1.1	#	Gets and Sets rotation double
		self.map = 1	#	Gets current map id
		self.hit_dice = PyDice()	#	Gets GetHitDice
		self.hit_dice_num = 1	#	Gets GetHitDiceNum
		self.get_size = 1	#	Gets GetSize
		self.off_x = 1.1	#	Gets GetOffsetX double
		self.off_y = 1.1	#	Gets GetOffsetY double
		#	Gets and Sets obj_script[38] = 1234
		#self.scripts = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A]	
		self.scripts = PyObjScripts()
		self.origin= 1	#	GetOriginMapId	SetOriginMapId
		if (1 == 2):
			self.substitute_inventory = PyObjHandle()	#	Gets and Sets object inventory substitute
		self.factions = [0, 1]	#	Gets object factions tuple
		self.feats = [0, 1]	#	Gets object feats tuple
		self.spells_known = [PySpell(), PySpell()]	#	Gets spells known
		self.spells_memorized = [PySpell(), PySpell()]	#	Gets spells memorized
		self.loots = 1	#	Gets and Sets LootBehaviour
		self.proto = 1	#	GetProtoId
		self.id = "G_123456"

		#helpers
		self.__state = "(2, (1880286368, 14202, 17600, (132, 111, 66, 228, 212, 83, 245, 5)))"
		return

	def __getstate__(self):
		return self.__state

	def __reduce__(self):
		pickledValue = __getstate__(self)
		return [PyObjHandle, None, pickledValue]
	
	def __setstate__(self, pickledData):
		self.__state = pickledData
		return

	def add_to_initiative(self):
		""" Adds self to initiative (combat). pc.add_to_initiative() -> none"""
		return

	def ai_flee_add(self):
		""" Adds self to flee from target. npc.ai_flee_add(PyObjHandle: target) -> none"""
		return

	def ai_follower_add(self):
		""" Adds follower to pc. pc.ai_follower_add(PyObjHandle: follower) -> int"""
		return 0

	def ai_follower_remove(self):
		""" Do not use!"""
		return 0

	def ai_follower_atmax(self):
		""" Do not use!"""
		return 0

	def ai_shitlist_add(self):
		""" 0x1005CC10::NpcAiListAppend. Probably favored enemy?"""
		return 0

	def ai_shitlist_remove(self):
		""" Stop attacking?"""
		return

	def ai_strategy_set_custom(self, triplets, save = 1):
		""" npc.ai_strategy_set_custom(tuple: triplets, int: save = 1) -> none"""
		return

	def allegiance_shared(self, target):
		""" npc.allegiance_shared(PyObjHandle: triplets) -> int"""
		return 0
	
	def anim_goal_push_attack(self, tgt, anim_idx, is_crit, is_secondary):
		""" npc.anim_goal_push_attack(PyObjHandle: tgt, anim_idx, is_crit, is_secondary) -> int"""
		return

	def anim_goal_use_object(self, target, goal_type = 40, target_loc = None, some_flag = None):
		""" npc.anim_goal_use_object(PyObjHandle: target, int: goal_type = 40, int: target_loc = None, int: some_flag = None) -> int"""
		return

	def anim_goal_get_new_id(self):
		return 0

	def ai_stop_attacking(self):
		""" npc.ai_stop_attacking() -> None"""
		return

	def anim_goal_interrupt(self):
		""" npc.anim_goal_interrupt() -> None"""
		return

	def attack(self, target):
		""" npc.attack(PyObjHandle: target) -> None"""
		return

	def award_experience(self, xp_awarded):
		""" pc.award_experience(int: xp_awarded) -> None"""
		return

	def begin_dialog(self, target, line):
		"""Schedules a Python dialog time event in 1ms. pc.begin_dialog(PyObjHandle: target, int: line) -> none"""
		return

	def can_sneak_attack(self, target):
		"""npc.can_sneak_attack(PyObjHandle: target) -> int
		Check for:
			self (Sneak Attack Dice) e.g. rogue, otherwise 0
			target DK_QUE_Critter_Is_Immune_Critical_Hits, otherwise 0
			self.CanSense(target), otherwise 0
				self.CanSeeWithBlindsight(target) or
					target.DK_QUE_Critter_Is_Invisible vs self.DK_QUE_Critter_Can_See_Invisible and
					not self.DK_QUE_Critter_Is_Blinded and
					not target.IsConcealed() and
					not target.IsMovingSilently() and 
					not oldCanSense(distance check base hide vs base spot)
		"""
		return 1

	def can_see(self, target):
		return 0

	def can_sense(self, target):
		return 0

	def can_find_path_to_obj(self, target, flags):
		"""npc.can_find_path_to_obj(PyObjHandle: target, int: flags) -> int[ft]"""
		return
	
	def critter_flags_get(self):
		"""npc.critter_flags_get() -> OCF_IS_CONCEALED"""
		return

	def critter_flag_set(self, flag):
		"""npc.critter_flag_set(int[OCF_IS_CONCEALED...]: flag) -> None"""
		return

	def critter_flag_unset(self, flag):
		"""npc.critter_flag_unset(int[OCF_IS_CONCEALED...]: flag) -> None"""
		return
	
	def critter_kill(self):
		""" killed by no one """
		return
	
	def critter_kill_by_effect(self, killer = None):
		"""npc.critter_kill_by_effect(PyObjHandle: killer = None) -> None"""
		return

	def concealed_set(self, concealed):
		"""npc.concealed_set(int: concealed) -> None"""
		return

	def condition_add(self, cond_name):
		""" npc.condition_add(str: cond_name) -> int"""
		return 0

	def condition_add_with_args(self, cond_name, arg0 = None, arg1 = None, arg2 = None):
		""" npc.condition_add_with_args(str: cond_name, int: arg0 = None, int: arg1 = None, int: arg2 = None) -> int"""
		return 0

	def conditions_get(self, kind = None):
		result = [("condition name", 2)]
		return

	def container_flags_get(self):
		"""npc.container_flags_get() -> OCOF_LOCKED"""
		return

	def container_flag_set(self, flag):
		"""npc.container_flag_set(int[OCOF_LOCKED...]: flag) -> None"""
		return

	def container_flag_unset(self, flag):
		"""npc.container_flag_unset(int[OCOF_LOCKED...]: flag) -> None"""
		return

	def container_toggle_open(self):
		"""door.container_toggle_open() -> None"""
		return

	def container_open_ui(self):
		"""npc.container_open_ui(PyObjHandle: container) -> int"""
		return 1

	def cast_spell(self, spellEnum, targetObj):
		"""npc.cast_spell(int: spellEnum, PyObjHandle: targetObj) -> None"""
		#npc.cast_spell(int[spell_aid...]: spellEnum|, PyObjHandle: targetObj) -> None
		return

	def d20_send_signal(self, signalId, obj):
		"""Send d20 signal. npc.d20_send_signal(int[DK_SIG_HP_Changed+signalId]: signalId, PyObjHandle: obj)"""
		return

	def d20_query(self, key):
		"""npc.d20_query(int: key) -> int
		key --- if string then D20QueryPython
		key --- if int then d20Query, e.g. EK_Q_Helpless
		"""
		return 0

	def d20_query_has_spell_condition(self, spellId):
		"""npc.d20_query_has_spell_condition(int[spell_sleep]: spellId) -> int"""
		return 0

	def d20_query_has_condition(self, name):
		"""npc.d20_query_has_condition(str: name) -> int"""
		return 0

	def d20_query_with_data(self, key, data1, data2):
		"""npc.d20_query_with_data(int[EK_Q_Critter_Has_Condition]: key, int: data1, int: data2) -> int
		key --- like EK_Q_Critter_Has_Condition
		data1 --- tpdp.hash("Monster Fast Healing")
		data2 -- usually 0
		"""
		return 0

	def d20_status_init(self):
		return

	def damage(self, attacker, damageType, dice, attackPower, actionType):
		"""npc.damage(PyObjHandle: attacker, int[D20DT_BLUDGEONING]: damageType, PyDice: dice, int[D20DAP_UNSPECIFIED]: attackPower, int[D20A_NONE]: actionType) -> None"""
		return

	def damage_with_reduction(self, attacker, damageType, dice, attackPower, reduction, actionType):
		"""npc.damage_with_reduction(PyObjHandle: attacker, int[D20DT_BLUDGEONING]: damageType, PyDice: dice, int[D20DAP_UNSPECIFIED]: attackPower, int[DAMAGE_REDUCTION_HALF]: reduction,int[D20A_NONE]: actionType) -> None"""
		return

	def deal_attack_damage(self, attacker, d20_data, flags, actionType):
		"""npc.deal_attack_damage(PyObjHandle: attacker, int[dispatcher]: d20_data, int[D20CAF_HIT]: flags, int[D20A_NONE]: actionType) -> None"""
		return

	def destroy(self):
		"""Destroys the object"""
		return
	
	def distance_to(self, value):
		"""npc.distance_to(key) -> double: feets
		value --- if PyObjHandle then DistanceToObj
		value --- if long then DistanceToLoc
		value --- if float, float then DistanceToLoc
		"""
		return

	def identify_all(self):
		"""npc.identify_all()"""
		return

	def is_spell_known(self, spellEnum):
		"""npc.is_spell_known(self, spellEnum) -> int"""
		return 1

	def is_friendly(self, npc):
		"""npc.is_friendly(PyObjHandle: npc) -> int"""
		return 1

	def is_active_combatant(self):
		"""npc.is_active_combatant() -> int"""
		return 1

	def inventory_item(self, index):
		"""npc.inventory_item(int: index) -> PyObjHandle"""
		return PyObjHandle()

	def item_find_by_proto(self, proto):
		"""npc.item_find_by_proto(int: proto) -> PyObjHandle"""
		return PyObjHandle()

	def item_get(self, item, flags = 0):
		"""npc.item_get(item: PyObjHandle, flags: int = 0) -> int"""
		return 1

	def item_flags_get(self):
		"""item.item_flags_get() -> OIF_IDENTIFIED"""
		return

	def item_flag_set(self, flag):
		"""item.item_flag_set(int[OIF_IDENTIFIED...]: flag) -> None"""
		return

	def item_flag_unset(self, flag):
		"""item.item_flag_unset(int[OIF_IDENTIFIED...]: flag) -> None"""
		return

	def item_wield(self, item, equipSlot):
		"""npc.item_wield(item: PyObjHandle, int[item_wear_weapon_primary...]: index) -> None"""
		return 

	def item_wield_best_all(self):
		"""npc.item_wield_best_all() -> None"""
		return 

	def item_worn_at(self, equip_slot):
		"""npc.item_worn_at(int[item_wear_helmet-item_wear_lockpicks]: equip_slot) -> PyObjHandle"""
		return PyObjHandle()

	def item_worn_unwield(self, equip_slot, drop_flag):
		"""Move item to inventory or drop. npc.item_worn_unwield(int[item_wear_helmet-item_wear_lockpicks]: equip_slot, int: drop_flag) -> none"""
		return PyObjHandle()

	def get_weapon_type(self):
		return wt_gauntlet
	
	def faction_has(self, faction_num):
		"""npc.faction_has(int: faction_num) -> int"""
		return 1

	def faction_add(self, faction_num):
		"""npc.faction_add(int: faction_num) -> int"""
		return 1

	def fall_down(self, unk_arg = None):
		"""npc.fall_down(int: unk_arg = None) -> None"""
		return

	def feat_add(self, featCode, do_refresh_d20_status):
		"""Adds a feat. npc.feat_add(int[FEAT_ACROBATIC - FEAT_INDOMITABLE_WILL]: featCode, int: do_refresh_d20_status) -> int
		npc.feat_add(string[feat_enums]: featCode) -> int"""
		return 1

	def float_line(self, lineId, pc):
		"""npc.float_line(int: lineId, PyObjHandle: pc) -> None"""
		return
	
	def float_mesfile_line(self, mesFilename, lineId, colorId):
		"""npc.float_mesfile_line(str: mesFilename, int: lineId, int[tf_white]: colorId) -> None"""
		return
	
	def float_text_line(self, line, colorId = tf_white):
		"""npc.float_text_line(str: line, int[tf_white]: colorId) -> None"""
		return

	def get_base_attack_bonus(self):
		"""npc.get_base_attack_bonus() -> int"""
		return

	def get_category_type(self):
		"""npc.get_category_type() -> int"""
		return

	def get_initiative(self):
		"""npc.get_initiative() -> int"""
		return

	def group_list(self):
		return (PyObjHandle(), PyObjHandle())
	
	def set_initiative(self, initiative):
		"""npc.set_initiative(int: initiative) -> None"""
		return

	def leader_get(self):
		"""npc.leader_get() -> PyObjHandle"""
		return PyObjHandle()

	def has_los(self, target):
		"""npc.has_los(PyObjHandle: target) -> int"""
		return 1

	def has_met(self, target):
		"""npc.has_met(PyObjHandle: target) -> int"""
		return 1

	def has_item(self, nameId):
		"""npc.has_item(PyObjHandle: target) -> int"""
		return 1
	

	def make_class(self, stat_class, level):
		"""Makes npc to have class levels. npc.make_class(int[stat_level_barbarian - ...]: stat_class, int: level) -> int"""
		return 1

	def make_wiz(self, level):
		"""Makes npc to have wizard levels. npc.make_wiz(int: level) -> int"""
		return 1
	
	def money_get(self):
		"""Get npc money in copper. npc.money_get() -> int"""
		return 1
	
	def money_adj(self, copper):
		"""Add npc coppers, converted to money gp/10 etc. npc.money_adj(int: copper) -> None"""
		return

	def move(self, new_loc, off_x, off_y):
		return
	
	def move(self, new_loc_x, new_loc_y, off_x, off_y):
		return
	
	def npc_flags_get(self):
		return 1 #ONF_EX_FOLLOWER
	
	def npc_flag_set(self, flag):
		"""npc.npc_flag_set(int[ONF_EX_FOLLOWER...]: flag) -> None"""
		return

	def npc_flag_unset(self, flag):
		"""npc.critter_flag_unset(int[ONF_EX_FOLLOWER...]: flag) -> None"""
		return

	def object_flags_get(self):
		"""npc.object_flags_get(int[OF_DESTROYED...]: flag) -> int"""
		return 0

	def object_flag_set(self, flag):
		"""npc.object_flag_set(int[OF_DESTROYED...]: flag) -> None"""
		return

	def object_flag_unset(self, flag):
		"""npc.object_flag_unset(int[OF_DESTROYED...]: flag) -> None"""
		return

	def object_event_append(self, filter, radius_ft):
		"""npc.object_event_append(int[OLC_CRITTERS...]: filter, int: radius_ft) -> int: event_id"""
		return 1

	def obj_get_int(self, field):
		"""Get internal field int value. npc.obj_get_int(int[obj_f_*]: field) -> int"""
		return 0

	def obj_get_idx_int(self, field, subIdx):
		"""Get internal field array int value. npc.obj_get_idx_int(int[obj_f_*]: field, subIdx) -> int"""
		return 0

	def obj_get_idx_int64(self, field, subIdx):
		"""Get internal field array int value. npc.obj_get_idx_int(int[obj_f_*]: field, subIdx) -> int"""
		return 0

	def obj_set_idx_int(self, field, subIdx, value):
		"""Set internal field array int value. npc.obj_set_idx_int(int[obj_f_*]: field, subIdx, value) -> None"""
		return

	def obj_get_int64(self, field):
		"""Get internal field long value. npc.obj_get_int64(int[obj_f_*]: field) -> long"""
		return 0

	def obj_set_int(self, field, value):
		"""Set internal field int value. npc.obj_set_int(int[obj_f_*]: field, int: value) -> None"""
		return

	def obj_set_obj(self, field, value):
		"""Set internal field obj value. npc.obj_set_obj(int[obj_f_*]: field, PyObjHandle: value) -> int"""
		return 1

	def obj_get_obj(self, field):
		"""Get internal field obj value. npc.obj_get_obj(int[obj_f_*]: field) -> PyObjHandle"""
		return PyObjHandle()

	def object_script_execute(self, triggerer, scriptEvent):
		"""npc.object_script_execute(PyObjHandle: triggerer, int[sn_first_heartbeat]: field) -> int"""
		return 1
	
	def pc_add(self, dude):
		""" Adds object as a PC party member.	pc.pc_add(PyObjHandle: dude) -> int"""
		return 0

	def perform_touch_attack(self, target, isMelee):
		""" Performs touch attack (if isMelee=0 then ranged).	pc.perform_touch_attack(PyObjHandle: target, [bool: isMelee]) -> int"""
		return 0

	def portal_toggle_open(self):
		return

	def portal_flags_get(self):
		"""npc.portal_flags_get(int[OPF_LOCKED...]: flag) -> int"""
		return 0

	def portal_flag_set(self, flag):
		"""npc.portal_flag_set(int[OPF_LOCKED...]: flag) -> None"""
		return

	def portal_flag_unset(self, flag):
		"""npc.portal_flag_unset(int[OPF_LOCKED...]: flag) -> None"""
		return

	def reflex_save_and_damage(self, attacker, dc, reduction, flags, damageDice, damageType, attackPower, actionType, spellId):
		"""npc.reflex_save_and_damage(PyObjHandle: attacker, int: dc, int[D20_Save_Reduction_Half]: reduction, int[D20SavingThrowFlag]: flags, PyDice: damageDice, int[D20DAP_UNSPECIFIED]: damageType, int[D20DAP_UNSPECIFIED]: attackPower, int[D20A_NONE]: actionType, int: spellId) -> int[saved]"""
		return 1

	def refresh_turn(self):
		return

	def runoff(self, loc, off_x, off_y):
		return

	def saving_throw(self, dc, type, saving_throw_flags, attacker, d20a_type = None):
		"""npc.saving_throw_spell(int: dc, int[D20_Save_Fortitude]: type, int[D20STD_F_REROLL]: saving_throw_flags, PyObjHandle: attacker) -> int (finalSaveThrowMod + diceResult >= dc): """
		return 0

	def saving_throw_spell(self, dc, type, saving_throw_flags, attacker, spellId, spellId2 = None):
		"""npc.saving_throw_spell(int: dc, int[D20_Save_Fortitude]: type, int[D20STD_F_REROLL]: saving_throw_flags, PyObjHandle: attacker, int[spell_aid]: spellId) -> int (finalSaveThrowMod + diceResult >= dc): """
		return 0

	def skill_level_get(self, obj2, skillId):
		"""Gets specific skill value. npc.skill_level_get(PyObjHandle: obj2, int[skill_appraise...]: skillId) -> int"""
		return 0

	def skill_level_get(self, skillId):
		"""Gets specific skill value. npc.skill_level_get(int[skill_appraise...]: skillId) -> int"""
		return 0

	def skill_level_get(self, skillId):
		"""Gets specific skill value. npc.skill_level_get(int[skill_appraise...]: skillId) -> int"""
		return 0

	def skill_ranks_get(self, skillId):
		"""Gets specific skill rank. npc.skill_ranks_get(int[skill_appraise...]: skillId) -> int"""
		return 0

	def skill_roll(self, skill_id, dc, flags):
		""" npc.skill_roll(int[skill_appraise...]: skill_id, int: dc, int: flags) -> int"""
		return 0

	def spell_known_add(self, spellIdx, spellClassCode, slotLevel):
		"""npc.spell_known_add(int[...]: spellIdx, int: spellClassCode, int: slotLevel [zero based]) -> None"""
		return

	def spell_memorized_add(self, spellIdx, spellClassCode, slotLevel):
		"""npc.spell_memorized_add(int: spellIdx, int: spellClassCode, int: slotLevel) -> None"""
		return
	
	def spells_pending_to_memorized(self):
		return

	def standpoint_set(self, type, jumppoint, loc = 0, mapid = None, loc_x = 0.0, loc_y = 0.0):
		"""npc.standpoint_set(int[STANDPOINT_DAY]: type, int: jumppoint, long: loc = 0, int: mapid = None, float: loc_x = 0.0, float: loc_y = 0.0) -> None, see jumppoint.tab"""
		return

	def stat_base_set(self, stat, value):
		"""Sets specific stat. npc.stat_base_set(int[stat_strength-stat_psi_points_cur]: stat, int: value) -> int"""
		return

	def stat_base_get(self, stat):
		"""Gets specific stat. npc.stat_base_get(int[stat_strength-stat_psi_points_cur]: stat) -> int"""
		return

	def stat_level_get(self, stat, statArg):
		"""get specific stat. npc.stat_level_get(int[stat_strength-stat_psi_points_cur]: stat , int: statArg = None) -> int"""
		return 0

	def turn_towards(self, target):
		"""npc.turn_towards(PyObjHandle: target) -> None"""
		return

	def unconceal(self):
		"""npc.unconceal() -> int"""
		return

	def use_item(self, item, target = None):
		"""npc.use_item(PyObjHandle: item, PyObjHandle: target = None) -> int"""
		return 1


class game(object):
	"""access to game engine"""
	leader = PyObjHandle()
	party = (PyObjHandle(), PyObjHandle())
	combat_turn = 0
	quests = PyQuests()
	char_ui_display_type = 0
	global_flags = PyGlobalFlags()
	time = PyTimeStamp()

	@staticmethod
	def obj_create(protoId, loc, offset_x = None, offset_y = None):
		""" Will create PyObjHandle based on protoId and place it on location. game.obj_create(int: protoId, int64: loc, int: offset_x = None, int: offset_y = None) -> PyObjHandle"""
		return PyObjHandle()

	@staticmethod
	def is_ranged_weapon(weapon_type):
		"""Check weapon type if ranged. game.is_ranged_weapon(int[wt_gauntlet]: weapon_type) -> int"""
		return 1
	
	@staticmethod
	def make_custom_name(name):
		"""Will create new custom description. game.make_custom_name('new name') -> int: name_id"""
		return 1

	@staticmethod
	def get_feat_name(feat_code):
		""" Get feat name from code. game.get_feat_name(int: feat_code) -> string"""
		return ""
	
	@staticmethod
	def getproto(protoId):
		""" Get proto PyObjHandle based on protoId. game.getproto(int: protoId) -> PyObjHandle"""
		return PyObjHandle()

	@staticmethod
	def combat_is_active():
		""" Get 1 if combat is active. game.combat_is_active() -> int"""
		return 0
	
	@staticmethod
	def written_ui_show(obj):
		""" Show written ui dialog if obj.type == obj_t_written and obj_f_written_text_start_line is set and exists in rules\\written_ui.mes. returns 1 if did displayed that"""
		assert isinstance(obj, PyObjHandle)
		return 1

	@staticmethod
	def is_daytime():
		h = game.time.time_elapsed() // 3600000 % 24
		return (h >= 6 and h < 18)

	@staticmethod
	def create_history_freeform(histText):
		""" game.create_history_freeform(str: histText) -> None"""
		return

	@staticmethod
	def create_history_from_id(histId):
		""" game.create_history_from_id(int: histId) -> None"""
		return

	@staticmethod
	def create_history_from_pattern(pattern_id, actor, target):
		""" game.create_history_from_pattern(int[history.mes]: pattern_id, PyObjHandle: actor, PyObjHandle: target) -> None"""
		return

	@staticmethod
	def create_history_type6_opposed_check(performer, combatant, performer_bonus_list, combatant_bonus_list, performer_roll, combatant_roll, combat_mesline_title, combat_mesline_result, flags):
		""" game.create_history_type6_opposed_check(PyObjHandle: performer, PyObjHandle: combatant, PyBonusList: performer_bonus_list, PyBonusList: combatant_bonus_list, int: performer_roll, int: combatant_roll, int: combat_mesline_title, int: combat_mesline_result, int: flags) -> int: rollHistId"""
		return 0

	@staticmethod
	def fade_and_teleport(time_to_advance, sound_id, movie_id, dest_map, dest_loc_x, dest_loc_y):
		""" game.fade_and_teleport(int[seconds]: time_to_advance, int: sound_id, int: movie_id, int: dest_map, int: dest_loc_x, int: dest_loc_y) -> int: result"""
		return
	
	@staticmethod
	def obj_list_range(location, radius, flags):
		""" obj_list_range(long: location, int[feet]: radius, int[OLC_NONE]: flags) -> (PyObjHandle(), PyObjHandle())"""
		return (PyObjHandle(), PyObjHandle())

	@staticmethod
	def obj_list_vicinity(location, flags):
		""" obj_list_vicinity(long: location, int[OLC_NONE]: flags) -> (PyObjHandle(), PyObjHandle())"""
		return (PyObjHandle(), PyObjHandle())

	@staticmethod
	def obj_list_cone(originHndl, flags, radius, coneLeft, coneArc):
		""" obj_list_cone(PyObjHandle: originHndl, int[OLC_NONE]: flags, int[feet]: radius, int: coneLeft, int: coneArc) -> (PyObjHandle(), PyObjHandle())"""
		return (PyObjHandle(), PyObjHandle())

	@staticmethod
	def timevent_add(func, func_args_tuple, time_ms, is_realtime = 0):
		""" Schedule function call game.timevent_add(func, func_args_tuple, time_ms, is_realtime = 0) -> None"""
		return 0
	
	@staticmethod
	def particles(name, loc_or_obj):
		""" return particles.CreateAtObj(name, objHandle) == game.particles(str: name, PyObjHandle: loc_or_obj) -> int
		 return particles.CreateAtPos(name, objHandle) == game.particles(str: name, int: loc_or_obj) -> int
		"""
		return 0

	@staticmethod
	def particles_end(part_id):
		""" game.particles_end(int: part_id) -> None
		gameSystems->GetParticleSys().Remove(partSysId);
		"""
		return
	
	@staticmethod
	def particles_kill(part_id):
		""" game.particles_kill(int: part_id) -> None
		partSys->EndPrematurely();
		"""
		return
	
	@staticmethod
	def random_range(_from, to):
		""" game.random_range(int: _from, int: to) -> int"""
		return 0

	@staticmethod
	def get_obj_by_id(id):
		""" game.get_obj_by_id(str: id) -> PyObjHandle"""
		return PyObjHandle()

	@staticmethod
	def alert_show(text, button_text):
		""" game.alert_show(str: text, str: button_text) -> int"""
		return 0

	@staticmethod
	def sleep_status_update():
		""" game.sleep_status_update() -> None"""
		return
	
	@staticmethod
	def scroll_to(locOrObj):
		""" game.scroll_to(PyObjHandle: locOrObj) -> int
		game.scroll_to(long: locOrObj) -> int
		"""
		return

	@staticmethod
	def is_melee_weapon(weapon_type):
		""" game.is_melee_weapon(weapon_type[wt_gauntlet]: int) -> int"""
		return 1
	
	@staticmethod
	def is_ranged_weapon(weapon_type):
		""" game.is_ranged_weapon(weapon_type[wt_gauntlet]: int) -> int"""
		return 1


def anyone(targetObjs, methodName, methodArg):
	return PyObjHandle()

class PyObjScripts(object):
	def __getitem__(self, key):
		return PyObjHandle()
	def __setitem__(self, key, value):
		return

class PyRandomEncounter(object):
	def __init__(self):
		self.id = 0
		self.flags = 0
		self.title = 0
		self.dc = 0
		self.map = 0
		proto_id = 0
		enemy = 0
		self.enemies = [[proto_id, enemy_count], [proto_id, enemy_count]]
		self.location = 0
		return

class PyRandomEncounterSetup(object):
	def __init__(self):
		self.terrain = TERRAIN_SCRUB
		self.flags = ES_F_NONE
		return

class PyBonusList(object):
	def __init__(self):
		return

	def get_sum(self):
		return 0

	def add(self, value, bonType, mesline):
		""" bonus_list.add(int: value, int: bonType, int: mesline) -> int """
		return 0

	def add_text(self, value, bonType, text):
		""" bonus_list.add(int: value, int: bonType, str: text) -> int """
		return 0

	def add_cap(self, value, capType, mesline):
		""" Adds cap for a particular bonus type
		bonus_list.add_cap(int: value, int: capType, int: mesline) -> int """
		return 0

	def add_from_feat(self, value, bonType, mesline, featEnum):
		""" bonus_list.add_from_feat(int: value, int: bonType, int: mesline, int: featEnum) -> int """
		return 0

class PyQuests:
	def __init__(self):
		return

	def __getitem__(self, idx):
		"""game.quests[idx] -> PyQuest, idx <= 200"""
		return PyQuest(idx)

class PyQuest:
	def __init__(self, idx):
		self.state = qs_unknown
		return

	def unbotch(self):
		return qs_accepted

class PyDice(object):
	def __init__(self):
		self.number = 1	#	GetCount
		self.size = 1		#	GetSides
		self.bonus = 1	#	GetModifier
		self.packed = 1
		return

	def roll(self):
		return 1

def dice_new(dice_str):
	"""dice_new(str: dice_str) -> PyDice"""
	return PyDice()

class PySpell(object):
	def __init__(self, spellEnum = 0):
		self.spell = PySpell()
		self.begin_round_obj = PyObjHandle()
		self.caster = PyObjHandle()
		self.caster_class = stat_level_wizard
		self.caster_level = 1
		self.spell_level = 0
		self.range_exact = 0
		self.target_loc = 0
		self.dc = 1
		self.id = 0
		self.duration = 1
		self.duration_remaining = 1
		self.num_of_targets = 1
		self.num_of_projectiles = 1
		self.caster_partsys_id = 1
		self.target_list = PySpellTargets()
		self.spell_radius = 1
		self.spell = spell_aid
		# todo
		return

	def spell_end(self, spell_id, endDespiteTargetList = 0):
		return

	def spell_remove(self, unk1):
		return

	def spell_target_list_sort(self, criteria, descending):
		criteria = SORT_TARGET_LIST_BY_OBJ_HANDLE
		return

	def spell_get_menu_arg(self, setting):
		setting = RADIAL_MENU_PARAM_MIN_SETTING
		return 1

	def spell_get_picker_end_point(self):
		return object()

	def is_object_selected(self):
		return 1

	def summon_monsters(self, isAiFollower, protoId = 17000):
		return 1

class PySpellTargets(object):
	def __init__(self):
		return

	def __getitem__(self, index):
		return PySpellTargetsEntry()

	def __setitem__(self, index, data):
		assert isinstance(data, PySpellTargetsEntry)
		return

	def remove_target(self, target):
		assert isinstance(target, PyObjHandle)
		return

	def remove_list(self, alist):
		assert isinstance(alist, list)
		return

class PySpellTargetsEntry(object):
	def __init__(self):
		self.obj = PyObjHandle()
		self.partsys_id = 1
		return


class PyTrapDamage(object):
	def __init__(self):
		self.damage = PyDice()
		self.type = D20DT_BLUDGEONING
		return

class PyTrap(object):
	def __init__(self):
		self.obj = PyObjHandle()
		self.id = 1
		self.san = 1
		self.partsys = 1
		self.damage = [PyTrapDamage(), PyTrapDamage()]
		return

	def attack(self, target, attack_bonus, crit_hit_range_start, is_ranged):
		""" trap.attack(PyObjHandle: target, int: attack_bonus, int: crit_hit_range_start, int: is_ranged) -> int"""
		return D20CAF_HIT

class PyGlobalFlags(object):
	def __init__(self):
		return

	def __getitem__(self, index):
		return 1

	def __setitem__(self, index, data):
		assert isinstance(data, int)
		return

class PyTimeStamp:
	def time_elapsed(self, time_stamp):
		assert isinstance(time_stamp, PyTimeStamp)
		return PyTimeStamp()

	def time_game_in_hours(self, time_stamp):
		""" game's today's time hour """
		assert isinstance(time_stamp, PyTimeStamp)
		return 1

	def time_game_in_hours2(self, time_stamp):
		""" hours from the beginning in game in game time"""
		assert isinstance(time_stamp, PyTimeStamp)
		return 1

RUN_DEFAULT = 1
SKIP_DEFAULT = 0

OBJ_HANDLE_NULL = PyObjHandle(0)

#obj_f fields
obj_f_begin = 0
obj_f_current_aid = 1
obj_f_location = 2
obj_f_offset_x = 3
obj_f_offset_y = 4
obj_f_shadow = 5
obj_f_overlay_fore = 6
obj_f_overlay_back = 7
obj_f_underlay = 8
obj_f_blit_flags = 9
obj_f_blit_color = 10
obj_f_blit_alpha = 11
obj_f_scale = 12
obj_f_light_flags = 13
obj_f_light_aid = 14
obj_f_light_color = 15
obj_f_overlay_light_flags = 16
obj_f_overlay_light_aid = 17
obj_f_overlay_light_color = 18
obj_f_flags = 19
obj_f_spell_flags = 20
obj_f_blocking_mask = 21
obj_f_name = 22
obj_f_description = 23
obj_f_aid = 24
obj_f_destroyed_aid = 25
obj_f_size = 26
obj_f_hp_pts = 27
obj_f_hp_adj = 28
obj_f_hp_damage = 29
obj_f_material = 30
obj_f_scripts_idx = 31
obj_f_sound_effect = 32
obj_f_category = 33
obj_f_rotation = 34
obj_f_speed_walk = 35
obj_f_speed_run = 36
obj_f_base_mesh = 37
obj_f_base_anim = 38
obj_f_radius = 39
obj_f_3d_render_height = 40
obj_f_conditions = 41
obj_f_condition_arg0 = 42
obj_f_permanent_mods = 43
obj_f_initiative = 44
obj_f_dispatcher = 45
obj_f_subinitiative = 46
obj_f_secretdoor_flags = 47
obj_f_secretdoor_effectname = 48
obj_f_secretdoor_dc = 49
obj_f_pad_i_7 = 50
obj_f_pad_i_8 = 51
obj_f_pad_i_9 = 52
obj_f_pad_i_0 = 53
obj_f_offset_z = 54
obj_f_rotation_pitch = 55
obj_f_pad_f_3 = 56
obj_f_pad_f_4 = 57
obj_f_pad_f_5 = 58
obj_f_pad_f_6 = 59
obj_f_pad_f_7 = 60
obj_f_pad_f_8 = 61
obj_f_pad_f_9 = 62
obj_f_pad_f_0 = 63
obj_f_pad_i64_0 = 64
obj_f_pad_i64_1 = 65
obj_f_pad_i64_2 = 66
obj_f_pad_i64_3 = 67
obj_f_pad_i64_4 = 68
obj_f_last_hit_by = 69
obj_f_pad_obj_1 = 70
obj_f_pad_obj_2 = 71
obj_f_pad_obj_3 = 72
obj_f_pad_obj_4 = 73
obj_f_permanent_mod_data = 74
obj_f_attack_types_idx = 75
obj_f_attack_bonus_idx = 76
obj_f_strategy_state = 77
obj_f_pad_ias_4 = 78
obj_f_pad_i64as_0 = 79
obj_f_pad_i64as_1 = 80
obj_f_pad_i64as_2 = 81
obj_f_pad_i64as_3 = 82
obj_f_pad_i64as_4 = 83
obj_f_pad_objas_0 = 84
obj_f_pad_objas_1 = 85
obj_f_pad_objas_2 = 86
obj_f_end = 87
obj_f_portal_begin = 88
obj_f_portal_flags = 89
obj_f_portal_lock_dc = 90
obj_f_portal_key_id = 91
obj_f_portal_notify_npc = 92
obj_f_portal_pad_i_1 = 93
obj_f_portal_pad_i_2 = 94
obj_f_portal_pad_i_3 = 95
obj_f_portal_pad_i_4 = 96
obj_f_portal_pad_i_5 = 97
obj_f_portal_pad_obj_1 = 98
obj_f_portal_pad_ias_1 = 99
obj_f_portal_pad_i64as_1 = 100
obj_f_portal_end = 101
obj_f_container_begin = 102
obj_f_container_flags = 103
obj_f_container_lock_dc = 104
obj_f_container_key_id = 105
obj_f_container_inventory_num = 106
obj_f_container_inventory_list_idx = 107
obj_f_container_inventory_source = 108
obj_f_container_notify_npc = 109
obj_f_container_pad_i_1 = 110
obj_f_container_pad_i_2 = 111
obj_f_container_pad_i_3 = 112
obj_f_container_pad_i_4 = 113
obj_f_container_pad_i_5 = 114
obj_f_container_pad_obj_1 = 115
obj_f_container_pad_obj_2 = 116
obj_f_container_pad_ias_1 = 117
obj_f_container_pad_i64as_1 = 118
obj_f_container_pad_objas_1 = 119
obj_f_container_end = 120
obj_f_scenery_begin = 121
obj_f_scenery_flags = 122
obj_f_scenery_pad_obj_0 = 123
obj_f_scenery_respawn_delay = 124
obj_f_scenery_pad_i_0 = 125
obj_f_scenery_pad_i_1 = 126
obj_f_scenery_teleport_to = 127
obj_f_scenery_pad_i_4 = 128
obj_f_scenery_pad_i_5 = 129
obj_f_scenery_pad_obj_1 = 130
obj_f_scenery_pad_ias_1 = 131
obj_f_scenery_pad_i64as_1 = 132
obj_f_scenery_end = 133
obj_f_projectile_begin = 134
obj_f_projectile_flags_combat = 135
obj_f_projectile_flags_combat_damage = 136
obj_f_projectile_parent_weapon = 137
obj_f_projectile_parent_ammo = 138
obj_f_projectile_part_sys_id = 139
obj_f_projectile_acceleration_x = 140
obj_f_projectile_acceleration_y = 141
obj_f_projectile_acceleration_z = 142
obj_f_projectile_pad_i_4 = 143
obj_f_projectile_pad_obj_1 = 144
obj_f_projectile_pad_obj_2 = 145
obj_f_projectile_pad_obj_3 = 146
obj_f_projectile_pad_ias_1 = 147
obj_f_projectile_pad_i64as_1 = 148
obj_f_projectile_pad_objas_1 = 149
obj_f_projectile_end = 150
obj_f_item_begin = 151
obj_f_item_flags = 152
obj_f_item_parent = 153
obj_f_item_weight = 154
obj_f_item_worth = 155
obj_f_item_inv_aid = 156
obj_f_item_inv_location = 157
obj_f_item_ground_mesh = 158
obj_f_item_ground_anim = 159
obj_f_item_description_unknown = 160
obj_f_item_description_effects = 161
obj_f_item_spell_idx = 162
obj_f_item_spell_idx_flags = 163
obj_f_item_spell_charges_idx = 164
obj_f_item_ai_action = 165
obj_f_item_wear_flags = 166
obj_f_item_material_slot = 167
obj_f_item_quantity = 168
obj_f_item_pad_i_1 = 169
obj_f_item_pad_i_2 = 170
obj_f_item_pad_i_3 = 171
obj_f_item_pad_i_4 = 172
obj_f_item_pad_i_5 = 173
obj_f_item_pad_i_6 = 174
obj_f_item_pad_obj_1 = 175
obj_f_item_pad_obj_2 = 176
obj_f_item_pad_obj_3 = 177
obj_f_item_pad_obj_4 = 178
obj_f_item_pad_obj_5 = 179
obj_f_item_pad_wielder_condition_array = 180
obj_f_item_pad_wielder_argument_array = 181
obj_f_item_pad_i64as_1 = 182
obj_f_item_pad_i64as_2 = 183
obj_f_item_pad_objas_1 = 184
obj_f_item_pad_objas_2 = 185
obj_f_item_end = 186
obj_f_weapon_begin = 187
obj_f_weapon_flags = 188
obj_f_weapon_range = 189
obj_f_weapon_ammo_type = 190
obj_f_weapon_ammo_consumption = 191
obj_f_weapon_missile_aid = 192
obj_f_weapon_crit_hit_chart = 193
obj_f_weapon_attacktype = 194
obj_f_weapon_damage_dice = 195
obj_f_weapon_animtype = 196
obj_f_weapon_type = 197
obj_f_weapon_crit_range = 198
obj_f_weapon_pad_i_1 = 199
obj_f_weapon_pad_i_2 = 200
obj_f_weapon_pad_obj_1 = 201
obj_f_weapon_pad_obj_2 = 202
obj_f_weapon_pad_obj_3 = 203
obj_f_weapon_pad_obj_4 = 204
obj_f_weapon_pad_obj_5 = 205
obj_f_weapon_pad_ias_1 = 206
obj_f_weapon_pad_i64as_1 = 207
obj_f_weapon_end = 208
obj_f_ammo_begin = 209
obj_f_ammo_flags = 210
obj_f_ammo_quantity = 211
obj_f_ammo_type = 212
obj_f_ammo_pad_i_1 = 213
obj_f_ammo_pad_i_2 = 214
obj_f_ammo_pad_obj_1 = 215
obj_f_ammo_pad_ias_1 = 216
obj_f_ammo_pad_i64as_1 = 217
obj_f_ammo_end = 218
obj_f_armor_begin = 219
obj_f_armor_flags = 220
obj_f_armor_ac_adj = 221
obj_f_armor_max_dex_bonus = 222
obj_f_armor_arcane_spell_failure = 223
obj_f_armor_armor_check_penalty = 224
obj_f_armor_pad_i_1 = 225
obj_f_armor_pad_ias_1 = 226
obj_f_armor_pad_i64as_1 = 227
obj_f_armor_end = 228
obj_f_money_begin = 229
obj_f_money_flags = 230
obj_f_money_quantity = 231
obj_f_money_type = 232
obj_f_money_pad_i_1 = 233
obj_f_money_pad_i_2 = 234
obj_f_money_pad_i_3 = 235
obj_f_money_pad_i_4 = 236
obj_f_money_pad_i_5 = 237
obj_f_money_pad_ias_1 = 238
obj_f_money_pad_i64as_1 = 239
obj_f_money_end = 240
obj_f_food_begin = 241
obj_f_food_flags = 242
obj_f_food_pad_i_1 = 243
obj_f_food_pad_i_2 = 244
obj_f_food_pad_ias_1 = 245
obj_f_food_pad_i64as_1 = 246
obj_f_food_end = 247
obj_f_scroll_begin = 248
obj_f_scroll_flags = 249
obj_f_scroll_pad_i_1 = 250
obj_f_scroll_pad_i_2 = 251
obj_f_scroll_pad_ias_1 = 252
obj_f_scroll_pad_i64as_1 = 253
obj_f_scroll_end = 254
obj_f_key_begin = 255
obj_f_key_key_id = 256
obj_f_key_pad_i_1 = 257
obj_f_key_pad_i_2 = 258
obj_f_key_pad_ias_1 = 259
obj_f_key_pad_i64as_1 = 260
obj_f_key_end = 261
obj_f_written_begin = 262
obj_f_written_flags = 263
obj_f_written_subtype = 264
obj_f_written_text_start_line = 265
obj_f_written_text_end_line = 266
obj_f_written_pad_i_1 = 267
obj_f_written_pad_i_2 = 268
obj_f_written_pad_ias_1 = 269
obj_f_written_pad_i64as_1 = 270
obj_f_written_end = 271
obj_f_bag_begin = 272
obj_f_bag_flags = 273
obj_f_bag_size = 274
obj_f_bag_end = 275
obj_f_generic_begin = 276
obj_f_generic_flags = 277
obj_f_generic_usage_bonus = 278
obj_f_generic_usage_count_remaining = 279
obj_f_generic_pad_ias_1 = 280
obj_f_generic_pad_i64as_1 = 281
obj_f_generic_end = 282
obj_f_critter_begin = 283
obj_f_critter_flags = 284
obj_f_critter_flags2 = 285
obj_f_critter_abilities_idx = 286
obj_f_critter_level_idx = 287
obj_f_critter_race = 288
obj_f_critter_gender = 289
obj_f_critter_age = 290
obj_f_critter_height = 291
obj_f_critter_weight = 292
obj_f_critter_experience = 293
obj_f_critter_pad_i_1 = 294
obj_f_critter_alignment = 295
obj_f_critter_deity = 296
obj_f_critter_domain_1 = 297
obj_f_critter_domain_2 = 298
obj_f_critter_alignment_choice = 299
obj_f_critter_school_specialization = 300
obj_f_critter_spells_known_idx = 301
obj_f_critter_spells_memorized_idx = 302
obj_f_critter_spells_cast_idx = 303
obj_f_critter_feat_idx = 304
obj_f_critter_feat_count_idx = 305
obj_f_critter_fleeing_from = 306
obj_f_critter_portrait = 307
obj_f_critter_money_idx = 308
obj_f_critter_inventory_num = 309
obj_f_critter_inventory_list_idx = 310
obj_f_critter_inventory_source = 311
obj_f_critter_description_unknown = 312
obj_f_critter_follower_idx = 313
obj_f_critter_teleport_dest = 314
obj_f_critter_teleport_map = 315
obj_f_critter_death_time = 316
obj_f_critter_skill_idx = 317
obj_f_critter_reach = 318
obj_f_critter_subdual_damage = 319
obj_f_critter_pad_i_4 = 320
obj_f_critter_pad_i_5 = 321
obj_f_critter_sequence = 322
obj_f_critter_hair_style = 323
obj_f_critter_strategy = 324
obj_f_critter_pad_i_3 = 325
obj_f_critter_monster_category = 326
obj_f_critter_pad_i64_2 = 327
obj_f_critter_pad_i64_3 = 328
obj_f_critter_pad_i64_4 = 329
obj_f_critter_pad_i64_5 = 330
obj_f_critter_damage_idx = 331
obj_f_critter_attacks_idx = 332
obj_f_critter_seen_maplist = 333
obj_f_critter_pad_i64as_2 = 334
obj_f_critter_pad_i64as_3 = 335
obj_f_critter_pad_i64as_4 = 336
obj_f_critter_pad_i64as_5 = 337
obj_f_critter_end = 338
obj_f_pc_begin = 339
obj_f_pc_flags = 340
obj_f_pc_pad_ias_0 = 341
obj_f_pc_pad_i64as_0 = 342
obj_f_pc_player_name = 343
obj_f_pc_global_flags = 344
obj_f_pc_global_variables = 345
obj_f_pc_voice_idx = 346
obj_f_pc_roll_count = 347
obj_f_pc_pad_i_2 = 348
obj_f_pc_weaponslots_idx = 349
obj_f_pc_pad_ias_2 = 350
obj_f_pc_pad_i64as_1 = 351
obj_f_pc_end = 352
obj_f_npc_begin = 353
obj_f_npc_flags = 354
obj_f_npc_leader = 355
obj_f_npc_ai_data = 356
obj_f_npc_combat_focus = 357
obj_f_npc_who_hit_me_last = 358
obj_f_npc_waypoints_idx = 359
obj_f_npc_waypoint_current = 360
obj_f_npc_standpoint_day_INTERNAL_DO_NOT_USE = 361
obj_f_npc_standpoint_night_INTERNAL_DO_NOT_USE = 362
obj_f_npc_faction = 363
obj_f_npc_retail_price_multiplier = 364
obj_f_npc_substitute_inventory = 365
obj_f_npc_reaction_base = 366
obj_f_npc_challenge_rating = 367
obj_f_npc_reaction_pc_idx = 368
obj_f_npc_reaction_level_idx = 369
obj_f_npc_reaction_time_idx = 370
obj_f_npc_generator_data = 371
obj_f_npc_ai_list_idx = 372
obj_f_npc_save_reflexes_bonus = 373
obj_f_npc_save_fortitude_bonus = 374
obj_f_npc_save_willpower_bonus = 375
obj_f_npc_ac_bonus = 376
obj_f_npc_add_mesh = 377
obj_f_npc_waypoint_anim = 378
obj_f_npc_pad_i_3 = 379
obj_f_npc_pad_i_4 = 380
obj_f_npc_pad_i_5 = 381
obj_f_npc_ai_flags64 = 382
obj_f_npc_pad_i64_2 = 383
obj_f_npc_pad_i64_3 = 384
obj_f_npc_pad_i64_4 = 385
obj_f_npc_pad_i64_5 = 386
obj_f_npc_hitdice_idx = 387
obj_f_npc_ai_list_type_idx = 388
obj_f_npc_pad_ias_3 = 389
obj_f_npc_pad_ias_4 = 390
obj_f_npc_pad_ias_5 = 391
obj_f_npc_standpoints = 392
obj_f_npc_pad_i64as_2 = 393
obj_f_npc_pad_i64as_3 = 394
obj_f_npc_pad_i64as_4 = 395
obj_f_npc_pad_i64as_5 = 396
obj_f_npc_end = 397
obj_f_trap_begin = 398
obj_f_trap_flags = 399
obj_f_trap_difficulty = 400
obj_f_trap_pad_i_2 = 401
obj_f_trap_pad_ias_1 = 402
obj_f_trap_pad_i64as_1 = 403
obj_f_trap_end = 404
obj_f_total_normal = 405
obj_f_transient_begin = 406
obj_f_render_color = 407
obj_f_render_colors = 408
obj_f_render_palette = 409
obj_f_render_scale = 410
obj_f_render_alpha = 411
obj_f_render_x = 412
obj_f_render_y = 413
obj_f_render_width = 414
obj_f_render_height = 415
obj_f_palette = 416
obj_f_color = 417
obj_f_colors = 418
obj_f_render_flags = 419
obj_f_temp_id = 420
obj_f_light_handle = 421
obj_f_overlay_light_handles = 422
obj_f_internal_flags = 423
obj_f_find_node = 424
obj_f_animation_handle = 425
obj_f_grapple_state = 426
obj_f_transient_end = 427
obj_f_type = 428
obj_f_prototype_handle = 429

# obj_f types
obj_t_portal = 0
obj_t_container = 1
obj_t_scenery = 2
obj_t_projectile = 3
obj_t_weapon = 4
obj_t_ammo = 5
obj_t_armor = 6
obj_t_money = 7
obj_t_food = 8
obj_t_scroll = 9
obj_t_key = 10
obj_t_written = 11
obj_t_generic = 12
obj_t_pc = 13
obj_t_npc = 14
obj_t_trap = 15
obj_t_bag = 16

item_wear_helmet = 0
item_wear_necklace = 1
item_wear_gloves = 2
item_wear_weapon_primary = 3
item_wear_weapon_secondary = 4
item_wear_armor = 5
item_wear_ring_primary = 6
item_wear_ring_secondary = 7
item_wear_boots = 8
item_wear_ammo = 9
item_wear_cloak = 10
item_wear_shield = 11
item_wear_robes = 12
item_wear_bracers = 13
item_wear_bardic_item = 14
item_wear_lockpicks = 15

feat_acrobatic = 0
feat_agile = 1
feat_alertness = 2
feat_animal_affinity = 3
feat_armor_proficiency_light = 4
feat_armor_proficiency_medium = 5
feat_armor_proficiency_heavy = 6
feat_athletic = 7
feat_augment_summoning = 8
feat_blind_fight = 9
feat_brew_potion = 10
feat_cleave = 11
feat_combat_casting = 12
feat_combat_expertise = 13
feat_craft_magic_arms_and_armor = 14
feat_craft_rod = 15
feat_craft_staff = 16
feat_craft_wand = 17
feat_craft_wondrous_item = 18
feat_deceitful = 19
feat_deft_hands = 20
feat_diehard = 21
feat_diligent = 22
feat_deflect_arrows = 23
feat_dodge = 24
feat_empower_spell = 25
feat_endurance = 26
feat_enlarge_spell = 27
feat_eschew_materials = 28
feat_exotic_weapon_proficiency_halfling_kama = 29
feat_exotic_weapon_proficiency_kukri = 30
feat_exotic_weapon_proficiency_halfling_nunchaku = 31
feat_exotic_weapon_proficiency_halfling_siangham = 32
feat_exotic_weapon_proficiency_kama = 33
feat_exotic_weapon_proficiency_nunchaku = 34
feat_exotic_weapon_proficiency_siangham = 35
feat_exotic_weapon_proficiency_bastard_sword = 36
feat_exotic_weapon_proficiency_dwarven_waraxe = 37
feat_exotic_weapon_proficiency_gnome_hooked_hammer = 38
feat_exotic_weapon_proficiency_orc_double_axe = 39
feat_exotic_weapon_proficiency_spike_chain = 40
feat_exotic_weapon_proficiency_dire_flail = 41
feat_exotic_weapon_proficiency_two_bladed_sword = 42
feat_exotic_weapon_proficiency_dwarven_urgrosh = 43
feat_exotic_weapon_proficiency_hand_crossbow = 44
feat_exotic_weapon_proficiency_shuriken = 45
feat_exotic_weapon_proficiency_whip = 46
feat_exotic_weapon_proficiency_repeating_crossbow = 47
feat_exotic_weapon_proficiency_net = 48
feat_extend_spell = 49
feat_extra_turning = 50
feat_far_shot = 51
feat_forge_ring = 52
feat_great_cleave = 53
feat_great_fortitude = 54
feat_greater_spell_focus_abjuration = 55
feat_greater_spell_focus_conjuration = 56
feat_greater_spell_focus_divination = 57
feat_greater_spell_focus_enchantment = 58
feat_greater_spell_focus_evocation = 59
feat_greater_spell_focus_illusion = 60
feat_greater_spell_focus_necromancy = 61
feat_greater_spell_focus_transmutation = 62
feat_greater_spell_penetration = 63
feat_greater_two_weapon_fighting = 64
feat_greater_weapon_focus_gauntlet = 65
feat_greater_weapon_focus_unarmed_strike_medium_sized_being = 66
feat_greater_weapon_focus_unarmed_strike_small_being = 67
feat_greater_weapon_focus_dagger = 68
feat_greater_weapon_focus_punching_dagger = 69
feat_greater_weapon_focus_spiked_gauntlet = 70
feat_greater_weapon_focus_light_mace = 71
feat_greater_weapon_focus_sickle = 72
feat_greater_weapon_focus_club = 73
feat_greater_weapon_focus_halfspear = 74
feat_greater_weapon_focus_heavy_mace = 75
feat_greater_weapon_focus_morningstar = 76
feat_greater_weapon_focus_quarterstaff = 77
feat_greater_weapon_focus_shortspear = 78
feat_greater_weapon_focus_light_crossbow = 79
feat_greater_weapon_focus_dart = 80
feat_greater_weapon_focus_sling = 81
feat_greater_weapon_focus_heavy_crossbow = 82
feat_greater_weapon_focus_javelin = 83
feat_greater_weapon_focus_throwing_axe = 84
feat_greater_weapon_focus_light_hammer = 85
feat_greater_weapon_focus_handaxe = 86
feat_greater_weapon_focus_light_lance = 87
feat_greater_weapon_focus_light_pick = 88
feat_greater_weapon_focus_sap = 89
feat_greater_weapon_focus_short_sword = 90
feat_greater_weapon_focus_battleaxe = 91
feat_greater_weapon_focus_light_flail = 92
feat_greater_weapon_focus_heavy_lance = 93
feat_greater_weapon_focus_longsword = 94
feat_greater_weapon_focus_heavy_pick = 95
feat_greater_weapon_focus_rapier = 96
feat_greater_weapon_focus_scimitar = 97
feat_greater_weapon_focus_trident = 98
feat_greater_weapon_focus_warhammer = 99
feat_greater_weapon_focus_falchion = 100
feat_greater_weapon_focus_heavy_flail = 101
feat_greater_weapon_focus_glaive = 102
feat_greater_weapon_focus_greataxe = 103
feat_greater_weapon_focus_greatclub = 104
feat_greater_weapon_focus_greatsword = 105
feat_greater_weapon_focus_guisarme = 106
feat_greater_weapon_focus_halberd = 107
feat_greater_weapon_focus_longspear = 108
feat_greater_weapon_focus_ranseur = 109
feat_greater_weapon_focus_scythe = 110
feat_greater_weapon_focus_shortbow = 111
feat_greater_weapon_focus_composite_shortbow = 112
feat_greater_weapon_focus_longbow = 113
feat_greater_weapon_focus_composite_longbow = 114
feat_greater_weapon_focus_halfling_kama = 115
feat_greater_weapon_focus_kukri = 116
feat_greater_weapon_focus_halfling_nunchaku = 117
feat_greater_weapon_focus_halfling_siangham = 118
feat_greater_weapon_focus_kama = 119
feat_greater_weapon_focus_nunchaku = 120
feat_greater_weapon_focus_siangham = 121
feat_greater_weapon_focus_bastard_sword = 122
feat_greater_weapon_focus_dwarven_waraxe = 123
feat_greater_weapon_focus_gnome_hooked_hammer = 124
feat_greater_weapon_focus_orc_double_axe = 125
feat_greater_weapon_focus_spike_chain = 126
feat_greater_weapon_focus_dire_flail = 127
feat_greater_weapon_focus_two_bladed_sword = 128
feat_greater_weapon_focus_dwarven_urgrosh = 129
feat_greater_weapon_focus_hand_crossbow = 130
feat_greater_weapon_focus_shuriken = 131
feat_greater_weapon_focus_whip = 132
feat_greater_weapon_focus_repeating_crossbow = 133
feat_greater_weapon_focus_net = 134
feat_greater_weapon_focus_grapple = 135
feat_greater_weapon_focus_ray = 136
feat_greater_weapon_specialization = 137
feat_heighten_spell = 138
feat_improved_bull_rush = 139
feat_improved_counterspell = 140
feat_improved_critical_gauntlet = 141
feat_improved_critical_unarmed_strike_medium_sized_being = 142
feat_improved_critical_unarmed_strike_small_being = 143
feat_improved_critical_dagger = 144
feat_improved_critical_punching_dagger = 145
feat_improved_critical_spiked_gauntlet = 146
feat_improved_critical_light_mace = 147
feat_improved_critical_sickle = 148
feat_improved_critical_club = 149
feat_improved_critical_halfspear = 150
feat_improved_critical_heavy_mace = 151
feat_improved_critical_morningstar = 152
feat_improved_critical_quarterstaff = 153
feat_improved_critical_shortspear = 154
feat_improved_critical_light_crossbow = 155
feat_improved_critical_dart = 156
feat_improved_critical_sling = 157
feat_improved_critical_heavy_crossbow = 158
feat_improved_critical_javelin = 159
feat_improved_critical_throwing_axe = 160
feat_improved_critical_light_hammer = 161
feat_improved_critical_handaxe = 162
feat_improved_critical_light_lance = 163
feat_improved_critical_light_pick = 164
feat_improved_critical_sap = 165
feat_improved_critical_short_sword = 166
feat_improved_critical_battleaxe = 167
feat_improved_critical_light_flail = 168
feat_improved_critical_heavy_lance = 169
feat_improved_critical_longsword = 170
feat_improved_critical_heavy_pick = 171
feat_improved_critical_rapier = 172
feat_improved_critical_scimitar = 173
feat_improved_critical_trident = 174
feat_improved_critical_warhammer = 175
feat_improved_critical_falchion = 176
feat_improved_critical_heavy_flail = 177
feat_improved_critical_glaive = 178
feat_improved_critical_greataxe = 179
feat_improved_critical_greatclub = 180
feat_improved_critical_greatsword = 181
feat_improved_critical_guisarme = 182
feat_improved_critical_halberd = 183
feat_improved_critical_longspear = 184
feat_improved_critical_ranseur = 185
feat_improved_critical_scythe = 186
feat_improved_critical_shortbow = 187
feat_improved_critical_composite_shortbow = 188
feat_improved_critical_longbow = 189
feat_improved_critical_composite_longbow = 190
feat_improved_critical_halfling_kama = 191
feat_improved_critical_kukri = 192
feat_improved_critical_halfling_nunchaku = 193
feat_improved_critical_halfling_siangham = 194
feat_improved_critical_kama = 195
feat_improved_critical_nunchaku = 196
feat_improved_critical_siangham = 197
feat_improved_critical_bastard_sword = 198
feat_improved_critical_dwarven_waraxe = 199
feat_improved_critical_gnome_hooked_hammer = 200
feat_improved_critical_orc_double_axe = 201
feat_improved_critical_spike_chain = 202
feat_improved_critical_dire_flail = 203
feat_improved_critical_two_bladed_sword = 204
feat_improved_critical_dwarven_urgrosh = 205
feat_improved_critical_hand_crossbow = 206
feat_improved_critical_shuriken = 207
feat_improved_critical_whip = 208
feat_improved_critical_repeating_crossbow = 209
feat_improved_critical_net = 210
feat_improved_disarm = 211
feat_improved_feint = 212
feat_improved_grapple = 213
feat_improved_initiative = 214
feat_improved_overrun = 215
feat_improved_shield_bash = 216
feat_improved_trip = 217
feat_improved_two_weapon_fighting = 218
feat_improved_turning = 219
feat_improved_unarmed_strike = 220
feat_improved_uncanny_dodge = 221
feat_investigator = 222
feat_iron_will = 223
feat_leadership = 224
feat_lightning_reflexes = 225
feat_magical_affinity = 226
feat_manyshot = 227
feat_martial_weapon_proficiency_throwing_axe = 228
feat_martial_weapon_proficiency_light_hammer = 229
feat_martial_weapon_proficiency_handaxe = 230
feat_martial_weapon_proficiency_light_lance = 231
feat_martial_weapon_proficiency_light_pick = 232
feat_martial_weapon_proficiency_sap = 233
feat_martial_weapon_proficiency_short_sword = 234
feat_martial_weapon_proficiency_battleaxe = 235
feat_martial_weapon_proficiency_light_flail = 236
feat_martial_weapon_proficiency_heavy_lance = 237
feat_martial_weapon_proficiency_longsword = 238
feat_martial_weapon_proficiency_heavy_pick = 239
feat_martial_weapon_proficiency_rapier = 240
feat_martial_weapon_proficiency_scimitar = 241
feat_martial_weapon_proficiency_trident = 242
feat_martial_weapon_proficiency_warhammer = 243
feat_martial_weapon_proficiency_falchion = 244
feat_martial_weapon_proficiency_heavy_flail = 245
feat_martial_weapon_proficiency_glaive = 246
feat_martial_weapon_proficiency_greataxe = 247
feat_martial_weapon_proficiency_greatclub = 248
feat_martial_weapon_proficiency_greatsword = 249
feat_martial_weapon_proficiency_guisarme = 250
feat_martial_weapon_proficiency_halberd = 251
feat_martial_weapon_proficiency_longspear = 252
feat_martial_weapon_proficiency_ranseur = 253
feat_martial_weapon_proficiency_scythe = 254
feat_martial_weapon_proficiency_shortbow = 255
feat_martial_weapon_proficiency_composite_shortbow = 256
feat_martial_weapon_proficiency_longbow = 257
feat_martial_weapon_proficiency_composite_longbow = 258
feat_maximize_spell = 259
feat_mobility = 260
feat_mounted_archery = 261
feat_mounted_combat = 262
feat_natural_spell = 263
feat_negotiator = 264
feat_nimble_fingers = 265
feat_persuasive = 266
feat_point_blank_shot = 267
feat_power_attack = 268
feat_precise_shot = 269
feat_quick_draw = 270
feat_quicken_spell = 271
feat_rapid_shot = 272
feat_rapid_reload = 273
feat_ride_by_attack = 274
feat_run = 275
feat_scribe_scroll = 276
feat_self_sufficient = 277
feat_shield_proficiency = 278
feat_shot_on_the_run = 279
feat_silent_spell = 280
feat_simple_weapon_proficiency = 281
feat_skill_focus_alchemy = 282
feat_skill_focus_animal_empathy = 283
feat_skill_focus_appraise = 284
feat_skill_focus_balance = 285
feat_skill_focus_bluff = 286
feat_skill_focus_climb = 287
feat_skill_focus_concentration = 288
feat_skill_focus_craft = 289
feat_skill_focus_decipher_script = 290
feat_skill_focus_diplomacy = 291
feat_skill_focus_disable_device = 292
feat_skill_focus_disguise = 293
feat_skill_focus_escape_artist = 294
feat_skill_focus_forgery = 295
feat_skill_focus_gather_information = 296
feat_skill_focus_handle_animal = 297
feat_skill_focus_heal = 298
feat_skill_focus_hide = 299
feat_skill_focus_innuendo = 300
feat_skill_focus_intimidate = 301
feat_skill_focus_intuit_direction = 302
feat_skill_focus_jump = 303
feat_skill_focus_knowledge = 304
feat_skill_focus_listen = 305
feat_skill_focus_move_silently = 306
feat_skill_focus_open_lock = 307
feat_skill_focus_performance = 308
feat_skill_focus_slight_of_hand = 309
feat_skill_focus_profession = 310
feat_skill_focus_read_lips = 311
feat_skill_focus_ride = 312
feat_skill_focus_scry = 313
feat_skill_focus_search = 314
feat_skill_focus_sense_motive = 315
feat_skill_focus_speak_language = 316
feat_skill_focus_spellcraft = 317
feat_skill_focus_spot = 318
feat_skill_focus_swim = 319
feat_skill_focus_tumble = 320
feat_skill_focus_use_magic_device = 321
feat_skill_focus_use_rope = 322
feat_skill_focus_survival = 323
feat_snatch_arrows = 324
feat_spell_focus_abjuration = 325
feat_spell_focus_conjuration = 326
feat_spell_focus_divination = 327
feat_spell_focus_enchantment = 328
feat_spell_focus_evocation = 329
feat_spell_focus_illusion = 330
feat_spell_focus_necromancy = 331
feat_spell_focus_transmutation = 332
feat_spell_mastery = 333
feat_spell_penetration = 334
feat_spirited_charge = 335
feat_spring_attack = 336
feat_stealthy = 337
feat_still_spell = 338
feat_stunning_fist = 339
feat_sunder = 340
feat_toughness = 341
feat_tower_shield_proficiency = 342
feat_track = 343
feat_trample = 344
feat_two_weapon_fighting = 345
feat_two_weapon_defense = 346
feat_weapon_finesse_gauntlet = 347
feat_weapon_finesse_unarmed_strike_medium_sized_being = 348
feat_weapon_finesse_unarmed_strike_small_being = 349
feat_weapon_finesse_dagger = 350
feat_weapon_finesse_punching_dagger = 351
feat_weapon_finesse_spiked_gauntlet = 352
feat_weapon_finesse_light_mace = 353
feat_weapon_finesse_sickle = 354
feat_weapon_finesse_club = 355
feat_weapon_finesse_halfspear = 356
feat_weapon_finesse_heavy_mace = 357
feat_weapon_finesse_morningstar = 358
feat_weapon_finesse_quarterstaff = 359
feat_weapon_finesse_shortspear = 360
feat_weapon_finesse_light_crossbow = 361
feat_weapon_finesse_dart = 362
feat_weapon_finesse_sling = 363
feat_weapon_finesse_heavy_crossbow = 364
feat_weapon_finesse_javelin = 365
feat_weapon_finesse_throwing_axe = 366
feat_weapon_finesse_light_hammer = 367
feat_weapon_finesse_handaxe = 368
feat_weapon_finesse_light_lance = 369
feat_weapon_finesse_light_pick = 370
feat_weapon_finesse_sap = 371
feat_weapon_finesse_short_sword = 372
feat_weapon_finesse_battleaxe = 373
feat_weapon_finesse_light_flail = 374
feat_weapon_finesse_heavy_lance = 375
feat_weapon_finesse_longsword = 376
feat_weapon_finesse_heavy_pick = 377
feat_weapon_finesse_rapier = 378
feat_weapon_finesse_scimitar = 379
feat_weapon_finesse_trident = 380
feat_weapon_finesse_warhammer = 381
feat_weapon_finesse_falchion = 382
feat_weapon_finesse_heavy_flail = 383
feat_weapon_finesse_glaive = 384
feat_weapon_finesse_greataxe = 385
feat_weapon_finesse_greatclub = 386
feat_weapon_finesse_greatsword = 387
feat_weapon_finesse_guisarme = 388
feat_weapon_finesse_halberd = 389
feat_weapon_finesse_longspear = 390
feat_weapon_finesse_ranseur = 391
feat_weapon_finesse_scythe = 392
feat_weapon_finesse_shortbow = 393
feat_weapon_finesse_composite_shortbow = 394
feat_weapon_finesse_longbow = 395
feat_weapon_finesse_composite_longbow = 396
feat_weapon_finesse_halfling_kama = 397
feat_weapon_finesse_kukri = 398
feat_weapon_finesse_halfling_nunchaku = 399
feat_weapon_finesse_halfling_siangham = 400
feat_weapon_finesse_kama = 401
feat_weapon_finesse_nunchaku = 402
feat_weapon_finesse_siangham = 403
feat_weapon_finesse_bastard_sword = 404
feat_weapon_finesse_dwarven_waraxe = 405
feat_weapon_finesse_gnome_hooked_hammer = 406
feat_weapon_finesse_orc_double_axe = 407
feat_weapon_finesse_spike_chain = 408
feat_weapon_finesse_dire_flail = 409
feat_weapon_finesse_two_bladed_sword = 410
feat_weapon_finesse_dwarven_urgrosh = 411
feat_weapon_finesse_hand_crossbow = 412
feat_weapon_finesse_shuriken = 413
feat_weapon_finesse_whip = 414
feat_weapon_finesse_repeating_crossbow = 415
feat_weapon_finesse_net = 416
feat_weapon_focus_gauntlet = 417
feat_weapon_focus_unarmed_strike_medium_sized_being = 418
feat_weapon_focus_unarmed_strike_small_being = 419
feat_weapon_focus_dagger = 420
feat_weapon_focus_punching_dagger = 421
feat_weapon_focus_spiked_gauntlet = 422
feat_weapon_focus_light_mace = 423
feat_weapon_focus_sickle = 424
feat_weapon_focus_club = 425
feat_weapon_focus_halfspear = 426
feat_weapon_focus_heavy_mace = 427
feat_weapon_focus_morningstar = 428
feat_weapon_focus_quarterstaff = 429
feat_weapon_focus_shortspear = 430
feat_weapon_focus_light_crossbow = 431
feat_weapon_focus_dart = 432
feat_weapon_focus_sling = 433
feat_weapon_focus_heavy_crossbow = 434
feat_weapon_focus_javelin = 435
feat_weapon_focus_throwing_axe = 436
feat_weapon_focus_light_hammer = 437
feat_weapon_focus_handaxe = 438
feat_weapon_focus_light_lance = 439
feat_weapon_focus_light_pick = 440
feat_weapon_focus_sap = 441
feat_weapon_focus_short_sword = 442
feat_weapon_focus_battleaxe = 443
feat_weapon_focus_light_flail = 444
feat_weapon_focus_heavy_lance = 445
feat_weapon_focus_longsword = 446
feat_weapon_focus_heavy_pick = 447
feat_weapon_focus_rapier = 448
feat_weapon_focus_scimitar = 449
feat_weapon_focus_trident = 450
feat_weapon_focus_warhammer = 451
feat_weapon_focus_falchion = 452
feat_weapon_focus_heavy_flail = 453
feat_weapon_focus_glaive = 454
feat_weapon_focus_greataxe = 455
feat_weapon_focus_greatclub = 456
feat_weapon_focus_greatsword = 457
feat_weapon_focus_guisarme = 458
feat_weapon_focus_halberd = 459
feat_weapon_focus_longspear = 460
feat_weapon_focus_ranseur = 461
feat_weapon_focus_scythe = 462
feat_weapon_focus_shortbow = 463
feat_weapon_focus_composite_shortbow = 464
feat_weapon_focus_longbow = 465
feat_weapon_focus_composite_longbow = 466
feat_weapon_focus_halfling_kama = 467
feat_weapon_focus_kukri = 468
feat_weapon_focus_halfling_nunchaku = 469
feat_weapon_focus_halfling_siangham = 470
feat_weapon_focus_kama = 471
feat_weapon_focus_nunchaku = 472
feat_weapon_focus_siangham = 473
feat_weapon_focus_bastard_sword = 474
feat_weapon_focus_dwarven_waraxe = 475
feat_weapon_focus_gnome_hooked_hammer = 476
feat_weapon_focus_orc_double_axe = 477
feat_weapon_focus_spike_chain = 478
feat_weapon_focus_dire_flail = 479
feat_weapon_focus_two_bladed_sword = 480
feat_weapon_focus_dwarven_urgrosh = 481
feat_weapon_focus_hand_crossbow = 482
feat_weapon_focus_shuriken = 483
feat_weapon_focus_whip = 484
feat_weapon_focus_repeating_crossbow = 485
feat_weapon_focus_net = 486
feat_weapon_focus_grapple = 487
feat_weapon_focus_ray = 488
feat_weapon_specialization_gauntlet = 489
feat_weapon_specialization_unarmed_strike_medium_sized_being = 490
feat_weapon_specialization_unarmed_strike_small_being = 491
feat_weapon_specialization_dagger = 492
feat_weapon_specialization_punching_dagger = 493
feat_weapon_specialization_spiked_gauntlet = 494
feat_weapon_specialization_light_mace = 495
feat_weapon_specialization_sickle = 496
feat_weapon_specialization_club = 497
feat_weapon_specialization_halfspear = 498
feat_weapon_specialization_heavy_mace = 499
feat_weapon_specialization_morningstar = 500
feat_weapon_specialization_quarterstaff = 501
feat_weapon_specialization_shortspear = 502
feat_weapon_specialization_light_crossbow = 503
feat_weapon_specialization_dart = 504
feat_weapon_specialization_sling = 505
feat_weapon_specialization_heavy_crossbow = 506
feat_weapon_specialization_javelin = 507
feat_weapon_specialization_throwing_axe = 508
feat_weapon_specialization_light_hammer = 509
feat_weapon_specialization_handaxe = 510
feat_weapon_specialization_light_lance = 511
feat_weapon_specialization_light_pick = 512
feat_weapon_specialization_sap = 513
feat_weapon_specialization_short_sword = 514
feat_weapon_specialization_battleaxe = 515
feat_weapon_specialization_light_flail = 516
feat_weapon_specialization_heavy_lance = 517
feat_weapon_specialization_longsword = 518
feat_weapon_specialization_heavy_pick = 519
feat_weapon_specialization_rapier = 520
feat_weapon_specialization_scimitar = 521
feat_weapon_specialization_trident = 522
feat_weapon_specialization_warhammer = 523
feat_weapon_specialization_falchion = 524
feat_weapon_specialization_heavy_flail = 525
feat_weapon_specialization_glaive = 526
feat_weapon_specialization_greataxe = 527
feat_weapon_specialization_greatclub = 528
feat_weapon_specialization_greatsword = 529
feat_weapon_specialization_guisarme = 530
feat_weapon_specialization_halberd = 531
feat_weapon_specialization_longspear = 532
feat_weapon_specialization_ranseur = 533
feat_weapon_specialization_scythe = 534
feat_weapon_specialization_shortbow = 535
feat_weapon_specialization_composite_shortbow = 536
feat_weapon_specialization_longbow = 537
feat_weapon_specialization_composite_longbow = 538
feat_weapon_specialization_halfling_kama = 539
feat_weapon_specialization_kukri = 540
feat_weapon_specialization_halfling_nunchaku = 541
feat_weapon_specialization_halfling_siangham = 542
feat_weapon_specialization_kama = 543
feat_weapon_specialization_nunchaku = 544
feat_weapon_specialization_siangham = 545
feat_weapon_specialization_bastard_sword = 546
feat_weapon_specialization_dwarven_waraxe = 547
feat_weapon_specialization_gnome_hooked_hammer = 548
feat_weapon_specialization_orc_double_axe = 549
feat_weapon_specialization_spike_chain = 550
feat_weapon_specialization_dire_flail = 551
feat_weapon_specialization_two_bladed_sword = 552
feat_weapon_specialization_dwarven_urgrosh = 553
feat_weapon_specialization_hand_crossbow = 554
feat_weapon_specialization_shuriken = 555
feat_weapon_specialization_whip = 556
feat_weapon_specialization_repeating_crossbow = 557
feat_weapon_specialization_net = 558
feat_weapon_specialization_grapple = 559
feat_whirlwind_attack = 560
feat_barbarian_rage = 561
feat_stunning_attacks = 562
feat_wholeness_of_body = 563
feat_lay_on_hands = 564
feat_smite_evil = 565
feat_remove_disease = 566
feat_detect_evil = 567
feat_aura_of_courage = 568
feat_divine_health = 569
feat_divine_grace = 570
feat_special_mount = 571
feat_code_of_conduct = 572
feat_associates = 573
feat_defensive_roll = 574
feat_turn_undead = 575
feat_rebuke_undead = 576
feat_domain_power = 577
feat_spontaneous_casting_cure = 578
feat_spontaneous_casting_inflict = 579
feat_combat_reflexes = 580
feat_martial_weapon_proficiency_all = 581
feat_simple_weapon_proficiency_druid = 582
feat_simple_weapon_proficiency_monk = 583
feat_simple_weapon_proficiency_rogue = 584
feat_simple_weapon_proficiency_wizard = 585
feat_simple_weapon_proficiency_elf = 586
feat_uncanny_dodge = 587
feat_fast_movement = 588
feat_bardic_music = 589
feat_bardic_knowledge = 590
feat_nature_sense = 591
feat_woodland_stride = 592
feat_trackless_step = 593
feat_resist_natures_lure = 594
feat_wild_shape = 595
feat_venom_immunity = 596
feat_armor_proficiency_druid = 597
feat_flurry_of_blows = 598
feat_evasion = 599
feat_still_mind = 600
feat_purity_of_body = 601
feat_improved_evasion = 602
feat_ki_strike = 603
feat_sneak_attack = 604
feat_traps = 605
feat_crippling_strike = 606
feat_opportunist = 607
feat_skill_mastery = 608
feat_slippery_mind = 609
feat_call_familiar = 610
feat_favored_enemy_aberration = 611
feat_favored_enemy_animal = 612
feat_favored_enemy_beast = 613
feat_favored_enemy_construct = 614
feat_favored_enemy_dragon = 615
feat_favored_enemy_elemental = 616
feat_favored_enemy_fey = 617
feat_favored_enemy_giant = 618
feat_favored_enemy_magical_beast = 619
feat_favored_enemy_monstrous_humanoid = 620
feat_favored_enemy_ooze = 621
feat_favored_enemy_plant = 622
feat_favored_enemy_shapechanger = 623
feat_favored_enemy_undead = 624
feat_favored_enemy_vermin = 625
feat_favored_enemy_outsider_evil = 626
feat_favored_enemy_outsider_good = 627
feat_favored_enemy_outsider_lawful = 628
feat_favored_enemy_outsider_chaotic = 629
feat_favored_enemy_humanoid_goblinoid = 630
feat_favored_enemy_humanoid_reptilian = 631
feat_favored_enemy_humanoid_dwarf = 632
feat_favored_enemy_humanoid_elf = 633
feat_favored_enemy_humanoid_gnoll = 634
feat_favored_enemy_humanoid_gnome = 635
feat_favored_enemy_humanoid_halfling = 636
feat_favored_enemy_humanoid_orc = 637
feat_favored_enemy_humanoid_human = 638
feat_ambidexterity_ranger = 639
feat_two_weapon_fighting_ranger = 640
feat_improved_two_weapon_fighting_ranger = 641
feat_animal_companion = 642
feat_ranger_two_weapon_style = 643
feat_ranger_archery_style = 644
feat_widen_spell = 645
feat_ranger_rapid_shot = 646
feat_ranger_manyshot = 647
feat_simple_weapon_proficiency_bard = 648
feat_none = 649
feat_exotic_weapon_proficiency_head = 650
feat_improved_critical_head = 651
feat_martial_weapon_proficiency_head = 652
feat_skill_focus_head = 653
feat_weapon_finesse_head = 654
feat_weapon_focus_head = 655
feat_greater_weapon_focus_head = 656
feat_weapon_specialization_head = 657
feat_diamond_body = 658
feat_abundant_step = 659
feat_diamond_soul = 660
feat_quivering_palm = 661
feat_empty_body = 662
feat_perfect_self = 663
feat_greater_two_weapon_fighting_ranger = 664
feat_improved_precise_shot = 665
feat_improved_precise_shot_ranger = 666
feat_sharp_shooting = 667
feat_divine_might = 668
feat_reckless_offense = 669
feat_knock_down = 670
feat_superior_expertise = 671
feat_deadly_precision = 672
feat_persistent_spell = 673
feat_power_critical = 674
feat_greater_rage = 675
feat_greater_weapon_specialization_gauntlet = 676
feat_greater_weapon_specialization_unarmed_strike = 677
feat_greater_weapon_specialization_unarmed_strike_small_being = 678
feat_greater_weapon_specialization_dagger = 679
feat_greater_weapon_specialization_punching_dagger = 680
feat_greater_weapon_specialization_spiked_gauntlet = 681
feat_greater_weapon_specialization_light_mace = 682
feat_greater_weapon_specialization_sickle = 683
feat_greater_weapon_specialization_club = 684
feat_greater_weapon_specialization_shortspear = 685
feat_greater_weapon_specialization_heavy_mace = 686
feat_greater_weapon_specialization_morningstar = 687
feat_greater_weapon_specialization_quarterstaff = 688
feat_greater_weapon_specialization_spear = 689
feat_greater_weapon_specialization_light_crossbow = 690
feat_greater_weapon_specialization_dart = 691
feat_greater_weapon_specialization_sling = 692
feat_greater_weapon_specialization_heavy_crossbow = 693
feat_greater_weapon_specialization_javelin = 694
feat_greater_weapon_specialization_throwing_axe = 695
feat_greater_weapon_specialization_light_hammer = 696
feat_greater_weapon_specialization_handaxe = 697
feat_greater_weapon_specialization_light_lance = 698
feat_greater_weapon_specialization_light_pick = 699
feat_greater_weapon_specialization_sap = 700
feat_greater_weapon_specialization_short_sword = 701
feat_greater_weapon_specialization_battleaxe = 702
feat_greater_weapon_specialization_light_flail = 703
feat_greater_weapon_specialization_heavy_lance = 704
feat_greater_weapon_specialization_longsword = 705
feat_greater_weapon_specialization_heavy_pick = 706
feat_greater_weapon_specialization_rapier = 707
feat_greater_weapon_specialization_scimitar = 708
feat_greater_weapon_specialization_trident = 709
feat_greater_weapon_specialization_warhammer = 710
feat_greater_weapon_specialization_falchion = 711
feat_greater_weapon_specialization_heavy_flail = 712
feat_greater_weapon_specialization_glaive = 713
feat_greater_weapon_specialization_greataxe = 714
feat_greater_weapon_specialization_greatclub = 715
feat_greater_weapon_specialization_greatsword = 716
feat_greater_weapon_specialization_guisarme = 717
feat_greater_weapon_specialization_halberd = 718
feat_greater_weapon_specialization_longspear = 719
feat_greater_weapon_specialization_ranseur = 720
feat_greater_weapon_specialization_scythe = 721
feat_greater_weapon_specialization_shortbow = 722
feat_greater_weapon_specialization_composite_shortbow = 723
feat_greater_weapon_specialization_longbow = 724
feat_greater_weapon_specialization_composite_longbow = 725
feat_greater_weapon_specialization_butterfly_sword = 726
feat_greater_weapon_specialization_kukri = 727
feat_greater_weapon_specialization_war_fan = 728
feat_greater_weapon_specialization_monk_spade = 729
feat_greater_weapon_specialization_kama = 730
feat_greater_weapon_specialization_tonfa = 731
feat_greater_weapon_specialization_siangham = 732
feat_greater_weapon_specialization_bastard_sword = 733
feat_greater_weapon_specialization_dwarven_waraxe = 734
feat_greater_weapon_specialization_gnome_hooked_hammer = 735
feat_greater_weapon_specialization_orc_double_axe = 736
feat_greater_weapon_specialization_spike_chain = 737
feat_greater_weapon_specialization_dire_flail = 738
feat_greater_weapon_specialization_two_bladed_sword = 739
feat_greater_weapon_specialization_dwarven_urgrosh = 740
feat_greater_weapon_specialization_hand_crossbow = 741
feat_greater_weapon_specialization_shuriken = 742
feat_greater_weapon_specialization_whip = 743
feat_greater_weapon_specialization_repeating_crossbow = 744
feat_greater_weapon_specialization_net = 745
feat_greater_weapon_specialization_grapple = 746
feat_tireless_rage = 747
feat_mighty_rage = 748
feat_indomitable_will = 749

stat_strength = 0
stat_dexterity = 1
stat_constitution = 2
stat_intelligence = 3
stat_wisdom = 4
stat_charisma = 5

stat_level = 6
stat_level_barbarian = 7
stat_level_bard = 8
stat_level_cleric = 9
stat_level_druid = 10
stat_level_fighter = 11
stat_level_monk = 12
stat_level_paladin = 13
stat_level_ranger = 14
stat_level_rogue = 15
stat_level_sorcerer = 16
stat_level_wizard = 17
stat_level_arcane_archer = 18
stat_level_arcane_trickster = 19
stat_level_archmage = 20
stat_level_assassin = 21
stat_level_blackguard = 22
stat_level_dragon_disciple = 23
stat_level_duelist = 24
stat_level_dwarven_defender = 25
stat_level_eldritch_knight = 26
stat_level_hierophant = 27
stat_level_horizon_walker = 28
stat_level_loremaster = 29
stat_level_mystic_theurge = 30
stat_level_shadowdancer = 31
stat_level_thaumaturgist = 32
stat_level_warlock = 33
stat_level_favored_soul = 34
stat_level_red_avenger = 35
stat_level_iaijutsu_master = 36
stat_level_sacred_fist = 37
stat_level_stormlord = 38
stat_level_elemental_savant = 39
stat_level_blood_magus = 40
stat_level_beastmaster = 41
stat_level_cryokineticist = 42
stat_level_frost_mage = 43
stat_level_artificer = 44
stat_level_abjurant_champion = 45
stat_level_psion = 58
stat_level_psychic_warrior = 59
stat_level_soulknife = 60
stat_level_wilder = 61
stat_level_cerebmancer = 62
stat_level_elocator = 63
stat_level_metamind = 64
stat_level_psion_uncarnate = 65
stat_level_psionic_fist = 66
stat_level_pyrokineticist = 67
stat_level_slayer = 68
stat_level_thrallherd = 69
stat_level_war_mind = 70
stat_level_crusader = 71
stat_level_swordsage = 72
stat_level_warblade = 73
stat_level_bloodclaw_master = 74
stat_level_bloodstorm_blade = 75
stat_level_deepstone_sentinel = 76
stat_level_eternal_blade = 77
stat_level_jade_phoenix_mage = 78
stat_level_master_of_nine = 79
stat_level_ruby_knight_vindicator = 80
stat_level_shadow_sun_ninja = 81
stat_hp_max = 228
stat_hp_current = 229
stat_race = 230
stat_category = 231
stat_gender = 232
stat_age = 233
stat_height = 234
stat_weight = 235
stat_size = 236
stat_experience = 237
stat_alignment = 238
stat_deity = 239
stat_domain_1 = 240
stat_domain_2 = 241
stat_alignment_choice = 242
stat_favored_enemies = 243
stat_known_spells = 244
stat_memorized_spells = 245
stat_spells_per_day = 246
stat_school_specialization = 247
stat_school_prohibited = 248
stat_money = 249
stat_money_pp = 250
stat_money_gp = 251
stat_money_ep = 252
stat_money_sp = 253
stat_money_cp = 254
stat_str_mod = 255
stat_dex_mod = 256
stat_con_mod = 257
stat_int_mod = 258
stat_wis_mod = 259
stat_cha_mod = 260
stat_ac = 261
stat_initiative_bonus = 262
stat_save_reflexes = 263
stat_save_fortitude = 264
stat_save_willpower = 265
stat_attack_bonus = 266
stat_damage_bonus = 267
stat_carried_weight = 268
stat_movement_speed = 269
stat_run_speed = 270
stat_load = 271
stat_subdual_damage = 272
stat_caster_level = 273
stat_caster_level_barbarian = 274
stat_caster_level_bard = 275
stat_caster_level_cleric = 276
stat_caster_level_druid = 277
stat_caster_level_fighter = 278
stat_caster_level_monk = 279
stat_caster_level_paladin = 280
stat_caster_level_ranger = 281
stat_caster_level_rogue = 282
stat_caster_level_sorcerer = 283
stat_caster_level_wizard = 284
stat_subrace = 285
stat_melee_attack_bonus = 286
stat_ranged_attack_bonus = 287
stat_spell_list_level = 288
stat_psi_points_max = 300
stat_psi_points_cur = 301

# NPC Flags (obj_f_npc_flags)
ONF_EX_FOLLOWER = 1
ONF_WAYPOINTS_DAY = 2
ONF_WAYPOINTS_NIGHT = 4
ONF_AI_WAIT_HERE = 8
ONF_AI_SPREAD_OUT = 16
ONF_JILTED = 32
ONF_LOGBOOK_IGNORES = 64
ONF_UNUSED_00000080 = 128
ONF_KOS = 256
ONF_USE_ALERTPOINTS = 512
ONF_FORCED_FOLLOWER = 1024
ONF_KOS_OVERRIDE = 2048
ONF_WANDERS = 4096
ONF_WANDERS_IN_DARK = 8192
ONF_FENCE = 16384
ONF_FAMILIAR = 32768
ONF_CHECK_LEADER = 65536
ONF_NO_EQUIP = 131072
ONF_CAST_HIGHEST = 262144
ONF_GENERATOR = 0x80000
ONF_GENERATED = 0x100000
ONF_GENERATOR_RATE1 = 0x200000
ONF_GENERATOR_RATE2 = 0x400000
ONF_GENERATOR_RATE3 = 0x800000
ONF_DEMAINTAIN_SPELLS = 16777216
ONF_UNUSED_02000000 = 33554432
ONF_UNUSED_04000000 = 67108864
ONF_UNUSED_08000000 = 134217728
ONF_BACKING_OFF = 0x10000000
ONF_NO_ATTACK = 0x20000000
ONF_BOSS_MONSTER = 0x40000000
ONF_EXTRAPLANAR = 0x80000000

# Critter Flags
OCF_IS_CONCEALED = 1
OCF_MOVING_SILENTLY = 2
OCF_EXPERIENCE_AWARDED = 4
OCF_UNUSED_00000008 = 8
OCF_FLEEING = 16
OCF_STUNNED = 32
OCF_PARALYZED = 64
OCF_BLINDED = 128
OCF_HAS_ARCANE_ABILITY = 256
OCF_UNUSED_00000200 = 512
OCF_UNUSED_00000400 = 1024
OCF_UNUSED_00000800 = 2048
OCF_SLEEPING = 4096
OCF_MUTE = 8192
OCF_SURRENDERED = 16384
OCF_MONSTER = 32768
OCF_SPELL_FLEE = 65536
OCF_ENCOUNTER = 131072
OCF_COMBAT_MODE_ACTIVE = 262144
OCF_LIGHT_SMALL = 524288
OCF_LIGHT_MEDIUM = 1048576
OCF_LIGHT_LARGE = 2097152
OCF_LIGHT_XLARGE = 4194304
OCF_UNREVIVIFIABLE = 8388608
OCF_UNRESSURECTABLE = 16777216
OCF_UNUSED_02000000 = 33554432
OCF_UNUSED_04000000 = 67108864
OCF_NO_FLEE = 134217728
OCF_NON_LETHAL_COMBAT = 268435456
OCF_MECHANICAL = 536870912
OCF_UNUSED_40000000 = 1073741824
OCF_FATIGUE_LIMITING = 2147483648


# D20ActionType
EK_D20A_UNSPECIFIED_MOVE = 75
EK_D20A_UNSPECIFIED_ATTACK = 76
EK_D20A_STANDARD_ATTACK = 77
EK_D20A_FULL_ATTACK = 78
EK_D20A_STANDARD_RANGED_ATTACK = 79
EK_D20A_RELOAD = 80
EK_D20A_5FOOTSTEP = 81
EK_D20A_MOVE = 82
EK_D20A_DOUBLE_MOVE = 83
EK_D20A_RUN = 84
EK_D20A_CAST_SPELL = 85
EK_D20A_HEAL = 86
EK_D20A_CLEAVE = 87
EK_D20A_ATTACK_OF_OPPORTUNITY = 88
EK_D20A_WHIRLWIND_ATTACK = 89
EK_D20A_TOUCH_ATTACK = 90
EK_D20A_TOTAL_DEFENSE = 91
EK_D20A_CHARGE = 92
EK_D20A_FALL_TO_PRONE = 93
EK_D20A_STAND_UP = 94
EK_D20A_TURN_UNDEAD = 95
EK_D20A_DEATH_TOUCH = 96
EK_D20A_PROTECTIVE_WARD = 97
EK_D20A_FEAT_OF_STRENGTH = 98
EK_D20A_BARDIC_MUSIC = 99
EK_D20A_PICKUP_OBJECT = 100
EK_D20A_COUP_DE_GRACE = 101
EK_D20A_USE_ITEM = 102
EK_D20A_BARBARIAN_RAGE = 103
EK_D20A_STUNNING_FIST = 104
EK_D20A_SMITE_EVIL = 105
EK_D20A_LAY_ON_HANDS_SET = 106
EK_D20A_DETECT_EVIL = 107
EK_D20A_STOP_CONCENTRATION = 108
EK_D20A_BREAK_FREE = 109
EK_D20A_TRIP = 110
EK_D20A_REMOVE_DISEASE = 111
EK_D20A_ITEM_CREATION = 112
EK_D20A_WHOLENESS_OF_BODY_SET = 113
EK_D20A_USE_MAGIC_DEVICE_DECIPHER_WRITTEN_SPELL = 114
EK_D20A_TRACK = 115
EK_D20A_ACTIVATE_DEVICE_STANDARD = 116
EK_D20A_SPELL_CALL_LIGHTNING = 117
EK_D20A_AOO_MOVEMENT = 118
EK_D20A_CLASS_ABILITY_SA = 119
EK_D20A_ACTIVATE_DEVICE_FREE = 120
EK_D20A_OPEN_INVENTORY = 121
EK_D20A_ACTIVATE_DEVICE_SPELL = 122
EK_D20A_DISABLE_DEVICE = 123
EK_D20A_SEARCH = 124
EK_D20A_SNEAK = 125
EK_D20A_TALK = 126
EK_D20A_OPEN_LOCK = 127
EK_D20A_SLEIGHT_OF_HAND = 128
EK_D20A_OPEN_CONTAINER = 129
EK_D20A_THROW = 130
EK_D20A_THROW_GRENADE = 131
EK_D20A_FEINT = 132
EK_D20A_READY_SPELL = 133
EK_D20A_READY_COUNTERSPELL = 134
EK_D20A_READY_ENTER = 135
EK_D20A_READY_EXIT = 136
EK_D20A_COPY_SCROLL = 137
EK_D20A_READIED_INTERRUPT = 138
EK_D20A_LAY_ON_HANDS_USE = 139
EK_D20A_WHOLENESS_OF_BODY_USE = 140
EK_D20A_DISMISS_SPELLS = 141
EK_D20A_FLEE_COMBAT = 142
EK_D20A_USE_POTION = 143
EK_D20A_DIVINE_MIGHT = 144
EK_D20A_EMPTY_BODY = 145
EK_D20A_QUIVERING_PALM = 146

# Disp Type | dispType
ET_On0 = 0
ET_OnConditionAdd = 1
ET_OnConditionRemove = 2
ET_OnConditionAddPre = 3
ET_OnConditionRemove2 = 4
ET_OnConditionAddFromD20StatusInit = 5
ET_OnD20AdvanceTime = 6
ET_OnTurnBasedStatusInit = 7
ET_OnInitiative = 8
ET_OnNewDay = 9
ET_OnAbilityScoreLevel = 10
ET_OnGetAC = 11
ET_OnGetACBonus2 = 12
ET_OnGetAcModifierFromAttacker = 12
ET_OnSaveThrowLevel = 13
ET_OnSaveThrowSpellResistanceBonus = 14
ET_OnToHitBonusBase = 15
ET_OnToHitBonus2 = 16
ET_OnToHitBonusFromDefenderCondition = 17
ET_OnDealingDamage = 18
ET_OnTakingDamage = 19
ET_OnDealingDamage2 = 20
ET_OnTakingDamage2 = 21
ET_OnReceiveHealing = 22
ET_OnGetCriticalHitRange = 23
ET_OnGetCriticalHitExtraDice = 24
ET_OnGetCurrentHP = 25
ET_OnGetMaxHP = 26
ET_OnGetInitiativeMod = 27
ET_OnD20Signal = 28
ET_OnD20Query = 29
ET_OnGetSkillLevel = 30
ET_OnBuildRadialMenuEntry = 31
ET_OnGetTooltip = 32
ET_OnDispelCheck = 33
ET_OnGetDefenderConcealmentMissChance = 34
ET_OnGetCasterLevelMod = 35
ET_OnD20ActionCheck = 36
ET_OnD20ActionPerform = 37
ET_OnD20ActionOnActionFrame = 38
ET_OnDestructionDomain = 39
ET_OnGetMoveSpeedBase = 40
ET_OnGetMoveSpeed = 41
ET_OnGetAbilityCheckModifier = 42
ET_OnGetAttackerConcealmentMissChance = 43
ET_OnCountersongSaveThrow = 44
ET_OnGetSpellResistanceMod = 45
ET_OnGetSpellDcBase = 46
ET_OnGetSpellDcMod = 47
ET_OnBeginRound = 48
ET_OnReflexThrow = 49
ET_OnDeflectArrows = 50
ET_OnGetNumAttacksBase = 51
ET_OnGetBonusAttacks = 52
ET_OnGetCritterNaturalAttacksNum = 53
ET_OnObjectEvent = 54
ET_OnProjectileCreated = 55
ET_OnProjectileDestroyed = 56
ET_On57 = 57
ET_On58 = 58
ET_OnGetAbilityLoss = 59
ET_OnGetAttackDice = 60
ET_OnGetLevel = 61
ET_OnImmunityTrigger = 62
ET_On63 = 63
ET_OnSpellImmunityCheck = 64
ET_OnGetEffectTooltip = 65
ET_OnStatBaseGet = 66
ET_OnWeaponGlowType = 67
ET_OnItemForceRemove = 68
ET_OnGetArmorToHitPenalty = 69
ET_OnGetMaxDexAcBonus = 70
ET_OnGetSizeCategory = 71
ET_OnGetBucklerAcPenalty = 72
ET_OnGetModelScale = 73
ET_OnD20PythonQuery = 74
ET_OnD20PythonSignal = 75
ET_OnD20PythonActionCheck = 76
ET_OnD20PythonActionPerform = 77
ET_OnD20PythonActionFrame = 78
ET_OnD20PythonActionAdd = 79
ET_OnPythonAdf = 80
ET_OnPythonReserved3 = 81
ET_OnPythonReserved4 = 82
ET_OnPythonReserved5 = 83
ET_OnPythonReserved6 = 84
ET_OnPythonReserved7 = 85
ET_OnPythonReserved8 = 86
ET_OnPythonReserved9 = 87
ET_OnSpellListExtensionGet = 88
ET_OnGetBaseCasterLevel = 89
ET_OnLevelupSystemEvent = 90
ET_OnDealingDamageWeaponlikeSpell = 91
ET_OnActionCostMod = 92
ET_OnMetaMagicMod = 93

# D20DispatcherKey
EK_NONE = 0
EK_STAT_STRENGTH = 1
EK_STAT_DEXTERITY = 2
EK_STAT_CONSTITUTION = 3
EK_STAT_INTELLIGENCE = 4
EK_STAT_WISDOM = 5
EK_STAT_CHARISMA = 6
EK_SAVE_FORTITUDE = 7
EK_SAVE_REFLEX = 8
EK_SAVE_WILL = 9
EK_IMMUNITY_SPELL = 10
EK_IMMUNITY_11 = 11
EK_IMMUNITY_12 = 12
EK_IMMUNITY_COURAGE = 13
EK_IMMUNITY_RACIAL = 14
EK_IMMUNITY_15 = 15
EK_IMMUNITY_SPECIAL = 16
EK_OnEnterAoE = 18
EK_OnLeaveAoE = 19
EK_SKILL_APPRAISE = 20
EK_SKILL_BLUFF = 21
EK_SKILL_CONCENTRATION = 22
EK_SKILL_RIDE = 59
EK_SKILL_SWIM = 60
EK_SKILL_USE_ROPE = 61
EK_LVL_Stats_Activate = 100
EK_LVL_Stats_Check_Complete = 101
EK_LVL_Stats_Finalize = 102
EK_NEWDAY_REST = 145
EK_NEWDAY_CALENDARICAL = 146
EK_S_HP_Changed = 147
EK_S_HealSkill = 148
EK_S_Sequence = 149
EK_S_Pre_Action_Sequence = 150
EK_S_Action_Recipient = 151
EK_S_BeginTurn = 152
EK_S_EndTurn = 153
EK_S_Dropped_Enemy = 154
EK_S_Concentration_Broken = 155
EK_S_Remove_Concentration = 156
EK_S_BreakFree = 157
EK_S_Spell_Cast = 158
EK_S_Spell_End = 159
EK_S_Spell_Grapple_Removed = 160
EK_S_Killed = 161
EK_S_AOOPerformed = 162
EK_S_Aid_Another = 163
EK_S_TouchAttackAdded = 164
EK_S_TouchAttack = 165
EK_S_Temporary_Hit_Points_Removed = 166
EK_S_Standing_Up = 167
EK_S_Bardic_Music_Completed = 168
EK_S_Combat_End = 169
EK_S_Initiative_Update = 170
EK_S_RadialMenu_Clear_Checkbox_Group = 171
EK_S_Combat_Critter_Moved = 172
EK_S_Hide = 173
EK_S_Show = 174
EK_S_Feat_Remove_Slippery_Mind = 175
EK_S_Broadcast_Action = 176
EK_S_Remove_Disease = 177
EK_S_Rogue_Skill_Mastery_Init = 178
EK_S_Spell_Call_Lightning = 179
EK_S_Magical_Item_Deactivate = 180
EK_S_Spell_Mirror_Image_Struck = 181
EK_S_Spell_Sanctuary_Attempt_Save = 182
EK_S_Experience_Awarded = 183
EK_S_Pack = 184
EK_S_Unpack = 185
EK_S_Teleport_Prepare = 186
EK_S_Teleport_Reconnect = 187
EK_S_Atone_Fallen_Paladin = 188
EK_S_Summon_Creature = 189
EK_S_Attack_Made = 190
EK_S_Golden_Skull_Combine = 191
EK_S_Inventory_Update = 192
EK_S_Critter_Killed = 193
EK_S_SetPowerAttack = 194
EK_S_SetExpertise = 195
EK_S_SetCastDefensively = 196
EK_S_Resurrection = 197
EK_S_Dismiss_Spells = 198
EK_S_DealNormalDamage = 199
EK_LVL_Features_Activate = 200
EK_S_Update_Encumbrance = 200
EK_S_Remove_AI_Controlled = 201
EK_LVL_Features_Check_Complete = 201
EK_LVL_Features_Finalize = 202
EK_S_Verify_Obj_Conditions = 202
EK_S_Web_Burning = 203
EK_S_Anim_CastConjureEnd = 204
EK_S_Item_Remove_Enhancement = 205
EK_S_Disarmed_Weapon_Retrieve = 206
EK_S_Disarm = 207
EK_Q_Helpless = 207
EK_S_AID_ANOTHER_WAKE_UP = 208
EK_Q_SneakAttack = 208
EK_Q_OpponentSneakAttack = 209
EK_Q_CoupDeGrace = 210
EK_Q_Mute = 211
EK_Q_CannotCast = 212
EK_Q_CannotUseIntSkill = 213
EK_Q_CannotUseChaSkill = 214
EK_Q_RapidShot = 215
EK_Q_Critter_Is_Concentrating = 216
EK_Q_Critter_Is_On_Consecrate_Ground = 217
EK_Q_Critter_Is_On_Desecrate_Ground = 218
EK_Q_Critter_Is_Held = 219
EK_Q_Critter_Is_Invisible = 220
EK_Q_Critter_Is_Afraid = 221
EK_Q_Critter_Is_Blinded = 222
EK_Q_Critter_Is_Charmed = 223
EK_Q_Critter_Is_Confused = 224
EK_Q_Critter_Is_AIControlled = 225
EK_Q_Critter_Is_Cursed = 226
EK_Q_Critter_Is_Deafened = 227
EK_Q_Critter_Is_Diseased = 228
EK_Q_Critter_Is_Poisoned = 229
EK_Q_Critter_Is_Stunned = 230
EK_Q_Critter_Is_Immune_Critical_Hits = 231
EK_Q_Critter_Is_Immune_Poison = 232
EK_Q_Critter_Has_Spell_Resistance = 233
EK_Q_Critter_Has_Condition = 234
EK_Q_Critter_Has_Freedom_of_Movement = 235
EK_Q_Critter_Has_Endure_Elements = 236
EK_Q_Critter_Has_Protection_From_Elements = 237
EK_Q_Critter_Has_Resist_Elements = 238
EK_Q_Critter_Has_True_Seeing = 239
EK_Q_Critter_Has_Spell_Active = 240
EK_Q_Critter_Can_Call_Lightning = 241
EK_Q_Critter_Can_See_Invisible = 242
EK_Q_Critter_Can_See_Darkvision = 243
EK_Q_Critter_Can_See_Ethereal = 244
EK_Q_Critter_Can_Discern_Lies = 245
EK_Q_Critter_Can_Detect_Chaos = 246
EK_Q_Critter_Can_Detect_Evil = 247
EK_Q_Critter_Can_Detect_Good = 248
EK_Q_Critter_Can_Detect_Law = 249
EK_Q_Critter_Can_Detect_Magic = 250
EK_Q_Critter_Can_Detect_Undead = 251
EK_Q_Critter_Can_Find_Traps = 252
EK_Q_Critter_Can_Dismiss_Spells = 253
EK_Q_Obj_Is_Blessed = 254
EK_Q_Unconscious = 255
EK_Q_Dying = 256
EK_Q_Dead = 257
EK_Q_AOOPossible = 258
EK_Q_AOOIncurs = 259
EK_Q_HoldingCharge = 260
EK_Q_Has_Temporary_Hit_Points = 261
EK_Q_SpellInterrupted = 262
EK_Q_ActionTriggersAOO = 263
EK_Q_ActionAllowed = 264
EK_Q_Prone = 265
EK_Q_RerollSavingThrow = 266
EK_Q_RerollAttack = 267
EK_Q_RerollCritical = 268
EK_Q_Commanded = 269
EK_Q_Turned = 270
EK_Q_Rebuked = 271
EK_Q_CanBeFlanked = 272
EK_Q_Critter_Is_Grappling = 273
EK_Q_Barbarian_Raged = 274
EK_Q_Barbarian_Fatigued = 275
EK_Q_NewRound_This_Turn = 276
EK_Q_Flatfooted = 277
EK_Q_Masterwork = 278
EK_Q_FailedDecipherToday = 279
EK_Q_Polymorphed = 280
EK_Q_IsActionInvalid_CheckAction = 281
EK_Q_CanBeAffected_PerformAction = 282
EK_Q_CanBeAffected_ActionFrame = 283
EK_Q_AOOWillTake = 284
EK_Q_Weapon_Is_Mighty_Cleaving = 285
EK_Q_Autoend_Turn = 286
EK_Q_ExperienceExempt = 287
EK_Q_FavoredClass = 288
EK_Q_IsFallenPaladin = 289
EK_Q_WieldedTwoHanded = 290
EK_Q_Critter_Is_Immune_Energy_Drain = 291
EK_Q_Critter_Is_Immune_Death_Touch = 292
EK_Q_Failed_Copy_Scroll = 293
EK_Q_Armor_Get_AC_Bonus = 294
EK_Q_Armor_Get_Max_DEX_Bonus = 295
EK_Q_Armor_Get_Max_Speed = 296
EK_Q_FightingDefensively = 297
EK_Q_Elemental_Gem_State = 298
EK_Q_Untripable = 299
EK_LVL_Skills_Activate = 300
EK_Q_Has_Thieves_Tools = 300
EK_Q_Critter_Is_Encumbered_Light = 301
EK_LVL_Skills_Check_Complete = 301
EK_LVL_Skills_Finalize = 302
EK_Q_Critter_Is_Encumbered_Medium = 302
EK_Q_Critter_Is_Encumbered_Heavy = 303
EK_Q_Critter_Is_Encumbered_Overburdened = 304
EK_Q_Has_Aura_Of_Courage = 305
EK_Q_BardicInstrument = 306
EK_Q_EnterCombat = 307
EK_Q_AI_Fireball_OK = 308
EK_Q_Critter_Cannot_Loot = 309
EK_Q_Critter_Cannot_Wield_Items = 310
EK_Q_Critter_Is_Spell_An_Ability = 311
EK_Q_Play_Critical_Hit_Anim = 312
EK_Q_Is_BreakFree_Possible = 313
EK_Q_Critter_Has_Mirror_Image = 314
EK_Q_Wearing_Ring_of_Change = 315
EK_Q_Critter_Has_No_Con_Score = 316
EK_Q_Item_Has_Enhancement_Bonus = 317
EK_Q_Item_Has_Keen_Bonus = 318
EK_Q_AI_Has_Spell_Override = 319
EK_Q_Weapon_Get_Keen_Bonus = 320
EK_Q_Disarmed = 321
EK_S_Destruction_Domain_Smite = 322
EK_Q_Can_Perform_Disarm = 323
EK_Q_Craft_Wand_Spell_Level = 324
EK_Q_Is_Ethereal = 325
EK_Q_Empty_Body_Num_Rounds = 326
EK_Q_Quivering_Palm_Can_Perform = 327
EK_Q_Trip_AOO = 328
EK_Q_Get_Arcane_Spell_Failure = 329
EK_Q_Is_Preferring_One_Handed_Wield = 330
EK_LVL_Feats_Activate = 400
EK_LVL_Feats_Check_Complete = 401
EK_LVL_Feats_Finalize = 402
EK_LVL_Spells_Activate = 500
EK_LVL_Spells_Check_Complete = 501
EK_LVL_Spells_Finalize = 502

skill_appraise = 0
skill_bluff = 1
skill_concentration = 2
skill_diplomacy = 3
skill_disable_device = 4
skill_gather_information = 5
skill_heal = 6
skill_hide = 7
skill_intimidate = 8
skill_listen = 9
skill_move_silently = 10
skill_open_lock = 11
skill_pick_pocket = 12
skill_search = 13
skill_sense_motive = 14
skill_spellcraft = 15
skill_spot = 16
skill_tumble = 17
skill_use_magic_device= 18
skill_wilderness_lore = 19
skill_perform = 20 
skill_alchemy = 21
skill_balance = 22
skill_climb = 23
skill_craft = 24
skill_decipher_script = 25
skill_disguise = 26
skill_escape_artist = 27
skill_forgery = 28
skill_handle_animal = 29
skill_innuendo = 30
skill_intuit_direction = 31
skill_jump = 32
skill_knowledge_arcana = 33
skill_knowledge_religion = 34
skill_knowledge_nature = 35
skill_knowledge_all = 36
skill_profession = 37
skill_read_lips = 38
skill_ride = 39
skill_swim = 40
skill_use_rope = 41

spell_acid_splash = 555
spell_ahobm = 570
spell_aid = 1
spell_air_walk = 2
spell_alarm = 3
spell_alter_self = 4
spell_analyze_dweomer = 5
spell_animal_friendship = 6
spell_animal_growth = 7
spell_animal_messenger = 8
spell_animal_shapes = 9
spell_animal_trance = 10
spell_animate_dead = 11
spell_animate_objects = 12
spell_animate_rope = 13
spell_antilife_shell = 14
spell_antimagic_field = 15
spell_antipathy = 16
spell_antiplant_shell = 17
spell_arcane_eye = 18
spell_arcane_lock = 19
spell_arcane_mark = 20
spell_astral_projection = 21
spell_atonement = 22
spell_augury = 23
spell_awaken = 24
spell_bane = 25
spell_banishment = 26
spell_barkskin = 27
spell_bestow_curse = 28
spell_bigbys_clenched_fist = 29
spell_bigbys_crushing_hand = 30
spell_bigbys_forceful_hand = 31
spell_bigbys_grasping_hand = 32
spell_bigbys_interposing_hand = 33
spell_binding = 34
spell_blade_barrier = 35
spell_blasphemy = 36
spell_bless = 37
spell_bless_water = 38
spell_bless_weapon = 39
spell_blight = 542
spell_blindness_deafness = 40
spell_blink = 41
spell_blur = 42
spell_break_enchantment = 43
spell_bulls_strength = 44
spell_burning_hands = 45
spell_call_lightning = 46
spell_call_lightning_storm = 560
spell_calm_animals = 47
spell_calm_emotions = 48
spell_cats_grace = 49
spell_cause_fear = 50
spell_chain_lightning = 51
spell_change_self = 52
spell_changestaff = 53
spell_chaos_hammer = 54
spell_charm_monster = 55
spell_charm_person = 56
spell_charm_person_or_animal = 57
spell_chill_metal = 58
spell_chill_touch = 59
spell_circle_of_death = 60
spell_circle_of_doom = 61
spell_clairaudience_clairvoyance = 62
spell_cloak_of_chaos = 63
spell_clone = 64
spell_cloudkill = 65
spell_color_spray = 66
spell_command = 67
spell_command_plants = 68
spell_commune = 69
spell_commune_with_nature = 70
spell_comprehend_languages = 71
spell_cone_of_cold = 72
spell_confusion = 73
spell_consecrate = 74
spell_contact_other_plane = 75
spell_contagion = 76
spell_contingency = 77
spell_continual_flame = 78
spell_control_plants = 79
spell_control_undead = 80
spell_control_water = 81
spell_control_weather = 82
spell_control_winds = 83
spell_create_food_and_water = 84
spell_create_greater_undead = 85
spell_create_undead = 86
spell_create_water = 87
spell_creeping_doom = 88
spell_crushing_despair = 563
spell_cure_critical_wounds = 89
spell_cure_light_wounds = 90
spell_cure_minor_wounds = 91
spell_cure_moderate_wounds = 92
spell_cure_serious_wounds = 93
spell_curse_water = 94
spell_dancing_lights = 95
spell_darkness = 96
spell_darkvision = 97
spell_daylight = 98
spell_daze = 99
spell_daze_monster = 556
spell_death_knell = 100
spell_death_ward = 101
spell_deathwatch = 102
spell_deep_slumber = 562
spell_deeper_darkness = 103
spell_delay_poison = 104
spell_delayed_blast_fireball = 105
spell_demand = 106
spell_desecrate = 107
spell_destruction = 108
spell_detect_animals_or_plants = 109
spell_detect_chaos = 110
spell_detect_evil = 111
spell_detect_good = 112
spell_detect_law = 113
spell_detect_magic = 114
spell_detect_poison = 115
spell_detect_scrying = 116
spell_detect_secret_doors = 117
spell_detect_snares_and_pits = 118
spell_detect_thoughts = 119
spell_detect_undead = 120
spell_dictum = 121
spell_dimension_door = 123
spell_dimensional_anchor = 122
spell_diminish_plants = 124
spell_discern_lies = 125
spell_discern_location = 126
spell_disguise_self = 52
spell_disintegrate = 127
spell_dismissal = 128
spell_dispel_air = 543
spell_dispel_chaos = 129
spell_dispel_earth = 544
spell_dispel_evil = 130
spell_dispel_fire = 545
spell_dispel_good = 131
spell_dispel_law = 132
spell_dispel_magic = 133
spell_dispel_water = 546
spell_displacement = 134
spell_disrupt_undead = 135
spell_divination = 136
spell_divine_favor = 137
spell_divine_power = 138
spell_dominate_animal = 139
spell_dominate_monster = 140
spell_dominate_person = 141
spell_doom = 142
spell_drawmijs_instant_summons = 143
spell_dream = 144
spell_eagles_splendor = 548
spell_earthquake = 145
spell_elemental_swarm = 146
spell_emotion = 147
spell_endurance = 148
spell_endure_elements = 149
spell_energy_drain = 150
spell_enervation = 151
spell_enlarge = 152
spell_entangle = 153
spell_enthrall = 154
spell_entropic_shield = 155
spell_ethereal_jaunt = 156
spell_etherealness = 157
spell_evards_black_tentacles = 158
spell_expeditious_retreat = 159
spell_explosive_runes = 160
spell_eyebite = 161
spell_fabricate = 162
spell_faerie_fire = 163
spell_false_life = 553
spell_false_vision = 164
spell_fear = 165
spell_feather_fall = 166
spell_feeblemind = 167
spell_find_the_path = 168
spell_find_traps = 169
spell_finger_of_death = 170
spell_fire_seeds = 172
spell_fire_shield = 173
spell_fire_storm = 174
spell_fire_trap = 175
spell_fireball = 171
spell_flame_arrow = 176
spell_flame_blade = 177
spell_flame_strike = 178
spell_flaming_sphere = 179
spell_flare = 180
spell_flesh_to_stone = 181
spell_fly = 182
spell_fog_cloud = 183
spell_forbiddance = 184
spell_forcecage = 185
spell_foresight = 186
spell_foxs_cunning = 549
spell_freedom = 187
spell_freedom_of_movement = 188
spell_gaseous_form = 189
spell_gate = 190
spell_geas_quest = 191
spell_gentle_repose = 192
spell_ghost_sound = 193
spell_ghoul_touch = 194
spell_giant_vermin = 195
spell_glibness = 552
spell_glitterdust = 196
spell_globe_of_invulnerability = 197
spell_glyph_of_warding = 198
spell_good_hope = 564
spell_goodberry = 199
spell_grease = 200
spell_greater_command = 201
spell_greater_dispelling = 202
spell_greater_glyph_of_warding = 203
spell_greater_heroism = 558
spell_greater_magic_fang = 204
spell_greater_magic_weapon = 205
spell_greater_planar_ally = 206
spell_greater_planar_binding = 207
spell_greater_restoration = 208
spell_greater_scrying = 209
spell_greater_shadow_conjuration = 210
spell_greater_shadow_evocation = 211
spell_guards_and_wards = 212
spell_guidance = 213
spell_gust_of_wind = 214
spell_hallow = 215
spell_hallucinatory_terrain = 216
spell_halt_undead = 217
spell_harm = 566
spell_haste = 219
spell_heal = 565
spell_heal_mount = 222
spell_healing_circle = 221
spell_heat_metal = 223
spell_helping_hand = 224
spell_heroes_feast = 225
spell_heroism = 557
spell_hold_animal = 226
spell_hold_monster = 227
spell_hold_person = 228
spell_hold_portal = 229
spell_holy_aura = 230
spell_holy_smite = 231
spell_holy_sword = 232
spell_holy_word = 233
spell_horrid_wilting = 234
spell_hypnotic_pattern = 235
spell_hypnotism = 236
spell_ice_storm = 237
spell_identify = 238
spell_illusory_script = 239
spell_illusory_wall = 240
spell_imbue_with_spell_ability = 241
spell_implosion = 242
spell_imprisonment = 243
spell_improved_invisibility = 244
spell_incendiary_cloud = 245
spell_inflict_critical_wounds = 246
spell_inflict_light_wounds = 247
spell_inflict_minor_wounds = 248
spell_inflict_moderate_wounds = 249
spell_inflict_serious_wounds = 250
spell_insanity = 251
spell_insect_plague = 252
spell_invisibility = 253
spell_invisibility_purge = 254
spell_invisibility_sphere = 255
spell_invisibility_to_animals = 256
spell_invisibility_to_undead = 257
spell_iron_body = 258
spell_ironwood = 259
spell_jump = 260
spell_keen_edge = 261
spell_knock = 262
spell_know_direction = 263
spell_label_level_0 = 803
spell_label_level_1 = 804
spell_label_level_2 = 805
spell_label_level_3 = 806
spell_label_level_4 = 807
spell_label_level_5 = 808
spell_label_level_6 = 809
spell_label_level_7 = 810
spell_label_level_8 = 811
spell_label_level_9 = 812
spell_legend_lore = 264
spell_leomunds_secret_chest = 265
spell_leomunds_secure_shelter = 266
spell_leomunds_tiny_hut = 267
spell_leomunds_trap = 268
spell_lesser_confusion = 561
spell_lesser_geas = 269
spell_lesser_globe_of_invulnerability = 311
spell_lesser_planar_ally = 270
spell_lesser_planar_binding = 271
spell_lesser_restoration = 272
spell_levitate = 273
spell_light = 274
spell_lightning_bolt = 275
spell_limited_wish = 276
spell_list_type_any = 1
spell_list_type_arcane = 2
spell_list_type_bardic = 3
spell_list_type_clerical = 4
spell_list_type_divine = 5
spell_list_type_druidic = 6
spell_list_type_extender = 11
spell_list_type_none = 0
spell_list_type_paladin = 7
spell_list_type_psionic = 8
spell_list_type_ranger = 9
spell_list_type_special = 10
spell_liveoak = 277
spell_locate_creature = 278
spell_locate_object = 279
spell_longstrider = 554
spell_mage_armor = 280
spell_mage_hand = 281
spell_magic_circle_against_chaos = 282
spell_magic_circle_against_evil = 283
spell_magic_circle_against_good = 284
spell_magic_circle_against_law = 285
spell_magic_fang = 286
spell_magic_jar = 287
spell_magic_missile = 288
spell_magic_mouth = 289
spell_magic_stone = 290
spell_magic_vestment = 291
spell_magic_weapon = 292
spell_major_creation = 293
spell_major_image = 294
spell_make_whole = 295
spell_mark_of_justice = 296
spell_mass_bears_endurance = 571
spell_mass_bulls_strength = 572
spell_mass_cats_grace = 573
spell_mass_charm_monster = 297
spell_mass_cure_critical_wounds = 579
spell_mass_cure_moderate_wounds = 577
spell_mass_cure_serious_wounds = 578
spell_mass_eagles_splendor = 574
spell_mass_foxs_cunning = 575
spell_mass_haste = 298
spell_mass_heal = 299
spell_mass_hold_monster = 585
spell_mass_hold_person = 588
spell_mass_inflict_critical_wounds = 583
spell_mass_inflict_moderate_wounds = 581
spell_mass_inflict_serious_wounds = 582
spell_mass_invisibility = 300
spell_mass_owls_wisdom = 576
spell_mass_suggestion = 301
spell_maze = 302
spell_meld_into_stone = 303
spell_melfs_acid_arrow = 304
spell_mending = 305
spell_message = 306
spell_meteor_swarm = 307
spell_mind_blank = 308
spell_mind_fog = 309
spell_minor_creation = 310
spell_minor_image = 312
spell_miracle = 313
spell_mirage_arcana = 314
spell_mirror_image = 315
spell_misdirection = 316
spell_mislead = 317
spell_modify_memory = 318
spell_mordenkainens_disjunction = 319
spell_mordenkainens_faithful_hound = 320
spell_mordenkainens_lucubration = 321
spell_mordenkainens_magnificent_mansion = 322
spell_mordenkainens_private_sanctum = 568
spell_mordenkainens_sword = 323
spell_mount = 324
spell_move_earth = 325
spell_negative_energy_protection = 326
spell_neutralize_poison = 327
spell_new_slot_lvl_0 = 1605
spell_new_slot_lvl_1 = 1606
spell_new_slot_lvl_2 = 1607
spell_new_slot_lvl_3 = 1608
spell_new_slot_lvl_4 = 1609
spell_new_slot_lvl_5 = 1610
spell_new_slot_lvl_6 = 1611
spell_new_slot_lvl_7 = 1612
spell_new_slot_lvl_8 = 1613
spell_new_slot_lvl_9 = 1614
spell_nightmare = 328
spell_nondetection = 329
spell_none = 0
spell_nystuls_magic_aura = 330
spell_nystuls_undetectable_aura = 331
spell_obscure_object = 332
spell_obscuring_mist = 333
spell_open_close = 334
spell_orders_wrath = 335
spell_otilukes_freezing_sphere = 336
spell_otilukes_resilient_sphere = 337
spell_otilukes_telekinetic_sphere = 338
spell_ottos_irresistible_dance = 339
spell_owls_wisdom = 550
spell_pass_without_trace = 341
spell_passwall = 340
spell_permanency = 342
spell_permanent_image = 343
spell_persistent_image = 344
spell_phantasmal_killer = 345
spell_phantom_steed = 346
spell_phase_door = 347
spell_planar_ally = 348
spell_planar_binding = 349
spell_plane_shift = 350
spell_plant_growth = 351
spell_poison = 352
spell_polar_ray = 586
spell_polymorph_any_object = 353
spell_polymorph_other = 354
spell_polymorph_self = 355
spell_power_word_blind = 356
spell_power_word_kill = 357
spell_power_word_stun = 358
spell_prayer = 359
spell_prestidigitation = 360
spell_prismatic_sphere = 361
spell_prismatic_spray = 362
spell_prismatic_wall = 363
spell_produce_flame = 364
spell_programmed_image = 365
spell_project_image = 366
spell_protection_from_arrows = 367
spell_protection_from_chaos = 368
spell_protection_from_elements = 369
spell_protection_from_evil = 370
spell_protection_from_good = 371
spell_protection_from_law = 372
spell_protection_from_spells = 373
spell_prying_eyes = 374
spell_purify_food_and_drink = 375
spell_pyrotechnics = 376
spell_quench = 559
spell_rage = 547
spell_rainbow_pattern = 378
spell_raise_dead = 379
spell_random_action = 380
spell_rarys_mnemonic_enhancer = 381
spell_rarys_telepathic_bond = 382
spell_ray_of_enfeeblement = 383
spell_ray_of_frost = 384
spell_read_magic = 385
spell_readying_innate = 1
spell_readying_vancian = 0
spell_reduce = 386
spell_reduce_animal = 551
spell_refuge = 387
spell_regenerate = 388
spell_reincarnate = 389
spell_reincarnation = 567
spell_remove_blindness_deafness = 390
spell_remove_curse = 391
spell_remove_disease = 392
spell_remove_fear = 393
spell_remove_paralysis = 394
spell_repel_metal_or_stone = 395
spell_repel_vermin = 396
spell_repel_wood = 397
spell_repulsion = 398
spell_resist_elements = 400
spell_resistance = 399
spell_restoration = 401
spell_resurrection = 402
spell_reverse_gravity = 403
spell_righteous_might = 404
spell_rope_trick = 405
spell_rusting_grasp = 406
spell_sanctuary = 407
spell_scare = 408
spell_screen = 409
spell_scrying = 410
spell_sculpt_sound = 411
spell_searing_light = 412
spell_secret_page = 413
spell_see_invisibility = 414
spell_seeming = 415
spell_sending = 416
spell_sepia_snake_sigil = 417
spell_sequester = 418
spell_shades = 419
spell_shadow_conjuration = 420
spell_shadow_evocation = 421
spell_shadow_walk = 422
spell_shambler = 423
spell_shapechange = 424
spell_shatter = 425
spell_shield = 426
spell_shield_of_faith = 427
spell_shield_of_law = 428
spell_shield_other = 429
spell_shillelagh = 430
spell_shocking_grasp = 431
spell_shout = 432
spell_shrink_item = 433
spell_silence = 434
spell_silent_image = 435
spell_simulacrum = 436
spell_slay_living = 437
spell_sleep = 438
spell_sleet_storm = 439
spell_slow = 440
spell_snare = 441
spell_soften_earth_and_stone = 442
spell_solid_fog = 443
spell_soul_bind = 444
spell_sound_burst = 445
spell_source_type_ability = 0
spell_source_type_arcane = 1
spell_source_type_divine = 2
spell_source_type_psionic = 3
spell_speak_with_animals = 446
spell_speak_with_dead = 447
spell_speak_with_plants = 448
spell_spectral_hand = 449
spell_spell_immunity = 450
spell_spell_resistance = 451
spell_spell_turning = 453
spell_spellstaff = 452
spell_spider_climb = 454
spell_spike_growth = 455
spell_spike_stones = 456
spell_spiritual_weapon = 457
spell_statue = 458
spell_status = 459
spell_stinking_cloud = 460
spell_stone_shape = 461
spell_stone_tell = 463
spell_stone_to_flesh = 464
spell_stoneskin = 462
spell_storm_of_vengeance = 465
spell_suggestion = 466
spell_summon_monster_i = 467
spell_summon_monster_ii = 468
spell_summon_monster_iii = 469
spell_summon_monster_iv = 470
spell_summon_monster_ix = 475
spell_summon_monster_v = 471
spell_summon_monster_vi = 472
spell_summon_monster_vii = 473
spell_summon_monster_viii = 474
spell_summon_natures_ally_i = 476
spell_summon_natures_ally_ii = 477
spell_summon_natures_ally_iii = 478
spell_summon_natures_ally_iv = 479
spell_summon_natures_ally_ix = 484
spell_summon_natures_ally_v = 480
spell_summon_natures_ally_vi = 481
spell_summon_natures_ally_vii = 482
spell_summon_natures_ally_viii = 483
spell_summon_swarm = 485
spell_sunbeam = 486
spell_sunburst = 487
spell_symbol = 488
spell_sympathy = 489
spell_tashas_hideous_laughter = 490
spell_telekinesis = 491
spell_teleport = 492
spell_teleport_without_error = 494
spell_teleportation_circle = 493
spell_temporal_stasis = 495
spell_tensers_floating_disk = 496
spell_tensers_transformation = 497
spell_time_stop = 498
spell_tongues = 499
spell_transmute_metal_to_wood = 500
spell_transmute_mud_to_rock = 501
spell_transmute_rock_to_mud = 502
spell_transport_via_plants = 503
spell_trap_the_soul = 504
spell_tree_shape = 505
spell_tree_stride = 506
spell_true_resurrection = 507
spell_true_seeing = 508
spell_true_strike = 509
spell_undeath_to_death = 587
spell_undetectable_alignment = 510
spell_unhallow = 511
spell_unholy_aura = 512
spell_unholy_blight = 513
spell_unseen_servant = 514
spell_vacant = 802
spell_vampiric_touch = 515
spell_vanish = 516
spell_veil = 517
spell_ventriloquism = 518
spell_virtue = 519
spell_vision = 520
spell_wail_of_the_banshee = 521
spell_wall_of_fire = 522
spell_wall_of_force = 523
spell_wall_of_ice = 524
spell_wall_of_iron = 525
spell_wall_of_stone = 526
spell_wall_of_thorns = 527
spell_warp_wood = 528
spell_water_breathing = 529
spell_water_walk = 530
spell_web = 531
spell_weird = 532
spell_whirlwind = 533
spell_whispering_wind = 534
spell_wind_walk = 535
spell_wind_wall = 536
spell_wish = 537
spell_wood_shape = 538
spell_word_of_chaos = 539
spell_word_of_recall = 540
spell_zone_of_truth = 541

# object flags
OF_DESTROYED = 1
OF_OFF = 2
OF_FLAT = 4
OF_TEXT = 8
OF_SEE_THROUGH = 16
OF_SHOOT_THROUGH = 32
OF_ANIMATED_DEAD = 536870912
OF_TRANSLUCENT = 64
OF_SHRUNK = 128
OF_CLICK_THROUGH = 2048
OF_DISALLOW_WADING = 67108864
OF_DONTDRAW = 256
OF_DONTLIGHT = 1048576
OF_DYNAMIC = 8192
OF_EXTINCT = 8388608
OF_HEIGHT_SET = 268435456
OF_INVENTORY = 4096
OF_INVISIBLE = 512
OF_INVULNERABLE = 4194304
OF_NOHEIGHT = 65536
OF_NO_BLOCK = 1024
OF_PROVIDES_COVER = 16384
OF_RADIUS_SET = 2147483648 #2147483648L
OF_RANDOM_SIZE = 32768
OF_STONED = 524288
OF_TELEPORTED = 1073741824
OF_TEXT_FLOATER = 2097152
OF_TRAP_PC = 16777216
OF_TRAP_SPOTTED = 33554432
OF_UNUSED_08000000 = 134217728
OF_UNUSED_40000 = 262144
OF_WADING = 131072

OPF_ALWAYS_LOCKED = 16
OPF_BUSTED = 128
OPF_JAMMED = 2
OPF_LOCKED = 1
OPF_LOCKED_DAY = 32
OPF_LOCKED_NIGHT = 64
OPF_MAGICALLY_HELD = 4
OPF_NEVER_LOCKED = 8
OPF_NOT_STICKY = 256
OPF_OPEN = 512

OLC_ALL = 262142
OLC_AMMO = 64
OLC_ARMOR = 128
OLC_BAG = 4096
OLC_CONTAINER = 4
OLC_CRITTERS = 98304
OLC_FOOD = 512
OLC_GENERIC = 16384
OLC_IMMOBILE = 131082
OLC_ITEMS = 32736
OLC_KEY = 2048
OLC_MOBILE = 131060
OLC_MONEY = 256
OLC_NONE = 0
OLC_NPC = 65536
OLC_PC = 32768
OLC_PORTAL = 2
OLC_PROJECTILE = 16
OLC_SCENERY = 8
OLC_SCROLL = 1024
OLC_TRAP = 131072
OLC_WEAPON = 32
OLC_WRITTEN = 8192

# Item Flags (obj_f_item_flags)
OIF_IDENTIFIED = 1
OIF_WONT_SELL = 2
OIF_IS_MAGICAL = 4
OIF_NO_PICKPOCKET = 8
OIF_NO_DISPLAY = 16
OIF_NO_DROP = 32
OIF_CAN_USE_BOX = 128
OIF_DRAW_WHEN_PARENTED = 4194304
OIF_EXPIRES_AFTER_USE = 8388608
OIF_LIGHT_LARGE = 2048
OIF_LIGHT_MEDIUM = 1024
OIF_LIGHT_SMALL = 512
OIF_LIGHT_XLARGE = 4096
OIF_MT_TRIGGERED = 16384
OIF_NEEDS_SPELL = 64
OIF_NEEDS_TARGET = 256
OIF_NO_DECAY = 131072
OIF_NO_LOOT = 16777216
OIF_NO_NPC_PICKUP = 524288
OIF_NO_RANGED_USE = 1048576
OIF_NO_TRANSFER = 67108864
OIF_PERSISTENT = 8192
OIF_STOLEN = 32768
OIF_UBER = 262144
OIF_USES_WAND_ANIM = 33554432
OIF_USE_IS_THROW = 65536
OIF_VALID_AI_ACTION = 2097152

# Damage Type
D20DT_BLUDGEONING = 0
D20DT_PIERCING = 1
D20DT_SLASHING = 2
D20DT_BLUDGEONING_AND_PIERCING = 3
D20DT_PIERCING_AND_SLASHING = 4
D20DT_SLASHING_AND_BLUDGEONING = 5
D20DT_SLASHING_AND_BLUDGEONING_AND_PIERCING = 6
D20DT_ACID = 7
D20DT_COLD = 8
D20DT_ELECTRICITY = 9
D20DT_FIRE = 10
D20DT_SONIC = 11
D20DT_NEGATIVE_ENERGY = 12
D20DT_SUBDUAL = 13
D20DT_POISON = 14
D20DT_POSITIVE_ENERGY = 15
D20DT_FORCE = 16
D20DT_BLOOD_LOSS = 17
D20DT_MAGIC = 18
D20DT_UNSPECIFIED = -1

# D20 Attack Power
D20DAP_NORMAL = 1
D20DAP_UNSPECIFIED = 2
D20DAP_SILVER = 4
D20DAP_ADAMANTIUM = 256
D20DAP_BLUDGEONING = 512
D20DAP_CHAOS = 64
D20DAP_COLD = 8192
D20DAP_FORCE = 16384
D20DAP_HOLY = 16
D20DAP_LAW = 128
D20DAP_MAGIC = 8
D20DAP_MITHRIL = 4096
D20DAP_PIERCING = 1024
D20DAP_SLASHING = 2048
D20DAP_UNHOLY = 32

D20ADF_None = 0
D20ADF_Breaks_Concentration = 1048576
D20ADF_CallLightningTargeting = 4096
D20ADF_DrawPathByDefault = 262144
D20ADF_MagicEffectTargeting = 16
D20ADF_Movement = 4
D20ADF_PathSthg = 524288
D20ADF_Python = 16777216
D20ADF_QueryForAoO = 128
D20ADF_SimulsCompatible = 131072
D20ADF_TargetContainer = 65536
D20ADF_TargetSingleExcSelf = 8
D20ADF_TargetSingleIncSelf = 512
D20ADF_TargetingBasedOnD20Data = 1024
D20ADF_TriggersAoO = 256
D20ADF_TriggersCombat = 2048
D20ADF_Unk1 = 1
D20ADF_Unk2 = 2
D20ADF_Unk20 = 32
D20ADF_Unk2000 = 8192
D20ADF_Unk40 = 64
D20ADF_Unk4000 = 16384
D20ADF_UseCursorForPicking = 32768

# D20TargetClassification
D20TC_Target0 = 0
D20TC_Movement = 1
D20TC_SingleExcSelf = 2
D20TC_SingleIncSelf = 4
D20TC_CallLightning = 5
D20TC_CastSpell = 3
D20TC_Invalid = -1
D20TC_ItemInteraction = 6

# D20ActionSpecFunc
D20ACT_NULL = 0
D20ACT_Move_Action = 1
D20ACT_Standard_Action = 2
D20ACT_Partial_Charge = 3
D20ACT_Full_Round_Action = 4

# D20CAF flags
D20CAF_HIT = 1
D20CAF_UNNECESSARY = 1
D20CAF_CRITICAL = 2
D20CAF_RANGED = 4
D20CAF_ACTIONFRAME_PROCESSED = 8
D20CAF_NEED_PROJECTILE_HIT = 16
D20CAF_NEED_ANIM_COMPLETED = 32
D20CAF_ATTACK_OF_OPPORTUNITY = 64
D20CAF_CONCEALMENT_MISS = 128
D20CAF_TOUCH_ATTACK = 256
D20CAF_FREE_ACTION = 512
D20CAF_CHARGE = 1024
D20CAF_REROLL = 2048
D20CAF_REROLL_CRITICAL = 4096
D20CAF_TRAP = 8192
D20CAF_ALTERNATE = 16384
D20CAF_NO_PRECISION_DAMAGE = 32768
D20CAF_FLANKED = 65536
D20CAF_DEFLECT_ARROWS = 131072
D20CAF_FULL_ATTACK = 262144
D20CAF_AOO_MOVEMENT = 524288
D20CAF_BONUS_ATTACK = 1048576
D20CAF_THROWN = 2097152
D20CAF_SAVE_SUCCESSFUL = 8388608
D20CAF_SECONDARY_WEAPON = 16777216
D20CAF_MANYSHOT = 33554432
D20CAF_ALWAYS_HIT = 67108864
D20CAF_COVER = 134217728
D20CAF_COUNTERSPELLED = 268435456
D20CAF_THROWN_GRENADE = 536870912
D20CAF_FINAL_ATTACK_ROLL = 1073741824
D20CAF_TRUNCATED = 2147483648 #2147483648L

# SavingThrowType
D20_Save_Fortitude = 0
D20_Save_Reduction_Half = 1
D20_Save_Reduction_None = 0
D20_Save_Reduction_Quarter = 2
D20_Save_Reflex = 1
D20_Save_Will = 2

# D20SavingThrowFlag
D20STD_F_NONE = 0
D20STD_F_REROLL = 1
D20STD_F_CHARM = 2
D20STD_F_TRAP = 3
D20STD_F_POISON = 4
D20STD_F_SPELL_LIKE_EFFECT = 5
D20STD_F_SPELL_SCHOOL_ABJURATION = 6
D20STD_F_SPELL_SCHOOL_CONJURATION = 7
D20STD_F_SPELL_SCHOOL_DIVINATION = 8
D20STD_F_SPELL_SCHOOL_ENCHANTMENT = 9
D20STD_F_SPELL_SCHOOL_EVOCATION = 10
D20STD_F_SPELL_SCHOOL_ILLUSION = 11
D20STD_F_SPELL_SCHOOL_NECROMANCY = 12
D20STD_F_SPELL_SCHOOL_TRANSMUTATION = 13
D20STD_F_SPELL_DESCRIPTOR_ACID = 14 # ACID
D20STD_F_SPELL_DESCRIPTOR_CHAOTIC = 15 # CHAOTIC
D20STD_F_SPELL_DESCRIPTOR_COLD = 16 # COLD
D20STD_F_SPELL_DESCRIPTOR_DARKNESS = 17 # DARKNESS
D20STD_F_SPELL_DESCRIPTOR_DEATH = 18 # DEATH
D20STD_F_SPELL_DESCRIPTOR_ELECTRICITY = 19 # ELECTRICITY
D20STD_F_SPELL_DESCRIPTOR_EVIL = 20 # EVIL
D20STD_F_SPELL_DESCRIPTOR_FEAR = 21 # FEAR
D20STD_F_SPELL_DESCRIPTOR_FIRE = 22 # FIRE
D20STD_F_SPELL_DESCRIPTOR_FORCE = 23 # FORCE
D20STD_F_SPELL_DESCRIPTOR_GOOD = 24 # GOOD
D20STD_F_SPELL_DESCRIPTOR_LANGUAGE_DEPENDENT = 25 # LANGUAGE
D20STD_F_SPELL_DESCRIPTOR_LAWFUL = 26 # LAWFUL
D20STD_F_SPELL_DESCRIPTOR_LIGHT = 27 # LIGHT
D20STD_F_SPELL_DESCRIPTOR_MIND_AFFECTING = 28 # MIND
D20STD_F_SPELL_DESCRIPTOR_SONIC = 29 # SONIC
D20STD_F_SPELL_DESCRIPTOR_TELEPORTATION = 30 # TELEPORTATION
D20STD_F_SPELL_DESCRIPTOR_AIR = 31 # AIR
D20STD_F_SPELL_DESCRIPTOR_EARTH = 32 # EARTH
D20STD_F_SPELL_DESCRIPTOR_WATER = 33 # WATER
D20STD_F_DISABLE_SLIPPERY_MIND = 34
D20STD_F_MAX = 0

# D20ActionType
D20A_NONE = -1
D20A_UNSPECIFIED_MOVE = 0
D20A_UNSPECIFIED_ATTACK = 1
D20A_5FOOTSTEP = 6
D20A_ACTIVATE_DEVICE_FREE = 45
D20A_ACTIVATE_DEVICE_SPELL = 47
D20A_ACTIVATE_DEVICE_STANDARD = 41
D20A_AID_ANOTHER_WAKE_UP = 79
D20A_AOO_MOVEMENT = 43
D20A_ATTACK_OF_OPPORTUNITY = 13
D20A_BARBARIAN_RAGE = 28
D20A_BARDIC_MUSIC = 24
D20A_BREAK_FREE = 34
D20A_BULLRUSH = 72
D20A_CAST_SPELL = 10
D20A_CHARGE = 17
D20A_CLASS_ABILITY_SA = 44
D20A_CLEAVE = 12
D20A_COPY_SCROLL = 62
D20A_COUP_DE_GRACE = 26
D20A_DEATH_TOUCH = 21
D20A_DETECT_EVIL = 32
D20A_DISABLE_DEVICE = 48
D20A_DISARM = 70
D20A_DISARMED_WEAPON_RETRIEVE = 78
D20A_DISMISS_SPELLS = 66
D20A_DIVINE_MIGHT = 69
D20A_DOUBLE_MOVE = 8
D20A_EMPTY_BODY = 80
D20A_FALL_TO_PRONE = 18
D20A_FEAT_OF_STRENGTH = 23
D20A_FEINT = 57
D20A_FLEE_COMBAT = 67
D20A_FULL_ATTACK = 3
D20A_GRAPPLE = 74
D20A_HEAL = 11
D20A_ITEM_CREATION = 37
D20A_LAY_ON_HANDS_SET = 31
D20A_LAY_ON_HANDS_USE = 64
D20A_MOVE = 7
D20A_OPEN_CONTAINER = 54
D20A_OPEN_INVENTORY = 46
D20A_OPEN_LOCK = 52
D20A_OVERRUN = 76
D20A_PICKUP_OBJECT = 25
D20A_PIN = 75
D20A_PROTECTIVE_WARD = 22
D20A_PYTHON_ACTION = 82
D20A_QUIVERING_PALM = 81
D20A_READIED_INTERRUPT = 63
D20A_READY_COUNTERSPELL = 59
D20A_READY_ENTER = 60
D20A_READY_EXIT = 61
D20A_READY_SPELL = 58
D20A_RELOAD = 5
D20A_REMOVE_DISEASE = 36
D20A_RUN = 9
D20A_SEARCH = 49
D20A_SHIELD_BASH = 77
D20A_SLEIGHT_OF_HAND = 53
D20A_SMITE_EVIL = 30
D20A_SNEAK = 50
D20A_SPELL_CALL_LIGHTNING = 42
D20A_STANDARD_ATTACK = 2
D20A_STANDARD_RANGED_ATTACK = 4
D20A_STAND_UP = 19
D20A_STOP_CONCENTRATION = 33
D20A_STUNNING_FIST = 29
D20A_SUNDER = 71
D20A_TALK = 51
D20A_THROW = 55
D20A_THROW_GRENADE = 56
D20A_TOTAL_DEFENSE = 16
D20A_TOUCH_ATTACK = 15
D20A_TRACK = 40
D20A_TRAMPLE = 73
D20A_TRIP = 35
D20A_TURN_UNDEAD = 20
D20A_USE_ITEM = 27
D20A_USE_MAGIC_DEVICE_DECIPHER_WRITTEN_SPELL = 39
D20A_USE_POTION = 68
D20A_WHIRLWIND_ATTACK = 14
D20A_WHOLENESS_OF_BODY_SET = 38
D20A_WHOLENESS_OF_BODY_USE = 65

# Damage Reduction (no damage reduction = 100!)
DAMAGE_REDUCTION_HALF = 50
DAMAGE_REDUCTION_QUARTER = 25

# ActionErrorCode
AEC_OK = 0
AEC_ACTION_INVALID = 14
AEC_ALREADY_MOVED = 4
AEC_AREA_NOT_SAFE = 26
AEC_CANNOT_CAST_NOT_ENOUGH_GP = 20
AEC_CANNOT_CAST_NOT_ENOUGH_XP = 19
AEC_CANNOT_CAST_OUT_OF_AVAILABLE_SPELLS = 18
AEC_CANNOT_CAST_SPELLS = 15
AEC_CANNOT_USE_MUST_USE_BEFORE_ATTACKING = 22
AEC_CANT_WHILE_PRONE = 13
AEC_INVALID_ACTION = 14
AEC_NEED_A_STRAIGHT_LINE = 23
AEC_NEED_MELEE_WEAPON = 12
AEC_NOT_ENOUGH_TIME1 = 1
AEC_NOT_ENOUGH_TIME2 = 2
AEC_NOT_ENOUGH_TIME3 = 3
AEC_NOT_IN_COMBAT = 25
AEC_NO_ACTIONS = 24
AEC_NO_LOS = 10
AEC_OUT_OF_AMMO = 11
AEC_OUT_OF_CHARGES = 16
AEC_OUT_OF_COMBAT_ONLY = 21
AEC_TARGET_BLOCKED = 7
AEC_TARGET_INVALID = 9
AEC_TARGET_OUT_OF_RANGE = 5
AEC_TARGET_TOO_CLOSE = 6
AEC_TARGET_TOO_FAR = 8
AEC_WRONG_WEAPON_TYPE = 17

# Container Flags
OCOF_LOCKED = 1
OCOF_JAMMED = 2
OCOF_MAGICALLY_HELD = 4
OCOF_NEVER_LOCKED = 8
OCOF_ALWAYS_LOCKED = 16
OCOF_BUSTED = 128
OCOF_HAS_BEEN_OPENED = 4096
OCOF_INVEN_SPAWN_INDEPENDENT = 1024
OCOF_INVEN_SPAWN_ONCE = 512
OCOF_LOCKED_DAY = 32
OCOF_LOCKED_NIGHT = 64
OCOF_NOT_STICKY = 256
OCOF_OPEN = 2048

# random_encounter.can_sleep()
SLEEP_SAFE = 0
SLEEP_DANGEROUS = 1
SLEEP_IMPOSSIBLE = 2
SLEEP_PASS_TIME_ONLY = 3

# Text Color (float)
tf_white = 0
tf_red = 1
tf_green = 2
tf_blue = 3
tf_yellow = 4
tf_light_blue = 5

# Races
race_deep_dwarf = 0
race_human = 0
race_derro = 1
race_dwarf = 1
race_duergar = 2
race_elf = 2
race_mountain_dwarf = 3
race_gnome = 3
race_aquatic_elf = 4
race_halfelf = 4
race_half_elf = 4
race_half_orc = 5
race_halforc = 5
race_halfling = 6
race_gray_elf = 6
race_wild_elf = 7
race_wood_elf = 8
race_svirfneblin = 9
race_forest_gnome = 10
race_hill_giant = 10
race_tallfellow = 11
race_troll = 11
race_deep_halfling = 12
race_drow = 66

# Gender
gender_female = 0
gender_male = 1

# Quests
qs_unknown = 0
qs_mentioned = 1
qs_accepted = 2
qs_achieved = 3
qs_completed = 4
qs_other = 5
qs_botched = 6

mc_subtype_air = 1
mc_subtype_aquatic = 2
mc_subtype_extraplanar = 4
mc_subtype_extraplaner = 4
mc_subtype_cold = 8
mc_subtype_chaotic = 16
mc_subtype_demon = 32
mc_subtype_devil = 64
mc_subtype_dwarf = 128
mc_subtype_earth = 256
mc_subtype_electricity = 512
mc_subtype_elf = 1024
mc_subtype_evil = 2048
mc_subtype_fire = 4096
mc_subtype_formian = 8192
mc_subtype_gnoll = 16384
mc_subtype_gnome = 32768
mc_subtype_goblinoid = 65536
mc_subtype_good = 131072
mc_subtype_guardinal = 262144
mc_subtype_half_orc = 524288
mc_subtype_halfling = 1048576
mc_subtype_human = 2097152
mc_subtype_lawful = 4194304
mc_subtype_incorporeal = 8388608
mc_subtype_orc = 16777216
mc_subtype_reptilian = 33554432
mc_subtype_slaadi = 67108864
mc_subtype_water = 134217728

mc_type_aberration = 0
mc_type_animal = 1
mc_type_beast = 2
mc_type_construct = 3
mc_type_dragon = 4
mc_type_elemental = 5
mc_type_fey = 6
mc_type_giant = 7
mc_type_humanoid = 8
mc_type_magical_beast = 9
mc_type_monstrous_humanoid = 10
mc_type_ooze = 11
mc_type_outsider = 12
mc_type_plant = 13
mc_type_shapechanger = 14
mc_type_undead = 15
mc_type_vermin = 16

ALIGNMENT_NEUTRAL = 0
ALIGNMENT_TRUE_NEUTRAL = 0
ALIGNMENT_LAWFUL = 1
ALIGNMENT_LAWFUL_NEUTRAL = 1
ALIGNMENT_CHAOTIC = 2
ALIGNMENT_CHAOTIC_NEUTRAL = 2
ALIGNMENT_GOOD = 4
ALIGNMENT_NEUTRAL_GOOD = 4
ALIGNMENT_LAWFUL_GOOD = 5
ALIGNMENT_CHAOTIC_GOOD = 6
ALIGNMENT_EVIL = 8
ALIGNMENT_NEUTRAL_EVIL = 8
ALIGNMENT_LAWFUL_EVIL = 9
ALIGNMENT_CHAOTIC_EVIL = 10

# Weapon Type
wt_bastard_sword = 57
wt_battleaxe = 26
wt_club = 8
wt_composite_longbow = 49
wt_composite_shortbow = 47
wt_dagger = 3
wt_dart = 15
wt_dire_flail = 62
wt_dwarven_urgrosh = 64
wt_dwarven_waraxe = 58
wt_falchion = 35
wt_gauntlet = 0
wt_glaive = 37
wt_gnome_hooked_hammer = 59
wt_grapple = 70
wt_greataxe = 38
wt_greatclub = 39
wt_greatsword = 40
wt_grenade = 72
wt_guisarme = 41
wt_halberd = 42
wt_halfling_kama = 50
wt_halfling_nunchaku = 52
wt_halfling_siangham = 53
wt_hand_crossbow = 65
wt_handaxe = 21
wt_heavy_crossbow = 17
wt_heavy_flail = 36
wt_heavy_lance = 28
wt_heavy_mace = 10
wt_heavy_pick = 30
wt_javelin = 18
wt_kama = 54
wt_kukri = 51
wt_light_crossbow = 14
wt_light_flail = 27
wt_light_hammer = 20
wt_light_lance = 22
wt_light_mace = 6
wt_light_pick = 23
wt_longbow = 48
wt_longspear = 43
wt_longsword = 29
wt_mindblade = 73
wt_morningstar = 11
wt_net = 69
wt_nunchaku = 55
wt_orc_double_axe = 60
wt_punching_dagger = 4
wt_quarterstaff = 12
wt_ranseur = 44
wt_rapier = 31
wt_ray = 71
wt_repeating_crossbow = 68
wt_sap = 24
wt_scimitar = 32
wt_scythe = 45
wt_short_sword = 25
wt_shortbow = 46
wt_shortspear = 9
wt_shuriken = 66
wt_siangham = 56
wt_sickle = 7
wt_sling = 16
wt_spear = 13
wt_spike_chain = 61
wt_spiked_gauntlet = 5
wt_throwing_axe = 19
wt_trident = 33
wt_two_bladed_sword = 63
wt_unarmed_strike_medium_sized_being = 1
wt_unarmed_strike_small_being = 2
wt_warhammer = 34
wt_whip = 67

OBJECT_SPELL_CLOUDKILL = 12003
OBJECT_SPELL_GENERIC = 12003

Q_AI_Fireball_OK = 101
Q_AI_Has_Spell_Override = 112
Q_AOOIncurs = 52
Q_AOOPossible = 51
Q_AOOWillTake = 77
Q_ActionAllowed = 57
Q_ActionTriggersAOO = 56
Q_Armor_Get_AC_Bonus = 87
Q_Armor_Get_Max_DEX_Bonus = 88
Q_Armor_Get_Max_Speed = 89
Q_Autoend_Turn = 79
Q_Barbarian_Fatigued = 68
Q_Barbarian_Raged = 67
Q_BardicInstrument = 99
Q_CanBeAffected_ActionFrame = 76
Q_CanBeAffected_PerformAction = 75
Q_CanBeFlanked = 65
Q_Can_Perform_Disarm = 116
Q_CannotCast = 5
Q_CannotUseChaSkill = 7
Q_CannotUseIntSkill = 6
Q_Commanded = 62
Q_CoupDeGrace = 3
Q_Craft_Wand_Spell_Level = 117
Q_Critter_Can_Call_Lightning = 34
Q_Critter_Can_Detect_Chaos = 39
Q_Critter_Can_Detect_Evil = 40
Q_Critter_Can_Detect_Good = 41
Q_Critter_Can_Detect_Law = 42
Q_Critter_Can_Detect_Magic = 43
Q_Critter_Can_Detect_Undead = 44
Q_Critter_Can_Discern_Lies = 38
Q_Critter_Can_Dismiss_Spells = 46
Q_Critter_Can_Find_Traps = 45
Q_Critter_Can_See_Darkvision = 36
Q_Critter_Can_See_Ethereal = 37
Q_Critter_Can_See_Invisible = 35
Q_Critter_Cannot_Loot = 102
Q_Critter_Cannot_Wield_Items = 103
Q_Critter_Has_Condition = 27
Q_Critter_Has_Endure_Elements = 29
Q_Critter_Has_Freedom_of_Movement = 28
Q_Critter_Has_Mirror_Image = 107
Q_Critter_Has_No_Con_Score = 109
Q_Critter_Has_Protection_From_Elements = 30
Q_Critter_Has_Resist_Elements = 31
Q_Critter_Has_Spell_Active = 33
Q_Critter_Has_Spell_Resistance = 26
Q_Critter_Has_True_Seeing = 32
Q_Critter_Is_AIControlled = 18
Q_Critter_Is_Afraid = 14
Q_Critter_Is_Blinded = 15
Q_Critter_Is_Charmed = 16
Q_Critter_Is_Concentrating = 9
Q_Critter_Is_Confused = 17
Q_Critter_Is_Cursed = 19
Q_Critter_Is_Deafened = 20
Q_Critter_Is_Diseased = 21
Q_Critter_Is_Encumbered_Heavy = 96
Q_Critter_Is_Encumbered_Light = 94
Q_Critter_Is_Encumbered_Medium = 95
Q_Critter_Is_Encumbered_Overburdened = 97
Q_Critter_Is_Grappling = 66
Q_Critter_Is_Held = 12
Q_Critter_Is_Immune_Critical_Hits = 24
Q_Critter_Is_Immune_Death_Touch = 85
Q_Critter_Is_Immune_Energy_Drain = 84
Q_Critter_Is_Immune_Poison = 25
Q_Critter_Is_Invisible = 13
Q_Critter_Is_On_Consecrate_Ground = 10
Q_Critter_Is_On_Desecrate_Ground = 11
Q_Critter_Is_Poisoned = 22
Q_Critter_Is_Spell_An_Ability = 104
Q_Critter_Is_Stunned = 23
Q_Dead = 50
Q_Disarmed = 114
Q_Dying = 49
Q_Elemental_Gem_State = 91
Q_Empty_Body_Num_Rounds = 119
Q_EnterCombat = 100
Q_ExperienceExempt = 80
Q_FailedDecipherToday = 72
Q_Failed_Copy_Scroll = 86
Q_FavoredClass = 81
Q_FightingDefensively = 90
Q_Flatfooted = 70
Q_Has_Aura_Of_Courage = 98
Q_Has_Temporary_Hit_Points = 54
Q_Has_Thieves_Tools = 93
Q_Helpless = 0
Q_HoldingCharge = 53
Q_IsActionInvalid_CheckAction = 74
Q_IsFallenPaladin = 82
Q_Is_BreakFree_Possible = 106
Q_Is_Ethereal = 118
Q_Item_Has_Enhancement_Bonus = 110
Q_Item_Has_Keen_Bonus = 111
Q_Masterwork = 71
Q_Mute = 4
Q_NewRound_This_Turn = 69
Q_Obj_Is_Blessed = 47
Q_OpponentSneakAttack = 2
Q_Play_Critical_Hit_Anim = 105
Q_Polymorphed = 73
Q_Prone = 58
Q_RapidShot = 8
Q_Rebuked = 64
Q_RerollAttack = 60
Q_RerollCritical = 61
Q_RerollSavingThrow = 59
Q_SneakAttack = 1
Q_SpellInterrupted = 55
Q_Turned = 63
Q_Unconscious = 48
Q_Untripable = 92
Q_Weapon_Get_Keen_Bonus = 113
Q_Weapon_Is_Mighty_Cleaving = 78
Q_Wearing_Ring_of_Change = 108
Q_WieldedTwoHanded = 83

PQF_10 = 16
PQF_ADJUST_RADIUS = 8192
PQF_ADJ_RADIUS_REQUIRE_LOS = 131072
PQF_ALLOW_ALTERNATIVE_TARGET_TILE = 262144
PQF_AVOID_AOOS = 16777216
PQF_A_STAR_TIME_CAPPED = 524288
PQF_DONT_USE_PATHNODES = 16384
PQF_DONT_USE_STRAIGHT_LINE = 32768
PQF_DOORS_ARE_BLOCKING = 1024
PQF_FORCED_STRAIGHT_LINE = 65536
PQF_HAS_CRITTER = 2
PQF_IGNORE_CRITTERS = 128
PQF_IGNORE_CRITTERS_ON_DESTINATION = 8388608
PQF_MAX_PF_LENGTH_STHG = 4
PQF_STRAIGHT_LINE = 8
PQF_STRAIGHT_LINE_ONLY_FOR_SANS_NODE = 512
PQF_TARGET_OBJ = 4096
PQF_TO_EXACT = 1

# Size
STAT_SIZE_NONE = 0
STAT_SIZE_FINE = 1
STAT_SIZE_DIMINUTIVE = 2
STAT_SIZE_TINY = 3
STAT_SIZE_SMALL = 4
STAT_SIZE_MEDIUM = 5
STAT_SIZE_LARGE = 6
STAT_SIZE_HUGE = 7
STAT_SIZE_GARGANTUAN = 8
STAT_SIZE_COLOSSAL = 9

SORT_TARGET_LIST_BY_OBJ_HANDLE = 0
SORT_TARGET_LIST_ORDER_ASCENDING = 0
SORT_TARGET_LIST_BY_HIT_DICE = 1
SORT_TARGET_LIST_ORDER_DESCENDING = 1
SORT_TARGET_LIST_BY_HIT_DICE_THEN_DIST = 2
SORT_TARGET_LIST_BY_DIST = 3
SORT_TARGET_LIST_BY_DIST_FROM_CASTER = 4

RADIAL_MENU_PARAM_MIN_SETTING = 1
RADIAL_MENU_PARAM_MAX_SETTING = 2
RADIAL_MENU_PARAM_ACTUAL_SETTING = 3

# PyRandomEncounterSetup
TERRAIN_SCRUB = 0
TERRAIN_F_ROAD = 1
TERRAIN_FOREST = 2
TERRAIN_SWAMP = 4
TERRAIN_RIVERSIDE = 6
ES_F_NONE = 0
ES_F_SLEEP_ENCOUNTER = 1

sp_Aid = 3
sp_Animal_Friendship = 4
sp_Animal_Growth = 5
sp_Animal_Trance = 6
sp_Animate_Dead = 7
sp_Bane = 8
sp_Barkskin = 9
sp_Bestow_Curse_Ability = 10
sp_Bestow_Curse_Actions = 12
sp_Bestow_Curse_Rolls = 11
sp_Bless = 13
sp_Blindness = 14
sp_Blink = 15
sp_Blur = 16
sp_Break_Enchantment = 17
sp_Bulls_Strength = 18
sp_Call_Lightning = 19
sp_Call_Lightning_Storm = 20
sp_Calm_Animals = 21
sp_Calm_Emotions = 22
sp_Cats_Grace = 23
sp_Cause_Fear = 24
sp_Chaos_Hammer = 25
sp_Charm_Monster = 26
sp_Charm_Person = 27
sp_Charm_Person_or_Animal = 28
sp_Chill_Metal = 29
sp_Chill_Touch = 30
sp_Clairaudience_Clairvoyance = 31
sp_Cloudkill = 32
sp_Cloudkill_Damage = 33
sp_Color_Spray_Blind = 34
sp_Color_Spray_Stun = 35
sp_Color_Spray_Unconscious = 36
sp_Command = 37
sp_Confusion = 38
sp_Consecrate = 39
sp_Consecrate_Hit = 40
sp_Consecrate_Hit_Undead = 41
sp_Control_Plants = 42
sp_Control_Plants_Charm = 44
sp_Control_Plants_Disentangle = 45
sp_Control_Plants_Entangle = 47
sp_Control_Plants_Entangle_Pre = 46
sp_Control_Plants_Tracking = 43
sp_Darkvision = 48
sp_Daze = 49
sp_Deafness = 52
sp_Death_Knell = 51
sp_Death_Ward = 50
sp_Delay_Poison = 53
sp_Desecrate = 54
sp_Desecrate_Hit = 55
sp_Desecrate_Hit_Undead = 56
sp_Detect_Chaos = 57
sp_Detect_Evil = 58
sp_Detect_Good = 59
sp_Detect_Law = 60
sp_Detect_Magic = 61
sp_Detect_Secret_Doors = 62
sp_Detect_Undead = 63
sp_Dimensional_Anchor = 64
sp_Discern_Lies = 65
sp_Dispel_Air = 66
sp_Dispel_Chaos = 70
sp_Dispel_Earth = 67
sp_Dispel_Evil = 71
sp_Dispel_Fire = 68
sp_Dispel_Good = 72
sp_Dispel_Law = 73
sp_Dispel_Magic = 74
sp_Dispel_Water = 69
sp_Displacement = 75
sp_Divine_Favor = 76
sp_Divine_Power = 77
sp_Dominate_Animal = 78
sp_Dominate_Person = 79
sp_Doom = 80
sp_Dust_of_Disappearance = 251
sp_Eagles_Splendor = 81
sp_Emotion_Despair = 82
sp_Emotion_Fear = 83
sp_Emotion_Friendship = 84
sp_Emotion_Hate = 85
sp_Emotion_Hope = 86
sp_Emotion_Rage = 87
sp_Endurance = 88
sp_Endure_Elements = 89
sp_Enlarge = 90
sp_Entangle = 91
sp_Entangle_Off = 93
sp_Entangle_On = 92
sp_Entropic_Shield = 94
sp_Expeditious_Retreat = 95
sp_Faerie_Fire = 96
sp_False_Life = 97
sp_Fear = 99
sp_Feeblemind = 98
sp_Find_Traps = 100
sp_Fire_Shield = 101
sp_Flare = 102
sp_Fog_Cloud = 103
sp_Fog_Cloud_Hit = 104
sp_Foxs_Cunning = 105
sp_Freedom_of_Movement = 106
sp_Frog_Tongue = 242
sp_Frog_Tongue_Grappled = 243
sp_Frog_Tongue_Swallowed = 244
sp_Frog_Tongue_Swallowing = 245
sp_Gaseous_Form = 107
sp_Ghoul_Touch = 108
sp_Ghoul_Touch_Paralyzed = 109
sp_Ghoul_Touch_Stench = 110
sp_Ghoul_Touch_Stench_Hit = 111
sp_Glibness = 112
sp_Glitterdust = 114
sp_Glitterdust_Blindness = 113
sp_Goodberry = 115
sp_Goodberry_Tally = 116
sp_Grease = 117
sp_Grease_Hit = 118
sp_Greater_Heroism = 119
sp_Greater_Magic_Fang = 120
sp_Greater_Magic_Weapon = 121
sp_Guidance = 122
sp_Gust_of_Wind = 123
sp_Halt_Undead = 125
sp_Harm = 126
sp_Haste = 124
sp_Heal = 127
sp_Heat_Metal = 128
sp_Heroism = 129
sp_Hold_Animal = 130
sp_Hold_Monster = 131
sp_Hold_Person = 132
sp_Hold_Portal = 133
sp_Holy_Smite = 134
sp_Ice_Storm = 135
sp_Ice_Storm_Hit = 136
sp_Improved_Invisibility = 144
sp_Invisibility = 137
sp_Invisibility_Purge = 138
sp_Invisibility_Purge_Hit = 139
sp_Invisibility_Sphere = 140
sp_Invisibility_Sphere_Hit = 141
sp_Invisibility_to_Animals = 142
sp_Invisibility_to_Undead = 143
sp_Keen_Edge = 145
sp_Lesser_Restoration = 146
sp_Longstrider = 147
sp_Mage_Armor = 148
sp_Magic_Circle_Inward = 149
sp_Magic_Circle_Outward = 150
sp_Magic_Fang = 151
sp_Magic_Missile = 152
sp_Magic_Stone = 153
sp_Magic_Vestment = 154
sp_Magic_Weapon = 155
sp_Meld_Into_Stone = 156
sp_Melfs_Acid_Arrow = 157
sp_Mind_Fog = 160
sp_Mind_Fog_Hit = 161
sp_Minor_Globe_of_Invulnerability = 158
sp_Minor_Globe_of_Invulnerability_Hit = 159
sp_Mirror_Image = 162
sp_Mordenkainens_Faithful_Hound = 163
sp_Negative_Energy_Protection = 164
sp_Neutralize_Poison = 165
sp_Obscuring_Mist = 166
sp_Obscuring_Mist_Hit = 167
sp_Orders_Wrath = 168
sp_Otilukes_Resilient_Sphere = 169
sp_Owls_Wisdom = 170
sp_Potion_of_Enlarge = 249
sp_Potion_of_Haste = 250
sp_Potion_of_charisma = 252
sp_Potion_of_glibness = 253
sp_Prayer = 171
sp_Produce_Flame = 172
sp_Protection_From_Alignment = 174
sp_Protection_From_Arrows = 173
sp_Protection_From_Elements = 175
sp_Rage = 176
sp_Raise_Dead = 177
sp_Ray_of_Enfeeblement = 178
sp_Reduce = 179
sp_Reduce_Animal = 180
sp_Remove_Blindness = 181
sp_Remove_Curse = 182
sp_Remove_Deafness = 183
sp_Remove_Disease = 184
sp_Remove_Fear = 185
sp_Remove_Paralysis = 186
sp_Repel_Vermin = 187
sp_Repel_Vermin_Hit = 188
sp_Resist_Elements = 190
sp_Resistance = 189
sp_Restoration = 191
sp_Resurrection = 192
sp_Righteous_Might = 193
sp_Ring_of_Freedom_of_Movement = 248
sp_Sanctuary = 194
sp_Sanctuary_Save_Failed = 196
sp_Sanctuary_Save_Succeeded = 195
sp_See_Invisibility = 197
sp_Shield = 198
sp_Shield_of_Faith = 199
sp_Shillelagh = 200
sp_Shocking_Grasp = 201
sp_Shout = 202
sp_Silence = 203
sp_Silence_Hit = 204
sp_Sleep = 205
sp_Sleet_Storm = 206
sp_Sleet_Storm_Hit = 207
sp_Slow = 208
sp_Soften_Earth_and_Stone = 209
sp_Soften_Earth_and_Stone_Hit = 210
sp_Soften_Earth_and_Stone_Hit_Save_Failed = 211
sp_Solid_Fog = 212
sp_Solid_Fog_Hit = 213
sp_Sound_Burst = 214
sp_Spell_Resistance = 215
sp_Spike_Growth = 216
sp_Spike_Growth_Damage = 218
sp_Spike_Growth_Hit = 217
sp_Spike_Stones = 219
sp_Spike_Stones_Damage = 221
sp_Spike_Stones_Hit = 220
sp_Spiritual_Weapon = 222
sp_Stinking_Cloud = 223
sp_Stinking_Cloud_Hit = 224
sp_Stinking_Cloud_Hit_Pre = 225
sp_Stoneskin = 226
sp_Suggestion = 227
sp_Summon_Swarm = 228
sp_Summoned = 241
sp_Tashas_Hideous_Laughter = 229
sp_Tree_Shape = 230
sp_True_Seeing = 231
sp_True_Strike = 232
sp_Unholy_Blight = 233
sp_Vampiric_Touch = 234
sp_Virtue = 235
sp_Vrock_Screech = 246
sp_Vrock_Spores = 247
sp_Web = 236
sp_Web_Off = 238
sp_Web_On = 237
sp_Wind_Wall = 239
sp_Wind_Wall_Hit = 240

none = 0
air = 1
animal = 2
chaos = 3
death = 4
destruction = 5
earth = 6
evil = 7
fire = 8
good = 9
healing = 10
knowledge = 11
law = 12
luck = 13
magic = 14
plant = 15
protection = 16
strength = 17
sun = 18
travel = 19
trickery = 20
war = 21
water = 22
special = 23

# Schools
Abjuration = 1
Conjuration = 2
Divination = 3
Enchantment = 4
Evocation = 5
Illusion = 6
Necromancy = 7
Transmutation = 8

# Subschools
Calling = 1
Creation = 2
Healing = 3
Summoning = 4
Charm = 5
Compulsion = 6
Figment = 7
Glamer = 8
Pattern = 9
Phantasm = 10
Shadow = 11
Scrying = 12

STANDPOINT_DAY = 0
STANDPOINT_NIGHT = 1
STANDPOINT_SCOUT = 2
