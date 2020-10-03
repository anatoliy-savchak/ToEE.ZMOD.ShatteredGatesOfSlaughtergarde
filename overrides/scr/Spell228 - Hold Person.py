import toee, sys, traceback

def OnBeginSpellCast(spell):
	assert isinstance(spell, toee.PySpell)
	print "Hold Person:: OnBeginSpellCast(spell.caster: {}, caster.level: {}, target_list: {}, )".format(spell.caster, spell.caster_level, spell.target_list)
	toee.game.particles( "sp-conjuration-conjure", spell.caster )
	return

def OnSpellEffect(spell):
	assert isinstance(spell, toee.PySpell)
	print "Hold Person:: OnSpellEffect(spell.caster: {}, caster.level: {}, target_list: {}, )".format(spell.caster, spell.caster_level, spell.target_list)
	try:
		spell.duration = 1 * spell.caster_level
		target = spell.target_list[0]

		if (target.obj.is_category_type(toee.mc_type_humanoid)):
			# allow Will saving throw to negate
			if (target.obj.saving_throw_spell(spell.dc, toee.D20_Save_Will, toee.D20STD_F_NONE, spell.caster, spell.id)):
				# saving throw successful
				target.obj.float_mesfile_line( 'mes\\spell.mes', 30001 )

				toee.game.particles( 'Fizzle', target.obj )
				spell.target_list.remove_target( target.obj )
			else:
				# saving throw unsuccessful
				target.obj.float_mesfile_line( 'mes\\spell.mes', 30002 )

				# HTN - apply condition HOLD (paralyzed)
				target.obj.condition_add_with_args( 'sp-Hold Person', spell.id, spell.duration, 0 )
				target.partsys_id = toee.game.particles( 'sp-Hold Person', target.obj )
		else:
			# not a person
			target.obj.float_mesfile_line( 'mes\\spell.mes', 30000 )
			target.obj.float_mesfile_line( 'mes\\spell.mes', 31004 )

			toee.game.particles( 'Fizzle', target.obj )
			spell.target_list.remove_target( target.obj )

	except Exception, e:
		print "Hold Person OnSpellEffect error:", sys.exc_info()[0]
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
	finally:
		spell.spell_end(spell.id)
	return

def OnBeginRound( spell ):
	print "Hold Person OnBeginRound"

def OnEndSpellCast( spell ):
	print "Hold Person OnEndSpellCast"

