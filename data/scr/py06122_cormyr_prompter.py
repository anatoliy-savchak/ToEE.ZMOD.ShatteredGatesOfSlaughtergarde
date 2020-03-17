from toee import *
from debugg import *
import utils_obj

def san_heartbeat( attachee, triggerer ):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	#breakp("py06122_cormyr_prompter san_heartbeat 1")
	if (game.combat_is_active()): return RUN_DEFAULT
	radar_radius_ft = attachee.obj_get_int(obj_f_hp_damage)
	if (radar_radius_ft <= 0): radar_radius_ft = 10
	foundTuple = game.obj_list_range(attachee.location, radar_radius_ft, OLC_PC)
	if (len(foundTuple) == 0): return RUN_DEFAULT
	line_id = attachee.obj_get_int(obj_f_hp_pts) - 100
	if (line_id > 0):
		breakp("py06122_cormyr_prompter san_heartbeat 2")
		attachee.float_line(line_id, foundTuple[0])
		#attachee.float_line(1, foundTuple[0]) # new line
	utils_obj.obj_scripts_clear(attachee)
	#utils_obj.obj_timed_off(attachee, 10000)
	utils_obj.obj_timed_destroy(attachee, 10000)
	breakp("py06122_cormyr_prompter utils_obj.obj_timed_destroy")
	return RUN_DEFAULT

