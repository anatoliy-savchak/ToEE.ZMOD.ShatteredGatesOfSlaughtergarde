import toee, py06122_cormyr_prompter, shattered_consts, utils_toee, const_toee, utils_storage, debug, utils_obj, utils_npc, ctrl_behaviour, monster_info, utils_item

class CtrlDaemon(object):
	def __init__(self):
		self.encounters_placed = 0
		self.monsters = dict()
		self.m2 = list()
		self.id = None
		self.haertbeats_since_sleep_status_update = 0
		self.first_entered_shrs = 0
		self.last_entered_shrs = 0
		self.last_leave_shrs = 0
		self.last_patrol_spawned_shrs = 0
		self.patrol_spawned_count = 0
		self.factions_existance = dict()
		self.promters_info = list()
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
			map_default = ctrl.get_map_default()
			if (map_default):
				CtrlDaemon.set_daemon(npc.id, map_default)
		return ctrl

	@classmethod
	def get_from_obj(cls, npc):
		data = utils_storage.obj_storage(npc).data
		if (cls.get_name() in data):
			return data[cls.get_name()]
		return None

	def created(self, npc):
		self.id = npc.id
		npc.origin = self.get_map_default()
		nameid = utils_toee.make_custom_name("Daemon-{}".format(npc.origin))
		if (nameid):
			npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
			npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		return

	# abstract
	@classmethod
	def get_name(cls):
		return "ABSTRACT ERROR!"

	@classmethod
	def get_from_obj(cls, npc):
		data = utils_storage.obj_storage(npc).data
		if (cls.get_name() in data):
			return data[cls.get_name()]
		return None

	def do_enter(self):
		this_entrance_time = toee.game.time.time_game_in_hours2(toee.game.time)
		print("this_entrance_time == {}".format(this_entrance_time))
		if (not self.encounters_placed):
			self.first_entered_shrs = this_entrance_time
		self.last_entered_shrs = this_entrance_time
		if (not self.last_leave_shrs):
			self.last_leave_shrs = this_entrance_time
		return

	def do_leave(self):
		self.last_leave_shrs = toee.game.time.time_game_in_hours2(toee.game.time)
		return

	def create_promter_at(self, loc, dialog_script_id, line_id, radar_radius_ft, method, new_name, rotation = None):
		npc = py06122_cormyr_prompter.create_promter_at(loc, dialog_script_id, line_id, radar_radius_ft, method, new_name)
		print("promter {}:{} placed {} {}".format(line_id, new_name, npc.id, npc))
		if (rotation):
			npc.rotation = rotation

		info = monster_info.MonsterInfo()
		info.id = npc.id
		info.proto = npc.proto
		self.promters_info.append(info)
		return npc

	def get_monster_faction_default(self, npc):
		return shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN

	def get_monster_prefix_default(self):
		return None

	# abstract
	def get_map_default(self):
		return 0

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		assert isinstance(npc, toee.PyObjHandle)
		if (not faction): faction = self.get_monster_faction_default(npc)
		if (faction and faction != -1):
			npc.faction_add(faction)
		if (no_kos):
			npc.npc_flag_unset(toee.ONF_KOS)
		if (no_draw):
			npc.object_flag_set(toee.OF_DONTDRAW)
		if (no_draw and no_kos):
			npc.npc_flag_set(toee.ONF_NO_ATTACK)

		if (monster_name):
			nameid = utils_toee.make_custom_name(monster_name)
			if (nameid):
				npc.obj_set_int(toee.obj_f_critter_description_unknown, nameid)
				npc.obj_set_int(const_toee.obj_f_description_correct, nameid)
		info = monster_info.MonsterInfo()
		info.id = npc.id
		info.proto = npc.proto
		info.cr = utils_npc.npc_get_cr(npc)
		info.encounter_code = encounter_name
		info.monster_code_name = monster_code_name
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

	def get_monsterinfo_and_npc_and_ctrl(self, encounter_name, monster_code_name):
		npc = None
		ctrl = None
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			ctrl = ctrl_behaviour.get_ctrl(info.id)
		return info, npc, ctrl

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

	def check_npc_enemy(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		if (npc.proto == py06122_cormyr_prompter.PROTO_NPC_PROMPTER): return 0
		result = npc.faction_has(shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN) or npc.faction_has(shattered_consts.FACTION_WILDERNESS_HOSTILE)
		return result

	def kill_enemy_all(self):
		sm = 0.0
		killer = toee.game.leader
		for info in self.m2:
			assert isinstance(info, monster_info.MonsterInfo)
			npc = toee.game.get_obj_by_id(info.id)
			if (not npc): continue
			villian = self.check_npc_enemy(npc)
			if (not villian): continue
			if (not sm):
				sm = utils_item.acquire_sell_modifier_once()
			print("Killing {}, {}".format(info.name, npc))

			items = utils_item.items_get(npc, 1)
			if (items):
				recieve_items = list()
				i = len(items)
				while i > 0:
					i -= 1
					item = items[i]
					assert isinstance(item, toee.PyObjHandle)
					if (not item.type in [toee.obj_t_weapon, toee.obj_t_ammo, toee.obj_t_armor, toee.obj_t_money, toee.obj_t_food]): 
						recieve_items.append(item)
						continue
					item_flags = item.item_flags_get()
					if (item_flags & toee.OIF_IS_MAGICAL):
						recieve_items.append(item)

				for item in recieve_items:
					items.remove(item)
					if (not killer.item_get(item)):
						for npc in toee.game.party:
							if (npc != killer):
								if (killer.item_get(item)):
									break

				if (items):
					utils_item.autosell(sm, items)

			npc.critter_kill_by_effect(killer)
		return

	def kill_enemy_by_encounter(self, encounter_code):
		sm = 0.0
		killer = toee.game.leader
		for info in self.m2:
			assert isinstance(info, monster_info.MonsterInfo)
			if (info.encounter_code != encounter_code): continue
			npc = toee.game.get_obj_by_id(info.id)
			if (not npc): continue
			villian = self.check_npc_enemy(npc)
			if (not villian): continue
			if (not sm):
				sm = utils_item.acquire_sell_modifier_once()
			print("Killing {}, {}".format(info.name, npc))

			items = utils_item.items_get(npc, 1)
			if (items):
				recieve_items = list()
				i = len(items)
				while i > 0:
					i -= 1
					item = items[i]
					assert isinstance(item, toee.PyObjHandle)
					if (not item.type in [toee.obj_t_weapon, toee.obj_t_ammo, toee.obj_t_armor, toee.obj_t_money, toee.obj_t_food]): 
						recieve_items.append(item)
						continue
					item_flags = item.item_flags_get()
					if (item_flags & toee.OIF_IS_MAGICAL):
						recieve_items.append(item)

				for item in recieve_items:
					items.remove(item)
					if (not killer.item_get(item)):
						for npc in toee.game.party:
							if (npc != killer):
								if (killer.item_get(item)):
									break

				if (items):
					utils_item.autosell(sm, items)

			npc.critter_kill_by_effect(killer)
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

	def destroy_all_npc(self):
		myself = toee.game.get_obj_by_id(self.id)
		for npc in toee.game.obj_list_range(myself.location, 200, toee.OLC_NPC):
			if (npc.id == self.id): continue
			npc.destroy()
		return

	# Sleep interface
	def can_sleep(self):
		for npc in toee.game.obj_list_vicinity(toee.game.leader.location, toee.OLC_NPC):
			if (utils_npc.npc_is_alive(npc, 1) and (npc.faction_has(shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN) or npc.faction_has(shattered_consts.FACTION_WILDERNESS_HOSTILE))): 
				return toee.SLEEP_IMPOSSIBLE

		spawn_left = 0
		if (self.factions_existance and (shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN in self.factions_existance)): 
			spawn_left = self.factions_existance[shattered_consts.FACTION_SLAUGHTERGARDE_SPAWN][0]

		if (spawn_left):
			return toee.SLEEP_DANGEROUS

		return toee.SLEEP_SAFE

	# Sleep interface
	def encounter_exists(self, setup, encounter):
		assert isinstance(setup, toee.PyRandomEncounterSetup)
		assert isinstance(encounter, toee.PyRandomEncounter)
		return 0

	# Sleep interface
	def encounter_create(self, encounter):
		assert isinstance(encounter, toee.PyRandomEncounter)
		return

	# Storage events
	def storage_skip_load(self, key, val):
		if (key == "m2"): return 1
		return 0

	# Storage events
	def storage_data_loaded(self):
		self.m2 = list()
		if (self.monsters):
			for val in self.monsters.itervalues():
				if (val and not val in self.m2):
					self.m2.append(val)
		return

	# Storage events
	def storage_data_loaded_all(self):
		print("storage_data_loaded_all map: {}".format(toee.game.leader.map))
		if (toee.game.leader.map != self.get_map_default()): return
		to_del = list()
		objs = utils_storage.Storage().objs
		assert isinstance(objs, dict)
		for o in objs.itervalues():
			assert isinstance(o, utils_storage.ObjectStorage)
			if (o.name.startswith("G_") and o.origin == self.get_map_default()):
				npc = toee.game.get_obj_by_id(o.name)
				#if (npc):print("npc hp: {}, npc: {}".format(utils_npc.npc_hp_current(npc), npc))
				if (not npc or (npc.object_flags_get() & toee.OF_DESTROYED) or utils_npc.npc_hp_current(npc) < 0):
					to_del.append(o)
		print("drop objects, count: {}".format(len(to_del)))
		for o in to_del:
			del objs[o.name]

		self.check_sleep_status_update(1)
		return

	def factions_existance_refresh(self):
		print("factions_existance_refresh")
		self.factions_existance = monster_info.MonsterInfo.get_factions_existance(self.m2, 0)
		print(self.factions_existance)
		return

	def critter_dying(self, attachee, triggerer):
		self.factions_existance_refresh()
		return

	def check_sleep_status_update(self, force = 0):
		self.haertbeats_since_sleep_status_update +=1
		if (force or self.haertbeats_since_sleep_status_update > 5):
			self.haertbeats_since_sleep_status_update = 0
			toee.game.sleep_status_update()
		return

	def remove_promters_all(self):
		for npc in toee.game.obj_list_range(toee.game.leader.location, 200, toee.OLC_NPC):
			if (npc.proto == py06122_cormyr_prompter.PROTO_NPC_PROMPTER):
				npc.destroy()
		return

	def print_promters_names(self):
		for npc in toee.game.obj_list_range(toee.game.leader.location, 200, toee.OLC_NPC):
			if (npc.proto == py06122_cormyr_prompter.PROTO_NPC_PROMPTER):
				print(npc.description)
		return

	def trigger_monster_step(self, encounter_name, monster_code_name, step):
		info = self.get_monsterinfo(encounter_name, monster_code_name)
		if (info):
			npc = toee.game.get_obj_by_id(info.id)
			if (npc):
				ctrl = ctrl_behaviour.CtrlBehaviour.get_from_obj(npc)
				if (ctrl and ("trigger_step" in dir(ctrl))):
					result = ctrl.trigger_step(npc, step)
					return result
		return
