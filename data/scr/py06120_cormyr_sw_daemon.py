from toee import *
from debugg import *
from utils_obj import *
from const_toee import *

# DAEMON
def cormyr_sw_san_new_map( attachee, triggerer ):
	return SKIP_DEFAULT


def cormyr_sw_init():
	do_hook_doors()
	return

def do_hook_doors():
	#breakp("do_hook_doors")
	for obj in game.obj_list_range(game.party[0].location, 200, OLC_PORTAL ):
		assert isinstance(obj, PyObjHandle)
		obj_scripts_clear(obj)
		obj.scripts[sn_use] = 6112
	return SKIP_DEFAULT
