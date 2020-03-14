from toee import *
from debugg import *
from utils_obj import *
from utils_item import item_do_use_getset, item_get_marker
from utils_storage import *
import py06110_daemon_cormyr_lor
import py06120_cormyr_sw_daemon

def san_use( attachee, triggerer ):
	#breakp("doors san_use")
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	if (attachee.type == obj_t_portal):
		if (not (attachee.portal_flags_get() & OPF_OPEN)):
			already_used = item_do_use_getset(attachee, 1)
			marker = item_get_marker(attachee)
			#objStorage = obj_storage(attachee)
			#print(objStorage)
			#assert isinstance(objStorage, ObjectStorage)
			#print(objStorage.name)
			#print(objStorage.data)
			#print(objStorage.daemon)
			#breakp("doors san_use Storage.getObjectStorage")
			should_destroy = 0
			if (attachee.scripts[sn_trap] == 6110):
				should_destroy = py06110_daemon_cormyr_lor.door_san_use(attachee, triggerer, already_used, marker)
			if (attachee.scripts[sn_trap] == 6120):
				should_destroy = py06120_cormyr_sw_daemon.door_san_use(attachee, triggerer, already_used, marker)

			#print("attachee: {}, triggerer: {}, already_used: {}, marker: {}, should_destroy: {}".format(attachee, triggerer, already_used, marker, should_destroy))
			#breakp("san_use door")
			if (should_destroy):
				obj_scripts_clear(attachee)
				obj_timed_destroy(attachee, 500)
				return RUN_DEFAULT
	if (attachee.type == obj_t_container):
		already_used = item_do_use_getset(attachee, 1)
		marker = item_get_marker(attachee)
		return py06110_daemon_cormyr_lor.chest_san_use(attachee, triggerer, already_used, marker)
	return RUN_DEFAULT

