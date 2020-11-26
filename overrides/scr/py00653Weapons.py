import toee, const_proto_list_weapons, utils_item, const_proto_list_weapons_masterwork, const_proto_list_weapons_magic
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
		if attachee.reaction_get(triggerer) <= 30:
			triggerer.begin_dialog(attachee, 150)
			return toee.SKIP_DEFAULT
		else:
			triggerer.begin_dialog(attachee, 100)
	return toee.SKIP_DEFAULT

def barter_sell(npc):
	assert isinstance(npc, toee.PyObjHandle)
	utils_item.item_clear_all(npc.substitute_inventory)
	return

def barter_list(npc, protos):
	assert isinstance(npc, toee.PyObjHandle)
	subs = npc.substitute_inventory
	utils_item.item_clear_all(subs)
	for i in protos:
		item = toee.game.obj_create(i, subs.location)
		item.item_flag_set(toee.OIF_IDENTIFIED)
		subs.item_get(item)
	return
