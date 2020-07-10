from toee import *
from utilities import *
import debug

diseases = 0,0,1,4,5,7,8,9
def OnBeginSpellCast( spell ):
	print "Contagion OnBeginSpellCast"
	print "spell.target_list=", spell.target_list
	print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
	game.particles( "sp-necromancy-conjure", spell.caster )

def OnSpellEffect( spell ):
	print "Contagion OnSpellEffect"

	spell.duration = 0
	target_item = spell.target_list[0]

	npc = spell.caster

	disease_index = spell.spell_get_menu_arg( RADIAL_MENU_PARAM_MIN_SETTING )
	## Solves Radial menu problem for Wands/NPCs
	#debug.breakp("disease_index")
	if disease_index != 1 and disease_index != 2 and disease_index != 3 and disease_index != 4 and disease_index != 5 and disease_index != 6 and disease_index != 7:
		#debug.breakp("disease query")
		disease_index = npc.d20_query("Contagion Desease Preference")
		print("disease_index: {}".format(disease_index))
		#debug.breakp("disease query2")
		if (not disease_index):
			disease_index = game.random_range(1,7)

	if ((target_item.obj.stat_level_get(stat_level_paladin) >= 3) and (target_item.obj.d20_query(Q_IsFallenPaladin) == 0)) or target_item.obj.is_category_type( mc_type_construct ) or target_item.obj.is_category_type( mc_type_undead ):
		target_item.obj.float_mesfile_line( 'mes\\spell.mes', 32000 )
		game.particles( 'Fizzle', target_item.obj )

	elif not target_item.obj.saving_throw_spell( spell.dc, D20_Save_Fortitude, D20STD_F_NONE, spell.caster, spell.id ):
		# saving throw unsuccesful
		target_item.obj.float_mesfile_line( 'mes\\spell.mes', 30002 )
		#target_item.obj.condition_add_with_args( 'sp-Contagion', spell.id, spell.duration, disease_index )
		#target_item.obj.condition_add_with_args( 'NSDiseased', 1, disease_index - 1, 0 )
		target_item.obj.condition_add_with_args( 'Incubating_Disease', 1, diseases[disease_index], 0 )
		target_item.partsys_id = game.particles( 'ef-MinoCloud', target_item.obj )

	else:
		# saving throw successful
		target_item.obj.float_mesfile_line( 'mes\\spell.mes', 30001 )
		game.particles( 'Fizzle', target_item.obj )

	spell.target_list.remove_target( target_item.obj )
	spell.spell_end( spell.id )

def OnBeginRound( spell ):
	print "Contagion OnBeginRound"

def OnEndSpellCast( spell ):
	print "Contagion OnEndSpellCast"