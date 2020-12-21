from toee import *
from utilities import *

def san_use( attachee, triggerer ):
	if game.quests[1].state != qs_unknown:
		game.fade_and_teleport( 0,0,0,5121,518,454 )
	else:
		attachee.float_mesfile_line( 'mes\\narrative.mes', 1080 )
	return SKIP_DEFAULT