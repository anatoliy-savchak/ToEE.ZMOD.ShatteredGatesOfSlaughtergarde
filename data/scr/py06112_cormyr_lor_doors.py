from toee import *
from debugg import *
from utils_obj import *
from py06110_daemon_cormyr_lor import door_san_use, chest_san_use
from utils_item import item_do_use_getset, item_get_marker

def san_use( attachee, triggerer ):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	if (attachee.type == obj_t_portal):
		if (not (attachee.portal_flags_get() & OPF_OPEN)):
			already_used = item_do_use_getset(attachee, 1)
			marker = item_get_marker(attachee)
			should_destroy = door_san_use(attachee, triggerer, already_used, marker)
			#print("attachee: {}, triggerer: {}, already_used: {}, marker: {}, should_destroy: {}".format(attachee, triggerer, already_used, marker, should_destroy))
			#breakp("san_use door")
			if (should_destroy):
				obj_scripts_clear(attachee)
				obj_timed_destroy(attachee, 500)
				return RUN_DEFAULT
	if (attachee.type == obj_t_container):
		already_used = item_do_use_getset(attachee, 1)
		marker = item_get_marker(attachee)
		return chest_san_use(attachee, triggerer, already_used, marker)
	return RUN_DEFAULT

