from toee import *
from debugg import *

def san_new_map( attachee, triggerer ):
	#breakp("py06101_daemon_pc::san_new_map")
	if (attachee.map == 5195): #CORMYR_LOST_REFUGE
		from py06110_daemon_cormyr_lor import cormyr_lor_san_new_map
		return cormyr_lor_san_new_map(attachee, triggerer)
	if (attachee.map == 5196): #CORMYR_LOST_REFUGE
		from py06120_cormyr_sw_daemon import cormyr_sw_init
		return cormyr_sw_init()
	return SKIP_DEFAULT