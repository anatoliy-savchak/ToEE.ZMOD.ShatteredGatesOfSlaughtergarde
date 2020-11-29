from toee import *
from utilities import *
from scripts import *

def san_use( attachee, triggerer ):
	loc = triggerer.location
	npc = game.obj_create( 14413, loc )
	if triggerer.stat_level_get(stat_level_barbarian) >= 1:
		npc.float_line( 200, triggerer )
		game.timevent_add(npc.destroy, (), 3000 )
		return SKIP_DEFAULT
	else:
		triggerer.begin_dialog(npc,1)
	return SKIP_DEFAULT

def san_dialog( attachee, triggerer ):
	triggerer.begin_dialog(attachee,1)
	return SKIP_DEFAULT

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