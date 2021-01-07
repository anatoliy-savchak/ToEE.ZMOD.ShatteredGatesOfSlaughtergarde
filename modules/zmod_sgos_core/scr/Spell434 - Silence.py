import toee, debug

def OnBeginSpellCast(spell):
	assert isinstance(spell, toee.PySpell)
	print("Silence OnBeginSpellCast")
	print("spell.target_list={}".format(spell.target_list))
	print("spell.caster={}, caster.level={}".format(spell.caster, spell.caster_level))
	toee.game.particles("sp-illusion-conjure", spell.caster )
	return

def	OnSpellEffect(spell):
	assert isinstance(spell, toee.PySpell)
	print("Silence OnSpellEffect")

	npc = spell.caster			##  added so NPC's can use wand/potion/scroll
	if (npc.type != toee.obj_t_pc and npc.leader_get() == toee.OBJ_HANDLE_NULL and spell.caster_level <= 0):
		spell.caster_level = 8

	spell.duration = 10 * spell.caster_level

	# test whether we targeted the ground or an object
	is_object = spell.is_object_selected()
	if (is_object and not len(spell.target_list)):
		print("is_object_selected returns 0 targets!")
		debug.breakp("")
		is_object = 0

	if (is_object):
		target_item = spell.target_list[0]
		# allow Will saving throw to negate
		if target_item.obj.saving_throw_spell(spell.dc, toee.D20_Save_Will, toee.D20STD_F_NONE, spell.caster, spell.id):
			# saving throw successful
			target_item.obj.float_mesfile_line( 'mes\\spell.mes', 30001 )

			toee.game.particles( 'Fizzle', target_item.obj )
			spell.target_list.remove_target( target_item.obj )
		else:
			# put sp-Silence condition on target
			target_item.obj.float_mesfile_line( 'mes\\spell.mes', 30002 )
			spell_obj_partsys_id = toee.game.particles( 'sp-Silence', target_item.obj )
			target_item.obj.condition_add_with_args( 'sp-Silence', spell.id, spell.duration, 0, spell_obj_partsys_id )

	else:
		# spawn one spell_object object
		spell_obj = toee.game.obj_create(toee.OBJECT_SPELL_GENERIC, spell.target_loc, spell.target_loc_off_x, spell.target_loc_off_y )

		# add to d20initiative
		caster_init_value = spell.caster.get_initiative()
		spell_obj.d20_status_init()
		spell_obj.set_initiative( caster_init_value )

		# put sp-Silence condition on obj
		spell_obj_partsys_id = toee.game.particles( 'sp-Silence', spell_obj )
		spell_obj.condition_add_with_args( 'sp-Silence', spell.id, spell.duration, 0, spell_obj_partsys_id )
	return

def OnBeginRound( spell ):
	print("Silence OnBeginRound")
	return

def OnEndSpellCast( spell ):
	print("Silence OnEndSpellCast")
	return

def OnAreaOfEffectHit( spell ):
	print("Silence OnAreaOfEffectHit")

def OnSpellStruck( spell ):
	print("Silence OnSpellStruck")