from toee import *
from utilities import *

def san_use( attachee, triggerer ):
	loc = triggerer.location
	npc = game.obj_create( 14026, loc )
	triggerer.turn_towards(attachee)
	triggerer.begin_dialog( npc,1 )
	return SKIP_DEFAULT

def san_dialog( attachee, triggerer ):
	triggerer.begin_dialog(attachee,1)
	return SKIP_DEFAULT
