import toee, utils_npc, debug, utils_toee

class MonsterInfo:
	def __init__(self):
		self.proto = 0
		self.id = None
		self.cr = 0
		self.name = None
		self.activated = 0
		self.revealed = 0
		self.encounter_code = None
		self.monster_code_name = None
		return

	def get_npc(self):
		npc = toee.OBJ_HANDLE_NULL
		if (self.id and self.id != ""):
			npc = utils_toee.get_obj_by_id(self.id)
		else: print("null get_npc {}".format(self.id))
		return npc

	@staticmethod
	def get_factions_existance(monsters, debug = 0, result = None):
		assert isinstance(monsters, list)
		if (result is None):
			result = dict() # of tuple(alive, dead)
		notfound = list()
		for monster in monsters:
			assert isinstance(monster, MonsterInfo)
			npc = monster.get_npc()
			if (not npc): 
				if (debug):
					print("monster {} not found!".format(monster.id))
				#debug.breakp("wtf")
				#npc = monster.get_npc()
				continue
			alive = utils_npc.npc_is_alive(npc, 1)
			if (debug):
				print("alive: {}, npc: {}".format(alive, npc))
			dead = alive == 0
			if (npc): 
				for faction in npc.factions:
					value = (0, 0)
					if (faction in result):
						value = result[faction]
					value = (value[0] + alive, value[1] + dead)
					result[faction] = value
		return result