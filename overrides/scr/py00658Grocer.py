from toee import *
from utilities import *

def san_dialog( attachee, triggerer ):
	randy1 = game.random_range(100,107)
	attachee.float_line(randy1,triggerer)
	return SKIP_DEFAULT

def san_dying( attachee, triggerer ):
	return RUN_DEFAULT

def san_heartbeat( attachee, triggerer ):
	randy2 = game.random_range(1,65)
	if randy2 < 9:
		attachee.float_line(randy2,triggerer)
		randy1 = 0
        	return RUN_DEFAULT
	if randy2 > 61:
		randy2 -= 60
		attachee.rotation = randy2
	return RUN_DEFAULT

def san_resurrect( attachee, triggerer ):
	return RUN_DEFAULT