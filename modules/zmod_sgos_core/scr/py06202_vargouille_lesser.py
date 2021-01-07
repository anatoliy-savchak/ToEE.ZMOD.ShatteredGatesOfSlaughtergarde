import toee, debugg, utils_storage, utils_npc_spells, const_toee, utils_tactics, utils_toee

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlVargouilleLesser.get_from_obj(attachee)
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = CtrlVargouilleLesser.get_from_obj(attachee)
	if (ctrl):
		return ctrl.enter_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

class CtrlVargouilleLesser(object):
	def __init__(self):
		self.round = 0
		self.spells = utils_npc_spells.NPCSpells()
		self.performed_shriek_count = 0
		return

	def npc_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = 6202
		npc.scripts[const_toee.sn_enter_combat] = 6202
		if (not utils_toee.supports_custom_name()):
			npc.condition_add_with_args("Caster_Level_Add", 4, 0)
			self.spells.add_spell(toee.spell_fear, toee.stat_level_wizard, 4)
		else:
			npc.condition_add("Python_Action_Shriek")
		return

	@staticmethod
	def get_name():
		return "CtrlVargouilleLesser"

	@classmethod
	def create_obj(cls, loc):
		PROTO_NPC_VARGOUILLE_LESSER = 14891
		npc = toee.game.obj_create(PROTO_NPC_VARGOUILLE_LESSER, loc)
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
			if (not self.performed_shriek_count and utils_toee.supports_custom_name()):
				tac.add_target_closest()
				tac.add_five_foot_step()
				tac.add_python_action(3003)
				print("do shriek")
				self.performed_shriek_count += 1
				break

			if (self.spells.get_spell_count(toee.spell_fear)):
				tac.add_target_closest()
				tac.add_five_foot_step()
				tac.add_cast_area_code(self.spells.prep_spell(attachee, toee.spell_fear, 1))
				self.performed_shriek_count += 1
				break
			tac.add_target_closest()
			tac.add_attack()
			break

		print(tac.custom_tactics)
		#debugg.breakp("CtrlKnellBeetleLesser::start_combat")
		if (tac.count > 0):
			tac.set_strategy(attachee)
		return toee.RUN_DEFAULT

	def enter_combat(self, attachee, triggerer):
		self.round = 0
		return toee.RUN_DEFAULT