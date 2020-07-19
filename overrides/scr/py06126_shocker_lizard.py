import toee
import debugg
import utils_storage
import utils_npc_spells
import const_toee
import utils_tactics

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlShockerLizard.get_from_obj(attachee)
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlShockerLizard.get_from_obj(attachee)
	if (ctrl):
		return ctrl.enter_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_spell_cast(attachee, triggerer, spell):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	ctrl = CtrlShockerLizard.get_from_obj(attachee)
	if (ctrl):
		return ctrl.spell_cast(attachee, triggerer, spell)
	return toee.RUN_DEFAULT

class CtrlShockerLizard(object):
	def __init__(self):
		self.round = 0
		self.current_attack_option = 0
		self.stunning_shock_off_field = toee.obj_f_npc_retail_price_multiplier
		self.stunning_shock_performed = 0
		return

	def npc_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = 6126
		npc.scripts[const_toee.sn_enter_combat] = 6126
		npc.scripts[const_toee.sn_spell_cast] = 6126
		npc.condition_add_with_args("Stunning_Shock", 0, self.stunning_shock_off_field)
		npc.condition_add_with_args("Lethal_Shock", 0, 0)
		return

	@staticmethod
	def get_name():
		return "CtrlShockerLizard"

	@classmethod
	def create_obj(cls, loc):
		PROTO_NPC_SHOCKER_LIZARD = 14838
		npc = toee.game.obj_create(PROTO_NPC_SHOCKER_LIZARD, loc)
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

		option = toee.game.random_range(1, 6)
		tac = utils_tactics.TacticsHelper(self.get_name())
		while (1):
			if (not self.stunning_shock_performed or (option == 5 or option == 6)):
				if (self.stunning_shock_off_field):
					attachee.npc_flag_unset(self.stunning_shock_off_field)
				tac.add_target_closest()
				tac.add_approach()
				tac.add_python_action(3001)
				print("option: {}, Lethal Shock!".format(option))
				self.stunning_shock_performed += 1
				break
			if (option == 1):
				if (self.stunning_shock_off_field):
					attachee.npc_flag_unset(self.stunning_shock_off_field)
				print("option: {}, Bite!".format(option))
				break
			if (option == 2 or option == 3 or option == 4):
				if (self.stunning_shock_off_field):
					attachee.npc_flag_set(self.stunning_shock_off_field)
				tac.add_attack()
				print("option: {}, Stunning Shock!".format(option))
				break
			break

		tac.add_attack()
		print(tac.custom_tactics)
		if (tac.count > 0):
			tac.set_strategy(attachee)
		return toee.RUN_DEFAULT

	def enter_combat(self, attachee, triggerer):
		self.round = 0
		return toee.RUN_DEFAULT

	def spell_cast(attachee, triggerer, spell):
		debugg.breakp("spell_cast")
		return toee.RUN_DEFAULT
