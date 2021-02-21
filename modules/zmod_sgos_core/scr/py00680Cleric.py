import toee, utils_item, const_proto_list_potions, const_proto_potions, const_proto_rings, const_proto_wands
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

def get_cleric_items():
	result = []

	result = result + [ \
	 const_proto_potions.PROTO_POTION_OF_CURE_LIGHT_WOUNDS, 10\
	, const_proto_potions.PROTO_POTION_OF_CURE_MODERATE_WOUNDS, 10\
	, const_proto_potions.PROTO_POTION_OF_DELAY_POISON, 10\
	, const_proto_potions.PROTO_POTION_OF_CURE_SERIOUS_WOUNDS, 10\
	, const_proto_potions.PROTO_POTION_OF_REMOVE_DISEASE, 10\

	, const_proto_rings.PROTO_RING_OF_PROTECTION_PLUS_1, 1\
	, const_proto_rings.PROTO_RING_OF_PROTECTION_PLUS_2, 1\
	, const_proto_rings.PROTO_RING_OF_PROTECTION_PLUS_3, 1\
	, const_proto_rings.PROTO_RING_OF_PROTECTION_PLUS_4, 1\

	, const_proto_wands.PROTO_WAND_OF_CURE_LIGHT_WOUNDS, 1\
	, const_proto_wands.PROTO_WAND_OF_BLESS, 1\
	, const_proto_wands.PROTO_WAND_OF_CURE_MODERATE_WOUNDS, 1\
	, const_proto_wands.PROTO_WAND_OF_RESTORATION_LESSER, 1\
	, ]

	return result