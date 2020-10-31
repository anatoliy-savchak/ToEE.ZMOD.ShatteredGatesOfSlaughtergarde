from toee import *
from utilities import *
from scripts import *

def san_dialog( attachee, triggerer ):
	attachee.turn_towards(triggerer)
	if not attachee.has_met( triggerer ):
		triggerer.begin_dialog( attachee, 1 )
		return SKIP_DEFAULT
	else:
		if (attachee.leader_get() != OBJ_HANDLE_NULL):		## in party
			triggerer.begin_dialog( attachee, 300 )
			return SKIP_DEFAULT
		if get_1(attachee):		## haven't engaged
			triggerer.begin_dialog( attachee, 500 )
			return SKIP_DEFAULT
		elif get_2(attachee):	## met, unchained
			triggerer.begin_dialog( attachee, 100 )
			return SKIP_DEFAULT
		else:					## met, still chained
			triggerer.begin_dialog( attachee, 150 )
			return SKIP_DEFAULT
	return SKIP_DEFAULT

def san_first_heartbeat( attachee, triggerer ):
	return RUN_DEFAULT

def san_dying( attachee, triggerer ):
	return RUN_DEFAULT

def san_resurrect( attachee, triggerer ):
	return RUN_DEFAULT

def san_heartbeat( attachee, triggerer ):
	attachee.item_wield_best_all()
	weap = attachee.item_worn_at(3)
	if weap != OBJ_HANDLE_NULL:
		game.new_sid = 0
		return RUN_DEFAULT
	else:
		get_something(attachee)
	return RUN_DEFAULT

def san_new_map( attachee, triggerer, spell ):
	if (attachee.map == 5122):
		attachee.float_line(350,triggerer)
		game.new_sid = 0
	return RUN_DEFAULT

def run_aways( attachee ):
	attachee.critter_flag_set(OCF_MUTE)
	game.timevent_add(run_off, (attachee), 1000 )
	RETURN

def run_off( attachee ):
	attachee.runoff(attachee.location+3)
	game.timevent_add(run_off2, (attachee), 2000 )
	return RUN_DEFAULT
	
def run_off2( attachee ):
	attachee.destroy()
	return RUN_DEFAULT

def buttin2( attachee, triggerer):
	npc = find_npc_near(attachee,14040)
	triggerer.begin_dialog(npc,470)
	npc.turn_towards(triggerer)
	attachee.turn_towards(npc)
	return