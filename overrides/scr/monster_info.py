import toee, utils_npc

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
		npc = toee.game.get_obj_by_id(self.id)
		return npc

	@staticmethod
	def get_factions_existance(monsters):
		assert isinstance(monsters, list)
		result = dict() # of tuple(alive, dead)
		notfound = list()
		for monster in monsters:
			assert isinstance(monster, MonsterInfo)
			npc = monster.get_npc()
			if (not npc): continue
			alive = utils_npc.npc_is_alive(npc, 1)
			#print("alive: {}, npc: {}".format(alive, npc))
			dead = alive == 0
			if (npc): 
				for faction in npc.factions:
					value = (0, 0)
					if (faction in result):
						value = result[faction]
					value = (value[0] + alive, value[1] + dead)
					result[faction] = value
		return result