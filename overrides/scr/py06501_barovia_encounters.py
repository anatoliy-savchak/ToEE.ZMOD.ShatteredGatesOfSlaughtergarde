import toee, debug, tpdp, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls, ctrl_behaviour
import const_proto_potions, utils_obj, const_proto_food, utils_npc, utils_target_list, const_proto_wands, utils_sneak, const_deseases, utils_npc_spells, utils_npc
import py06401_shattered_temple_encounters, const_proto_items, const_proto_rings, const_proto_cloth

barovia_encounters = 6501

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.start_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.enter_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_end_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.end_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_exit_combat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.exit_combat(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_will_kos(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	print("will_kos({}, {})".format(attachee, triggerer))
	ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(attachee)
	if (ctrl):
		return ctrl.will_kos(attachee, triggerer)
	else: print("san_will_kos ctrl not found")
	return toee.RUN_DEFAULT

class CtrlBehaviourBarovia(ctrl_behaviour.CtrlBehaviour):
	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		npc.scripts[const_toee.sn_start_combat] = barovia_encounters
		npc.scripts[const_toee.sn_enter_combat] = barovia_encounters
		return

class CtrlZombieInfected(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14840

class CtrlCarcassEater(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14841

class CtrlDireMaggot(ctrl_behaviour.CtrlBehaviour):
	@classmethod
	def get_proto_id(cls): return 14842

class CtrlVargouilleLesser(CtrlBehaviourBarovia):
	@classmethod
	def get_proto_id(cls): return 14891

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = None

		shrieked = self.get_var("shrieked")
		if (not shrieked): shrieked = 0

		while (not tac):
			if (shrieked < 1): 
				npc.condition_add("Python_Action_Shriek")
				tac = utils_tactics.TacticsHelper(self.get_name())
				tac.add_target_closest()
				tac.add_approach_single()
				tac.add_python_action(3003)
				self.vars["shrieked"] = 1
				tac.add_halt()
				tac.add_total_defence()
				break
			break
		return tac
