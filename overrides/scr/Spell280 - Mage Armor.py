import toee

def OnBeginSpellCast(spell):
	assert isinstance(spell, toee.PySpell)
	print "Mage Armor:: OnBeginSpellCast(spell.caster: {}, caster.level: {}, target_list: {}, )".format(spell.caster, spell.caster_level, spell.target_list)
	toee.game.particles( "sp-conjuration-conjure", spell.caster )
	return

def OnSpellEffect(spell):
	assert isinstance(spell, toee.PySpell)
	print "Mage Armor:: OnSpellEffect(spell.caster: {}, caster.level: {}, target_list: {}, )".format(spell.caster, spell.caster_level, spell.target_list)
	armor_bonus = 4
	spell.duration = 600 * spell.caster_level

	target = spell.target_list[0]
	npc = target.obj

	# check if target is friendly (willing target)
	if (npc == spell.caster or npc.is_friendly(spell.caster)):
			# HTN - WIP! this needs to be changed to a 'force_armor_bonus' that doesn't stack 
			# 	with 'armor_bonus' (in addition, we need to allow non-corporeal monsters 
			#	to pass thru squares occupied by people without 'force_armor')
			npc.condition_add_with_args('sp-Mage Armor', spell.id, spell.duration, armor_bonus)
			
			#A: disable it for yourself. annoying
			if (npc != spell.caster):
				target.partsys_id = toee.game.particles( 'sp-Mage Armor', npc)
	else:
		# allow Will saving throw to negate
		if npc.saving_throw_spell(spell.dc, toee.D20_Save_Will, toee.D20STD_F_NONE, spell.caster, spell.id ):
			# saving throw successful
			npc.float_mesfile_line('mes\\spell.mes', 30001 )

			toee.game.particles('Fizzle', npc)
			spell.target_list.remove_target(npc)
		else:
			# saving throw unsuccessful
			npc.float_mesfile_line('mes\\spell.mes', 30002)

			# HTN - WIP! this needs to be changed to a 'force_armor_bonus' that doesn't stack 
			# 	with 'armor_bonus' (in addition, we need to allow non-corporeal monsters 
			#	to pass thru squares occupied by people without 'force_armor')
			npc.condition_add_with_args( 'sp-Mage Armor', spell.id, spell.duration, armor_bonus )
			target.partsys_id = game.particles('sp-Mage Armor', npc)

	spell.spell_end(spell.id)
	return

def OnBeginRound(spell):
	assert isinstance(spell, toee.PySpell)
	#print "Mage Armor OnBeginRound"
	return

def OnEndSpellCast(spell):
	assert isinstance(spell, toee.PySpell)
	#print "Mage Armor OnEndSpellCast"
	return
