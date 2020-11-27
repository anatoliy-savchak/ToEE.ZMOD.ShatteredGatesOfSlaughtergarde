import toee, pc_gen, utils_item
import const_proto_armor, const_proto_weapon, const_proto_wands, const_proto_cloth

# import barovia_pc
# barovia_pc.barovia_team5()

def barovia_team5():

	pc = toee.game.party[0] # Ostap, Paladin 5
	if (pc):
		pcg = pc_gen.PCGen()
		pcg.set_abilities(15, 12, 14, 8, 12, 12)
		pcg.class_levels.append((toee.stat_level_paladin, 5))
		pcg.feats.append(toee.feat_power_attack)
		pcg.apply_pc(pc)

		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_BOOTS_BREASTPLATE_BOOTS, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_GLOVES_BREASTPLATE_GLOVES, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_HELMES_PLUMED_SILVER, pc)

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_TOWER_STEEL, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE_PLUS_1, pc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_LONGSWORD_PLUS_1, pc)
		pc.item_wield_best_all()

	pc = toee.game.party[1] # Andriy, Barbarian 5
	if (pc):
		pcg = pc_gen.PCGen()
		pcg.set_abilities(16, 14, 14, 9, 12, 8) # pcg.set_abilities(18, 14, 14, 7, 12, 6)
		pcg.class_levels.append((toee.stat_level_barbarian, 5))
		pcg.feats.append(toee.feat_dodge)
		pcg.feats.append(toee.feat_cleave)
		pcg.feats.append(toee.feat_combat_reflexes)
		pcg.apply_pc(pc)

		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_BOOTS_PADDED_RED, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_GLOVES_PADDED_RED, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, pc)
		utils_item.item_create_in_inventory(PROTO_CLOAK_BLUE.PROTO_CLOAK_BLUE, pc)

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_CHAINMAIL_MITHRAL_PLUS_1, pc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GREATAXE_PLUS_1, pc)
		pc.item_wield_best_all()

	pc = toee.game.party[2] # Eugene, Warblade 5
	if (pc):
		pcg = pc_gen.PCGen()
		pcg.set_abilities(16, 12, 14, 14, 8, 8)
		#pcg.class_levels.append((toee.stat_level_barbarian, 5))
		pcg.class_levels.append((toee.stat_level_fighter, 5))
		pcg.feats.append(toee.feat_cleave)
		pcg.feats.append(toee.feat_weapon_focus_greatsword)
		pcg.apply_pc(pc)

		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_BOOTS_BREASTPLATE_BOOTS, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_GLOVES_BREASTPLATE_GLOVES, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_CLOAK_RED, pc)

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE_PLUS_1, pc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_GREATSWORD_PLUS_1, pc)
		pc.item_wield_best_all()

	pc = toee.game.party[3] # Volodya, Cleric 5
	if (pc):
		pcg = pc_gen.PCGen()
		pcg.set_abilities(13, 14, 14, 10, 16, 6) # pcg.set_abilities(13, 12, 16, 10, 16, 6)
		pcg.class_levels.append((toee.stat_level_cleric, 5))
		pcg.feats.append(toee.feat_craft_wondrous_item)
		pcg.apply_pc(pc)

		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_BOOTS_BREASTPLATE_BOOTS, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_GLOVES_BREASTPLATE_GLOVES, pc)

		utils_item.item_create_in_inventory(const_proto_armor.PROTO_ARMOR_FULL_PLATE_MASTERWORK, pc)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_SHIELD_SMALL_WOODEN, pc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_MACE_LIGHT, pc)

		utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_CURE_LIGHT_WOUNDS, pc)
		utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_RESTORATION_LESSER, pc)
		utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_CURE_MODERATE_WOUNDS, pc)
		
		pc.item_wield_best_all()

	pc = toee.game.party[4] # Lesya, Wizard 5
	if (pc):
		pcg = pc_gen.PCGen()
		pcg.set_abilities(9, 14, 12, 16, 10, 12)
		pcg.class_levels.append((toee.stat_level_wizard, 5))
		pcg.feats.append(toee.feat_precise_shot)
		pcg.feats.append(toee.feat_craft_wand)
		pcg.apply_pc(pc)

		utils_item.item_clear_by_proto(pc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		utils_item.item_create_in_inventory(const_proto_armor.PROTO_BOOTS_LEATHER_BOOTS_GREEN, pc)
		#utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_LEATHER_CLOTHING, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_MONK_OUTFIT, pc)
		utils_item.item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, pc)

		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_WEAPON_LONGBOW, pc)
		utils_item.item_create_in_inventory(const_proto_weapon.PROTO_AMMO_ARROW_QUIVER, pc)

		utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_ENLARGE_PERSON, pc)
		utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_SCORCHING_RAY_1ST, pc)
		wand = utils_item.item_create_in_inventory(const_proto_wands.PROTO_WAND_OF_HASTE, pc)
		if (wand):
			wand.obj_set_int(toee.obj_f_item_spell_charges_idx, 25)

		pc.spell_known_add(toee.spell_fireball, toee.stat_level_wizard, 3)
		#game.leader.spell_known_add(spell_fireball, stat_level_wizard, 3)
		
		pc.item_wield_best_all()
	return