import toee, utils_obj

def san_use( attachee, triggerer ):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)
	if (attachee.type == obj_t_portal):
		utils_obj.obj_scripts_clear(attachee)
		utils_obj.obj_timed_destroy(attachee, 500)
		#attachee.object_flag_set(toee.OF_DONTDRAW)
		for obj in toee.game.obj_list_range(attachee.location, 10, toee.OLC_PORTAL):
			if (obj == attachee): continue
			utils_obj.obj_scripts_clear(obj)
			utils_obj.obj_timed_destroy(obj, 1000)
			obj.portal_toggle_open()

	return toee.RUN_DEFAULT

