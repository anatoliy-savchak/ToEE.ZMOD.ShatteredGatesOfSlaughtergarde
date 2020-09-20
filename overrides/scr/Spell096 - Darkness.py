import toee

spell_radius = 20

def OnBeginSpellCast( spell ):
	print("Darkness OnBeginSpellCast")
	print("spell.target_list={}".format(spell.target_list))
	print("spell.caster={}  caster.level= {}".format(spell.caster, spell.caster_level))
	toee.game.particles( "sp-conjuration-conjure", spell.caster)
	return

def	OnSpellEffect( spell ):
	print("Darkness OnSpellEffect")

	spell.duration = 10*60 * spell.caster_level
	radius = spell_radius

	# spawn one spell_object object
	spell_obj = toee.game.obj_create(toee.OBJECT_SPELL_GENERIC, spell.target_loc)

	# add to d20initiative
	caster_init_value = spell.caster.get_initiative()
	spell_obj.d20_status_init()
	spell_obj.set_initiative( caster_init_value )

	# put sp-Solid Fog condition on obj
	spell_obj.condition_add_with_args("sp-Darkness", spell.id, spell.duration, 0, radius)
	return

def OnBeginRound( spell ):
	print("Darkness OnBeginRound")
	#assert isinstance(spell, toee.PySpell)
	#if (not toee.game.combat_turn):
	#	print("enforcing spell end {}".format(spell.id))
	#	#spell.spell_end(spell.id, 1)
	return

def OnEndSpellCast( spell ):
	print("Darkness OnEndSpellCast")
	return

def OnAreaOfEffectHit( spell ):
	print("Darkness OnAreaOfEffectHit")
	return

def OnSpellStruck( spell ):
	print("Darkness OnSpellStruck")
	return
