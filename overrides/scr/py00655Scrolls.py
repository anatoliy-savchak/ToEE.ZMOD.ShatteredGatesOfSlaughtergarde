import toee, utils_item, const_proto_list_scrolls
from utilities import *
from scripts import *

def san_dialog(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(triggerer, toee.PyObjHandle)

	attachee.obj_set_int(toee.obj_f_critter_inventory_source, 0)
	box = attachee.substitute_inventory
	if (box):
		box.obj_set_int(toee.obj_f_container_inventory_source, 0)

	attachee.turn_towards(triggerer)
	if not attachee.has_met(triggerer):
		triggerer.begin_dialog(attachee, 1)
		return toee.SKIP_DEFAULT
	else:
		triggerer.begin_dialog(attachee, 100)
	return toee.SKIP_DEFAULT

# crashes when removed
def respawn(attachee):
	return
