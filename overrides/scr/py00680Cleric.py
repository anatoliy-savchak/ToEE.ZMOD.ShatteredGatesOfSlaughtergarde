from toee import *
from utilities import *
from scripts import *
from InventoryRespawn import *
import utils_inventory_source

def san_dialog( attachee, triggerer ):
	attachee.spells_pending_to_memorized()
	attachee.turn_towards(triggerer)
	if not attachee.has_met( triggerer ):
		triggerer.begin_dialog( attachee, 1 )
		return SKIP_DEFAULT
	else:
		triggerer.begin_dialog( attachee, 100 )
	return SKIP_DEFAULT

def san_first_heartbeat( attachee, triggerer ):
#	game.particles( "sp-summon monster I", game.party[1] )
	y = box1(attachee)
	if game.quests[2].state == qs_completed:			## Temple cleared
		if y != 65:
			box2(attachee, 65)
			game.new_sid = 0
	elif game.quests[1].state == qs_completed:			## Chicane stuff returned
		if y != 64:
			box2(attachee, 64)		
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
	box = find_container_near(attachee, 1315)
	x = box.obj_get_int( obj_f_container_inventory_source )
	return x

def box2(attachee, inven_source):
	box = find_container_near(attachee, 1315)
	if box != OBJ_HANDLE_NULL:
		box.obj_set_int( obj_f_container_inventory_source, inven_source )
		attachee.scripts[19] = 680
	return

def box3(attachee, triggerer):
	box = find_container_near(attachee, 1315)
	if box != OBJ_HANDLE_NULL:
		game.global_vars[350] = box.obj_get_int( obj_f_container_inventory_source )
	return

def respawn(attachee):
#	game.particles( "sp-summon monster I", game.party[0] )
	for box in game.obj_list_vicinity( attachee.location, OLC_CONTAINER ): 
		if box.name == 1315:
			#RespawnInventory(box)
			utils_inventory_source.inventory_source_respawn(box)
			game.timevent_add(respawn, (attachee), 86400000 )
	return