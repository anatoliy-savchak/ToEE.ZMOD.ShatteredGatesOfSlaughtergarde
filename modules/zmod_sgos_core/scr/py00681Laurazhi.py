from toee import *
from utilities import *
from scripts import *
import utils_npc, shattered_consts, const_toee

def san_dialog( attachee, triggerer ):
	assert isinstance(attachee, PyObjHandle)
	attachee.turn_towards(triggerer)
	attachee.npc_flag_set(ONF_NO_ATTACK)
	attachee.critter_flag_unset(OCF_SURRENDERED)
	attachee.scripts[const_toee.sn_will_kos] = 681

	if not attachee.has_met( triggerer ):
		triggerer.begin_dialog( attachee, 1 )
		return SKIP_DEFAULT
	else:
		if game.global_flags[shattered_consts.GLOBAL_FLAG_LAURAZHI_CONSIDERING] == 1:
			triggerer.begin_dialog( attachee, 800 )
			return SKIP_DEFAULT
		elif game.global_flags[shattered_consts.GLOBAL_FLAG_WARCHIEF_KILLED] == 1:
			triggerer.begin_dialog( attachee, 650 )
			return SKIP_DEFAULT
		elif (attachee.leader_get() != OBJ_HANDLE_NULL):
			attachee.float_line( 750, triggerer )
			return SKIP_DEFAULT
		elif get_2(attachee):		## friendly, willing to talk
			triggerer.begin_dialog( attachee, 100 )
			return SKIP_DEFAULT
		else:					## indifferent or unfriendly, wants them to go away and die
			triggerer.begin_dialog( attachee, 600 )
			return SKIP_DEFAULT
	return SKIP_DEFAULT

def san_will_kos(attachee, triggerer):
	print("san_will_kos = 0: {}, {}".format(attachee, triggerer))
	return 0

def san_first_heartbeat( attachee, triggerer ):
	return RUN_DEFAULT

def san_dying( attachee, triggerer ):
	return RUN_DEFAULT

def san_resurrect( attachee, triggerer ):
	return RUN_DEFAULT

def san_spell_cast( attachee, triggerer, spell ):
	return RUN_DEFAULT

def just_floatin(attachee, triggerer):
	attachee.float_line( 30, triggerer )
	return

def succ_dipl(attachee, triggerer):
	ddc = get_ddc(attachee, triggerer)
	o = game.random_range(1,20)
	skill_modd = triggerer.skill_level_get(attachee, skill_diplomacy)
	p = o + skill_modd
	attachee.turn_towards(triggerer)
	if p >= (ddc + 10):    ## helpful
		npc_2(attachee)
		triggerer.begin_dialog( attachee, 500 )
		return
	elif p >= ddc:    ## friednly
		npc_2(attachee)
		triggerer.begin_dialog( attachee, 400 )
		return
	elif p <= (ddc-10):     ## unfriendly
		triggerer.begin_dialog( attachee, 200 )
		return
	else:
		triggerer.begin_dialog( attachee, 300 )
	return

def get_ddc(attachee, triggerer):
	dip_start = 0
	ddc = 0
	## are they a good cleric?
	if (triggerer.stat_level_get(stat_alignment) == CHAOTIC_GOOD or triggerer.stat_level_get(stat_alignment) == NEUTRAL_GOOD or triggerer.stat_level_get(stat_alignment) == LAWFUL_GOOD) and triggerer.stat_level_get(stat_level_cleric) >= 1:
		dip_start -= 2
	## are they a lawful cleric?
	if (triggerer.stat_level_get(stat_alignment) == LAWFUL_NEUTRAL or triggerer.stat_level_get(stat_alignment) == LAWFUL_EVIL or triggerer.stat_level_get(stat_alignment) == LAWFUL_GOOD) and triggerer.stat_level_get(stat_level_cleric) >= 1:
		dip_start -= 4
	## are they a paladin?
	if triggerer.stat_level_get(stat_level_paladin) >= 1:
		dip_start -= 6
	## are they wounded?
	if group_percent_hp( triggerer ) < 50:
		dip_start -= 2
	## negative impression modifier
	if get_1(attachee):
		dip_start -= 2
	## check for ark and sigil
	if anyone( triggerer.group_list(), "has_item", 12883):
		dip_start += 2
	if anyone( triggerer.group_list(), "has_item", 12881):
		dip_start += 4
	## standard DC to change attitude is 15
	ddc = (15 - dip_start)
	if ddc < 2:
		ddc = 2
	return ddc

def move_her(attachee):
	attachee.move(location_from_axis(423, 441))
	attachee.rotation = 4.8
	return

def ark(attachee, triggerer):
	party_transfer_to( attachee, 12883 )
	party_transfer_to( attachee, 12881 )
	ark = attachee.item_find(12883)
	sigil = attachee.item_find(12881)
	ark2 = game.obj_create(12883, location_from_axis(423, 441))
	if sigil != OBJ_HANDLE_NULL:
		sigil.destroy()
	if ark != OBJ_HANDLE_NULL:
		ark.destroy()
	if anyone( triggerer.group_list(), "has_item", 12882):
		party_transfer_to( attachee, 12882 )
	return

def final_run(attachee, triggerer):
	triggerer.follower_remove(attachee)
	attachee.float_line(715,triggerer)
	attachee.critter_flag_set(OCF_MUTE)
	game.timevent_add(run_off, (attachee, triggerer), 1000 )
	game.timevent_add(destroy_it_all, (), 4000)
	game.global_flags[20] == 1
	return

def run_off( attachee, triggerer ):
	attachee.runoff(location_from_axis(423, 435))
	return RUN_DEFAULT


def find_gnrc_near( obj, name ):
	for gnrc in game.obj_list_vicinity( obj.location, OLC_GENERIC ):
		if (gnrc.name == name):
			return gnrc
	return OBJ_HANDLE_NULL
	
def do_the_ark(triggerer):
	a = 0
	for pc in triggerer.group_list():
		ark = pc.item_find( 12883 )
		if ark != OBJ_HANDLE_NULL:
			ark.destroy()
			a = 1
	if a == 0:
		ark2 = find_gnrc_near( triggerer, 12883 )
		ark2.move(location_from_axis(423, 441))
	else:
		ark2 = game.obj_create(12883, location_from_axis(423, 441))
	ark2.rotation = 5.5
	return
	
def do_the_sigil(triggerer):
	b = 0
	for pc in triggerer.group_list():
		sigil = pc.item_find( 12881 )
		if sigil != OBJ_HANDLE_NULL:
			sigil.destroy()
			b = 1
	if b == 0:
		sigil2 = find_gnrc_near( triggerer, 12881 )
		sigil2.destroy()
	return
	
def light_up_ark(triggerer):
	ark = find_gnrc_near( triggerer, 12883 )
	if (ark):
		game.particles( 'sp-Detect Secret Doors', ark )
	
def light_up_sigils(triggerer):
	for gnrc in game.obj_list_vicinity( triggerer.location, OLC_GENERIC ):
		if (gnrc.name == 12880):
			game.particles( 'sp-Detect Undead 3 High', gnrc )
	return
	
def destroy_it_all():
	game.global_flags[20] = 1
	for gnrc in game.obj_list_vicinity( location_from_axis(423, 433), OLC_GENERIC ):
		if (gnrc.name == 12880):
			game.particles( 'sp-Disrupt Undead-hit', gnrc )
			game.timevent_add(gnrc.destroy, (), 2000 )
	for ark in game.obj_list_vicinity( location_from_axis(423, 441), OLC_GENERIC ):
		if (ark.name == 12883):
			game.particles( 'Orb-Summon-Balor', ark )
			game.timevent_add(ark.destroy, (), 2000 )
	for gate in game.obj_list_vicinity( location_from_axis(423, 433), OLC_SCENERY ):
		if (gate.name == 2006):
			game.particles( 'sp-Fireball-Hit', gate )
			game.timevent_add(gate.destroy, (), 2000 )
	return

def go_gate(npc):
	assert isinstance(npc, PyObjHandle)
	npc.standpoint_set(STANDPOINT_DAY, 887)
	npc.standpoint_set(STANDPOINT_NIGHT, 887)
	#npc.move(location_from_axis(450, 443))
	#npc.faction_add(1)
	for obj in game.obj_list_vicinity(location_from_axis(422, 444), OLC_NPC):
		print("clearing obj_f_npc_combat_focus for: {}".format(obj))
		obj.obj_set_obj(obj_f_npc_combat_focus, OBJ_HANDLE_NULL)
	return