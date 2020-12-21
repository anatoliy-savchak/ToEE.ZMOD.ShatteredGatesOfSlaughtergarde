from toee import *
from utilities import *
from scripts import *

def san_dialog( attachee, triggerer ):
	attachee.turn_towards(triggerer)
	if not attachee.has_met( triggerer ):
		triggerer.begin_dialog( attachee, 1 )
		return SKIP_DEFAULT
	else:
		triggerer.begin_dialog( attachee, 100 )
	return SKIP_DEFAULT

def san_first_heartbeat( attachee, triggerer ):
	return RUN_DEFAULT

def san_dying( attachee, triggerer ):
	return RUN_DEFAULT

def san_resurrect( attachee, triggerer ):
	return RUN_DEFAULT


def set_room_flag( attachee, triggerer ):
	game.global_flags[56] = 1
	game.timeevent_add( room_no_longer_available, (), 86390000 )
	game.sleep_status_update()
	return RUN_DEFAULT

def room_no_longer_available():
	game.global_flags[56] = 0
	game.sleep_status_update()
	return RUN_DEFAULT
