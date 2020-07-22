from toee import *
from utilities import *
from Co8 import *
from combat_standard_routines import *
import startup_zmod

def san_dialog( attachee, triggerer ):
	get_Co8_options_from_ini()
	if (game.global_flags[601] == 1):
		triggerer.begin_dialog( attachee, 20 )
	else:
		triggerer.begin_dialog( attachee, 1 )
	return SKIP_DEFAULT


def san_start_combat( attachee, triggerer ):
	leader = game.party[0]
	StopCombat(attachee, 0)
	leader.begin_dialog( attachee, 4000 )
	return RUN_DEFAULT


def intro_movie_setup( attachee, triggerer ):
	set_intro_slides()
	return


def set_intro_slides():
	game.moviequeue_add(428)
	game.moviequeue_add(420)
	game.moviequeue_add(421)
	game.moviequeue_add(422)
	game.moviequeue_add(423)
	game.moviequeue_add(424)
	game.moviequeue_add(425)
	game.moviequeue_add(426)
	game.moviequeue_add(427)
	game.moviequeue_add(429)
	if (game.party_alignment == LAWFUL_GOOD):
		game.moviequeue_add(1000)
	if (game.party_alignment == NEUTRAL_GOOD):
		game.moviequeue_add(1005)
	if (game.party_alignment == CHAOTIC_GOOD):
		game.moviequeue_add(1001)
	if (game.party_alignment == LAWFUL_NEUTRAL):
		game.moviequeue_add(1007)
	if (game.party_alignment == TRUE_NEUTRAL):
		game.moviequeue_add(1004)
	if (game.party_alignment == CHAOTIC_NEUTRAL):
		game.moviequeue_add(1008)
	if (game.party_alignment == LAWFUL_EVIL):
		game.moviequeue_add(1002)
	if (game.party_alignment == NEUTRAL_EVIL):
		game.moviequeue_add(1006)
	if (game.party_alignment == CHAOTIC_EVIL):
		game.moviequeue_add(1003)
	game.moviequeue_play()
	return RUN_DEFAULT

def zmod_startup():
	startup_zmod.zmod_conditions_apply_pc()
	return