import toee, debugg, utils_obj, const_toee, utils_item, utils_toee, py06122_cormyr_prompter

MAP_ID_ADASK = 5120

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	if (attachee.map != MAP_ID_ADASK): toee.RUN_DEFAULT
	do_hook_doors()
	do_setup_chests()
	do_place_promters()
	attachee.scripts[const_toee.sn_new_map] = 0
	return toee.SKIP_DEFAULT

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	option = 0
	if (not (attachee.portal_flags_get() & toee.OPF_OPEN)):
		option = utils_item.item_get_marker(attachee)
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
	return

def do_place_promters():
	#return
	#py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(556, 477), 6201, 1, 20, 1, "The Storm") # A1
	#py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(533, 477), 6201, 11, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_FLOAT_DIALOG_LINE, "HIGHTOWER MAIN HALL") # A2
	prompter = py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(533, 457), 6201, 20, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_DIALOG, "RAT RACE") # A3
	#if (prompter):
	#	prompter.scripts[const_toee.sn_bust] = 6201
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

