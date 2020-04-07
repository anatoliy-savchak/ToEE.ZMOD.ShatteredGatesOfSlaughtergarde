import toee
import debugg
import utils_storage
import utils_npc_spells
import const_toee
import utils_tactics

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlKnellBeetleLesser.get_from_obj(attachee)
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlKnellBeetleLesser.get_from_obj(attachee)
	if (ctrl):
		return ctrl.enter_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

class CtrlKnellBeetleLesser(object):
	def __init__(self):
		self.round = 0
		self.spells = utils_npc_spells.NPCSpells()
		return

	def npc_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = 6125
		npc.scripts[const_toee.sn_enter_combat] = 6125
		self.spells.add_spell(toee.spell_shout, toee.stat_level_wizard, 4)
		return

	@staticmethod
	def get_name():
		return "CtrlKnellBeetleLesser"

	@classmethod
	def create_obj(cls, loc):
		PROTO_NPC_KNELL_BEETLE = 14837
		npc = toee.game.obj_create(PROTO_NPC_KNELL_BEETLE, loc)
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
		tac = utils_tactics.TacticsHelper(self.get_name())
		while (1):
			if (self.round >= 2 and self.spells.get_spell_count(toee.spell_shout)):
				tac.add_target_closest()
				tac.add_five_foot_step()
				tac.add_cast_area_code(self.spells.prep_spell(attachee, toee.spell_shout, 1))
				break
			tac.add_target_closest()
			tac.add_attack()
			break

		print(tac.custom_tactics)
		#debugg.breakp("CtrlKnellBeetleLesser::start_combat")
		if (tac.count > 0):
			tac.make_name()
			attachee.ai_strategy_set_custom(tac.custom_tactics)
		return toee.RUN_DEFAULT

	def enter_combat(self, attachee, triggerer):
		self.round = 0
		return toee.RUN_DEFAULT