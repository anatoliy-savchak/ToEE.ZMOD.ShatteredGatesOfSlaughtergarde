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
