import toee
import debugg
import utils_storage
import utils_npc_spells
import const_toee
import utils_tactics
import utils_npc

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlShamblingMound.get_from_obj(attachee)
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlShamblingMound.get_from_obj(attachee)
	if (ctrl):
		return ctrl.enter_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

class CtrlShamblingMound(object):
	def __init__(self):
		self.round = 0
		self.has_pulled_down_a_ceiling = 0
		return

	def npc_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = 6127
		npc.scripts[const_toee.sn_enter_combat] = 6127
		npc.condition_add("Pull_Down_Ceiling")
		return

	@staticmethod
	def get_name():
		return "CtrlShamblingMound"

	@classmethod
	def create_obj(cls, loc):
		PROTO_NPC_SHAMBLING_MOUND = 14889
		npc = toee.game.obj_create(PROTO_NPC_SHAMBLING_MOUND, loc)
		ctrl = cls()
		utils_storage.obj_storage(npc).data[cls.get_name()] = ctrl
		ctrl.npc_created(npc)
		return npc

	@classmethod
	def get_from_obj(cls, npc):
		data = utils_storage.obj_storage(npc).data
		if (cls.get_name() in data):
			return data[cls.get_name()]
		return

	def start_combat(self, attachee, triggerer):
		self.round += 1
		print("{}::{} (round: {})".format(type(self).__name__, "start_combat", self.round))

		hp_percent = utils_npc.npc_hp_current_percent(attachee)
		#print("hp: {}%".format(hp_percent))
		#hp_percent = 40
		tac = utils_tactics.TacticsHelper(self.get_name())
		while (1):
			if (hp_percent <= 50 and not self.has_pulled_down_a_ceiling):
				tac.add_target_closest()
				#tac.add_approach() _pull_down_ceiling
				tac.add_python_action(3002)
				print("Pull Down Ceiling!")
				self.has_pulled_down_a_ceiling += 1
				break
			break

		tac.add_approach()
		tac.add_attack()
		print(tac.custom_tactics)
		if (tac.count > 0):
			tac.set_strategy(attachee)
		return toee.RUN_DEFAULT

	def enter_combat(self, attachee, triggerer):
		self.round = 0
		return toee.RUN_DEFAULT
