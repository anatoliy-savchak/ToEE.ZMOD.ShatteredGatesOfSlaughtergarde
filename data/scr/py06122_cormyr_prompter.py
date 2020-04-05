import toee, debugg, utils_obj, const_toee, utils_toee

PROMTER_PARAM_FIELD_LINEID = toee.obj_f_npc_pad_i_3
PROMTER_PARAM_FIELD_RADAR_RADIUS = toee.obj_f_npc_pad_i_4
PROMTER_PARAM_FIELD_METHOD = toee.obj_f_npc_pad_i_5

def create_promter_at(loc, dialog_script_id, line_id, radar_radius_ft, method, new_name):
	PROTO_NPC_PROMPTER = 14830
	obj = toee.game.obj_create(PROTO_NPC_PROMPTER, loc)
	obj.scripts[const_toee.sn_dialog] = dialog_script_id
	obj.scripts[const_toee.sn_heartbeat] = 6122
	obj.obj_set_int(PROMTER_PARAM_FIELD_RADAR_RADIUS, radar_radius_ft)
	obj.obj_set_int(PROMTER_PARAM_FIELD_METHOD, method)
	#obj.object_flag_unset(toee.OF_FLAT)
	#obj.object_flag_unset(toee.OF_SEE_THROUGH)
	#obj.object_flag_unset(toee.OF_SHOOT_THROUGH)
	#obj.object_flag_unset(toee.OF_DONTDRAW)
	#obj.object_flag_unset(toee.OF_CLICK_THROUGH)
	#obj.object_flag_unset(toee.OF_NOHEIGHT)
	#obj.object_flag_unset(toee.OF_DONTLIGHT)
	#line_id = line_id + 100
	#print("line_id before: {}".format(line_id))
	obj.obj_set_int(PROMTER_PARAM_FIELD_LINEID, line_id)
	#line_id = obj.obj_get_int(toee.obj_f_npc_pad_i_3)
	#print("line_id after: {}".format(line_id))
	if (new_name):
		new_name_id = utils_toee.make_custom_name(new_name)
		if (new_name_id > 0):
			obj.obj_set_int(toee.obj_f_critter_description_unknown, new_name_id)
			obj.obj_set_int(const_toee.obj_f_description_correct, new_name_id)
	return obj

def san_heartbeat( attachee, triggerer ):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	#debugg.breakp("py06122_cormyr_prompter san_heartbeat 1")
	if (game.combat_is_active()): return toee.RUN_DEFAULT
	#return RUN_DEFAULT
	radar_radius_ft = attachee.obj_get_int(PROMTER_PARAM_FIELD_RADAR_RADIUS)
	if (radar_radius_ft <= 0): radar_radius_ft = 10
	foundTuple = toee.game.obj_list_range(attachee.location, radar_radius_ft, OLC_PC)
	if (len(foundTuple) == 0): return toee.RUN_DEFAULT
	#line_id = attachee.obj_get_int(obj_f_hp_pts) - 100
	line_id = attachee.obj_get_int(PROMTER_PARAM_FIELD_LINEID)
	method = attachee.obj_get_int(PROMTER_PARAM_FIELD_METHOD)
	print("line_id: {}, method: {}".format(line_id, method))
	#debugg.breakp("py06122_cormyr_prompter san_heartbeat 2")
	if (method == 1):
		foundTuple[0].begin_dialog(attachee, line_id)
	elif (line_id > 0):
		utils_obj.obj_float_line_dialog(attachee, method, line_id, foundTuple[0])
	#utils_obj.obj_scripts_clear(attachee)
	attachee.scripts[const_toee.sn_heartbeat] = 0
	utils_obj.obj_timed_destroy(attachee, 10000)
	return toee.RUN_DEFAULT
