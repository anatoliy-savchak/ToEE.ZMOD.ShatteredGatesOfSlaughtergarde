from toee import *
from utilities import *

def san_use( attachee, triggerer ):
	if game.quests[2].state != qs_unknown or game.quests[3].state != qs_unknown:
		game.fade_and_teleport( 0,0,0,5123,486,475 )
	else:
		attachee.float_mesfile_line( 'mes\\narrative.mes', 1081 )
	return SKIP_DEFAULT