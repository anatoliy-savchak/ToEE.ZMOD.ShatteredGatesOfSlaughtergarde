from toee import *
from utilities import *
from scripts import *

def san_dialog( attachee, triggerer ):
	attachee.turn_towards(triggerer)
	if not attachee.has_met( triggerer ):
		triggerer.begin_dialog( attachee, 1 )
	else:
		if game.quests[1].state == qs_completed:
			triggerer.begin_dialog( attachee, 400 )
			return SKIP_DEFAULT
		elif game.quests[1].state == qs_accepted:
			triggerer.begin_dialog( attachee, 300 )
			return SKIP_DEFAULT
		elif game.quests[1].state == qs_mentioned:
			triggerer.begin_dialog( attachee, 150 )
			return SKIP_DEFAULT
		else:
			triggerer.begin_dialog( attachee, 100 )
			return SKIP_DEFAULT
	return SKIP_DEFAULT

def san_first_heartbeat( attachee, triggerer ):
	return RUN_DEFAULT

def san_dying( attachee, triggerer ):
	return RUN_DEFAULT

def san_resurrect( attachee, triggerer ):
	return RUN_DEFAULT

def pay_the_man_full(triggerer):
	foll = len(game.party)
	pay = foll * 20000
	triggerer.money_adj(pay)
	return
	
def pay_the_man(triggerer):
	foll = len(game.party)
	pay = foll * 10000
	triggerer.money_adj(pay)
	return


