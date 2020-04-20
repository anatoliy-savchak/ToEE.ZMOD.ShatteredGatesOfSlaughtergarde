import toee, tpdp

class PythonModifier(tpdp.ModifierSpec):
    def AddHook(self, eventType, eventKey, callbackFcn, argsTuple ):
        """ PythonModifier.AddHook(int[ET_OnGetNumAttacksBase]: eventType, int[EK_NONE]: eventKey, func: callbackFcn, (): argsTuple) -> None"""
        self.add_hook(eventType, eventKey, callbackFcn, argsTuple)
    def ExtendExisting(self, condName):
        self.extend_existing(condName)
    def AddItemForceRemoveHandler(self): # in charge of backing up condition args
        self.add_item_force_remove_callback()
    def MapToFeat(self, feat_enum, feat_list_max = -1, feat_cond_arg2 = 0):
        self.add_to_feat_dict(feat_enum, feat_list_max, feat_cond_arg2)
    # Spell related standard hooks
    def AddSpellCountdownStandardHook(self):
        # adds an ET_OnBeginRound handler that (normally) does:
        # If countdown expired: (<0)
        #   1. Float text "Spell Expired"
        #   2. RemoveSpell() (has case-by-case handlers for Spell_End; Temple+ adds generic handling for wall spells here)
        #   3. RemoveSpellMod()
        # Else:
        #   Decrement count, update spell packet duration
        self.add_spell_countdown_standard()    
    def AddAoESpellEndStandardHook(self): 
        # adds a EK_S_Spell_End handler that:
        # 1. Ends particles for all spell objects
        # 2. RemoveSpellMod()
        self.add_aoe_spell_ender()
    def AddSpellDismissStandardHook(self):
        self.add_spell_dismiss_hook()

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
        self.evt_obj_type = 0 # enum_dispIO_type
        self.return_val = 0
        self.arg1 = 0
        self.arg2 = 0
        self.modifier_spec = object() # CondStruct
        return

    def is_modifier(self, s): 
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
        return tpdp.D20Action()

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

class DispIoD20Signal(EventObj):
    def __init__(self):
        self.evt_obj_type = 48 # dispTypeD20AdvanceTime, dispTypeD20Signal, dispTypePythonSignal, dispTypeBeginRound, dispTypeDestructionDomain
        self.return_val = 0
        self.data1 = 0
        self.data2 = 0
        return

    def get_d20_action(self):
        return tpdp.D20Action()

class EventObjTurnBasedStatus(EventObj):
    def __init__(self):
        self.evt_obj_type = 7 # dispTypeTurnBasedStatusInit
        self.tb_status = tpdp.TurnBasedStatus()
        return

class EventObjAttack(EventObj):
    """ Used for fetching attack or AC bonuses """
    def __init__(self):
        #  dispConfirmCriticalBonus, dispTypeGetAC, dispTypeAcModifyByAttacker, dispTypeToHitBonusBase, dispTypeToHitBonus2
        #, dispTypeToHitBonusFromDefenderCondition, dispTypeGetCriticalHitRange, dispTypeGetCriticalHitExtraDice
        #, dispTypeGetDefenderConcealmentMissChance, dispTypeDeflectArrows, dispTypeProjectileCreated, dispTypeProjectileDestroyed, dispTypeBucklerAcPenalty:
        self.bonus_list = tpdp.BonusList()
        self.attack_packet = tpdp.AttackPacket()
        return
