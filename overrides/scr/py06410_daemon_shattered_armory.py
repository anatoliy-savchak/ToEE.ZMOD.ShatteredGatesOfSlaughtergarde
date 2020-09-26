import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon
import ctrl_behaviour, py06122_cormyr_prompter, shattered_consts, py06211_shuttered_monster, const_proto_scrolls, const_proto_wands, utils_npc
import py06411_shattered_armory_encounters, startup_zmod, utils_sneak

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print(attachee.id)
	#debugg.breakp("san_new_map")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_ARMORY): toee.RUN_DEFAULT
	ctrl = CtrlShatteredArmory.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_ARMORY): toee.RUN_DEFAULT
	ctrl = CtrlShatteredArmory.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#debug.breakp("san_heartbeat")
	if (attachee.map != shattered_consts.MAP_ID_SHATERRED_ARMORY): toee.RUN_DEFAULT
	ctrl = csa()
	if (not ctrl):
		ctrl = CtrlShatteredArmory.ensure(attachee)
		ctrl.place_encounters(1)
	if (ctrl):
		ctrl.heartbeat()
	return toee.RUN_DEFAULT

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))

	if (attachee.name == 1643): #{1643}{Shattered Armory Exit}
		toee.game.fade_and_teleport( 0, 0, 0, 5107, 491, 480 ) #shopmap
	elif (attachee.name == 939): #{939}{A6 Door}
		print("A6 Door")
		attachee.object_flag_set(toee.OF_DONTDRAW)
		if (toee.game.combat_turn):
			csa().encounter_a6_premature(attachee, triggerer)
	else:
		attachee.object_flag_set(toee.OF_DONTDRAW)
		if (attachee.name == 938): #{938}{A5 Fiery Demon Arch}
			promter = utils_npc.npc_find_nearest_npc_by_proto(attachee, 15, py06122_cormyr_prompter.PROTO_NPC_PROMPTER)
			if (promter):
				py06122_cormyr_prompter.promter_talk(promter, triggerer)
			else:
				print("promter not found!")
				#debug.breakp("promter not found!")
		elif (attachee.name == 942): #{942}{A10 Fiery Demon Arch}
			print("A10 Door")
			promter = utils_npc.npc_find_nearest_npc_by_proto(attachee, 15, py06122_cormyr_prompter.PROTO_NPC_PROMPTER)
			if (promter):
				py06122_cormyr_prompter.promter_talk(promter, triggerer)
			else:
				print("promter not found!")
		elif (attachee.name == 944): #{944}{A12 Fiery Demon Arch}
			print("A12 Door")
			promter = utils_npc.npc_find_nearest_npc_by_proto(attachee, 10, py06122_cormyr_prompter.PROTO_NPC_PROMPTER)
			if (promter):
				py06122_cormyr_prompter.promter_talk(promter, triggerer)
			else:
				print("promter not found!")
				
	#debug.breakp("san_use")
	return toee.RUN_DEFAULT

def csa():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(shattered_consts.SHATERRED_ARMORY_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlShatteredArmory.get_name() in o.data):
		result = o.data[CtrlShatteredArmory.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlShatteredArmory(ctrl_daemon.CtrlDaemon):
	def __init__(self):
		super(CtrlShatteredArmory, self).__init__()
		return

	def created(self, npc):
		super(CtrlShatteredArmory, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = shattered_consts.SHATERRED_ARMORY_DAEMON_SCRIPT
		return

	@staticmethod
	def get_name():
		return "CtrlShatteredArmory"

	def get_map_default(self):
		return shattered_consts.MAP_ID_SHATERRED_ARMORY

	def place_encounters(self, new_map):
		print("new_map: {}".format(new_map))
		print("place_encounters.encounters_placed == {}".format(self.encounters_placed))
		startup_zmod.zmod_templeplus_config_apply()
		startup_zmod.zmod_conditions_apply_pc()

		if (self.encounters_placed and new_map == 0): return

		this_entrance_time = toee.game.time.time_game_in_hours2(toee.game.time)
		print("this_entrance_time == {}".format(this_entrance_time))
		if (not self.encounters_placed):
			self.first_entered_shrs = this_entrance_time
		self.last_entered_shrs = this_entrance_time
		if (not self.last_leave_shrs):
			self.last_leave_shrs = this_entrance_time

		#todo - remember destroyed doors
		#self.remove_door_by_name(921) #{921}{Portcullis A2}
		if (not self.encounters_placed):
			#self.place_encounter_a1()
			#self.place_encounter_a2()
			#self.place_encounter_a3()
			#self.place_encounter_a4()
			#self.place_encounter_a5()
			#self.place_encounter_a6()
			#self.place_encounter_a7()
			#self.place_encounter_a9()
			#self.place_encounter_a10()
			#self.place_encounter_a11()
			#self.place_encounter_a12()
			self.place_encounter_a14()
			self.place_encounter_a15()

		self.encounters_placed += 1
		self.factions_existance_refresh()
		self.check_sleep_status_update(1)
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 460, 499) #a5
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 429, 481) #a7
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 496, 498) #a10
		#toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 528, 481) #a11
		toee.game.fade_and_teleport(0, 0, 0, shattered_consts.MAP_ID_SHATERRED_ARMORY, 496, 457) #a15

		#self.check_entrance_patrol()
		utils_obj.scroll_to_leader()
		return

	def heartbeat(self):
		#self.remove_door_by_name(921) #{921}{Portcullis A2}
		return

	def debug_fix(self):
		toee.game.get_obj_by_id(self.id).scripts[const_toee.sn_heartbeat] = shattered_consts.SHATERRED_ARMORY_DAEMON_SCRIPT
		return

	def get_dialogid_default(self):
		return shattered_consts.SHATERRED_ARMORY_DAEMON_DIALOG

	def place_encounter_a0(self):
		self.create_npc_at(utils_obj.sec2loc(419, 518), py06411_shattered_armory_encounters.CtrlFlindSoldier, const_toee.rotation_0100_oclock, "a0", "flind")[1]
		self.reveal_monster("a0", "flind")
		self.activate_monster("a0", "flind")

		if (1): # testing
			self.create_npc_at(utils_obj.sec2loc(419, 521), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0100_oclock, "a0", "gnoll1")
			self.reveal_monster("a0", "gnoll1")
			self.activate_monster("a0", "gnoll1")

			self.create_npc_at(utils_obj.sec2loc(419, 525), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0000_oclock, "a0", "gnoll2")
			self.reveal_monster("a0", "gnoll2")
			self.activate_monster("a0", "gnoll2")
		return

	def place_encounter_a1(self):
		self.create_promter_at(utils_obj.sec2loc(415, 520), self.get_dialogid_default(), 10, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Outer Stockade", const_toee.rotation_0000_oclock)

		ctrl = self.create_npc_at(utils_obj.sec2loc(419, 518), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0100_oclock, "a1", "gnoll1")[1]
		ctrl.vars["tag"] = 1
		ctrl = self.create_npc_at(utils_obj.sec2loc(419, 521), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0100_oclock, "a1", "gnoll2")[1]
		ctrl.vars["tag"] = 2
		ctrl = self.create_npc_at(utils_obj.sec2loc(419, 525), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0000_oclock, "a1", "gnoll3")[1]
		ctrl.vars["tag"] = 3
		return

	def display_encounter_a1(self):
		print("display_encounter_a1")
		self.reveal_monster("a1", "gnoll1")
		self.reveal_monster("a1", "gnoll2")
		self.reveal_monster("a1", "gnoll3")
		return

	def activate_encounter_a1(self):
		print("activate_encounter_a1")
		self.activate_monster("a1", "gnoll1")
		self.activate_monster("a1", "gnoll2")
		self.activate_monster("a1", "gnoll3")
		return

	def place_encounter_a2(self):
		self.create_promter_at(utils_obj.sec2loc(448, 521), self.get_dialogid_default(), 20, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Inner Stockade", const_toee.rotation_0000_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(463, 518), py06411_shattered_armory_encounters.CtrlGnollArcher, const_toee.rotation_0100_oclock, "a2", "gnoll1")
		self.create_npc_at(utils_obj.sec2loc(463, 525), py06411_shattered_armory_encounters.CtrlGnollArcher, const_toee.rotation_0100_oclock, "a2", "gnoll2")
		return

	def display_encounter_a2(self):
		print("display_encounter_a2")
		self.reveal_monster("a2", "gnoll1")
		self.reveal_monster("a2", "gnoll2")

		self.reveal_monster("a3", "troll", 1)
		return

	def activate_encounter_a2(self):
		print("activate_encounter_a2")
		self.activate_monster("a2", "gnoll1")
		self.activate_monster("a2", "gnoll2")
		return

	def place_encounter_a3(self):
		self.create_promter_at(utils_obj.sec2loc(469, 520), self.get_dialogid_default(), 30, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Blind Troll", const_toee.rotation_0000_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(475, 517), py06411_shattered_armory_encounters.CtrlBlindTroll, const_toee.rotation_0200_oclock, "a3", "troll", 75)
		return

	def display_encounter_a3(self):
		print("display_encounter_a3")
		self.reveal_monster("a3", "troll")
		return

	def activate_encounter_a3(self):
		print("activate_encounter_a3")
		self.activate_monster("a3", "troll")
		return

	def place_encounter_a4(self):
		self.create_promter_at(utils_obj.sec2loc(479, 490), self.get_dialogid_default(), 40, 15, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Elevator Room", const_toee.rotation_0600_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(485, 476), py06411_shattered_armory_encounters.CtrlHillGiant, const_toee.rotation_0500_oclock, "a4", "giant")
		return

	def display_encounter_a4(self):
		print("display_encounter_a4")
		self.reveal_monster("a4", "giant")
		return

	def activate_encounter_a4(self):
		print("activate_encounter_a4")
		self.activate_monster("a4", "giant")
		return

	def place_encounter_a5(self):
		self.create_promter_at(utils_obj.sec2loc(453, 503), self.get_dialogid_default(), 50, 15, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Eastern Room", const_toee.rotation_0800_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(450, 503), py06411_shattered_armory_encounters.CtrlHalfFiendOgre, const_toee.rotation_0800_oclock, "a5", "ogre")
		return

	def display_encounter_a5(self):
		print("display_encounter_a5")
		self.reveal_monster("a5", "ogre")
		return

	def activate_encounter_a5(self):
		print("activate_encounter_a5")
		self.activate_monster("a5", "ogre")
		return

	def place_encounter_a6(self):
		self.create_promter_at(utils_obj.sec2loc(443, 509), self.get_dialogid_default(), 60, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Redspwan Prison", const_toee.rotation_0800_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(443, 500), py06411_shattered_armory_encounters.CtrlRedspwawnFirebelcher, const_toee.rotation_0400_oclock, "a6", "firebelcher")
		return

	def display_encounter_a6(self):
		print("display_encounter_a6")
		self.reveal_monster("a6", "firebelcher", 1)
		return

	def activate_encounter_a6(self):
		print("activate_encounter_a6")
		self.activate_monster("a6", "firebelcher", 1)
		return

	def encounter_a6_get_alive_monster(self):
		info = self.get_monsterinfo("a6", "firebelcher")
		if (not info): return None
		npc = toee.game.get_obj_by_id(info.id)
		if (not npc): return None
		if (not utils_npc.npc_is_alive(npc, 1)): return None
		return npc

	def encounter_a6_is_monster_alive(self):
		npc = self.encounter_a6_get_alive_monster()
		if (not npc): return 0
		return 1

	def encounter_a6_premature(self, door, triggerer):
		print("encounter_a6_premature ({}, {})".format(door, triggerer))
		assert isinstance(triggerer, toee.PyObjHandle)
		if (triggerer and triggerer.type == toee.obj_t_pc):
			# only when npc is doing that
			return 0

		npc = self.encounter_a6_get_alive_monster()
		if (not npc): return 0
		assert isinstance(npc, toee.PyObjHandle)

		self.display_encounter_a6()
		self.activate_encounter_a6()
		promter = utils_npc.npc_find_nearest_npc_by_proto(door, 15, py06122_cormyr_prompter.PROTO_NPC_PROMPTER)
		if (promter):
			promter.destroy()

		# move it before the door
		npc.move(utils_obj.sec2loc(444, 508))
		npc.rotation = const_toee.rotation_0800_oclock

		npc.d20_status_init()
		npc.set_initiative(triggerer.get_initiative())
		return

	def place_encounter_a7(self):
		p1 = self.create_promter_at(utils_obj.sec2loc(420, 481), self.get_dialogid_default(), 70, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Southeastern Arsenal", const_toee.rotation_0800_oclock)
		p2 = self.create_promter_at(utils_obj.sec2loc(416, 479), self.get_dialogid_default(), 70, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Southeastern Arsenal", const_toee.rotation_1100_oclock)
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)
		
		self.create_npc_at(utils_obj.sec2loc(419, 484), py06411_shattered_armory_encounters.CtrlTroglodyteBarbarians, const_toee.rotation_0900_oclock, "a7", "troglodyte_barb1")
		self.create_npc_at(utils_obj.sec2loc(418, 489), py06411_shattered_armory_encounters.CtrlTroglodyteBarbarians, const_toee.rotation_0900_oclock, "a7", "troglodyte_barb2")
		self.create_npc_at(utils_obj.sec2loc(415, 489), py06411_shattered_armory_encounters.CtrlTroglodyteBarbarians, const_toee.rotation_0900_oclock, "a7", "troglodyte_barb3")
		return

	def display_encounter_a7(self):
		print("display_encounter_a7")
		self.reveal_monster("a7", "troglodyte_barb1")
		self.reveal_monster("a7", "troglodyte_barb2")
		self.reveal_monster("a7", "troglodyte_barb3")
		return

	def activate_encounter_a7(self):
		print("activate_encounter_a7")
		self.activate_monster("a7", "troglodyte_barb1")
		self.activate_monster("a7", "troglodyte_barb2")
		self.activate_monster("a7", "troglodyte_barb3")
		return

	def place_encounter_a9(self):
		p1 = self.create_promter_at(utils_obj.sec2loc(416, 475), self.get_dialogid_default(), 90, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Northeastern Arsenal", const_toee.rotation_0800_oclock)
		p2 = self.create_promter_at(utils_obj.sec2loc(419, 473), self.get_dialogid_default(), 90, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Northeastern Arsenal", const_toee.rotation_0800_oclock)
		p1.obj_set_obj(toee.obj_f_last_hit_by, p2)
		p2.obj_set_obj(toee.obj_f_last_hit_by, p1)

		self.create_npc_at(utils_obj.sec2loc(420, 475), py06411_shattered_armory_encounters.CtrlTroglodyteThug, const_toee.rotation_0300_oclock, "a9", "troglodyte_thug1")
		self.create_npc_at(utils_obj.sec2loc(413, 475), py06411_shattered_armory_encounters.CtrlTroglodyteThug, const_toee.rotation_0600_oclock, "a9", "troglodyte_thug2")

		self.create_npc_at(utils_obj.sec2loc(420, 468), py06411_shattered_armory_encounters.CtrlTroglodyteSoldier, const_toee.rotation_0400_oclock, "a9", "troglodyte_sold1")
		self.create_npc_at(utils_obj.sec2loc(413, 468), py06411_shattered_armory_encounters.CtrlTroglodyteSoldier, const_toee.rotation_0400_oclock, "a9", "troglodyte_sold2")

		self.create_npc_at(utils_obj.sec2loc(416, 471), py06411_shattered_armory_encounters.CtrlTroglodyteCleric, const_toee.rotation_0600_oclock, "a9", "troglodyte_cleric")
		return

	def display_encounter_a9(self):
		print("display_encounter_a9")
		self.reveal_monster("a9", "troglodyte_thug1")
		self.reveal_monster("a9", "troglodyte_thug2")

		self.reveal_monster("a9", "troglodyte_sold1")
		self.reveal_monster("a9", "troglodyte_sold2")

		self.reveal_monster("a9", "troglodyte_cleric")
		return

	def activate_encounter_a9(self):
		print("activate_encounter_a9")
		npc, info = self.activate_monster("a9", "troglodyte_thug1")
		utils_sneak.npc_make_hide(npc, 1)

		npc, info = self.activate_monster("a9", "troglodyte_thug2")
		utils_sneak.npc_make_hide(npc, 1)

		self.activate_monster("a9", "troglodyte_sold1")
		self.activate_monster("a9", "troglodyte_sold2")

		self.activate_monster("a9", "troglodyte_cleric")
		return

	def trigger_monster_step_a9(self, step):
		self.trigger_monster_step("a9", "troglodyte_cleric", step)
		return

	def place_encounter_a10(self):
		self.create_promter_at(utils_obj.sec2loc(496, 509), self.get_dialogid_default(), 100, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Western Tower", const_toee.rotation_1000_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(495, 512), py06411_shattered_armory_encounters.CtrlOrcharix, const_toee.rotation_0900_oclock, "a10", "orcharix")
		return

	def display_encounter_a10(self):
		print("display_encounter_a10")
		self.reveal_monster("a10", "orcharix")
		return

	def activate_encounter_a10(self):
		print("activate_encounter_a10")
		self.activate_monster("a10", "orcharix")
		return

	def place_encounter_a11(self):
		self.create_promter_at(utils_obj.sec2loc(501, 517), self.get_dialogid_default(), 110, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Tiefling Quarters", const_toee.rotation_1000_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(496, 516), py06411_shattered_armory_encounters.CtrlTieflingBlademaster, const_toee.rotation_0900_oclock, "a11", "tiefling_blade1")
		self.create_npc_at(utils_obj.sec2loc(496, 520), py06411_shattered_armory_encounters.CtrlTieflingBlademaster, const_toee.rotation_0900_oclock, "a11", "tiefling_blade2")

		self.create_npc_at(utils_obj.sec2loc(492, 517), py06411_shattered_armory_encounters.CtrlTieflingWizard, const_toee.rotation_0900_oclock, "a11", "tiefling_wiz")
		return

	def display_encounter_a11(self):
		print("display_encounter_a11")
		self.reveal_monster("a11", "tiefling_blade1")
		self.reveal_monster("a11", "tiefling_blade2")
		self.reveal_monster("a11", "tiefling_wiz")
		return

	def activate_encounter_a11(self):
		print("activate_encounter_a11")
		self.activate_monster("a11", "tiefling_blade1")
		self.activate_monster("a11", "tiefling_blade2")
		self.activate_monster("a11", "tiefling_wiz")
		return

	def trigger_monster_step_a11(self, step):
		self.trigger_monster_step("a11", "tiefling_wiz", step)
		return

	def place_encounter_a12(self):
		self.create_promter_at(utils_obj.sec2loc(538, 481), self.get_dialogid_default(), 120, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Southwestern Arsenal", const_toee.rotation_1000_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(537, 484), py06411_shattered_armory_encounters.CtrlFlindSoldier, const_toee.rotation_0200_oclock, "a12", "flind_soldier1")
		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(541, 487), py06411_shattered_armory_encounters.CtrlGnollPriestess, const_toee.rotation_0200_oclock, "a12", "priestess1")
		ctrl.vars["a12"] = 1
		return

	def display_encounter_a12(self):
		print("display_encounter_a12")
		self.reveal_monster("a12", "flind_soldier1")
		self.reveal_monster("a12", "priestess1")
		return

	def activate_encounter_a12(self):
		print("activate_encounter_a12")
		self.activate_monster("a12", "flind_soldier1")
		self.activate_monster("a12", "priestess1")
		return

	def trigger_monster_step_a12(self, step):
		self.trigger_monster_step("a12", "priestess1", step)
		return

	def place_encounter_a14(self):
		self.create_promter_at(utils_obj.sec2loc(542, 475), self.get_dialogid_default(), 140, 5, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Northwestern Arsenal", const_toee.rotation_0500_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(542, 472), py06411_shattered_armory_encounters.CtrlFlindSoldier, const_toee.rotation_0500_oclock, "a14", "flind_soldier2")
		self.create_npc_at(utils_obj.sec2loc(547, 472), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0300_oclock, "a14", "barb1")
		self.create_npc_at(utils_obj.sec2loc(538, 472), py06411_shattered_armory_encounters.CtrlGnollBarbarian2, const_toee.rotation_0600_oclock, "a14", "barb2")

		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(544, 467), py06411_shattered_armory_encounters.CtrlGnollPriestess, const_toee.rotation_0500_oclock, "a14", "priestess2")
		ctrl.vars["a14"] = 1
		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(542, 467), py06411_shattered_armory_encounters.CtrlGnollPriestess, const_toee.rotation_0500_oclock, "a14", "priestess3")
		ctrl.vars["a14"] = 2
		npc, ctrl = self.create_npc_at(utils_obj.sec2loc(540, 467), py06411_shattered_armory_encounters.CtrlGnollPriestess, const_toee.rotation_0500_oclock, "a14", "priestess4")
		ctrl.vars["a14"] = 3
		return

	def display_encounter_a14(self):
		print("display_encounter_a14")
		self.reveal_monster("a14", "flind_soldier2")
		self.reveal_monster("a14", "barb1")
		self.reveal_monster("a14", "barb2")

		self.reveal_monster("a14", "priestess2")
		self.reveal_monster("a14", "priestess3")
		self.reveal_monster("a14", "priestess4")
		return

	def activate_encounter_a14(self):
		print("activate_encounter_a14")
		self.activate_monster("a14", "flind_soldier2")
		self.activate_monster("a14", "barb1")
		self.activate_monster("a14", "barb2")

		self.activate_monster("a14", "priestess2")
		self.activate_monster("a14", "priestess3")
		self.activate_monster("a14", "priestess4")
		return

	def trigger_monster_step_a14(self, step):
		self.trigger_monster_step("a14", "priestess2", step)
		self.trigger_monster_step("a14", "priestess3", step)
		self.trigger_monster_step("a14", "priestess4", step)
		return

	def place_encounter_a15(self):
		self.create_promter_at(utils_obj.sec2loc(500, 444), self.get_dialogid_default(), 150, 20, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "Foundry Foyer", const_toee.rotation_0300_oclock)
		
		self.create_npc_at(utils_obj.sec2loc(509, 445), py06411_shattered_armory_encounters.CtrlTrollMercenary, const_toee.rotation_0400_oclock, "a15", "troll")
		return

	def display_encounter_a15(self):
		print("display_encounter_a15")
		self.reveal_monster("a15", "troll")
		return

	def activate_encounter_a15(self):
		print("activate_encounter_a15")
		self.activate_monster("a15", "troll")
		return
