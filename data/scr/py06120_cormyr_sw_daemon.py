from toee import *
from debugg import *
from utils_obj import *
from const_toee import *
from utils_item import *
from utils_storage import *
from behavior import Behavior

# DAEMON
def cormyr_sw_san_new_map( attachee, triggerer ):
	return SKIP_DEFAULT


def cormyr_sw_init():
	do_hook_doors()
	return

def do_hook_doors():
	#breakp("do_hook_doors sw")
	for obj in game.obj_list_range(game.party[0].location, 200, OLC_PORTAL ):
		#breakp("obj in game.obj_list_range")
		assert isinstance(obj, PyObjHandle)
		obj_scripts_clear(obj)
		obj.scripts[sn_use] = 6112
		obj.scripts[sn_dialog] = 6112
		obj.scripts[sn_trap] = 6120 # daemon ref
		objStorage = obj_storage(obj)
		objStorage.daemon = 6120
		#objStorage.data["behavior"] = Behavior()
		
	#breakp("do_hook_doors sw exit")
	return SKIP_DEFAULT

# DOOR
def door_san_use( attachee, triggerer, already_used, marker):
	#breakp("door_san_use sw")
	if (already_used): return 1 # should_destroy

	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)

	if (marker == 31): 
		do_encounter_w3()
	if ((marker == 61) or (marker == 62)): 
		do_encounter_w6()
	return 1 # should_destroy

def do_encounter_w3():
	leader = create_shadowscale_marauder_at(sec2loc(513, 489))
	leader.critter_flag_set(OCF_UNRESSURECTABLE) # say Leader
	leader.scripts[sn_heartbeat] = 6121
	leader.scripts[sn_enter_combat] = 6121
	leader.scripts[sn_dialog] = 6120

	create_shadowscale_marauder_at(sec2loc(508, 483))
	create_shadowscale_marauder_at(sec2loc(511, 493))
	return

def do_encounter_w6():
	leader = create_shadowscale_marauder_at(sec2loc(458, 455))
	leader.critter_flag_set(OCF_UNRESSURECTABLE) # say Leader
	leader.scripts[sn_heartbeat] = 6121
	leader.scripts[sn_enter_combat] = 6121
	leader.scripts[sn_dialog] = 6120

	create_shadowscale_marauder_at(sec2loc(463, 462))
	create_shadowscale_marauder_at(sec2loc(466, 458))
	return

def create_shadowscale_marauder_at(loc):
	PROTO_NPC_SHADOWSCALE_MARAUDER = 14833
	#newDescription = 14019
	npc = game.obj_create(PROTO_NPC_SHADOWSCALE_MARAUDER, loc)

	#npc.obj_set_int(obj_f_critter_description_unknown, newDescription)
	#npc.obj_set_int(obj_f_description_correct, newDescription)

	obj_scripts_clear(npc)
	item_clear_all(npc)

	#item_create_in_inventory(6341, npc)

	npc.item_wield_best_all()
	npc.faction_add(1)
	npc.critter_flag_set(OCF_MOVING_SILENTLY)
	npc.npc_flag_unset(ONF_KOS)
	npc.concealed_set(1)
	return npc
