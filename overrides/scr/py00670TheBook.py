from toee import *

def san_use( attachee, triggerer ):
	loc = triggerer.location
	npc = game.obj_create( 14413, loc )
	triggerer.begin_dialog(npc,1)
	return SKIP_DEFAULT

def san_dialog( attachee, triggerer ):
	triggerer.begin_dialog(attachee,1)
	return SKIP_DEFAULT
