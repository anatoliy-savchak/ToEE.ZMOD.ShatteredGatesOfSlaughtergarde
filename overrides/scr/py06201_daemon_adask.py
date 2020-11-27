import toee, debugg, utils_obj, const_toee, utils_item, utils_toee, py06122_cormyr_prompter, utils_npc, const_proto_armor, utils_item, const_proto_items, const_proto_weapon
import py06202_vargouille_lesser, const_proto_wands, math, const_proto_potions, const_proto_scrolls, const_proto_cloth, const_proto_wondrous

MAP_ID_ADASK = 5120
PROTO_NPC_ZOMBIE_BUGBEAR = 14890

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	if (attachee.map != MAP_ID_ADASK): toee.RUN_DEFAULT
	do_hook_doors()
	do_setup_chests()
	do_place_promters()
	attachee.scripts[const_toee.sn_new_map] = 0
	toee.game.leader.scripts[const_toee.sn_true_seeing] = 6201
	return toee.SKIP_DEFAULT

def san_true_seeing(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	subevent = toee.game.leader.obj_get_int(toee.obj_f_pad_i_7)
	#debugg.breakp("san_true_seeing")
	return toee.SLEEP_PASS_TIME_ONLY

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	option = 0
	if (not (attachee.portal_flags_get() & toee.OPF_OPEN)):
		option = utils_item.item_get_marker(attachee)
	return toee.RUN_DEFAULT

def san_dying(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	if (attachee.proto == PROTO_NPC_ZOMBIE_BUGBEAR):
		# todo scan PC and determine who will have masterwork and which
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD_MASTERWORK, attachee)
	return toee.RUN_DEFAULT

# remove
def san_bust(attachee, triggerer):
	do_encounter_a3()
	return toee.SKIP_DEFAULT

def do_hook_doors():
	for obj in toee.game.obj_list_range(toee.game.party[0].location, 200, toee.OLC_PORTAL):
		assert isinstance(obj, toee.PyObjHandle)
		utils_obj.obj_scripts_clear(obj)
		obj.scripts[const_toee.sn_use] = 6201
		obj.portal_flag_unset(toee.OPF_OPEN)
		obj.portal_flag_set(toee.OPF_LOCKED)
		obj.portal_flag_set(toee.OPF_JAMMED)
	return

def do_setup_chests():
	PROTO_CONTAINER_CHEST_TRAPPED = 1301
	obj = toee.game.obj_create(PROTO_CONTAINER_CHEST_TRAPPED, utils_obj.sec2loc(543, 531))
	utils_item.item_create_in_inventory(const_proto_cloth.PROTO_HELM_HEADBAND_OF_THE_STOUT_HEART, obj)
	utils_item.item_create_in_inventory(const_proto_items.PROTO_GENERIC_PEARL_WHITE, obj, 2)
	utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OF_CURE_LIGHT_WOUNDS, obj)
	utils_item.item_create_in_inventory(const_proto_scrolls.PROTO_SCROLL_OF_IDENTIFY, obj)
	utils_item.item_money_create_in_inventory(obj, 0, 100, 0, 0)
	obj.rotation = math.radians(const_toee.rotation_grad_south_east)
	return

def do_place_promters():
	py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(556, 477), 6201, 1, 20, 1, "The Storm") # A1
	py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(552, 477), 6201, 11, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_FLOAT_DIALOG_LINE, "HIGHTOWER MAIN HALL") # A2
	py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(533, 457), 6201, 20, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "RAT RACE") # A3
	py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(442, 477), 6201, 30, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "PREPARATION CHAMBER") # A4
	py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(420, 514), 6201, 50, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "WHAT A TANGLED WEB") # A5
	py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(410, 476), 6201, 80, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "THE DARK KNIGHT") # A8
	py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(532, 426), 6201, 70, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "GETTING AHEAD") # A7
	py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(542, 524), 6201, 60, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_FLOAT_DIALOG_LINE, "THE OFFERING CHEST") # A6
	return

def do_encounter_a3():
	#debugg.breakp("do_encounter_a3")
	for obj in toee.game.obj_list_range(toee.game.party[0].location, 200, toee.OLC_PORTAL):
		assert isinstance(obj, toee.PyObjHandle)
		toee.game.timevent_add(post_open_door, ( obj ), 100) # 1000 = 1 second
		#obj.destroy()
		#toee.game.sound(4053)
		obj.portal_flag_unset(toee.OPF_JAMMED)
		obj.portal_flag_unset(toee.OPF_LOCKED)
		#obj.portal_toggle_open()
		#utils_obj.obj_timed_destroy(obj, 500)
		#obj.portal_flag_unset(toee.OPF_OPEN)
	toee.game.timevent_add(post_create_rats, 0, 1000) # 1000 = 1 second
	return

def post_open_door(obj):
	assert isinstance(obj, toee.PyObjHandle)
	obj.portal_toggle_open()
	utils_obj.obj_timed_destroy(obj, 2000, 1)
	return

def post_create_rats(p):
	PROTO_NPC_ANIMAL_RAT = 14774
	obj = toee.game.obj_create(PROTO_NPC_ANIMAL_RAT, utils_obj.sec2loc(534, 453))
	obj = toee.game.obj_create(PROTO_NPC_ANIMAL_RAT, utils_obj.sec2loc(531, 453))

	obj = toee.game.obj_create(PROTO_NPC_ANIMAL_RAT, utils_obj.sec2loc(534, 451))
	obj = toee.game.obj_create(PROTO_NPC_ANIMAL_RAT, utils_obj.sec2loc(531, 451))

	obj = toee.game.obj_create(PROTO_NPC_ANIMAL_RAT, utils_obj.sec2loc(534, 449))
	obj = toee.game.obj_create(PROTO_NPC_ANIMAL_RAT, utils_obj.sec2loc(531, 449))

	obj = toee.game.obj_create(PROTO_NPC_ANIMAL_RAT, utils_obj.sec2loc(534, 447))
	obj = toee.game.obj_create(PROTO_NPC_ANIMAL_RAT, utils_obj.sec2loc(531, 447))

	# shut up prompter
	for obj in toee.game.obj_list_range(toee.game.party[0].location, 20, toee.OLC_NPC):
		assert isinstance(obj, toee.PyObjHandle)
		if (obj.proto == py06122_cormyr_prompter.PROTO_NPC_PROMPTER):
			obj.critter_flag_set(toee.OCF_MUTE)
			break
	toee.game.update_party_ui()
	return

def do_encounter_a4():
	PROTO_NPC_HOBGOBLIN_1 = 14188
	obj = toee.game.obj_create(PROTO_NPC_HOBGOBLIN_1, utils_obj.sec2loc(438, 467))
	utils_obj.obj_scripts_clear(obj)
	utils_item.item_create_in_inventory(const_proto_wondrous.PROTO_WONDROUS_BELT_LIFTING, obj)
	obj.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
	#utils_item.item_clear_all(obj)
	nearest_pc = utils_npc.npc_find_nearest_pc(obj, 30, 1)
	if (nearest_pc):
		obj.turn_towards(nearest_pc)
		obj.attack(nearest_pc)
	PROTO_NPC_HOBGOBLIN_2 = 14189
	obj = toee.game.obj_create(PROTO_NPC_HOBGOBLIN_2, utils_obj.sec2loc(438, 486))
	obj.condition_add_with_args("Base_Attack_Bonus1", 1, 0)
	utils_obj.obj_scripts_clear(obj)
	nearest_pc = utils_npc.npc_find_nearest_pc(obj, 30, 1)
	if (nearest_pc):
		obj.turn_towards(nearest_pc)
		obj.attack(nearest_pc)
	return

def do_encounter_a5():
	PROTO_MONSTROUS_SPIDER_MEDIUM = 14775
	obj = toee.game.obj_create(PROTO_MONSTROUS_SPIDER_MEDIUM, utils_obj.sec2loc(425, 518))
	utils_obj.obj_scripts_clear(obj)
	utils_item.item_create_in_inventory(const_proto_items.PROTO_GENERIC_PEARL_BLACK, obj)
	nearest_pc = utils_npc.npc_find_nearest_pc(obj, 30, 1)
	if (nearest_pc):
		obj.turn_towards(nearest_pc)
	return

def do_encounter_a8():
	obj = toee.game.obj_create(PROTO_NPC_ZOMBIE_BUGBEAR, utils_obj.sec2loc(406, 476))
	utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_MORNINGSTAR, obj)
	utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_SMALL_WOODEN, obj)
	obj.scripts[const_toee.sn_dying] = 6201
	nearest_pc = utils_npc.npc_find_nearest_pc(obj, 30, 1)
	if (nearest_pc):
		obj.turn_towards(nearest_pc)
	return

def do_encounter_a7():
	obj = py06202_vargouille_lesser.CtrlVargouilleLesser.create_obj(utils_obj.sec2loc(527, 421))
	utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_MAGIC_MISSILES_1ST, obj)
	utils_item.item_create_in_inventory(const_proto_potions.PROTO_POTION_OF_CURE_LIGHT_WOUNDS, obj)
	obj.rotation = math.radians(const_toee.rotation_grad_south)
	return