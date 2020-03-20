class TacticsHelper(object):
	def __init__(self, name_prefix):
		self.name_prefix = name_prefix
		self.custom_tactics = [self.name_prefix]
		self.count = 0
		return

	def add_triplet(self, tac_name, spell_spec):
		self.custom_tactics.append(tac_name)
		self.custom_tactics.append("")
		self.custom_tactics.append(spell_spec)
		self.count += 1
		return

	def add_simple(self, tac_name):
		self.custom_tactics.append(tac_name)
		self.custom_tactics.append("")
		self.custom_tactics.append("")
		self.count += 1
		return

	def add_spell(self, tac_name, spell_name, class_name, class_level):
		spell_code = "'{}' {} {}".format(spell_name, class_name, class_level)
		self.add_triplet(tac_name, spell_code)
		return

	def add_target_self(self):
		self.add_simple("target self")
		return

	def add_target_closest(self):
		self.add_simple("target closest")
		return

	def add_target_prone(self):
		self.custom_tactics.append("target prone")
		self.custom_tactics.append("")
		self.custom_tactics.append("")
		self.count += 1
		return

	def add_cast_single(self, spell_name, class_name, class_level):
		self.add_spell("cast single", spell_name, class_name, class_level)
		return

	def add_five_foot_step(self):
		self.add_simple("five foot step")
		return

	def add_attack(self):
		self.add_simple("attack")
		return

	def make_name(self):
		name = self.name_prefix
		for i in range(1, self.count):
			name = name + "-" + self.custom_tactics[i*3+1]
			if (self.custom_tactics[i*3+1+2]):
				name = name + "(" + self.custom_tactics[i*3+1+2] + ")"
		self.custom_tactics[0] = name
		return
