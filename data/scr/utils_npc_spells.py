import utils_npc
import toee
import utils_spell

class NPCSpells(object):
	def __init__(self):
		self.spells = dict()
		return

	def add_spell(self, spell_num, spell_class_stat, spell_level, count = 1):
		rec = None
		if (spell_num in self.spells): 
			rec = self.spells[spell_num]
			rec.count += count
		else: 
			rec = NPCSpell(spell_num, spell_class_stat, spell_level, count)
			self.spells[spell_num] = rec
		return rec

	def get_spell_count(self, spell_num):
		if (spell_num in self.spells): 
			return self.spells[spell_num].count
		return 0

	def get_spell(self, spell_num):
		if (spell_num in self.spells): 
			return self.spells[spell_num]
		return None

	def prep_spell(self, npc, spell_num, decr = 1):
		if (spell_num in self.spells): 
			rec = self.spells[spell_num]
			if (not rec.count): return None
			rec.count -= decr
			if (not rec.ensured):
				utils_npc.npc_spell_ensure(npc, rec.spell_num, rec.spell_class_stat, rec.spell_level)
				rec.ensured = 1
			npc.spells_pending_to_memorized()
			class_name = "class_wizard"
			if (rec.spell_class_stat == toee.stat_level_cleric):
				class_name = "class_cleric"
			if (rec.spell_class_stat == toee.stat_level_bard):
				class_name = "class_bard"
			spell_code = "'{}' {} {}".format(utils_spell.spell_name_safe(rec.spell_num), class_name, rec.spell_level)
			return spell_code
		return None

	def memorize_all(self, npc):
		for spell_num in self.spells.iterkeys():
			rec = self.spells[spell_num]
			if (not rec.ensured):
				utils_npc.npc_spell_ensure(npc, rec.spell_num, rec.spell_class_stat, rec.spell_level)
				rec.ensured = 1
		npc.spells_pending_to_memorized()
		return

class NPCSpell(object):
	def __init__(self, spell_num, spell_class_stat, spell_level, count = 1):
		self.spell_num = spell_num
		self.count = count
		self.spell_class_stat = spell_class_stat
		self.spell_level = spell_level
		self.ensured = 0
		return

