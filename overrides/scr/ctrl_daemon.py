import toee, py06122_cormyr_prompter, shattered_consts, utils_toee, const_toee, utils_storage, debug, utils_obj, utils_npc, ctrl_behaviour, monster_info

class CtrlDaemon(object):
	def __init__(self):
		self.encounters_placed = 0
		self.monsters = dict()
		self.m2 = list()
		self.id = None
		self.haertbeats_since_sleep_status_update = 0
		return

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

	def created(self, npc):
		self.id = npc.id
		return

	@classmethod
	def get_name(cls):
		return "ABSTRACT ERROR!"

	@classmethod
	def get_from_obj(cls, npc):
		data = utils_storage.obj_storage(npc).data
		if (cls.get_name() in data):
			return data[cls.get_name()]
		return None

	def create_promter_at(self, loc, dialog_script_id, line_id, radar_radius_ft, method, new_name, rotation = None):
		npc = py06122_cormyr_prompter.create_promter_at(loc, dialog_script_id, line_id, radar_radius_ft, method, new_name)
		print("promter {}:{} placed {} {}".format(line_id, new_name, npc.id, npc))
		if (rotation):
			npc.rotation = rotation
		return npc

	def get_monster_faction_default(self, npc):
		return shattered_consts.FACTION_SLAUGHTERGARDE_LABORATORY

	def get_monster_prefix_default(self):
		return shattered_consts.SHATERRED_TEMPLE

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		assert isinstance(npc, toee.PyObjHandle)
		if (not faction): faction = self.get_monster_faction_default(npc)
		if (faction and faction != -1):
			npc.faction_add(faction)
		#npc.npc_flag_set(toee.ONF_NO_ATTACK)
		if (no_kos):
			npc.npc_flag_unset(toee.ONF_KOS)
		if (no_draw):
			npc.object_flag_set(toee.OF_DONTDRAW)
		if (monster_name):
			nameid = utils_toee.make_custom_name(monster_name)
			if (nameid):
				npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
				npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		info = monster_info.MonsterInfo()
		info.id = npc.id
		info.proto = npc.proto
		info.cr = utils_npc.npc_get_cr(npc)
		info.name = "{}_{}_{}".format(self.get_monster_prefix_default(), encounter_name, monster_code_name)
		self.m2.append(info)
		self.monsters[info.name] = info
		return

	def get_monsterinfo(self, encounter_name, monster_code_name):
		key = "{}_{}_{}".format(self.get_monster_prefix_default(), encounter_name, monster_code_name)
		if (key in self.monsters):
			info = self.monsters[key]
			assert isinstance(info, monster_info.MonsterInfo)
			return info
		return None

	def print_portals(self):
		for obj in toee.game.obj_list_range(toee.game.party[0].location, 200, toee.OLC_PORTAL ):
			assert isinstance(obj, toee.PyObjHandle)
			x, y = utils_obj.loc2sec(obj.location)
			print("Name: {}, Proto: {}, id: {}, x:{}, y: {}, rot: {}, obj: {}".format(obj.name, obj.proto, obj.id, x, y, obj.rotation, obj))
		return


	def create_npc_at(self, npc_loc, ctrl_class, rot, encounter, code_name, faction = None):
		npc, ctrl = ctrl_class.create_obj_and_class(npc_loc)
		x, y = utils_obj.loc2sec(npc.location)
		print("create_npc_at npc: {}, ctrl: {}, id: {}, coord: {},{}".format(npc, ctrl, npc.id, x, y))
		if (npc):
			npc.move(npc_loc)
			npc.rotation = rot
			self.monster_setup(npc, encounter, code_name, None, 1, 1, faction)
		return npc, ctrl

	def reveal_monster(self, encounter_name, monster_code_name, no_error = 0):
		npc = None
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc and not info.revealed):
				ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(npc)
				if (ctrl and ("revealing" in dir(ctrl))):
					ctrl.revealing(npc)
				info.revealed = 1
				npc.object_flag_unset(toee.OF_DONTDRAW)
				if (ctrl and ("revealed" in dir(ctrl))):
					ctrl.revealed(npc)
		if (not npc and not no_error and (not info or not info.revealed)):
			print("Monster {} {} not found!".format(encounter_name, monster_code_name))
			debug.breakp("Monster not found")
		return npc, info

	def activate_monster(self, encounter_name, monster_code_name, remove_no_attack = 1, remove_no_kos = 1, no_error = 0):
		npc = None
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc):
				if (not info.activated):
					ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(npc)
					if (ctrl and ("activating" in dir(ctrl))):
						ctrl.activating(npc)
					if (remove_no_attack):
						npc.npc_flag_unset(toee.ONF_NO_ATTACK)
					info.activated = 1
					print("ACTIVATED: {}".format(npc))
					if (remove_no_kos):
						npc.npc_flag_set(toee.ONF_KOS)
					if (ctrl and ("activated" in dir(ctrl))):
						ctrl.activated(npc)
				else: info.activated +=1
		if (not npc and not no_error):
			print("Monster {} {} not found!".format(encounter_name, monster_code_name))
			debug.breakp("Monster not found")
		return npc, info

	def remove_door_by_name(self, door_name_id):
		for obj in toee.game.obj_list_range(toee.game.party[0].location, 200, toee.OLC_PORTAL):
			assert isinstance(obj, toee.PyObjHandle)
			if (obj.name == door_name_id):
				utils_obj.obj_timed_destroy(obj, 500, 1)
		return

	@staticmethod
	def get_current_daemon():
		sglobal = utils_storage.obj_storage_by_id("global")
		if (sglobal):
			daemon_id = sglobal.get_data("daemon-{}".format(toee.game.leader.map))
			if (daemon_id):
				daemon_storage = utils_storage.obj_storage_by_id(daemon_id)
				if (daemon_storage and daemon_storage.data):
					for ctrl in daemon_storage.data.itervalues():
						if ("can_sleep" in dir(ctrl)):
							return ctrl
		return None

	@staticmethod
	def set_daemon(deamon_id, map_id):
		sglobal = utils_storage.obj_storage_by_id("global")
		if (sglobal):
			sglobal.data["daemon-{}".format(map_id)] = deamon_id
		return None