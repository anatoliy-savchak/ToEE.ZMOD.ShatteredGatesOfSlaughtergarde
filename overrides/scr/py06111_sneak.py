from toee import *
from debugg import breakp
from utils_sneak import *

def san_start_combat(attachee, triggerer):
	#breakp("sneak san_start_combat")
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)

	#check = perform_sneak_for_attack(attachee, game.party[0])
	#breakp("sneak check={}".format(check))

	# todo better ai, currently its just cheat
	attachee.anim_goal_interrupt()
	attachee.critter_flag_set(OCF_MOVING_SILENTLY)

	is_ranged = False
	orig_strat = attachee.obj_get_int(obj_f_critter_strategy)
	if (orig_strat>=8 and orig_strat <= 12): is_ranged = True
	if (is_ranged): return RUN_DEFAULT

	strat = ["sneaker - tripper" \
		  , "clear target", "", "" \
		  , "target closest", "", "" \
		  #, "flank", "", "" \
		  , "trip", "", "" \
		  , "attack", "", "" \
		  ]

	strat.set_strategy(attachee)
	return RUN_DEFAULT

def san_end_combat(attachee, triggerer):
	attachee.critter_flag_unset(OCF_MOVING_SILENTLY)
	attachee.anim_goal_interrupt()
	return RUN_DEFAULT

