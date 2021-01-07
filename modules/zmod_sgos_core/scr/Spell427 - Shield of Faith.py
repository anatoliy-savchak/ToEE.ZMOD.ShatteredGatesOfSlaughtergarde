from toee import *

def OnBeginSpellCast( spell ):
	print "Shield of Faith OnBeginSpellCast"
	print "spell.target_list=", spell.target_list
	print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
	#game.particles( "sp-abjuration-conjure", spell.caster )
	game.particles( "cast-Abjuration-cast", spell.caster )

def OnSpellEffect( spell ):
	print "Shield of Faith OnSpellEffect"

	bonus = 2 + min( 3, spell.caster_level / 6 )

	spell.duration = 10 * spell.caster_level
	target_item = spell.target_list[0]

	npc = spell.caster			##  added so NPC's can pre-buff
	if npc.type != obj_t_pc and npc.leader_get() == OBJ_HANDLE_NULL and not game.combat_is_active():
		spell.duration = 2000 * spell.caster_level

	if target_item.obj.is_friendly( spell.caster ):
		if (target_item.obj.type == obj_t_pc) or (target_item.obj.type == obj_t_npc):
			target_item.obj.condition_add_with_args( 'sp-Shield of Faith', spell.id, spell.duration, bonus )
			target_item.partsys_id = game.particles( 'sp-Shield of Faith', target_item.obj )

		else:
			target_item.obj.float_mesfile_line( 'mes\\spell.mes', 30000 )
			target_item.obj.float_mesfile_line( 'mes\\spell.mes', 31001 )
			game.particles( 'Fizzle', target_item.obj )
			spell.target_list.remove_target( target_item.obj )

	elif not target_item.obj.saving_throw_spell( spell.dc, D20_Save_Will, D20STD_F_NONE, spell.caster, spell.id ):
		# saving throw unsuccessful
		target_item.obj.float_mesfile_line( 'mes\\spell.mes', 30002 )
		target_item.obj.condition_add_with_args( 'sp-Shield of Faith', spell.id, spell.duration, bonus )
		target_item.partsys_id = game.particles( 'sp-Shield of Faith', target_item.obj )

	else:
		# saving throw successful
		target_item.obj.float_mesfile_line( 'mes\\spell.mes', 30001 )
		game.particles( 'Fizzle', target_item.obj )
		spell.target_list.remove_target( target_item.obj )

	spell.spell_end( spell.id )

def OnBeginRound( spell ):
	print "Shield of Faith OnBeginRound"

def OnEndSpellCast( spell ):
	print "Shield of Faith OnEndSpellCast"