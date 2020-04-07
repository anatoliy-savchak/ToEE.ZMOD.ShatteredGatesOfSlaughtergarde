from toee import *
from debugg import *
from const_toee import *
import char_editor

def caster_class2caster_stat_level(caster_class):
	if (caster_class == stat_level_sorcerer): return stat_caster_level_sorcerer
	if (caster_class == stat_level_bard): return stat_caster_level_bard
	return stat_caster_level

def get_caster_class_level(caster_class, level):
	if (caster_class == stat_level_sorcerer): 
		if (level == 1): return 1
		else: return level * 2
	if (caster_class == stat_level_bard): 
		if (level < 3): return level * 2
		else: return 1 + level * 3
	return 100

def spell_get_name(spellStore):
	s = str(spellStore).split("(")[0]
	print(s)
	return s[13:-1]

def san_insert_item(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)

	if (not (attachee.item_flags_get() & OIF_NO_RANGED_USE)):
		lastDenyMessage = ""
		for idx in range(0, 19):
			spell = attachee.obj_get_spell(obj_f_item_spell_idx, idx)
			if (spell.spell_enum == 0): break
			#print(spell)
			spellName = spell_get_name(spell)
			#print(spellName)
			#print(spell.spell_enum)
			#breakp("san_insert_item 0")
			spi = char_editor.KnownSpellInfo()
			spi.spell_enum = spell.spell_enum
			spi.spell_status = 1
			spi.spell_class = spell.spell_class
			spi.spell_level = spell.spell_level
			caster_class = spi.get_casting_class()
			#print(spi)
			#print(caster_class)
			#caster_stat = caster_class2caster_stat_level(caster_class)
			#print(caster_stat)
			#breakp("san_insert_item 1")
			current_level = triggerer.stat_level_get(caster_class)
			need_level_caster = get_caster_class_level(caster_class, spell.spell_level)
			#print("triggerer.stat_level_get(caster_class: {}): {}".format(caster_class, current_level))
			#print("need level: {}".format(need_level_caster))
			#breakp("san_insert_item 2")
			if (spell.spell_level > current_level):
				lastDenyMessage = "Spell {} cannot be added, as target requires spell level {} of {} but has {}!".format(spellName, need_level_caster, caster_class, current_level)
				print(lastDenyMessage)
				break
			lastDenyMessage = ""
			if (not triggerer.is_spell_known(spell.spell_enum)):
				triggerer.spell_known_add(spell.spell_enum, spell.spell_class, spell.spell_level)
				triggerer.float_text_line("Added new spell {}!".format(spellName), Green)
				attachee.item_flag_set(OIF_NO_RANGED_USE)
			else: triggerer.float_text_line("Spell {} already known!".format(spellName), Yellow)
			break

	if (lastDenyMessage != ""):
		triggerer.float_text_line(lastDenyMessage, Red)
		game.create_history_freeform(lastDenyMessage)
	return RUN_DEFAULT

def san_remove_item(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)

	if (attachee.item_flags_get() & OIF_NO_RANGED_USE):
		spell = attachee.obj_get_spell(obj_f_item_spell_idx, 0)
		if (spell.spell_enum > 0):
			# you cannot remove it... 10075BC0                 ; void __cdecl SpellKnownRemove
			#triggerer.spell_known_add(spell.spell_enum, spell.spell_class, spell.spell_level)
			attachee.item_flag_unset(OIF_NO_RANGED_USE)
	return RUN_DEFAULT
