class TacticsHelper(object):
	def __init__(self, name_prefix):
		self.name_prefix = name_prefix
		self.custom_tactics = [self.name_prefix]
		self.count = 0
		return

	def add_tuple(self, tac_name, spell_spec):
		self.custom_tactics.append(tac_name)
		self.custom_tactics.append("")
		self.custom_tactics.append(spell_spec)
		self.count += 1
		return

	def add_triplet(self, tac_name, middle, spell_spec):
		self.custom_tactics.append(tac_name)
		self.custom_tactics.append(middle)
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
		self.add_tuple(tac_name, spell_code)
		return

	def add_approach(self):
		""" If target is set, then will try to approach to it, otherwise fail 0. AiApproach. """
		self.add_simple("approach")
		return

	def add_clear_target(self):
		""" Will set target to 0 for ongoing tactics processing. AiClearTarget. """
		self.add_simple("clear target")
		return

	def add_target_self(self):
		self.add_simple("target self")
		return

	def add_target_closest(self):
		self.add_simple("target closest")
		return

	def add_target_low_ac(self):
		self.add_simple("target low ac")
		return

	def add_target_high_ac(self):
		self.add_simple("target high ac")
		return

	def add_target_damaged(self):
		self.add_simple("target damaged")
		return

	def add_target_ranged(self):
		self.add_simple("target ranged")
		return

	def add_target_prone(self):
		self.add_simple("target prone")
		return

	def add_target_friend_high_ac(self):
		self.add_simple("target friend high ac")
		return

	def add_target_friend_low_ac(self):
		self.add_simple("target friend low ac")
		return

	def add_target_friend_hurt(self):
		self.add_simple("target friend hurt")
		return

	def add_target_friend_nospell(self):
		self.add_simple("target friend nospell")
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

	def add_cast_fireball(self, spell_name, class_name, class_level):
		self.add_spell("cast fireball", spell_name, class_name, class_level)
		return

	def add_cast_area(self, spell_name, class_name, class_level):
		self.add_spell("cast area", spell_name, class_name, class_level)
		return

	def add_cast_party(self, spell_name, class_name, class_level):
		self.add_spell("cast party", spell_name, class_name, class_level)
		return

	def add_five_foot_step(self):
		self.add_simple("five foot step")
		return

	def add_use_potion(self):
		self.add_simple("use potion")
		return

	def add_attack(self):
		""" AiDefault. Will try to attack target D20A_UNSPECIFIED_ATTACK first.
		If self is not wielding ranged then it will try to move, consider by 5 foot step otherwise simple approach."""
		self.add_simple("attack")
		return

	def add_attack_threatened(self):
		""" If CanMeleeTarget(current target) then Attack, otherwise fail. 
		CanMeleeTarget(target): 
			not OF_INVULNERABLE, 
			and not target has Sancturary,
			and not self has Sancturary 
			and either attack by primary weapon
				or attack by secondary weapon
				or attack natural (first) weapon
		"""
		self.add_simple("attack threatened")
		return

	def add_ready_vs_approach(self):
		self.add_simple("ready vs approach")
		return

	def make_name(self):
		name = self.name_prefix
		for i in range(1, self.count):
			name = name + "-" + self.custom_tactics[i*3+1]
			if (self.custom_tactics[i*3+1+2]):
				name = name + "(" + self.custom_tactics[i*3+1+2] + ")"
		self.custom_tactics[0] = name
		return

	def add_goto_loc(self, loc):
		self.add_triplet("goto", str(loc), "")
		return

	def add_goto(self, locx, locy):
		self.add_triplet("goto", str(locx) + " " + str(locy), "")
		return

	def add_halt(self):
		self.add_simple("halt")
		return

	def add_stop(self):
		self.add_simple("stop")
		return

	def add_target_obj(self, handle_lower, handle_upper):
		self.add_triplet("target obj", str(handle_lower) + " " + str(handle_upper), "")
		return
