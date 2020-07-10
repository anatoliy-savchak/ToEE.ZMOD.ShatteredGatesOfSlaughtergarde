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