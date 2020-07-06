import toee

def hash(text):
	"""hash(str: text) -> int"""
	return 0

def dispatch_skill(obj, skill_enum, bon_list, obj2 = toee.OBJ_HANDLE_NULL, flag = 1):
	""" dispatch_skill(toee.PyObjHandle: obj, int: skill_enum, BonusList: bon_list, toee.PyObjHandle: obj2 = toee.OBJ_HANDLE_NULL, int: flag = 1) -> int: skill_value"""
	return 0

def create_history_type6_opposed_check(performer, defender, performerRoll, defenderRoll, performerBonList, defenderBonList, combatMesLineTitle, combatMesLineResult, flag):
	""" create_history_type6_opposed_check(toee.PyObjHandle: performer, toee.PyObjHandle: defender, int: performerRoll, int: defenderRoll, BonusList: performerBonList, BonusList: defenderBonList, int: combatMesLineTitle, int: combatMesLineResult, int: flag) -> int: rollHistId"""
	return 0

def dispatch_stat(obj, stat, bonlist):
	""" dispatch_stat(toee.PyObjHandle: performer, int: stat, BonusList: bon_list) -> int: stat_value"""
	return 0

def create_history_type4(performer, dc, dice, roll, text, bonlist):
	""" create_history_type4(toee.PyObjHandle: performer, int: dc, toee.PyDice: dice, int: roll, str: tex, BonusList: bon_list) -> int: rollHistId"""
	return 0

class TurnBasedStatus:
	def __init__(self):
		self.hourglass_state = toee.D20ACT_Full_Round_Action
		self.num_bonus_attacks = 0
		self.surplus_move_dist = 0
		self.flags = 0 # TurnBasedStatusFlags
		self.attack_mode_code = 0
		return

class D20Action:
	def __init__(self, action_type = 0):
		self.performer = toee.PyObjHandle()
		self.target = toee.PyObjHandle()
		self.spell_id = 0
		self.data1 = 0
		self.flags = toee.D20CAF_HIT # D20CAF_ flags
		self.path = object() #todo
		self.action_type = action_type #See D20A_ constants
		self.loc = 0
		self.anim_id = 0
		self.spell_data = D20SpellData()
		self.roll_id_0 = 0
		self.roll_id_1 = 0
		self.roll_id_2 = 0
		return

	def query_is_action_invalid(self, handle):
		return 0

	def to_hit_processing(self):
		return

	def filter_spell_targets(self, pkt):
		return 0

	def create_projectile_and_throw(self, protoNum, endLoc):
		return

	def to_hit_processing(self, projHndl, thrownItem):
		return

class BonusList:
	def __init__(self):
		# init 0; 0x1 - overallCapHigh set; 0x2 - overallCapLow set; 0x4 - force cap override (otherwise it can only impose restrictions i.e. it will only change the cap if it's lower than the current one)
		self.flags = 0
		return

	def add(self, value, bonType, mesline):
		""" bonus_list.add(int: value, int: bonType, int: mesline) -> None """
		return
	
	def add(self, value, bonType, text):
		""" bonus_list.add(int: value, int: bonType, str: text) -> None """
		return

	def add_from_feat(self, value, bonType, mesline, feat):
		""" bonus_list.add_from_feat(int: value, int: bonType, int: mesline, int: feat) -> int """
		return 0

	def set_overall_cap(self, bonflags, newCap, newCapType, bonusMesline):
		""" bonus_list.set_overall_cap(int: bonflags, int: newCap, int: newCapType, int: bonusMesline) -> None """
		return

	def modify(self, value, bonType, meslineIdentifier):
		""" bonus_list.modify(int: value, int: bonType, int: meslineIdentifier) -> int """
		return 0

	def modify(self, value, bonType, meslineIdentifier):
		""" bonus_list.modify(int: value, int: bonType, int: meslineIdentifier) -> int """
		return 0

	def get_sum(self, mesline):
		""" bonus_list.get_sum() -> int """
		return 0

	def get_total(self, mesline):
		""" bonus_list.get_sum() -> int """
		return 0

	def add_cap(self, bonType, value, mesline):
		""" Adds cap for a particular bonus type
		bonus_list.add_cap(int: bonType, int: value, int: mesline) -> None """
		return

	def add_cap(self, bonType, value, mesline, text):
		""" Adds cap for a particular bonus type
		bonus_list.add_cap(int: bonType, int: value, int: mesline, int: text) -> None """
		return

class AttackPacket:
	def __init__(self):
		self.attacker = toee.PyObjHandle()
		self.target = toee.PyObjHandle()
		self.action_type = toee.D20A_UNSPECIFIED_MOVE
		self.event_key = 0 # dispKey
		return

	def get_weapon_used(self):
		""" attack_packet.get_weapon_used() -> PyObjHandle """
		return toee.PyObjHandle()

	def is_offhand_attack(self):
		""" attack_packet.is_offhand_attack() -> int """
		return 0

	def get_flags(self):
		""" attack_packet.get_flags() -> int """
		return toee.D20CAF_HIT

	def set_flags(self, flagsNew):
		""" attack_packet.set_flags(int: flagsNew) -> None """
		return

class RadialMenuEntry:
	def __init__(self):
		self.flags = 0 # RadialMenuEntryFlags: HasMinArg = 0x2, HasMaxArg = 0x4
		self.min_arg = 0
		self.max_arg = 0
		return

	def add_as_child(self, handle, parentId):
		"""Adds this node as a child to a specified node ID, and returns the newly created node ID (so you may give it other children, etc.)"""
		assert isinstance(handle, toee.PyObjHandle)
		assert isinstance(parentId, int)
		return 0

	def add_child_to_standard(self, handle, stdNode):
		"""Adds this node as a child to a Standard Node (one of several hardcoded root nodes such as class, inventory etc.), and returns the newly created node ID (so you may give it other children, etc.)"""
		assert isinstance(handle, toee.PyObjHandle)
		assert isinstance(stdNode, RadialMenuStandardNode)
		return 0

class RadialMenuEntryAction(RadialMenuEntry):
	def set_spell_data(self, spellData):
		assert isinstance(spellData, D20SpellData)
		return

class RadialMenuEntryPythonAction(RadialMenuEntryAction):
	def __init__(self, combatMesLine, action_type, action_id, data1, helpTopic):
		"""RadialMenuEntryPythonAction(int: combatMesLine, int: action_type, int: action_id, int: data1, str: helpTopic)"""
		return
	def __init__(self, combatMesLine, action_type, action_name, data1, helpTopic):
		"""RadialMenuEntryPythonAction(int: combatMesLine, int: action_type, str: action_name, int: data1, str: helpTopic)"""
		return
	def __init__(self, radialText, action_type, action_id, data1, helpTopic):
		"""RadialMenuEntryPythonAction(str: radialText, int: action_type, str: action_name, int: data1, str: helpTopic)"""
		return
	def __init__(self, spell_store, action_type, action_id, data1, helpTopic):
		"""RadialMenuEntryPythonAction(PySpellStore: spell_store, int: action_type, int: action_id, int: data1, str: helpTopic)"""
		return

class RadialMenuEntryParent:
	def __init__(self, combesMesLine):
		assert isinstance(combesMesLine, int)
		return

	def __init__(self, radialText):
		assert isinstance(radialText, str)
		return

	def add_as_child(self, handle, parentId):
		"""Adds this node as a child to a specified node ID, and returns the newly created node ID (so you may give it other children, etc.)"""
		assert isinstance(handle, toee.PyObjHandle)
		assert isinstance(parentId, int)
		return 0

	def add_child_to_standard(self, handle, stdNode):
		"""Adds this node as a child to a Standard Node (one of several hardcoded root nodes such as class, inventory etc.), and returns the newly created node ID (so you may give it other children, etc.)"""
		assert isinstance(handle, toee.PyObjHandle)
		assert isinstance(stdNode, RadialMenuStandardNode)
		return 0

class RadialMenuStandardNode:
	Root = 0
	Spells = 1
	Skills = 2
	Feats = 3
	Class = 4
	Combat = 5
	Items = 6
	Alchemy = 7
	Movement = 8
	Offense = 9
	Tacitical = 10
	Options = 11
	Potions = 12
	Wands = 13
	Scrolls = 14

class RadialMenuEntryParent:
	def add_as_child(self, objHandle, parentId):
		"""Adds this node as a child to a specified node ID, and returns the newly created node ID (so you may give it other children, etc.)"""
		return RadialMenuEntryParent()
	def add_as_child(self, objHandle, stdNode):
		"""Adds this node as a child to a Standard Node (one of several hardcoded root nodes such as class, inventory etc.), and returns the newly created node ID (so you may give it other children, etc.)"""
		return RadialMenuEntryParent()

class DamagePacket:
	def __init__(self):
		self.final_damage = 0 # Final Damage Value
		self.flags = 0 # 1 - maximized, 2 - empowered
		self.bonus_list = BonusList()
		self.critical_multiplier = 2 # 1 by default, gets increased by various things
		self.attack_power = toee.D20DAP_NORMAL
		return

	def add_dice(self, dice, damType, damageMesLine):
		"""add_dice(PyDice: dice, int[D20DT_BLUDGEONING]: damType, int: damageMesLine)"""
		return

	def add_dice(self, dice, damType, damageMesLine, reason):
		"""add_dice(PyDice: dice, int[D20DT_BLUDGEONING]: damType, int: damageMesLine, str: reason)"""
		return

	def add_physical_damage_res(self, amount, bypassingAttackPower, damMesLine):
		"""add_physical_damage_res(int: amount, int[D20DAP_NORMAL]: bypassingAttackPower, int: damMesLine)
		Adds physical (Slashing/Piercing/Crushing) damage resistance."""
		return

	def add_damage_bonus(self, damBonus, bonType, bonMesline):
		"""add_damage_bonus(int: damBonus, int[D20DT_BLUDGEONING]: bonType, int: bonMesline)"""
		return

	def add_damage_resistance(self, amount, damType, damMesLine):
		"""add_damage_resistance(int: amount, int[D20DT_BLUDGEONING]: damType, int: damMesLine)"""
		return

class ModifierSpec:
	def __init__(self):
		self.name = None
		return
	def __init__(self, name, numArgs, preventDup):
		self.name = name
		return
	def add_hook(self, dispType, dispKey, pycallback, pydataTuple):
		""" add_hook(int: dispType, int: dispKey, pycallback, pydataTuple)"""
		return
	def add_hook(self, dispType, dispKey, pycallback, pydataTuple):
		""" add_hook(int: dispType, str: dispKey, pycallback, pydataTuple)"""
		return
	def add_to_feat_dict(self, feat_enum, feat_max, feat_offset):
		""" add_to_feat_dict(int: feat_enum, int: feat_max, int: feat_offset)"""
		return
	def add_to_feat_dict(self, feat_name, feat_max, feat_offset):
		""" add_to_feat_dict(str: feat_name, int: feat_max, int: feat_offset)"""
		return
	def extend_existing(self, condName):
		""" extend_existing(str: condName)"""
		return
	def add_item_force_remove_callback(self):
		""" add_item_force_remove_callback()"""
		return
	def add_spell_countdown_standard(self):
		""" add_spell_countdown_standard()"""
		return
	def add_aoe_spell_ender(self):
		""" add_aoe_spell_ender()"""
		return
	def add_spell_dismiss_hook(self):
		""" add_spell_dismiss_hook()"""
		return

#ET_On0 = 0
#ET_OnConditionAdd = 1
#ET_OnConditionRemove = 2
#ET_OnConditionAddPre = EventObjModifier
#ET_OnConditionRemove2 = 4
#ET_OnConditionAddFromD20StatusInit = 5
#ET_OnD20AdvanceTime = 6
#ET_OnTurnBasedStatusInit = 7
#ET_OnInitiative = 8
#ET_OnNewDay = 9
#ET_OnAbilityScoreLevel = EventObjBonusList
#ET_OnGetAC = EventObjAttack
#ET_OnGetACBonus2 = 12
#ET_OnGetAcModifierFromAttacker = EventObjAttack
#ET_OnSaveThrowLevel = EventObjSavingThrow
#ET_OnSaveThrowSpellResistanceBonus = EventObjSavingThrow
#ET_OnToHitBonusBase = EventObjAttack
#ET_OnToHitBonus2 = EventObjAttack
#ET_OnToHitBonusFromDefenderCondition = EventObjAttack
#ET_OnDealingDamage = 18
#ET_OnTakingDamage = 19
#ET_OnDealingDamage2 = 20
#ET_OnTakingDamage2 = 21
#ET_OnReceiveHealing = 22
#ET_OnGetCriticalHitRange = EventObjAttack
#ET_OnGetCriticalHitExtraDice = EventObjAttack
#ET_OnGetCurrentHP = EventObjBonusList
#ET_OnGetMaxHP = EventObjBonusList
#ET_OnGetInitiativeMod = 27
#ET_OnD20Signal = 28
#ET_OnD20Query = 29
#ET_OnGetSkillLevel = 30
#ET_OnBuildRadialMenuEntry = 31
#ET_OnGetTooltip = 32
#ET_OnDispelCheck = 33
#ET_OnGetDefenderConcealmentMissChance = EventObjAttack
#ET_OnGetCasterLevelMod = 35
#ET_OnD20ActionCheck = 36
#ET_OnD20ActionPerform = 37
#ET_OnD20ActionOnActionFrame = 38
#ET_OnDestructionDomain = 39
#ET_OnGetMoveSpeedBase = 40
#ET_OnGetMoveSpeed = 41
#ET_OnGetAbilityCheckModifier = 42
#ET_OnGetAttackerConcealmentMissChance = 43
#ET_OnCountersongSaveThrow = EventObjSavingThrow
#ET_OnGetSpellResistanceMod = 45
#ET_OnGetSpellDcBase = 46
#ET_OnGetSpellDcMod = 47
#ET_OnBeginRound = 48
#ET_OnReflexThrow = 49
#ET_OnDeflectArrows = EventObjAttack
#ET_OnGetNumAttacksBase = 51
#ET_OnGetBonusAttacks = 52
#ET_OnGetCritterNaturalAttacksNum = 53
#ET_OnObjectEvent = 54
#ET_OnProjectileCreated = EventObjAttack
#ET_OnProjectileDestroyed = EventObjAttack
#ET_On57 = 57
#ET_On58 = 58
#ET_OnGetAbilityLoss = 59
#ET_OnGetAttackDice = 60
#ET_OnGetLevel = 61
#ET_OnImmunityTrigger = 62
#ET_On63 = 63
#ET_OnSpellImmunityCheck = 64
#ET_OnGetEffectTooltip = 65
#ET_OnStatBaseGet = EventObjBonusList
#ET_OnWeaponGlowType = 67
#ET_OnItemForceRemove = 68
#ET_OnGetArmorToHitPenalty = 69
#ET_OnGetMaxDexAcBonus = 70
#ET_OnGetSizeCategory = 71
#ET_OnGetBucklerAcPenalty = EventObjAttack
#ET_OnGetModelScale = 73
#ET_OnD20PythonQuery = 74
#ET_OnD20PythonSignal = 75
#ET_OnD20PythonActionCheck = 76
#ET_OnD20PythonActionPerform = 77
#ET_OnD20PythonActionFrame = 78
#ET_OnD20PythonActionAdd = 79
#ET_OnPythonAdf = 80
#ET_OnPythonReserved3 = 81
#ET_OnPythonReserved4 = 82
#ET_OnPythonReserved5 = 83
#ET_OnPythonReserved6 = 84
#ET_OnPythonReserved7 = 85
#ET_OnPythonReserved8 = 86
#ET_OnPythonReserved9 = 87
#ET_OnSpellListExtensionGet = 88
#ET_OnGetBaseCasterLevel = 89
#ET_OnLevelupSystemEvent = 90
#ET_OnDealingDamageWeaponlikeSpell = 91
#ET_OnActionCostMod = 92
#ET_OnMetaMagicMod = 93

class EventObj(object):
    def __init__(self):
        self.evt_obj_type = 0 # enum_dispIO_type
        return

class EventArgs(object):
    def __init__(self):
        self.evt_obj = EventObj()
        return
    def get_arg(self, arg_idx):
        return 1
    def set_arg(self, arg_idx, value):
        """ args.set_arg(int: arg_idx, int: value) -> None """
        return
    def get_obj_from_args(self, arg_idx):
        return toee.PyObjHandle()
    def set_args_from_obj(self, arg_idx, handle):
        """ args.set_arg(int: arg_idx, PyObjHandle: handle) -> None """
        return
    def get_param(self, param_idx):
        return 1
    def condition_remove(self):
        return
    def remove_spell_mod(self):
        return
    def remove_spell(self):
        return

class EventObjModifier(EventObj):
    def __init__(self):
        self.evt_obj_type = 3 # dispTypeConditionAddPre
        self.return_val = 0
        self.arg1 = 0
        self.arg2 = 0
        self.modifier_spec = ModifierSpec() # CondStruct, foreign
        return

    def is_modifier(self, s): # foreign
        return 0

class EventObjD20Query(EventObj):
    def __init__(self):
        self.evt_obj_type = 29 # dispTypeD20Query
        self.return_val = 0
        self.data1 = 0
        self.data2 = 0
        return

    def get_spell_packet(self): 
        return object() # SpellPacketBody

    def get_d20_action(self): 
        return D20Action()

    def get_obj(self):
        return toee.PyObjHandle()

class EventObjTooltip(EventObj):
    """ Tooltip event for mouse-overed objects. """
    def __init__(self):
        self.evt_obj_type = 32 # dispTypeTooltip
        self.num_strings = 0
        return

    def append(self, cs): 
        """ evt_obj.append(str: cs) -> None """
        return

class EventObjEffectTooltip(EventObj):
    """ Used for tooltips when hovering over the status effect indicators in the party portrait row """
    def __init__(self):
        self.evt_obj_type = 65 # dispTypeEffectTooltip
        return

    def append(self, effectTypeId, spellEnum, text): 
        """ evt_obj.append(int: effectTypeId, int: spellEnum, str: text) -> None 
        effectTypeId: art\\interface\\player_conditions\\
        """
        return

class EventObjD20Signal(EventObj):
    def __init__(self):
        self.evt_obj_type = 48 # dispTypeD20AdvanceTime, dispTypeD20Signal, dispTypePythonSignal, dispTypeBeginRound, dispTypeDestructionDomain, ET_OnD20Signal
        self.return_val = 0
        self.data1 = 0
        self.data2 = 0
        return

    def get_d20_action(self):
        return D20Action()

class EventObjTurnBasedStatus(EventObj):
    def __init__(self):
        self.evt_obj_type = 7 # dispTypeTurnBasedStatusInit
        self.tb_status = TurnBasedStatus()
        return

class EventObjAttack(EventObj):
    """ Used for fetching attack or AC bonuses """
    def __init__(self):
        #  dispConfirmCriticalBonus, dispTypeGetAC, dispTypeAcModifyByAttacker, dispTypeToHitBonusBase, dispTypeToHitBonus2
        #, dispTypeToHitBonusFromDefenderCondition, dispTypeGetCriticalHitRange, dispTypeGetCriticalHitExtraDice
        #, dispTypeGetDefenderConcealmentMissChance, dispTypeDeflectArrows, dispTypeProjectileCreated, dispTypeProjectileDestroyed, dispTypeBucklerAcPenalty:
        self.bonus_list = BonusList()
        self.attack_packet = AttackPacket()
        return

class EventObjD20Action(EventObj):
    def __init__(self):
        self.evt_obj_type = 36 # dispTypeD20ActionCheck,dispTypeD20ActionPerform, dispTypeD20ActionOnActionFrame,dispTypeGetNumAttacksBase, dispTypeGetBonusAttacks, dispTypeGetCritterNaturalAttacksNum,dispTypePythonActionPerform,dispTypePythonActionAdd ,dispTypePythonActionCheck ,dispTypePythonActionFrame
        self.return_val = 0
        self.d20a = D20Action()
        self.turnbased_status = EventObjTurnBasedStatus()
        self.bonus_list = BonusList()
        return

class EventObjDamage(EventObj):
    def __init__(self):
        self.evt_obj_type = 91 # dispTypeDealingDamageWeaponlikeSpell, dispTypeDealingDamage, dispTypeTakingDamage, dispTypeDealingDamage2, dispTypeTakingDamage2
        self.attack_packet = AttackPacket()
        self.damage_packet = DamagePacket()
        return

class EventObjBonusList(EventObj):
    def __init__(self):
        self.evt_obj_type = toee.ET_OnAbilityScoreLevel # dispTypeAbilityScoreLevel, dispTypeCurrentHP, dispTypeMaxHP, dispTypeStatBaseGet
        self.flags = 0
        self.bonus_list = BonusList()
        return

class EventObjSavingThrow(EventObj):
    def __init__(self):
        self.evt_obj_type = toee.ET_OnSaveThrowLevel # dispTypeSaveThrowLevel, dispTypeSaveThrowSpellResistanceBonus, dispTypeCountersongSaveThrow
        self.bonus_list = BonusList()
        self.return_val = 0
        self.obj = toee.PyObjHandle()
        self.flags = 0
        return

class EventObjImmunityQuery(EventObj):
    def __init__(self):
        self.evt_obj_type = toee.ET_OnSpellImmunityCheck # dispTypeSpellImmunityCheck
        self.spell_entry = SpellEntry()
        self.spell_packet = SpellPacket()
        self.return_val = 0
        return

class D20SpellData:
	def __init__(self, spell_enum = 0):
		self.spell_enum = 0
		self.spell_class = 0
		self.inven_idx = 0
		return

	def set_spell_level(self, spLvl): 
		return

	def get_spell_level(self): 
		return 1

	def get_spell_store(self): 
		return object()

	def set_spell_class(self, spClass): 
		return

	def get_metamagic_data(self, spLvl): 
		return object()

class SpellEntry:
	def __init__(self, spell_enum = 0):
		self.spell_enum = toee.spell_aid
		self.spell_school_enum = 0
		self.spell_subschool_enum = 0
		self.descriptor = 0
		self.casting_time = 0
		self.saving_throw_type = toee.D20_Save_Fortitude
		self.min_target = 0
		self.max_target = 0
		self.mode_target = 0
		return

	def is_base_mode_target(self, type): 
		return 1

	def get_level_specs(self): 
		return list()

	def level_for_spell_class(self, spellClass): 
		return 1

class SpellPacket:
	def __init__(self, spell_enum = 0):
		self.spell_enum = toee.spell_aid
		self.spell_known_slot_level = 0
		self.inventory_idx = 0
		self.picker_result = 0
		self.spell_class = 0
		self.spell_id = 0
		self.caster_level = 0
		self.loc = 0
		self.caster = toee.PyObjHandle()
		return

	def get_spell_casting_class(self): 
		return 1

	def get_metamagic_data(self): 
		return SpellPacket()

	def get_target(self, idx): 
		return toee.PyObjHandle()

	def set_projectile(self, projectile): 
		assert isinstance(projectile, toee.PyObjHandle)
		return

	def is_divine_spell(self):
		return 1

	def debit_spell(self):
		return

	def update_registry(self):
		return

	def set_spell_object(self, idx,  spellObj, partsysId):
		return

	def add_spell_object(self, spellObj, partsysId):
		return

	def add_target(self, handle, partsysId):
		return

	def end_target_particles(self, handle):
		return

	def remove_target(self, handle):
		return

	def check_spell_resistance(self, tgt):
		return

	def trigger_aoe_hit(self):
		return

	def float_spell_line(self, handle, lineId, color):
		return

class D20ActionType:
	FiveFootStep = toee.D20A_5FOOTSTEP
	PythonAction = toee.D20A_PYTHON_ACTION
	StandardAttack = toee.D20A_STANDARD_ATTACK
	FullAttack = toee.D20A_FULL_ATTACK
	StandardRangedAttack = toee.D20A_STANDARD_RANGED_ATTACK
	StandUp = toee.D20A_STAND_UP
	TurnUndead = toee.D20A_TURN_UNDEAD
	ClassAbility = toee.D20A_CLASS_ABILITY_SA
	CastSpell = toee.D20A_CAST_SPELL
	UseItem = toee.D20A_USE_ITEM
	UsePotion = toee.D20A_USE_POTION
	Feint = toee.D20A_FEINT
	Move = toee.D20A_UNSPECIFIED_MOVE
