from toee import *
from debugg import *
from utils_obj import *
from const_toee import *
from utils_item import *
from utils_npc import *
from const_proto_armor import *
from const_proto_weapon import *
from const_proto_items import *
from const_proto_potions import *
from const_proto_wands import *
import const_proto_cloth

def cmrlv5():
	kostyantyn = game.party[0]
	andriy = game.party[1]
	eugene = game.party[2]
	wolodya = game.party[3]
	lesya = game.party[4]

	# kostyantyn
	npc = kostyantyn
	npc.feat_add(feat_weapon_finesse_spike_chain, 1) # game.party[0].feat_add(feat_weapon_finesse_spike_chain, 0)
	obj_scripts_clear(npc)
	item_create_in_inventory(PROTO_ARMOR_MITHRAL_SHIRT_PLUS_1, npc)
	item_create_in_inventory(PROTO_GLOVES_GLOVES_OF_DEXTERITY_2, npc)
	item_create_in_inventory(PROTO_CLOAK_OF_CHARISMA_4_STARS, npc)
	item_create_in_inventory(PROTO_WEAPON_SPIKED_CHAIN_PLUS_1, npc)
	item_create_in_inventory(PROTO_WEAPON_CROSSBOW_LIGHT_MASTERWORK, npc)
	item_create_in_inventory(PROTO_AMMO_BOLT_QUIVER, npc)
	item_create_in_inventory(PROTO_WAND_OF_CURE_LIGHT_WOUNDS, npc)
	item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
	npc.identify_all()
	npc.item_wield_best_all()

	# andriy
	npc = andriy
	obj_scripts_clear(npc)
	item_create_in_inventory(PROTO_ARMOR_MITHRAL_SHIRT_PLUS_1, npc)
	item_create_in_inventory(PROTO_CLOAK_OF_RESISTANCE_1_GREEN, npc)
	item_create_in_inventory(PROTO_WEAPON_GREATAXE_PLUS_1, npc)
	item_create_in_inventory(PROTO_WEAPON_LONGBOW, npc)
	item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
	item_create_in_inventory(PROTO_WEAPON_HALBERD, npc)
	item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
	npc.identify_all()
	npc.item_wield_best_all()
	
	# eugene
	npc = eugene
	obj_scripts_clear(npc)
	item_create_in_inventory(PROTO_ARMOR_FULL_PLATE_PLUS_1_BLACK, npc)
	item_create_in_inventory(PROTO_GLOVES_GAUNTLETS_OF_OGRE_POWER, npc)
	item_create_in_inventory(PROTO_CLOAK_OF_RESISTANCE_1_BLACK, npc)
	item_create_in_inventory(PROTO_WEAPON_HANDAXE_MASTERWORK, npc)
	item_create_in_inventory(PROTO_WEAPON_WARHAMMER_PLUS_1, npc)
	item_create_in_inventory(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
	item_create_in_inventory(PROTO_AMMO_BOLT_QUIVER, npc)
	item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
	npc.identify_all()
	npc.item_wield_best_all()
	
	# wolodya
	npc = wolodya
	obj_scripts_clear(npc)
	item_create_in_inventory(PROTO_ARMOR_FULL_PLATE_PLUS_1, npc)
	item_create_in_inventory(PROTO_GLOVES_GAUNTLETS_OF_OGRE_POWER, npc)
	item_create_in_inventory(PROTO_WEAPON_GREATAXE_PLUS_1, npc)
	item_create_in_inventory(PROTO_WEAPON_LONGBOW, npc)
	item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
	item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
	npc.identify_all()
	npc.item_wield_best_all()
	
	# lesya
	npc = lesya
	obj_scripts_clear(npc)
	item_create_in_inventory(PROTO_CLOAK_OF_RESISTANCE_1_WHITE, npc)
	item_create_in_inventory(PROTO_WEAPON_CROSSBOW_LIGHT_MASTERWORK, npc)
	item_create_in_inventory(PROTO_AMMO_BOLT_QUIVER, npc)
	item_create_in_inventory(PROTO_WAND_OF_MAGIC_MISSILES_1, npc)
	item_create_in_inventory(PROTO_WAND_OF_SCORCHING_RAY_1, npc)
	item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
	npc.identify_all()
	npc.item_wield_best_all()

	return

def c1():
	rogue = game.party[0]
	fighter = game.party[1]
	cleric = game.party[2]
	sorcerer = game.party[3]

	npc = rogue
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_GREEN, npc)
		item_create_in_inventory(PROTO_WEAPON_SHORTSWORD, npc)
		item_create_in_inventory(PROTO_SHIELD_WOODEN_SMALL, npc)
		item_create_in_inventory(PROTO_WEAPON_SHORTBOW, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		item_create_in_inventory(PROTO_GENERIC_TOOLS_THIEVES, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = fighter
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_ARMOR_SCALE_MAIL, npc)
		item_create_in_inventory(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory(PROTO_WEAPON_GREATAXE, npc)
		item_create_in_inventory(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = cleric
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_CLOAK_GREEN, npc)
		item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc)
		item_create_in_inventory(PROTO_ARMOR_PADDED_ARMOR_TAN, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_FINE, npc)
		#item_create_in_inventory(PROTO_WEAPON_MORNINGSTAR, npc)
		#item_create_in_inventory(PROTO_SHIELD_WOODEN_SMALL, npc)
		item_create_in_inventory(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = sorcerer
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_CLOAK_WHITE, npc)
		item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_NICE, npc)
		item_create_in_inventory(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_LEATHER_CLOTHING, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_WHITE, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	return

def c2():
	swashbuckler = game.party[0]
	barbarian = game.party[1]
	cleric = game.party[2]
	wizard = game.party[3]

	npc = swashbuckler
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_GREEN, npc)
		item_create_in_inventory(PROTO_WEAPON_SHORTSWORD, npc)
		item_create_in_inventory(PROTO_WEAPON_SHORTBOW, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = barbarian
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory(PROTO_WEAPON_GREATAXE, npc)
		item_create_in_inventory(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = cleric
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_CLOAK_GREEN, npc)
		item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc)
		item_create_in_inventory(PROTO_ARMOR_BANDED_MAIL, npc)
		item_create_in_inventory(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory(PROTO_LONGSWORD, npc)
		item_create_in_inventory(PROTO_SHIELD_WOODEN_SMALL, npc)
		item_create_in_inventory(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = wizard
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_CLOAK_WHITE, npc)
		item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_NICE, npc)
		item_create_in_inventory(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_LEATHER_CLOTHING, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_WHITE, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	return

def c3():
	thief = game.party[0]
	barbarian = game.party[1]
	cleric = game.party[2]
	warmage = game.party[3]

	npc = thief
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_GREEN, npc)
		item_create_in_inventory(PROTO_WEAPON_SHORTSWORD, npc)
		item_create_in_inventory(PROTO_WEAPON_SHORTSWORD, npc)
		item_create_in_inventory(PROTO_WEAPON_SHORTBOW, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = barbarian
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory(PROTO_WEAPON_GREATAXE, npc)
		item_create_in_inventory(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = cleric
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_CLOAK_GREEN, npc)
		#item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc)
		item_create_in_inventory(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory(PROTO_WEAPON_MORNINGSTAR, npc)
		item_create_in_inventory(PROTO_SHIELD_WOODEN_SMALL, npc)
		item_create_in_inventory(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = warmage
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_CLOAK_WHITE, npc)
		item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_NICE, npc)
		item_create_in_inventory(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		#item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_LEATHER_CLOTHING, npc)
		item_create_in_inventory(PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_WHITE, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	return

def c4():
	scout = game.party[0]
	barbarian = game.party[1]
	fighter = game.party[2]
	cleric = game.party[3]
	warmage = game.party[4]

	npc = scout
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory_buy(PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_LEATHER_BOOTS_GREEN, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_SHORTBOW, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		item_create_in_inventory_buy(PROTO_GENERIC_TOOLS_THIEVES, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = barbarian
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		#item_create_in_inventory_buy(PROTO_WEAPON_GREATAXE, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = fighter
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		#item_create_in_inventory_buy(PROTO_LONGSWORD, npc)
		item_create_in_inventory_buy(PROTO_SHIELD_WOODEN_LARGE, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = cleric
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory_buy(PROTO_CLOAK_GREEN, npc)
		#item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_MORNINGSTAR, npc)
		item_create_in_inventory_buy(PROTO_SHIELD_WOODEN_SMALL, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = warmage
	if (1==1):
		#item_clear_all(npc)

		item_create_in_inventory_buy(PROTO_CLOAK_WHITE, npc)
		item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_CIRCLET_NICE, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		#item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_LEATHER_CLOTHING, npc)
		item_create_in_inventory_buy(PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_LEATHER_BOOTS_WHITE, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	return

def pc_get_clw_half():
	npc = game.leader
	item = game.obj_create(PROTO_WAND_OF_CURE_LIGHT_WOUNDS, npc.location)
	item.obj_set_int(obj_f_item_spell_charges_idx, 25)
	worth = item.obj_get_int(obj_f_item_worth)
	worth = worth // 2
	item.obj_set_int(obj_f_item_worth, worth)
	npc.money_adj(-worth)
	npc.item_get(item)
	npc.identify_all()
	return

def pc_grand_inspect():
	game.leader.condition_add("Inspect")
	for pc in game.party: pc.condition_add("Inspect")
	return

def c5():
	scout = game.party[0]
	barbarian = game.party[1]
	fighter = game.party[2]
	cleric = game.party[3]
	wizard = game.party[4]

	npc = scout
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory(PROTO_ARMOR_STUDDED_LEATHER_ARMOR_MASTERWORK, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_GREEN, npc)
		item_create_in_inventory(PROTO_WEAPON_SHORTBOW_MASTERWORK, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		item_create_in_inventory(PROTO_GENERIC_TOOLS_THIEVES, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = barbarian
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory(PROTO_ARMOR_BREASTPLATE_MASTERWORK, npc)
		item_create_in_inventory(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory(PROTO_WEAPON_GREATAXE_MASTERWORK, npc)
		item_create_in_inventory(PROTO_WEAPON_LONGBOW_MASTERWORK, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = fighter
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory(PROTO_ARMOR_BREASTPLATE_MASTERWORK, npc)
		item_create_in_inventory(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory(PROTO_LONGSWORD_MASTERWORK, npc, 2)
		item_create_in_inventory(PROTO_SHIELD_WOODEN_LARGE_MASTERWORK, npc)
		item_create_in_inventory(PROTO_WEAPON_LONGBOW_MASTERWORK, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = cleric
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory(PROTO_CLOAK_GREEN, npc)
		#item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc)
		item_create_in_inventory(PROTO_ARMOR_HALF_PLATE_MASTERWORK, npc)
		item_create_in_inventory(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory(PROTO_WEAPON_MORNINGSTAR_MASTERWORK, npc)
		item_create_in_inventory(PROTO_LONGSWORD_MASTERWORK, npc)
		item_create_in_inventory(PROTO_SHIELD_WOODEN_SMALL, npc)
		item_create_in_inventory(PROTO_WEAPON_CROSSBOW_LIGHT_MASTERWORK, npc)
		item = item_create_in_inventory(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = wizard
	if (1==1):
		#item_clear_all(npc)

		item_create_in_inventory(PROTO_CLOAK_WHITE, npc)
		item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_NICE, npc)
		item_create_in_inventory(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_LEATHER_CLOTHING, npc)
		#item_create_in_inventory(PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_WHITE, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	return

def c6():
	rogue = game.party[0]
	barbarian = game.party[1]
	fighter = game.party[2]
	cleric = game.party[3]

	npc = rogue
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory_buy(PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_LEATHER_BOOTS_GREEN, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_SHORTBOW, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		item_create_in_inventory_buy(PROTO_GENERIC_TOOLS_THIEVES, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = barbarian
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		#item_create_in_inventory_buy(PROTO_WEAPON_GREATAXE, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = fighter
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		#item_create_in_inventory_buy(PROTO_LONGSWORD, npc)
		item_create_in_inventory_buy(PROTO_SHIELD_WOODEN_LARGE, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = cleric
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory_buy(PROTO_CLOAK_GREEN, npc)
		#item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_MORNINGSTAR, npc)
		item_create_in_inventory_buy(PROTO_SHIELD_WOODEN_SMALL, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()
	return

def c7():
	wizard = game.party[0]
	barbarian = game.party[1]
	fighter = game.party[2]
	cleric = game.party[3]

	npc = wizard
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_LEATHER_CLOTHING, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_LEATHER_BOOTS_GREEN, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		#item_create_in_inventory_buy(PROTO_GENERIC_TOOLS_THIEVES, npc)
		wand = item_create_in_inventory_buy(PROTO_WAND_OF_RAY_OF_FROST, npc, None, 0.5)
		if (wand):
			wand.obj_set_int(obj_f_item_spell_charges_idx, 25)
		
		npc.identify_all()
		npc.item_wield_best_all()

	npc = barbarian
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		#item_create_in_inventory_buy(PROTO_WEAPON_GREATAXE, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = fighter
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		#item_create_in_inventory_buy(PROTO_LONGSWORD, npc)
		item_create_in_inventory_buy(PROTO_SHIELD_WOODEN_LARGE, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = cleric
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory_buy(PROTO_CLOAK_GREEN, npc)
		#item_create_in_inventory(const_proto_cloth.PROTO_CLOTH_CIRCLET_HOODLESS, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_MORNINGSTAR, npc)
		item_create_in_inventory_buy(PROTO_SHIELD_WOODEN_SMALL, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_CROSSBOW_LIGHT, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory(PROTO_WAND_OF_CURE_LIGHT_WOUNDS, npc)
		wand = item_create_in_inventory_buy(PROTO_WAND_OF_CURE_LIGHT_WOUNDS, npc, 140, 0.5)
		if (wand):
			wand.obj_set_int(obj_f_item_spell_charges_idx, 25)
		#item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()
	return

def d():
	fighter_bard = game.party[0]
	paladin = game.party[1]
	monk = game.party[2]
	rogue_wizard = game.party[3]

	npc = fighter_bard
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_FINE, npc)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = paladin
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_BROWN, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_GREATSWORD, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = monk
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_MONK_OUTFIT, npc)
		item_create_in_inventory_buy(const_proto_cloth.PROTO_BOOTS_MONK, npc)
		#item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE, npc)
		#item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = rogue_wizard
	if (1==1):
		item_clear_all(npc)
		item_create_in_inventory(PROTO_ARMOR_STUDDED_LEATHER_ARMOR, npc)
		item_create_in_inventory(PROTO_BOOTS_LEATHER_BOOTS_GREEN, npc)
		item_create_in_inventory(PROTO_WEAPON_SHORTSWORD, npc)
		#item_create_in_inventory(PROTO_SHIELD_WOODEN_SMALL, npc)
		item_create_in_inventory(PROTO_WEAPON_SHORTBOW, npc)
		item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		item_create_in_inventory(PROTO_GENERIC_TOOLS_THIEVES, npc)
		npc.identify_all()
		npc.item_wield_best_all()
	return

def del2():
	fighter_bard = game.party[0]
	paladin = game.party[1]
	monk = game.party[2]
	rogue_wizard = game.party[3]

	npc = fighter_bard
	if (1==1):
		#item_clear_all(npc)
		item_create_in_inventory_buy(PROTO_ARMOR_LEATHER_ARMOR_MASTERWORK, npc)
		item_create_in_inventory_buy(PROTO_WAND_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = paladin
	if (1==1):
		item_create_in_inventory_buy(PROTO_ARMOR_FULL_PLATE_MASTERWORK, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory_buy(PROTO_SHIELD_WOODEN_SMALL, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = monk
	if (1==1):
		npc.identify_all()

	npc = rogue_wizard
	if (1==1):
		wand = item_create_in_inventory_buy(PROTO_WAND_OF_MAGIC_MISSILES_1ST, npc)
		npc.identify_all()
		npc.item_wield_best_all()
	return

def elv2():
	wizard = game.party[0]
	barbarian = game.party[1]
	fighter = game.party[2]
	cleric = game.party[3]

	npc = wizard
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory_buy(const_proto_cloth.PROTO_CLOTH_LEATHER_CLOTHING, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_LEATHER_BOOTS_GREEN, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_CROSSBOW_LIGHT_MASTERWORK, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 100)
		wand = item_create_in_inventory_buy(PROTO_WAND_OF_MAGIC_MISSILES_1ST, npc)
		
		npc.identify_all()
		npc.item_wield_best_all()

	npc = barbarian
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory_buy(PROTO_ARMOR_BREASTPLATE_MASTERWORK, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_GREATAXE_MASTERWORK, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_LONGBOW_COMPOSITE_16_MASTERWORK, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 100)
		item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = fighter
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory(PROTO_ARMOR_FULL_PLATE_MASTERWORK, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory_buy(PROTO_LONGSWORD_MASTERWORK, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_SHORTSWORD_MASTERWORK, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_LONGBOW, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_ARROW_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory_buy(PROTO_POTION_OF_CURE_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()

	npc = cleric
	if (1==1):
		#item_clear_all(npc)
		item_clear_by_proto(npc, const_proto_cloth.PROTO_CLOTH_GARB_BROWN)
		item_create_in_inventory(PROTO_ARMOR_FULL_PLATE_MASTERWORK, npc)
		item_create_in_inventory_buy(PROTO_BOOTS_BREASTPLATE_BOOTS, npc)
		item_create_in_inventory_buy(PROTO_SHIELD_WOODEN_SMALL, npc)
		item_create_in_inventory_buy(PROTO_WEAPON_CROSSBOW_LIGHT_MASTERWORK, npc)
		item = item_create_in_inventory_buy(PROTO_AMMO_BOLT_QUIVER, npc)
		if (item):
			item.obj_set_int(obj_f_ammo_quantity, 50)
		item_create_in_inventory_buy(PROTO_WAND_OF_CURE_LIGHT_WOUNDS, npc)
		item_create_in_inventory_buy(PROTO_WAND_OF_INFLICT_LIGHT_WOUNDS, npc)
		npc.identify_all()
		npc.item_wield_best_all()
	return
