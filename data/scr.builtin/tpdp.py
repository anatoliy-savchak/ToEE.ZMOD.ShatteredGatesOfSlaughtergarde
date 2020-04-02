import toee

class TurnBasedStatus:
	def __init__(self):
		self.hourglass_state = toee.D20ACT_Full_Round_Action
		self.num_bonus_attacks = 0
		self.surplus_move_dist = 0
		self.flags = 0
		self.attack_mode_code = 0
		return

class D20Action:
	def __init__(self):
		self.performer = toee.PyHandle()
		self.target = toee.PyHandle()
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
