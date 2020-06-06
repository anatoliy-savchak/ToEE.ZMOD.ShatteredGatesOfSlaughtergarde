import toee

class StatGenerator:
	def __init__(self, values):
		self.values = values
		print(values)
		return

	def generate(self):
		lines = list()
		line = ""

		# title
		if (1):
			line = self.values["full_name"]
			cr = self.values["cr"]
			if (cr):
				line = "{}                              CR {}".format(line, cr)
			if (line):
				lines.append(line)

		# Race, Class, and Level
		if (1):
			line = ""
			gender = self.values["gender"]
			if (gender): line = gender + " "
			class_name_dict = self.values["class_name_dict"]
			if (class_name_dict):
				phrase = ""
				comma = ""
				for k in class_name_dict.keys():
					l = class_name_dict[k]
					phrase = "{}{} {}".format(comma, k, l)
					if (phrase):
						line = line + phrase
						comma = "/"
			if (line):
				lines.append(line)

		# Alignment, Size and Type
		if (1):
			line = ""
			alignment_short = self.values["alignment_short"]
			if (alignment_short): line = line + alignment_short + " "
			size_name = self.values["size_name"]
			if (size_name): line = line + size_name + " "
			type_name = self.values["type_name"]
			if (type_name): line = line + type_name + " "
			subtype_name_list = self.values["subtype_name_list"]
			if (subtype_name_list):
				line = line + "("
				phrase = ""
				comma = ""
				for k in subtype_name_list:
					phrase = "{}{}".format(comma, k)
					if (phrase):
						line = line + phrase
						comma = ", "
				line = line + ")"
			if (line):
				lines.append(line)

		# Init, Senses
		if (1):
			line = ""
			initiative_bonus = self.values["initiative_bonus"]
			if (not initiative_bonus is None): 
				line = "Init {}; Senses: ".format(self.str_signed(initiative_bonus))

			comma = ""
			skill_listen = self.values["skill_listen"]
			if (not skill_listen is None): 
				line = "{}{}Listen {}".format(line, comma, self.str_signed(skill_listen))
				comma = ", "
			skill_spot = self.values["skill_spot"]
			if (not skill_spot is None): line = "{}{}Spot {} ".format(line, comma, self.str_signed(skill_spot))
			if (line):
				lines.append(line)

		lines.append(self.dashes())

		# Init, Senses
		if (1):
			line = ""
			line = "AC {}, touch {}, flat-footed {}".format(self.values["ac"], self.values["ac_touch"], self.values["ac_flatfooted"])
			comma = "; "
			if (toee.feat_dodge in self.values["feats"]):
				line += comma + "Dodge"
				comma = ", "
			if (toee.feat_mobility in self.values["feats"]):
				line += comma + "Mobility"
				comma = ", "
			if (toee.feat_improved_uncanny_dodge in self.values["feats"]):
				line += comma + "Improved Uncanny Dodge"
				comma = ", "
			elif (toee.feat_uncanny_dodge in self.values["feats"]):
				line += comma + "Uncanny Dodge"
				comma = ", "

			if (line):
				lines.append(line)

		# hp, fast healing, regeneration, damage reduction (DR)
		if (1):
			hp_max = self.values["hp_max"]
			hp_current = self.values["hp_current"]
			hd = self.values["hd"]
			stemplate = "hp {0} ({1} HD)"
			if (hp_max != hp_current): stemplate = "hp {2}/{0} ({1} HD)"
			line = stemplate.format(hp_max, hd, hp_current)
			if (line):
				lines.append(line)

		# Immune
		# Resist
		# Fort, Ref, Will
		if (1):
			line = "Fort {}, Ref {}, Will {}".format(self.str_signed(self.values["save_fort"]), self.str_signed(self.values["save_ref"]), self.str_signed(self.values["save_will"]))
			if (line):
				lines.append(line)

		#
		lines.append(self.dashes())

		# Speed
		if (1):
			line = "Speed {} ft. ({} squares)".format(self.values["speed_ft"], self.values["speed_sq"])
			if (line):
				lines.append(line)

		line_melee = ""
		line_ranged = ""
		# Melee, ranged
		if (1):
			weapon_list = self.values["weapon_list"]
			if (weapon_list):
				comma = ""
				comma_ranged = ""
				for w in weapon_list:
					assert isinstance(w, stat_inspect.StatInspectWeapon)
					crit_str = ""
					if (not w.crit_chart or w.crit_chart != 2): crit_str = "x{}".format(w.crit_chart)
					crit_info = ""
					if (w.crit_range_str and crit_str): crit_info = "/{}{}".format(w.crit_range_str, crit_str)
					numstr = ""
					if (w.atk_num > 1): numstr = "{} ".format(w.atk_num)
					wname = str(w.name)
					if ("+1" in wname): wname = "+1 " + wname.replace("+1", "")
					elif ("+2" in wname): wname = "+2 " + wname.replace("+2", "")
					elif ("+3" in wname): wname = "+3 " + wname.replace("+3", "")
					elif ("+4" in wname): wname = "+4 " + wname.replace("+4", "")
					damage_dice_str = w.damage_dice_str
					if (w.damage_bonus_dice_str): damage_dice_str = damage_dice_str + " " + w.damage_bonus_dice_str
					phrase = "{}{} {} ({}){}".format(numstr, wname, self.str_signed(w.attack_bonus), damage_dice_str, crit_info)
					if (w.is_ranged):
						line_ranged += comma_ranged + phrase
						comma_ranged = " and "
					else: 
						line_melee += comma + phrase
						comma = " and "

		# Melee
		if (1):
			if (line_melee):
				line_melee = "Melee " + line_melee
				lines.append(line_melee)
		# Ranged
		if (1):
			if (line_ranged):
				line_ranged = "Ranged " + line_ranged
				lines.append(line_ranged)

		# Base Atk
		if (1):
			line = "Base Atk {}".format(self.str_signed(self.values["bab"]))
			if (line):
				lines.append(line)
		# Attack options
		if (0):
			line = "Atk Options "
			if (line):
				lines.append(line)
		# Combat gear
		if (1):
			line = ""
			combat_gear_dic = self.values["combat_gear_dic"]
			if (combat_gear_dic):
				line = "Combat Gear "
				phrase = ""
				comma = ""
				for gear in combat_gear_dic.keys():
					cnt = combat_gear_dic[gear]
					if (cnt > 1): phrase = "{}{} {}".format(comma, cnt, gear)
					else: phrase = "{}{}".format(comma, gear)
					comma = ", "
					line += phrase
			if (line):
				lines.append(line)
		#
		lines.append(self.dashes())

		# Abilities
		if (1):
			line = "Abilities Str {}, Dex {}, Con {}, Int {}, Wis {}, Cha {}".format(self.values["str"], self.values["dex"], self.values["con"], self.values["int"], self.values["wis"], self.values["cha"])
			if (line):
				lines.append(line)
		# SQ
		if (0):
			line = "SQ "
			if (line):
				lines.append(line)
		# Feats
		if (1):
			line = ""
			feat_name_dic = self.values["feat_name_dic"]
			if (feat_name_dic):
				line = "Feats "
				comma = ""
				for fn in feat_name_dic.keys():
					line += comma + fn
					comma = ", "
			if (line):
				lines.append(line)
		# Skills
		if (1):
			line = ""
			skill_name_dic = self.values["skill_name_dic"]
			if (skill_name_dic):
				line = "Skills "
				comma = ""
				for fn in sorted(skill_name_dic.keys()):
					v = skill_name_dic[fn]
					if (v):
						line += "{}{} {}".format(comma, fn, self.str_signed(v))
						comma = ", "
			if (line):
				lines.append(line)
		# Posessions
		if (1):
			line = ""
			combat_gear_dic = self.values["posessions_dic"]
			if (combat_gear_dic):
				line = "Posessions "
				phrase = ""
				comma = ""
				for gear in combat_gear_dic.keys():
					cnt = combat_gear_dic[gear]
					if (cnt > 1): phrase = "{}{} {}".format(comma, cnt, gear)
					else: phrase = "{}{}".format(comma, gear)
					comma = ", "
					line += phrase
			if (line):
				lines.append(line)
		#
		result = "\n".join(lines)
		print(result)
		return result

	def str_signed(self, i):
		if (not i is None):
			if (i >=0 ): return "+{}".format(i)
			else: return "{}".format(i)
		return

	def dashes(self):
		return "---------------------------------------------------------"