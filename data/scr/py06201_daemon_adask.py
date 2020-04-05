import toee, debugg, utils_obj, const_toee, utils_item, utils_toee, py06122_cormyr_prompter


def san_new_map(attachee, triggerer):
	do_hook_doors()
	do_setup_chests()
	do_place_promters()
	return toee.SKIP_DEFAULT

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	option = 0
	if (not (attachee.portal_flags_get() & toee.OPF_OPEN)):
		option = utils_item.item_get_marker(attachee)
	return toee.RUN_DEFAULT

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
	py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(556, 477), 6201, 1, 20, 1, "The Storm") # A1
	py06122_cormyr_prompter.create_promter_at(utils_obj.sec2loc(533, 477), 6201, 11, 10, py06122_cormyr_prompter.PROMTER_DIALOG_METHOD_FLOAT_DIALOG_LINE, "HIGHTOWER MAIN HALL") # A2
	return
