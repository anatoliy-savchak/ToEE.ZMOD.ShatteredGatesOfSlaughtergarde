from toee import *
from debugg import *
from obj_utils import *
from const_toee import *
from item_utils import *
from npc_utils import *
from const_proto_armor import *
from const_proto_weapon import *
from const_proto_items import *

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