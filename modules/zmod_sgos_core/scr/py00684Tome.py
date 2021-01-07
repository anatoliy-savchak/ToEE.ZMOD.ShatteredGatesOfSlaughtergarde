from toee import *
from utilities import *

def san_use( attachee, triggerer ):
	loc = triggerer.location
	npc = game.obj_create( 14413, loc )
	if triggerer.stat_level_get(stat_level_barbarian) >= 1:
		npc.float_line( 200, triggerer )
		game.timevent_add(npc.destroy, (), 3000 )
		return SKIP_DEFAULT
	elif (anyone( triggerer.group_list(), "has_item", 12883) or find_gnrc_near( triggerer, 12883 )) and (anyone( triggerer.group_list(), "has_item", 12881) or find_gnrc_near( triggerer, 12881 )):
		triggerer.begin_dialog(npc,400)
		return SKIP_DEFAULT
	else:
		triggerer.begin_dialog(npc,300)
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
	ark2.rotation = 4.8
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
	ark.partsys_id = game.particles( 'sp-Detect Secret Doors', ark.obj )
	
def light_up_sigils(triggerer):
	for gnrc in game.obj_list_vicinity( triggerer.location, OLC_GENERIC ):
		if (gnrc.name == 12880):
			gnrc.partsys_id = game.particles( 'ef-Globe_green', gnrc.obj )
	return
	
