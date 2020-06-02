import toee

debug_print = 1
class StatInspect:
	def __init__(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		self.stats = dict()
		self.npc = npc
		self.feats = None
		return

	def build(self):
		self.feats = self.npc.feats
		self.stats["feats"] = self.feats
		# IDENTIFICATION AND ENCOUNTER
		# Name
		self.stats["full_name"] = self.npc.description
		# CR
		self.stats["cr"] = self.get_cr()
		# Race, Class, and Level
		self.stats["race_name"] = self.get_race_name()
		self.stats["gender"] = self.get_gender_name()
		self.stats["class_name_dict"] = self.get_class_name_level_dict()
		self.stats["level"] = self.get_level()
		# Alignment
		self.stats["alignment_short"] = self.get_alignment_short()
		# Size and Type
		self.stats["size_name"] = self.get_size_name()
		self.stats["type_name"] = self.get_type_name()
		self.stats["subtype_name_list"] = self.get_subtype_name_list()
		# Init
		self.stats["initiative_bonus"] = self.get_initiative_bonus()
		# Senses
		self.stats["skill_listen"] = self.npc.skill_level_get(toee.skill_listen)
		self.stats["skill_spot"] = self.npc.skill_level_get(toee.skill_spot)

		# DEFENSIVE INFORMATION
		# AC
		self.stats["ac"] = self.get_ac()
		self.stats["ac_touch"] = self.get_ac_touch()
		self.stats["ac_flatfooted"] = self.get_ac_flatfooted()

		# hp
		self.stats["hp_max"] = self.get_hp_max()
		self.stats["hp_current"] = self.get_hp_current()
		self.stats["hd"] = self.get_hd()

		# saves
		self.stats["save_fort"] = self.get_save_fort()
		self.stats["save_ref"] = self.get_save_ref()
		self.stats["save_will"] = self.get_save_will()

		# speed
		speed_ft = self.get_speed_ft()
		self.stats["speed_ft"] = speed_ft
		self.stats["speed_sq"] = speed_ft // 5

		# abilities
		self.stats["str"] = self.get_str()
		self.stats["dex"] = self.get_dex()
		self.stats["con"] = self.get_con()
		self.stats["int"] = self.get_int()
		self.stats["wis"] = self.get_wis()
		self.stats["cha"] = self.get_cha()

		# feats
		self.stats["feat_name_dic"] = self.get_feat_name_dic()

		# skills
		self.stats["skill_name_dic"] = self.get_skill_name_dic()

		# bab
		self.stats["bab"] = self.get_bab()
		
		# attack
		self.stats["weapon_list"] = self.get_weapon_list()

		return self.stats

	def get_cr(self):
		# see toee.dll@CritterKillAwardXp
		cr = 0
		if (self.npc.type == toee.obj_t_npc):
			cr = self.npc.obj_get_int(toee.obj_f_npc_challenge_rating)
		level_cr = self.npc.stat_level_get(toee.stat_level)
		result = cr + level_cr
		return result

	def get_alignment_short(self):
		a = self.npc.obj_get_int(toee.obj_f_critter_alignment)
		if (a == toee.ALIGNMENT_NEUTRAL): return "N"
		if (a == toee.ALIGNMENT_LAWFUL): return "L"
		if (a == toee.ALIGNMENT_LAWFUL_NEUTRAL): return "LN"
		if (a == toee.ALIGNMENT_CHAOTIC): return "C"
		if (a == toee.ALIGNMENT_CHAOTIC_NEUTRAL): return "CN"
		if (a == toee.ALIGNMENT_GOOD): return "G"
		if (a == toee.ALIGNMENT_NEUTRAL_GOOD): return "NG"
		if (a == toee.ALIGNMENT_LAWFUL_GOOD): return "LG"
		if (a == toee.ALIGNMENT_CHAOTIC_GOOD): return "CG"
		if (a == toee.ALIGNMENT_EVIL): return "E"
		if (a == toee.ALIGNMENT_NEUTRAL_EVIL): return "NE"
		if (a == toee.ALIGNMENT_LAWFUL_EVIL): return "LE"
		if (a == toee.ALIGNMENT_CHAOTIC_EVIL ): return "CE"
		return None

	def get_race_name(self):
		race = self.npc.stat_level_get(toee.stat_race)
		if (race == toee.race_deep_dwarf): return "Deep Dwarf"
		if (race == toee.race_human): return "Human"
		if (race == toee.race_derro): return "Derro"
		if (race == toee.race_dwarf): return "Dwarf"
		if (race == toee.race_duergar): return "Duergar"
		if (race == toee.race_elf): return "Elf"
		if (race == toee.race_mountain_dwarf): return "Mountain Dwarf"
		if (race == toee.race_gnome): return "Gnome"
		if (race == toee.race_aquatic_elf): return "Aquatic Elf"
		if (race == toee.race_halfelf): return "Halfelf"
		if (race == toee.race_half_elf): return "Half Elf"
		if (race == toee.race_half_orc): return "Half Orc"
		if (race == toee.race_halforc): return "Halforc"
		if (race == toee.race_halfling): return "Halfling"
		if (race == toee.race_gray_elf): return "Gray Elf"
		if (race == toee.race_wild_elf): return "Wild Elf"
		if (race == toee.race_wood_elf): return "Wood Elf"
		if (race == toee.race_svirfneblin): return "Svirfneblin"
		if (race == toee.race_forest_gnome): return "Forest Gnome"
		if (race == toee.race_hill_giant): return "Hill Giant"
		if (race == toee.race_tallfellow): return "Tallfellow"
		if (race == toee.race_troll): return "Troll"
		if (race == toee.race_deep_halfling): return "Deep Halfling"
		if (race == toee.race_drow): return "Drow"
		return race

	def get_class_name_level_dict(self):
		classes = self.npc.char_classes
		result = dict()
		for c in classes:
			cs = self.get_class_title(c)
			if (cs is None): continue
			l = self.npc.stat_level_get(c)
			result[cs] = l
		if (debug_print): print(result)
		return result

	def get_class_title(self, c):
		if (c == toee.stat_level_barbarian): return "barbarian"
		if (c == toee.stat_level_bard): return "bard"
		if (c == toee.stat_level_cleric): return "cleric"
		if (c == toee.stat_level_druid): return "druid"
		if (c == toee.stat_level_fighter): return "fighter"
		if (c == toee.stat_level_monk): return "monk"
		if (c == toee.stat_level_paladin): return "paladin"
		if (c == toee.stat_level_ranger): return "ranger"
		if (c == toee.stat_level_rogue): return "rogue"
		if (c == toee.stat_level_sorcerer): return "sorcerer"
		if (c == toee.stat_level_wizard): return "wizard"
		if (c == toee.stat_level_arcane_archer): return "arcane_archer"
		if (c == toee.stat_level_arcane_trickster): return "arcane_trickster"
		if (c == toee.stat_level_archmage): return "archmage"
		if (c == toee.stat_level_assassin): return "assassin"
		if (c == toee.stat_level_blackguard): return "blackguard"
		if (c == toee.stat_level_dragon_disciple): return "dragon_disciple"
		if (c == toee.stat_level_duelist): return "duelist"
		if (c == toee.stat_level_dwarven_defender): return "dwarven_defender"
		if (c == toee.stat_level_eldritch_knight): return "eldritch_knight"
		if (c == toee.stat_level_hierophant): return "hierophant"
		if (c == toee.stat_level_horizon_walker): return "horizon_walker"
		if (c == toee.stat_level_loremaster): return "loremaster"
		if (c == toee.stat_level_mystic_theurge): return "mystic_theurge"
		if (c == toee.stat_level_shadowdancer): return "shadowdancer"
		if (c == toee.stat_level_thaumaturgist): return "thaumaturgist"
		if (c == toee.stat_level_warlock): return "warlock"
		if (c == toee.stat_level_favored_soul): return "favored_soul"
		if (c == toee.stat_level_red_avenger): return "red_avenger"
		if (c == toee.stat_level_iaijutsu_master): return "iaijutsu_master"
		if (c == toee.stat_level_sacred_fist): return "sacred_fist"
		if (c == toee.stat_level_stormlord): return "stormlord"
		if (c == toee.stat_level_elemental_savant): return "elemental_savant"
		if (c == toee.stat_level_blood_magus): return "blood_magus"
		if (c == toee.stat_level_beastmaster): return "beastmaster"
		if (c == toee.stat_level_cryokineticist): return "cryokineticist"
		if (c == toee.stat_level_frost_mage): return "frost_mage"
		if (c == toee.stat_level_artificer): return "artificer"
		if (c == toee.stat_level_abjurant_champion): return "abjurant_champion"
		if (c == toee.stat_level_psion): return "psion"
		if (c == toee.stat_level_psychic_warrior): return "psychic_warrior"
		if (c == toee.stat_level_soulknife): return "soulknife"
		if (c == toee.stat_level_wilder): return "wilder"
		if (c == toee.stat_level_cerebmancer): return "cerebmancer"
		if (c == toee.stat_level_elocator): return "elocator"
		if (c == toee.stat_level_metamind): return "metamind"
		if (c == toee.stat_level_psion_uncarnate): return "psion_uncarnate"
		if (c == toee.stat_level_psionic_fist): return "psionic_fist"
		if (c == toee.stat_level_pyrokineticist): return "pyrokineticist"
		if (c == toee.stat_level_slayer): return "slayer"
		if (c == toee.stat_level_thrallherd): return "thrallherd"
		if (c == toee.stat_level_war_mind): return "war_mind"
		if (c == toee.stat_level_crusader): return "crusader"
		if (c == toee.stat_level_swordsage): return "swordsage"
		if (c == toee.stat_level_warblade): return "warblade"
		if (c == toee.stat_level_bloodclaw_master): return "bloodclaw_master"
		if (c == toee.stat_level_bloodstorm_blade): return "bloodstorm_blade"
		if (c == toee.stat_level_deepstone_sentinel): return "deepstone_sentinel"
		if (c == toee.stat_level_eternal_blade): return "eternal_blade"
		if (c == toee.stat_level_jade_phoenix_mage): return "jade_phoenix_mage"
		if (c == toee.stat_level_master_of_nine): return "master_of_nine"
		if (c == toee.stat_level_ruby_knight_vindicator): return "ruby_knight_vindicator"
		if (c == toee.stat_level_shadow_sun_ninja): return "shadow_sun_ninja"
		return None

	def get_level(self):
		level = self.npc.stat_level_get(toee.stat_level)
		return level

	def get_initiative_bonus(self):
		#result = self.npc.stat_level_get(toee.stat_initiative_bonus)
		#result = self.npc.stat_base_get(toee.stat_initiative_bonus)
		dex_stat = self.npc.stat_level_get(toee.stat_dex_mod)
		base = self.npc.obj_get_int(toee.obj_f_initiative)
		result = dex_stat + base
		return result

	def get_size_name(self):
		size = self.npc.get_size
		if (not size): return None
		if (size == 1): return "Fine"
		if (size == 2): return "Diminutive"
		if (size == 3): return "Tiny"
		if (size == 4): return "Small"
		if (size == 5): return "Medium"
		if (size == 6): return "Large"
		if (size == 7): return "Huge"
		if (size == 8): return "Gargantuan"
		if (size == 9): return "Clossal"
		return None

	def get_type_name(self):
		cat = self.npc.get_category_type()
		if (cat == toee.mc_type_aberration): return "aberration"
		if (cat == toee.mc_type_animal): return "animal"
		if (cat == toee.mc_type_beast): return "beast"
		if (cat == toee.mc_type_construct): return "construct"
		if (cat == toee.mc_type_dragon): return "dragon"
		if (cat == toee.mc_type_elemental): return "elemental"
		if (cat == toee.mc_type_fey): return "fey"
		if (cat == toee.mc_type_giant): return "giant"
		if (cat == toee.mc_type_humanoid): return "humanoid"
		if (cat == toee.mc_type_magical_beast): return "magical_beast"
		if (cat == toee.mc_type_monstrous_humanoid): return "monstrous_humanoid"
		if (cat == toee.mc_type_ooze): return "ooze"
		if (cat == toee.mc_type_outsider): return "outsider"
		if (cat == toee.mc_type_plant): return "plant"
		if (cat == toee.mc_type_shapechanger): return "shapechanger"
		if (cat == toee.mc_type_undead): return "undead"
		if (cat == toee.mc_type_vermin): return "vermin"
		return None

	def get_subtype_name_list(self):
		cat = self.npc.obj_get_int64(toee.obj_f_critter_monster_category)
		scat = cat >> 32
		result = list()
		if (scat & toee.mc_subtype_air): result.append("air")
		if (scat & toee.mc_subtype_aquatic): result.append("aquatic")
		if (scat & toee.mc_subtype_extraplanar): result.append("extraplanar")
		#if (scat & toee.mc_subtype_extraplaner): result.append("extraplaner")
		if (scat & toee.mc_subtype_cold): result.append("cold")
		if (scat & toee.mc_subtype_chaotic): result.append("chaotic")
		if (scat & toee.mc_subtype_demon): result.append("demon")
		if (scat & toee.mc_subtype_devil): result.append("devil")
		if (scat & toee.mc_subtype_dwarf): result.append("dwarf")
		if (scat & toee.mc_subtype_earth): result.append("earth")
		if (scat & toee.mc_subtype_electricity): result.append("electricity")
		if (scat & toee.mc_subtype_elf): result.append("elf")
		if (scat & toee.mc_subtype_evil): result.append("evil")
		if (scat & toee.mc_subtype_fire): result.append("fire")
		if (scat & toee.mc_subtype_formian): result.append("formian")
		if (scat & toee.mc_subtype_gnoll): result.append("gnoll")
		if (scat & toee.mc_subtype_gnome): result.append("gnome")
		if (scat & toee.mc_subtype_goblinoid): result.append("goblinoid")
		if (scat & toee.mc_subtype_good): result.append("good")
		if (scat & toee.mc_subtype_guardinal): result.append("guardinal")
		if (scat & toee.mc_subtype_half_orc): result.append("half_orc")
		if (scat & toee.mc_subtype_halfling): result.append("halfling")
		if (scat & toee.mc_subtype_human): result.append("human")
		if (scat & toee.mc_subtype_lawful): result.append("lawful")
		if (scat & toee.mc_subtype_incorporeal): result.append("incorporeal")
		if (scat & toee.mc_subtype_orc): result.append("orc")
		if (scat & toee.mc_subtype_reptilian): result.append("reptilian")
		if (scat & toee.mc_subtype_slaadi): result.append("slaadi")
		if (scat & toee.mc_subtype_water): result.append("water")
		return result

	def get_gender_name(self):
		gender = self.npc.stat_level_get(toee.stat_gender)
		if (gender == toee.gender_female): return "Female"
		if (gender == toee.gender_male): return "Male"
		return None

	def get_ac(self):
		result = self.npc.stat_level_get(toee.stat_ac)
		return result

	def get_ac_touch(self):
		result = 10 + self.npc.stat_level_get(toee.stat_dex_mod)
		if (toee.feat_dodge in self.feats):
			result += 1
		return result

	def get_ac_flatfooted(self):
		result = self.npc.stat_level_get(toee.stat_ac)
		result -= self.npc.stat_level_get(toee.stat_dex_mod)
		if (toee.feat_dodge in self.feats):
			result -= 1
		return result

	def get_hp_max(self):
		result = self.npc.stat_level_get(toee.stat_hp_max)
		return result

	def get_hp_current(self):
		result = self.npc.stat_level_get(toee.stat_hp_current)
		return result

	def get_hd(self):
		result = self.npc.hit_dice_num
		return result

	def get_save_fort(self):
		result = self.npc.stat_level_get(toee.stat_save_fortitude)
		return result

	def get_save_ref(self):
		result = self.npc.stat_level_get(toee.stat_save_reflexes)
		return result

	def get_save_will(self):
		result = self.npc.stat_level_get(toee.stat_save_willpower)
		return result

	def get_speed_ft(self):
		result = self.npc.stat_level_get(toee.stat_movement_speed)
		return result
	
	def get_str(self):
		result = self.npc.stat_level_get(toee.stat_strength)
		return result
	
	def get_dex(self):
		result = self.npc.stat_level_get(toee.stat_dexterity)
		return result
	
	def get_con(self):
		result = self.npc.stat_level_get(toee.stat_constitution)
		return result
	
	def get_int(self):
		result = self.npc.stat_level_get(toee.stat_intelligence)
		return result
	
	def get_wis(self):
		result = self.npc.stat_level_get(toee.stat_wisdom)
		return result
	
	def get_cha(self):
		result = self.npc.stat_level_get(toee.stat_charisma)
		return result

	def get_feat_name_dic(self):
		result = dict()
		for f in self.feats:
			fn = toee.game.get_feat_name(f)
			if (fn):
				result[fn] = f
		return result
	
	def get_skill_name_dic(self):
		result = dict()
		result["Appraise"] = self.npc.skill_level_get(toee.skill_appraise)
		result["Bluff"] = self.npc.skill_level_get(toee.skill_bluff)
		result["Concentration"] = self.npc.skill_level_get(toee.skill_concentration)
		result["Diplomacy"] = self.npc.skill_level_get(toee.skill_diplomacy)
		result["Disable Device"] = self.npc.skill_level_get(toee.skill_disable_device)
		result["Gather Information"] = self.npc.skill_level_get(toee.skill_gather_information)
		result["Heal"] = self.npc.skill_level_get(toee.skill_heal)
		result["Hide"] = self.npc.skill_level_get(toee.skill_hide)
		result["Intimidate"] = self.npc.skill_level_get(toee.skill_intimidate)
		result["Listen"] = self.npc.skill_level_get(toee.skill_listen)
		result["Move Silently"] = self.npc.skill_level_get(toee.skill_move_silently)
		result["Open Lock"] = self.npc.skill_level_get(toee.skill_open_lock)
		result["Pick Pocket"] = self.npc.skill_level_get(toee.skill_pick_pocket)
		result["Search"] = self.npc.skill_level_get(toee.skill_search)
		result["Sense Motive"] = self.npc.skill_level_get(toee.skill_sense_motive)
		result["Spellcraft"] = self.npc.skill_level_get(toee.skill_spellcraft)
		result["Spot"] = self.npc.skill_level_get(toee.skill_spot)
		result["Tumble"] = self.npc.skill_level_get(toee.skill_tumble)
		result["Use Magic Devic"] = self.npc.skill_level_get(toee.skill_use_magic_device)
		#result["Wilderness Lore"] = self.npc.skill_level_get(toee.skill_wilderness_lore)
		result["Perform"] = self.npc.skill_level_get(toee.skill_perform)
		#result["Alchemy"] = self.npc.skill_level_get(toee.skill_alchemy)
		result["Balance"] = self.npc.skill_level_get(toee.skill_balance)
		result["Climb"] = self.npc.skill_level_get(toee.skill_climb)
		#result["Craft"] = self.npc.skill_level_get(toee.skill_craft)
		result["Decipher Script"] = self.npc.skill_level_get(toee.skill_decipher_script)
		#result["Disguise"] = self.npc.skill_level_get(toee.skill_disguise)
		result["Escape Artist"] = self.npc.skill_level_get(toee.skill_escape_artist)
		#result["Forgery"] = self.npc.skill_level_get(toee.skill_forgery)
		#result["Handle Animal"] = self.npc.skill_level_get(toee.skill_handle_animal)
		#result["Innuendo"] = self.npc.skill_level_get(toee.skill_innuendo)
		#result["Intuit Direction"] = self.npc.skill_level_get(toee.skill_intuit_direction)
		result["Jump"] = self.npc.skill_level_get(toee.skill_jump)
		result["Knowledge Arcana"] = self.npc.skill_level_get(toee.skill_knowledge_arcana)
		result["Knowledge Religion"] = self.npc.skill_level_get(toee.skill_knowledge_religion)
		result["Knowledge Nature"] = self.npc.skill_level_get(toee.skill_knowledge_nature)
		result["Knowledge All"] = self.npc.skill_level_get(toee.skill_knowledge_all)
		#result["Profession"] = self.npc.skill_level_get(toee.skill_profession)
		#result["Read Lips"] = self.npc.skill_level_get(toee.skill_read_lips)
		#result["Ride"] = self.npc.skill_level_get(toee.skill_ride)
		#result["Swim"] = self.npc.skill_level_get(toee.skill_swim)
		result["Use Rope"] = self.npc.skill_level_get(toee.skill_use_rope)
		return result

	def get_bab(self):
		result = self.npc.get_base_attack_bonus()
		return result

	def get_weapon_list(self):
		result = list()
		weapon = self.npc.item_worn_at(toee.item_wear_weapon_primary)
		if (weapon):
			item = StatInspectWeapon()
			item.name = weapon.description
			item.attack_bonus = self.npc.stat_level_get(toee.stat_melee_attack_bonus)
			weapon_type = weapon.obj_get_int(toee.obj_f_weapon_type)
			item.is_ranged = toee.game.is_ranged_weapon(weapon_type)
			if (item.is_ranged):
				item.attack_bonus = self.npc.stat_level_get(toee.stat_ranged_attack_bonus)

			if (1):
				dmg_dice_packed = weapon.obj_get_int(toee.obj_f_weapon_damage_dice)
				if (debug_print): print("Weapon dmg_dice_packed: {}".format(dmg_dice_packed))
				dmg_dice = toee.dice_new("1d1")
				dmg_dice.packed = dmg_dice_packed
				if (not item.is_ranged):
					damage_bonus = self.npc.stat_level_get(toee.stat_damage_bonus)
					if (debug_print): print("Weapon damage_bonus: {}".format(damage_bonus))
					dmg_dice.bonus += damage_bonus
				dmg_dice_str = str(dmg_dice)
				if (debug_print): print("Weapon dmg_dice_str: {}".format(dmg_dice_str))
				item.damage_dice_str = dmg_dice_str

			if (1):
				crit_range = weapon.obj_get_int(toee.obj_f_weapon_crit_range)
				if (debug_print): print("Weapon crit_range: {}".format(crit_range))
				if (crit_range == 0): crit_range = 20
				else: crit_range = 21-crit_range
				crit_range_str = ""
				if (crit_range < 20):
					crit_range_str = "{}-20".format(crit_range)
				if (debug_print): print("Weapon crit_range_str: {}".format(crit_range_str))
				item.crit_range_str = crit_range_str

			if (1):
				crit_hit_chart = weapon.obj_get_int(toee.obj_f_weapon_crit_hit_chart)
				if (crit_hit_chart == 0): crit_hit_chart = 2
				item.crit_chart = crit_hit_chart
			
			result.append(item)
		return result

class StatInspectWeapon:
	def __init__(self):
		self.name = None
		self.attack_bonus = 0
		self.ench_bonus = 0
		self.is_ranged = 0
		self.damage_dice_str = ""
		self.crit_range_str = ""
		self.crit_chart = 2
		return