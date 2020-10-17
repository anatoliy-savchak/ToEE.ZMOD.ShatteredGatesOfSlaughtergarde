from toee import *
from utilities import *
from scripts import *
import utils_obj
from utils_npc import *

def san_dialog( attachee, triggerer ):
	attachee.turn_towards(triggerer)
	if not attachee.has_met( triggerer ):
		triggerer.begin_dialog( attachee, 1 )
		return SKIP_DEFAULT
	else:
		if get_2(attachee):
			triggerer.begin_dialog( attachee, 100 )
		elif get_1(attachee):
			if game.global_vars[5] <= keep_away1(attachee, triggerer):
				triggerer.begin_dialog( attachee, 250 )
			else:
				triggerer.begin_dialog( attachee, 200 )
		else:
			triggerer.begin_dialog( attachee, 250 )
	return SKIP_DEFAULT

def san_first_heartbeat( attachee, triggerer ):
	return RUN_DEFAULT

def san_dying( attachee, triggerer ):
	return RUN_DEFAULT

def san_resurrect( attachee, triggerer ):
	return RUN_DEFAULT

def keep_away2(attachee, triggerer):
	game.global_vars[5] = int(keep_away1(attachee, triggerer))
	print("attachee.scripts[0x9] = 682")
	game.timevent_add(activate_heartbeat, (attachee), 2000, 1)
	
	return
	
def keep_away1(attachee, triggerer):
	x = triggerer.distance_to(attachee)
	return x

def activate_heartbeat(attachee):
	attachee.scripts[0x13] = 682
	return

def san_heartbeat(attachee, triggerer):
	print("troll heartbeat")
	talkto = None
	maxx = 470
	for pc in game.party:
		x, y = utils_obj.loc2sec(pc.location)
		if (x > maxx):
			talkto = pc
			print("talkto: {}".format(talkto))
			break
	if (talkto): 
		san_dialog(attachee, talkto)
		attachee.scripts[0x13] = 0
	return