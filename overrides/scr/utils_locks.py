import toee, debug

BREAK_DC_CHEST_SMALL = 17
BREAK_DC_CHEST_TREASURE = 23

def container_setup_dc(obj, locked_dc, key_id, hp, hardeness, break_dc):
	assert isinstance(obj, toee.PyObjHandle)
	if (obj.type != toee.obj_t_container):
		print("container_setup_dc :: obj is not obj_t_container! {}".format(obj))
		debug.breakp("container_setup_dc")
		return
	
	obj.obj_set_int(toee.obj_f_secretdoor_dc, break_dc)

	if (locked_dc):
		obj.container_flag_set(toee.OCOF_LOCKED)
		if (locked_dc < 0):
			obj.container_flag_set(toee.OCOF_JAMMED)
		else:
			obj.obj_set_int(toee.obj_f_container_lock_dc, locked_dc)
			
		if (key_id):
			obj.obj_set_int(toee.obj_f_container_key_id, key_id)

	if (hp):
		obj.obj_set_int(toee.obj_f_hp_pts, hp)

	if (hardeness):
		obj.obj_set_int(toee.obj_f_hp_adj, hp)
	return obj