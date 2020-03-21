from toee import *
from debugg import *
from utils_obj import *
from const_toee import *
from utils_item import *
import utils_storage
#from behavior import Behavior
import utils_toee
import utils_npc
import py06123_banelar
from math import radians
#import debug

# DAEMON
def cormyr_sw_san_new_map( attachee, triggerer ):
	return SKIP_DEFAULT


def cormyr_sw_init():
	do_hook_doors()
	do_place_promters()
	return

def do_hook_doors():
	for obj in game.obj_list_range(game.party[0].location, 200, OLC_PORTAL ):
		assert isinstance(obj, PyObjHandle)
		obj_scripts_clear(obj)
		obj.scripts[sn_use] = 6112
		obj.scripts[sn_trap] = 6120 # daemon ref
	return SKIP_DEFAULT

# DOOR
def door_san_use( attachee, triggerer, already_used, marker):
	if (already_used): return 1 # should_destroy

	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)

	if (marker == 31): 
		do_encounter_w3()
	if ((marker == 61) or (marker == 62)): 
		do_encounter_w6()
	if (marker == 32): 
		do_encounter_w5()
	return 1 # should_destroy

def do_encounter_w3():
	return
	leader = create_shadowscale_marauder_at(sec2loc(513, 489))
	leader.critter_flag_set(OCF_UNRESSURECTABLE) # say Leader
	leader.scripts[sn_heartbeat] = 6121
	leader.scripts[sn_enter_combat] = 6121
	leader.scripts[sn_dialog] = 6120

	create_shadowscale_marauder_at(sec2loc(508, 483))
	create_shadowscale_marauder_at(sec2loc(511, 493))
	return

def do_encounter_w6():
	return
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

def do_place_promters():
	#return
	create_promter_at(sec2loc(517, 468), 6120, 21, 10, "Warren Entrance") # W1. WARREN ENTRANCE
	create_promter_at(sec2loc(493, 458), 6120, 22, 30, "Dark Lake") # W2. DARK LAKE
	create_promter_at(sec2loc(510, 489), 6120, 23, 20, "West Guard Chamber") # W3. WEST GUARD CHAMBER
	create_promter_at(sec2loc(506, 472), 6120, 24, 10, "Empty Den") # W4A. EMPTY DEN
	create_promter_at(sec2loc(489, 472), 6120, 24, 10, "Empty Den") # W4B. EMPTY DEN
	create_promter_at(sec2loc(485, 497), 6120, 25, 20, "Banelars Lair") # W5. BANELARS LAIR
	create_promter_at(sec2loc(461, 459), 6120, 26, 20, "North Guard Chamber") # W6. NORTH GUARD CHAMBER
	create_promter_at(sec2loc(441, 463), 6120, 27, 20, "Prisoner Pit") # W7. PRISONER PIT
	create_promter_at(sec2loc(460, 478), 6120, 28, 20, "Great Warren") # W8. GREAT WARREN
	create_promter_at(sec2loc(441, 474), 6120, 29, 20, "Chiefs Den") # W9. CHIEFS DEN
	create_promter_at(sec2loc(470, 493), 6120, 30,  5, "Egg Chamber") # W10. EGG CHAMBER
	create_promter_at(sec2loc(454, 499), 6120, 31, 20, "The Back Door") # W11. THE BACK DOOR
	create_promter_at(sec2loc(433, 505), 6120, 32, 70, "Monastery Trail") # W12. Monastery Trail
	return

def create_promter_at(loc, dialog_script_id, line_id, radar_radius_ft, new_name):
	PROTO_NPC_PROMPTER = 14830
	#PROTO_NPC_PROMPTER = 14833
	obj = game.obj_create(PROTO_NPC_PROMPTER, loc)
	obj_scripts_clear(obj)
	item_clear_all(obj)
	obj.scripts[sn_dialog] = dialog_script_id
	obj.scripts[sn_heartbeat] = 6122
	# test below
	obj.object_flag_set(OF_DONTDRAW)
	obj.object_flag_set(OF_CLICK_THROUGH)
	obj.object_flag_set(OF_SEE_THROUGH)
	obj.object_flag_set(OF_FLAT)
	obj.object_flag_set(OF_TRANSLUCENT)
	obj.object_flag_set(OF_NOHEIGHT)
	#
	obj.npc_flag_unset(ONF_KOS)
	obj.obj_set_int(obj_f_hp_damage, radar_radius_ft)
	line_id = line_id + 100
	obj.obj_set_int(obj_f_hp_pts, line_id)
	if (new_name):
		new_name_id = utils_toee.make_custom_name(new_name)
		if (new_name_id > 0):
			obj.obj_set_int(obj_f_critter_description_unknown, new_name_id)
			obj.obj_set_int(obj_f_description_correct, new_name_id)
	return obj

def do_encounter_w5():
	#loc = sec2loc(489, 495)
	loc = sec2loc(485, 498)
	#print(loc)
	#loc = 2121713844713L
	#print(loc)
	print("create_banelar_at")
	npc = create_banelar_at(loc)
	#npc.move(2121713844713L, 0, 0)
	return

def create_banelar_at(loc):
	PROTO_NPC_BANELAR = 14835
	npc = game.obj_create(PROTO_NPC_BANELAR, loc)

	#npc.obj_set_int(obj_f_critter_description_unknown, newDescription)
	#npc.obj_set_int(obj_f_description_correct, newDescription)

	obj_scripts_clear(npc)
	npc.scripts[sn_enter_combat] = 6123
	npc.scripts[sn_start_combat] = 6123
	npc.scripts[sn_spell_cast] = 6123
	npc.scripts[sn_heartbeat] = 6123
	#npc.scripts[sn_first_heartbeat] = 6123 mobs dont have this
	
	item_clear_all(npc)

	PROTO_RING_OF_PROTECTION_1 = 6082
	item_create_in_inventory(PROTO_RING_OF_PROTECTION_1, npc)

	npc.condition_add_with_args("Caster_Level_Add", 6, 0)
	#npc.condition_add_with_args("Spell_Quicken_All", 0, 0)
	npc.condition_add_with_args("Spell_Quicken", 2, 0) # one quicken spell per round
	npc.condition_add_with_args("Self_Saving_Fortitude", 20, 0)
	npc.item_wield_best_all()
	npc.faction_add(1)
	#npc.npc_flag_unset(ONF_KOS)
	npc.rotation = radians(225)
	npc.skill_ranks_set(skill_concentration, 11)

	# make it go first
	npc.stat_base_set(stat_dexterity, 50 )
	py06123_banelar.banelar_init_storage(npc)
	return npc