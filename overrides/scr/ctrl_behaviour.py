import toee, debugg, utils_storage, utils_npc_spells, const_toee, utils_tactics, const_proto_weapon, utils_item, const_proto_armor, const_proto_scrolls

class CtrlBehaviour(object):
	def __init__(self):
		self.spells = utils_npc_spells.NPCSpells()
		#self.items = dict()
		return

	def created(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		# assign scripts
		#npc.scripts[const_toee.sn_start_combat] = 6213
		# create inventory
		return

	@classmethod
	def get_proto_id():
		return 14919

	@classmethod
	def create_obj_and_class(cls, loc):
		protoid = cls.get_proto_id()
		npc = toee.game.obj_create(protoid, loc)
		ctrl = cls()
		utils_storage.obj_storage(npc).data[cls.get_name()] = ctrl
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

	def start_combat(self, attachee, triggerer):
		print("{}::{} (round: {})".format(type(self).__name__, "start_combat", toee.game.combat_turn))

		#debugg.breakp("start_combat")
		tac = self.create_tactics(attachee)
		if (not tac):
			tac = self.create_tactics_default(attachee)

		if (tac and tac.count > 0):
			tac.make_name()
			print(tac.custom_tactics)
			attachee.ai_strategy_set_custom(tac.custom_tactics)
		return toee.RUN_DEFAULT

	def enter_combat(self, attachee, triggerer):
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