from toee import *
from utilities import *

def san_dialog( attachee, triggerer ):
	randy1 = game.random_range(100,106)
	attachee.float_line(randy1,triggerer)
	return SKIP_DEFAULT

    
def san_first_heartbeat( attachee, triggerer ):
	return RUN_DEFAULT

def san_dying( attachee, triggerer ):
	return RUN_DEFAULT

def san_resurrect( attachee, triggerer ):
	return RUN_DEFAULT
