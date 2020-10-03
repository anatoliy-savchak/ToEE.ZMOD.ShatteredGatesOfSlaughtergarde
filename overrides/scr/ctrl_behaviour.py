import toee, debugg, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls
import utils_target_list, utils_npc

def get_ctrl(id):
	assert isinstance(id, str)
	ctrl = None
	storage = utils_storage.obj_storage_by_id(id)
	if (storage):
		for t in storage.data.iteritems():
			if (issubclass(type(t[1]), CtrlBehaviour)):
				ctrl = t[1]
				break
	return ctrl

class CtrlBehaviour(object):
	def __init__(self):
		self.id = None
		self.spells = utils_npc_spells.NPCSpells()
		self.vars = dict()
		#self.items = dict()
		return

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		# assign scripts
		#npc.scripts[const_toee.sn_start_combat] = 6213
		# create inventory
		self.id = npc.id
		self.after_created(npc)
		return

	def after_created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return

	@classmethod
	def get_proto_id():
		return 14919

	@classmethod
	def create_obj_and_class(cls, loc, call_created=1):
		protoid = cls.get_proto_id()
		npc = toee.game.obj_create(protoid, loc)
		ctrl = cls()
		utils_storage.obj_storage(npc).data[cls.get_name()] = ctrl
		if (call_created):
			ctrl.created(npc)
		return npc, ctrl

	@classmethod
	def create_obj(cls, loc):
		npc, ctrl = cls.create_obj_and_class(loc)
		return npc

	@classmethod
	def get_name(cls):
		return "CtrlBehaviour"

	@classmethod
	def ensure(cls, npc):
		data = utils_storage.obj_storage(npc).data
		ctrl = None
		if (cls.get_name() in data):
			ctrl = data[cls.get_name()]
		else:
			ctrl = cls()
			ctrl.created(npc)
			utils_storage.obj_storage(npc).data[cls.get_name()] = ctrl
		return ctrl

	@classmethod
	def get_from_obj(cls, npc):
		data = utils_storage.obj_storage(npc).data
		if (cls.get_name() in data):
			return data[cls.get_name()]
		return

	def npc_get(self):
		npc = None
		if (self.id):
			npc = toee.game.get_obj_by_id(self.id)
		if (not npc):
			print("Failed to get NPC ctrl: {}, id: {}".format(type(self).__name__, self.id))
		return npc

	def start_combat(self, attachee, triggerer):
		print("")
		print("{}::{} (round: {})".format(type(self).__name__, "start_combat", toee.game.combat_turn))
		print("------------------------")
		#debugg.breakp("start_combat")
		if (utils_npc.npc_hp_current(attachee) >= 0):
			tac = self.create_tactics(attachee)
			if (not tac):
				tac = self.create_tactics_default(attachee)

			if (tac and tac.count > 0):
				tac.set_strategy(attachee)
		return toee.RUN_DEFAULT

	def exit_combat(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def enter_combat(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def end_combat(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def will_kos(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def dying(self, attachee, triggerer):
		return toee.RUN_DEFAULT

	def join(self, npc, follower):
		return toee.RUN_DEFAULT

	def create_tactics(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return None

	def create_tactics_default(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		tac = utils_tactics.TacticsHelper(self.get_name())
		tac.add_clear_target()
		tac.add_target_closest()
		tac.add_sniper()
		tac.add_use_potion()
		tac.add_attack()
		tac.add_approach()
		tac.add_attack()
		return tac

	def revealed(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return

	def revealing(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return

	def activated(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return

	def activating(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		return

	def trigger_step(self, npc, step):
		assert isinstance(npc, toee.PyObjHandle)
		assert isinstance(step, int)
		return

	def get_var(self, name):
		if (self.vars and name in self.vars):
			return self.vars[name]
		return None

	def tactic_coup_de_grace(self, npc, foes = None):
		assert isinstance(npc, toee.PyObjHandle)
		if (foes is None):
			foes = utils_target_list.AITargetList(npc, 1, 0, utils_target_list.AITargetMeasure.by_all()).rescan()
		coup_de_grace_targets = foes.get_coup_de_grace_targets()
		if (coup_de_grace_targets): 
			#debug.breakp("coup_de_grace_targets")
			tac = utils_tactics.TacticsHelper(self.get_name())
			tac.add_target_closest()
			tac.add_target_obj(coup_de_grace_targets[0].target.id)
			tac.add_approach_single()
			tac.add_d20_action(toee.D20A_COUP_DE_GRACE, 0)
			tac.add_attack_threatened()
			tac.add_total_defence()
			return tac
		return