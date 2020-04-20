import toee

def dispatch_skill(obj, skill_enum, bon_list, obj2 = toee.OBJ_HANDLE_NULL, flag = 1):
	""" tpdp.dispatch_skill(toee.PyObjHandle: obj, int: skill_enum, BonusList: bon_list, toee.PyObjHandle: obj2 = toee.OBJ_HANDLE_NULL, int: flag = 1) -> int: skill_value"""
	return 0

def create_history_type6_opposed_check(performer, defender, performerRoll, defenderRoll, performerBonList, defenderBonList, combatMesLineTitle, combatMesLineResult, flag):
	""" tpdp.create_history_type6_opposed_check(toee.PyObjHandle: performer, toee.PyObjHandle: defender, int: performerRoll, int: defenderRoll, BonusList: performerBonList, BonusList: defenderBonList, int: combatMesLineTitle, int: combatMesLineResult, int: flag) -> int: rollHistId"""
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
	def __init__(self):
		self.performer = toee.PyObjHandle()
		self.target = toee.PyObjHandle()
		self.spell_id = 0
		self.data1 = 0
		self.flags0 # D20CAF_ flags
		self.path = object() #todo
		self.action_type = 0 #See D20A_ constants
		self.loc = 0
		self.anim_id = 0
		self.spell_data = object() # todo d20SpellData
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

