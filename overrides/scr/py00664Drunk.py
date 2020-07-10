from toee import *
from utilities import *

def san_dialog( attachee, triggerer ):
	randy1 = game.random_range(1,6)
	attachee.float_line(randy1,triggerer)
	return SKIP_DEFAULT
