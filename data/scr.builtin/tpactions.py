import toee
import tpdp

class ActionSequence:
	def __init__(self):
		self.cur_idx = 0
		self.performer = toee.PyObjHandle()
		self.tb_status = tpdp.TurnBasedStatus()
		self.target = toee.PyObjHandle()
		self.spell_packet = 0
		self.spell_action = 0
		return

	def add_action(self, actSeq, d20a):
		return

class PickerArgs:
	def __init__(self):
		self.spell_enum = 0
		self.caster = toee.PyObjHandle()
		self.mode_target = ModeTarget.Single
		return

	def get_base_mode_target(self):
		return ModeTarget.Single

	def set_mode_target_flag(self, type):
		return

	def is_mode_target_flag_set(self, type):
		return 1

class ModeTarget:
	Single = 1
	Cone = 3
	Area = 4
	Personal = 6
	Ray = 8
	Wall = 9
	EndEarlyMulti = 8192
	OnceMulti = 1024
	Any30Feet = 2048
	PickOrigin = 32768