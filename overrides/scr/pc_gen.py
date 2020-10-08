import toee, char_editor

class PCGen:
	def __init__(self):
		self.abilities = dict() # {str: 12}
		self.class_levels = list() # [(stat_level_bard, 2)]
		self.feats = list() # [feat_power_attack]
		return

	def set_abilities(self, str_, dex, con, int_, wis, cha):
		self.abilities["str"] = str_
		self.abilities["dex"] = dex
		self.abilities["con"] = con
		self.abilities["int"] = int_
		self.abilities["wis"] = wis
		self.abilities["cha"] = cha
		return

	def _apply_ability(self, pc, stat, stat_str):
		assert isinstance(pc, toee.PyObjHandle)
		assert isinstance(stat, int)
		assert isinstance(stat_str, str)
		val = self.abilities.get(stat_str)
		if (not val): return

		oldval = pc.stat_base_get(stat)
		if (val != oldval):
			print("{}: {} -> {}".format(stat_str, oldval, val))
			#pc.obj_set_idx_int(toee.obj_f_critter_abilities_idx, index, pc_class)
			pc.stat_base_set(stat, val)
		return

	def _apply_classes(self, pc):
		assert isinstance(pc, toee.PyObjHandle)

		if (not self.class_levels): return
		index = -1
		for t in self.class_levels:
			pc_class = t[0]
			pc_class_levels = t[1]
			pc.make_class(pc_class, pc_class_levels)
			index += pc_class_levels

			if (pc.highest_arcane_caster_level or pc.highest_divine_caster_level):
				maxSpellLvl = char_editor.get_max_spell_level(pc, pc_class, pc_class_levels)
				if (maxSpellLvl):
					class_spells = char_editor.get_learnable_spells(pc, pc_class, maxSpellLvl)
					char_editor.spell_known_add2(class_spells, pc)
				domain_1 = pc.obj_get_int(toee.obj_f_critter_domain_1)
				domain_2 = pc.obj_get_int(toee.obj_f_critter_domain_2)
				domain_1_spells = char_editor.get_learnable_spells(pc, domain_1, maxSpellLvl, 1)
				domain_2_spells = char_editor.get_learnable_spells(pc, domain_2, maxSpellLvl, 1)
				char_editor.spell_known_add2(domain_1_spells, pc)
				char_editor.spell_known_add2(domain_2_spells, pc)
			break
			for i in range(0, pc_class_levels):
				index += 1
				print("{}: {}".format(index, pc_class))
				pc.obj_set_idx_int(toee.obj_f_critter_level_idx, index, pc_class)

		pc.obj_set_int(toee.obj_f_hp_pts, -65535)
		hp = pc.stat_level_get(toee.stat_hp_current)

		xp = 0
		if (index == 1-1): xp = 0
		elif (index == 2-1): xp = 1000
		elif (index == 3-1): xp = 3000
		elif (index == 4-1): xp = 6000
		elif (index == 5-1): xp = 10000
		elif (index == 6-1): xp = 15000
		elif (index == 7-1): xp = 21000
		elif (index == 8-1): xp = 28000
		elif (index == 9-1): xp = 36000
		elif (index == 10-1): xp = 45000
		elif (index == 11-1): xp = 55000
		elif (index == 12-1): xp = 66000

		pc.obj_set_int(toee.obj_f_critter_experience, xp)
		return

	def _apply_feats(self, pc):
		assert isinstance(pc, toee.PyObjHandle)

		if (self.feats):
			for feat_index in range(0, len(self.feats)):
				rebuild = (feat_index == len(self.feats)-1)
				pc.feat_add(self.feats[feat_index], rebuild)
		return

	def apply_pc(self, pc):
		assert isinstance(pc, toee.PyObjHandle)

		self._apply_ability(pc, toee.stat_strength, "str")
		self._apply_ability(pc, toee.stat_dexterity, "dex")
		self._apply_ability(pc, toee.stat_constitution, "con")
		self._apply_ability(pc, toee.stat_intelligence, "int")
		self._apply_ability(pc, toee.stat_wisdom, "wis")
		self._apply_ability(pc, toee.stat_charisma, "cha")

		self._apply_classes(pc)
		self._apply_feats(pc)
		return
