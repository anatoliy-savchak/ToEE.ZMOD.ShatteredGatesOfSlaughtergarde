import toee, sys

def OnBeginSpellCast(spell):
	assert isinstance(spell, toee.PySpell)
	print "Harm OnBeginSpellCast"
	print "spell.target_list=", spell.target_list
	print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
	toee.game.particles("sp-necromancy-conjure", spell.caster)
	return

def	OnSpellEffect(spell):
	print "Harm OnSpellEffect"
	assert isinstance(spell, toee.PySpell)
	try:
		target = spell.target_list[0]
		toee.game.particles('sp-Harm', target.obj)

		attack_result = spell.caster.perform_touch_attack(target.obj, 1)
		if (attack_result & toee.D20CAF_HIT):
			# check if target is undead
			if not target.obj.is_category_type(toee.mc_type_undead):
				# Saving throw is performed on sp-Harm condition level
				# Harm target
				target.obj.condition_add_with_args('sp-Harm', spell.id, spell.duration, 0)
			else:
				# Heal undead
				target.obj.condition_add_with_args('sp-Heal', spell.id, spell.duration, 0)

		spell.target_list.remove_target(target)
	except Exception, e:
		print "Harm OnSpellEffect error:", sys.exc_info()[0]
		print(str(e))
	finally:
		spell.spell_end(spell.id, 1)
	return

def OnBeginRound(spell):
	print "Harm OnBeginRound"
	return

def OnEndSpellCast(spell):
	print "Harm OnEndSpellCast"
	return
