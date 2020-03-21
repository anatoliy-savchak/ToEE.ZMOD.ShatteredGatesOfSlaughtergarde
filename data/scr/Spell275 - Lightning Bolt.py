from toee import *

def OnBeginSpellCast( spell ):
	print "Lightning Bolt OnBeginSpellCast"
	print "spell.target_list=", spell.target_list
	print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
	game.particles( "sp-evocation-conjure", spell.caster )

def OnSpellEffect( spell ):
	print "Lightning Bolt OnSpellEffect"

	remove_list = []

	damage_dice = dice_new( '1d6' )
	damage_dice.number = min( 1 * spell.caster_level, 10 )

	game.particles( 'sp-Lightning Bolt', spell.target_loc )
	game.pfx_lightning_bolt( spell.caster, spell.target_loc, spell.target_loc_off_x, spell.target_loc_off_y, spell.target_loc_off_z )

	for target_item in spell.target_list:
		if target_item.obj.reflex_save_and_damage( spell.caster, spell.dc, D20_Save_Reduction_Half, D20STD_F_NONE, damage_dice, D20DT_ELECTRICITY, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id ) > 0:
			# saving throw successful
			target_item.obj.float_mesfile_line( 'mes\\spell.mes', 30001 )
		else:
			# saving throw unsuccessful
			target_item.obj.float_mesfile_line( 'mes\\spell.mes', 30002 )

		remove_list.append( target_item.obj )

	spell.target_list.remove_list( remove_list )
	spell.spell_end( spell.id )

def OnBeginRound( spell ):
	print "Lightning Bolt OnBeginRound"

def OnEndSpellCast( spell ):
	print "Lightning Bolt OnEndSpellCast"