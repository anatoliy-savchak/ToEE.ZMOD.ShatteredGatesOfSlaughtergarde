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

# crashes when removed
def respawn(attachee):
	return


def san_first_heartbeat( attachee, triggerer ):
#	game.particles( "sp-summon monster I", game.party[1] )
	y = box1(attachee)
	if game.quests[2].state == qs_completed:			## Temple cleared
		if y != 89:
			box2(attachee, 89)
			game.new_sid = 0
	elif game.quests[1].state == qs_completed:			## Chicane stuff returned
		if y != 88:
			box2(attachee, 88)		
	return RUN_DEFAULT

def san_dying( attachee, triggerer ):
	return RUN_DEFAULT

def san_heartbeat( attachee, triggerer ):
	respawn(attachee)
	game.new_sid = 0
	return RUN_DEFAULT

def san_resurrect( attachee, triggerer ):
	return RUN_DEFAULT

def box1(attachee):							## returns current invensource pointer
	box = find_container_near(attachee, 1314)
	x = box.obj_get_int( obj_f_container_inventory_source )
	return x

def box2(attachee, inven_source):
	box = find_container_near(attachee, 1314)
	if box != OBJ_HANDLE_NULL:
		box.obj_set_int( obj_f_container_inventory_source, inven_source )
		attachee.scripts[19] = 679
	return

def respawn(attachee):
#	game.particles( "sp-summon monster I", game.party[0] )
	for box in game.obj_list_vicinity( attachee.location, OLC_CONTAINER ): 
		if box.name == 1314:
			utils_inventory_source.inventory_source_respawn(box)
			#RespawnInventory(box) will not work with override folder
			game.timevent_add(respawn, (attachee), 24*60*60*100 )
	return