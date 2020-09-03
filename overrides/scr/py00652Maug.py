from toee import *
from utilities import *
from scripts import *

def san_dialog( attachee, triggerer ):
	if not attachee.has_met( triggerer ):
		triggerer.begin_dialog( attachee, 1 )
		return SKIP_DEFAULT
	else:
		if game.quests[4].state == qs_completed:
			triggerer.begin_dialog( attachee, 300 )
			return SKIP_DEFAULT
		elif game.quests[4].state == qs_accepted:
			triggerer.begin_dialog( attachee, 150 )
			return SKIP_DEFAULT
		else:
			maug_dipl(attachee, triggerer)
			return SKIP_DEFAULT
	return SKIP_DEFAULT

def san_first_heartbeat( attachee, triggerer ):
	return RUN_DEFAULT

def san_dying( attachee, triggerer ):
	if game.quests[4].state != qs_completed:
		create_item_in_inventory(6141,attachee)
	return RUN_DEFAULT

def san_resurrect( attachee, triggerer ):
	return RUN_DEFAULT

def san_spell_cast( attachee, triggerer, spell ):
	if ( spell.spell == spell_detect_evil ):
		game.global_flags[2] = 1
	if ( spell.spell == spell_detect_magic ):
		game.global_flags[15] = 1
	return RUN_DEFAULT

def set_KOS_flag1(attachee):
	game.timevent_add(set_KOS_flag2, (attachee), 10000 )
	return

def set_KOS_flag2(attachee):
	attachee.npc_flag_set( ONF_KOS )
	return

def just_floatin(attachee, triggerer):
	attachee.float_line( 30, triggerer )
	return

def maug_dipl(attachee, triggerer):
	ddc = get_ddc(attachee, triggerer)
	o = game.random_range(1,20)
	if (o < 10): o = 10 # take 10
	skill_modd = triggerer.skill_level_get(attachee, skill_diplomacy)
	p = o + skill_modd
	if p >= ddc:    ## friednly
		attachee.turn_towards(triggerer)
		if not attachee.has_met( triggerer ):
			triggerer.begin_dialog( attachee, 40 )
			return
		else:
			triggerer.begin_dialog( attachee, 40 )
			return
	elif p <= (ddc-10):     ## unfriendly
		triggerer.begin_dialog( attachee, 10 )
		return
	else:       ## indifferent
		if not attachee.has_met( triggerer ):
			triggerer.begin_dialog( attachee, 1 )
			return
		else:
			triggerer.begin_dialog( attachee, 220 )
	return

def get_ddc(attachee, triggerer):
	dip_start = 0
	ddc = 0
	## are they a chaotic cleric?
	if (triggerer.stat_level_get(stat_alignment) == CHAOTIC_NEUTRAL or triggerer.stat_level_get(stat_alignment) == NEUTRAL_EVIL or triggerer.stat_level_get(stat_alignment) == CHAOTIC_EVIL) and triggerer.stat_level_get(stat_level_cleric) >= 1:
		dip_start -= 4
	## are they a lawful cleric?
	if (triggerer.stat_level_get(stat_alignment) == LAWFUL_NEUTRAL or triggerer.stat_level_get(stat_alignment) == NEUTRAL_GOOD or triggerer.stat_level_get(stat_alignment) == LAWFUL_GOOD) and triggerer.stat_level_get(stat_level_cleric) >= 1:
		dip_start += 2
	## are they a paladin?
	if triggerer.stat_level_get(stat_level_paladin) >= 1:
		dip_start += 2
	## have they Detected Magic on the circles?
	if game.global_flags[15] == 1:
		dip_start += 4
	## have they killed the howler?
	if game.global_flags[103] == 1:
		dip_start += 8
	## for returning scenarios, npc_1 and npc_2 indicate Maug was antagonised
	if get_1(attachee):
		dip_start -= 2
	if get_2(attachee):
		dip_start -= 4
	## standard DC to change attitude is 15
	ddc = (15 - dip_start)
	if ddc < 2:
		ddc = 2
	return ddc

def det_mag(attachee, triggerer):
	party_transfer_to( attachee, 6334 )
	scroll = attachee.item_find(6334)
	if scroll != OBJ_HANDLE_NULL:
		scroll.destroy()
	game.particles( 'sp-Detect Magic', attachee )
	game.global_flags[15] = 1
	return