import toee, debugg, utils_toee

MAP_ID_CROSSROAD = 5194

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	if (attachee.map != MAP_ID_CROSSROAD): toee.RUN_DEFAULT
	if utils_toee.get_f("map_crossroad_initialized"): toee.RUN_DEFAULT

	return toee.RUN_DEFAULT
