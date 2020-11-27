from toee import *
from debugg import *
from utils_obj import *
from const_toee import *
from utils_item import *
from utils_npc import *
from const_proto_armor import *
from const_proto_weapon import *
from const_proto_containers import *
from math import radians
from const_proto_cloth import *

# DAEMON
def cormyr_lor_san_new_map( attachee, triggerer ):
	#breakp("cormyr_lor_san_new_map")

	do_hook_doors()
	do_setup_chests()
	return SKIP_DEFAULT

def do_hook_doors():
	breakp("do_hook_doors")
	for obj in game.obj_list_range(game.party[0].location, 200, OLC_PORTAL ):
		assert isinstance(obj, PyObjHandle)
		obj_scripts_clear(obj)
		obj.scripts[sn_use] = 6112
		obj.scripts[sn_trap] = 6110 # daemon ref
	return SKIP_DEFAULT

# DOOR
def door_san_use( attachee, triggerer, already_used, marker):
	if (already_used): return 1 # should_destroy

	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)

	if (marker == 11): #L1Door1
		do_encounter_l1()
	return 1 # should_destroy

def do_encounter_l1():
	create_guard_at(sec2loc(459, 523))
	create_guard_at(sec2loc(459, 522))
	create_shadowslain_lizardfolk_at(sec2loc(459, 520))
	create_shadowslain_lizardfolk_at(sec2loc(459, 519))
	create_will_o_wisp_at(sec2loc(439, 524))
	return

def do_encounter_l1a():
	create_shadar_kai_at(sec2loc(470, 523))
	create_shadar_kai_at(sec2loc(472, 508))
	create_shadar_kai_at(sec2loc(468, 507))
	create_kithguard_at(sec2loc(457, 508))
	return

def create_guard_at(loc):
	PROTO_NPC_MAN = 14831 #14000
	#newDescription = game.make_custom_name('Gatehouse Guard')
	newDescription = 14007
	npc = game.obj_create(PROTO_NPC_MAN, loc) # man

	npc.obj_set_int(obj_f_critter_description_unknown, newDescription)
	npc.obj_set_int(obj_f_description_correct, newDescription)

	npc_feats_print(npc)
	#breakp("npc_feats_print")
	obj_scripts_clear(npc)
	item_clear_all(npc)
	# armor
	item_create_in_inventory(PROTO_ARMOR_LEATHER_ARMOR_MASTERWORK, npc)
	# helm
	item_create_in_inventory(PROTO_HELMS_LEATHER_CAP, npc)
	# hands
	item_create_in_inventory(PROTO_GLOVES_PADDED_TAN, npc)
	# boots
	item_create_in_inventory(PROTO_BOOTS_PADDED_TAN, npc)
	# melee
	item_create_in_inventory(PROTO_WEAPON_SHORTSWORD, npc)
	# ranged
	item_create_in_inventory(PROTO_WEAPON_SHORTBOW_COMPOSITE_12_MASTERWORK, npc)
	item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
	item.obj_set_int(obj_f_ammo_quantity, 40)
	#item = item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER_OF_PIXIE_SLEEP_ARROWS, npc)
	#item.obj_set_int(obj_f_ammo_quantity, 1)
	npc.item_wield_best_all()

	npc.feat_add(feat_point_blank_shot, 0)
	npc.feat_add(feat_precise_shot, 0)
	npc.feat_add(feat_improved_precise_shot, 0) # specifically for this encounter
	
	#npc.feat_add(feat_sneak_attack, 0)
	#npc.condition_add_with_args("Sneak_Attack", 0, 0)
	#npc.condition_add_with_args("Sneak_Attack_Ex", 0, 0)
	#npc.condition_add_with_args("Rogue", 0, 0)#check!

	npc.stat_base_set(stat_strength, 13)
	npc.stat_base_set(stat_dexterity, 15)
	npc.stat_base_set(stat_constitution, 14)
	npc.stat_base_set(stat_intelligence, 12)
	npc.stat_base_set(stat_wisdom, 10)
	npc.stat_base_set(stat_charisma, 8)

	npc.make_class(stat_level_rogue, 1)
	rogLvl = npc.stat_level_get(stat_level_rogue)

	dex = (npc.stat_level_get(stat_dexterity) - 10) / 2
	wis = (npc.stat_level_get(stat_wisdom) - 10) / 2
	inte = (npc.stat_level_get(stat_intelligence) - 10) / 2

	npc.skill_ranks_set(skill_hide, 6 - dex)
	npc.skill_ranks_set(skill_listen, 4 - wis)
	npc.skill_ranks_set(skill_move_silently, 6 - dex)
	npc.skill_ranks_set(skill_spot, 4 - wis)
	npc.skill_ranks_set(skill_tumble, 6 - dex)


	#print("stat_level_rogue: {}".format(rogLvl))
	#breakp("rogLvl")
	npc.npc_flag_unset(ONF_NO_ATTACK)
	npc_generate_hp(npc)
	npc_money_set(npc, 31*gp)
	npc.obj_set_int(obj_f_npc_challenge_rating, 1)
	npc.scripts[sn_start_combat] = 6111
	npc.npc_flag_set(ONF_KOS)
	npc.faction_add(1)
	npc.obj_set_int(obj_f_critter_strategy, 10) # sniper
	return npc

def create_shadowslain_lizardfolk_at(loc):
	PROTO_NPC_SHADOWSLAIN_LIZARDFOLK = 14888
	#newDescription = game.make_custom_name('Shadowslain Lizardfolk')
	newDescription = 14014
	npc = game.obj_create(PROTO_NPC_SHADOWSLAIN_LIZARDFOLK, loc)

	npc.obj_set_int(obj_f_critter_description_unknown, newDescription)
	npc.obj_set_int(obj_f_description_correct, newDescription)

	#npc_feats_print(npc)
	#breakp("npc_feats_print")
	obj_scripts_clear(npc)
	item_clear_all(npc)
	npc.item_wield_best_all()
	npc.faction_add(1)
	return npc


def create_will_o_wisp_at(loc):
	PROTO_NPC_WILL_O_WISP = 14291
	#newDescription = game.make_custom_name('Shadowslain Lizardfolk')
	npc = game.obj_create(PROTO_NPC_WILL_O_WISP, loc)

	#npc.obj_set_int(obj_f_critter_description_unknown, newDescription)
	#npc.obj_set_int(obj_f_description_correct, newDescription)

	#npc_feats_print(npc)
	#breakp("npc_feats_print")
	obj_scripts_clear(npc)
	item_clear_all(npc)
	npc.item_wield_best_all()
	npc.faction_add(1)
	return npc

def create_shadar_kai_at(loc, make_inentory = 1):
	PROTO_NPC_SHADAR_KAI = 14832
	#newDescription = game.make_custom_name('Shadar Kai')
	npc = game.obj_create(PROTO_NPC_SHADAR_KAI, loc) # man
	item_clear_all(npc)

	if (make_inentory):
		# armor
		item_create_in_inventory(PROTO_ARMOR_STUDDED_LEATHER_ARMOR_MASTERWORK, npc)
		# helm
		item_create_in_inventory(PROTO_HELM_HOODLESS_CIRCLET, npc)
		# hands
		item_create_in_inventory(PROTO_GLOVES_PADDED_TAN, npc)
		# boots
		item_create_in_inventory(PROTO_BOOTS_PADDED_TAN, npc)
		# melee
		weapon_primary = item_create_in_inventory(PROTO_WEAPON_SPIKED_CHAIN, npc)
		# ranged
		#item_create_in_inventory(PROTO_WEAPON_SHORTBOW, npc)
		#item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
		item_create_in_inventory(PROTO_CLOAK_BLACK, npc)
		# wield best
		npc.item_wield_best_all()
		npc.item_wield(weapon_primary, item_wear_weapon_primary)

	#npc.feat_add(feat_point_blank_shot, 0)
	#npc.feat_add(feat_precise_shot, 0)
	#npc.feat_add(feat_improved_precise_shot, 0) # specifically for this encounter
	
	#npc.feat_add(feat_sneak_attack, 0)
	npc.condition_add_with_args("AI_Improved_Trip_Aoo", 0, 0)
	#npc.condition_add_with_args("Sneak_Attack_Ex", 0, 0)
	#npc.condition_add_with_args("Rogue", 0, 0)#check!

	#dex = npc.stat_level_get(stat_dexterity)
	#print("shadar_kai dex: {}".format(dex))
	#breakp("shadar_kai 1")

	dex = (npc.stat_level_get(stat_dexterity) - 10) / 2
	wis = (npc.stat_level_get(stat_wisdom) - 10) / 2
	inte = (npc.stat_level_get(stat_intelligence) - 10) / 2

	npc.skill_ranks_set(skill_hide, 9 - dex)
	npc.skill_ranks_set(skill_listen, 8 - wis)
	npc.skill_ranks_set(skill_move_silently, 9 - dex)
	npc.skill_ranks_set(skill_search, 7 - inte)
	npc.skill_ranks_set(skill_spot, 8 - wis)
	npc.skill_ranks_set(skill_wilderness_lore, 6 - wis)
	npc.skill_ranks_set(skill_tumble, 1)

	npc_generate_hp(npc)
	npc_money_set(npc, 31*gp)
	#breakp("shadar_kai 2")
	#npc.obj_set_int(obj_f_npc_challenge_rating, 1)
	npc.scripts[sn_start_combat] = 6111 # sneak
	#npc.npc_flag_set(ONF_KOS)
	npc.faction_add(1)
	#breakp("shadar_kai end")
	return npc

def create_kithguard_at(loc):
	#breakp("create_kithguard_at 1")
	npc = create_shadar_kai_at(loc, 0)
	#breakp("create_kithguard_at 2")

	#newDescription = game.make_custom_name('Kithguard Maurran')
	newDescription = 14018
	npc.obj_set_int(obj_f_critter_description_unknown, newDescription)
	npc.obj_set_int(obj_f_description_correct, newDescription)

	# armor
	item_create_in_inventory(PROTO_ARMOR_STUDDED_LEATHER_ARMOR_PLUS_1, npc)
	# helm
	item_create_in_inventory(PROTO_HELM_HOODLESS_CIRCLET, npc)
	# hands
	item_create_in_inventory(PROTO_GLOVES_PADDED_TAN, npc)
	# boots
	item_create_in_inventory(PROTO_BOOTS_PADDED_TAN, npc)
	# melee
	weapon_primary = item_create_in_inventory(PROTO_WEAPON_SPIKED_CHAIN_MASTERWORK, npc)
	# ranged
	#item_create_in_inventory(PROTO_WEAPON_SHORTBOW_COMPOSITE_12_MASTERWORK, npc)
	#item_create_in_inventory(PROTO_AMMO_ARROW_QUIVER, npc)
	item_create_in_inventory(PROTO_CLOAK_RED, npc)
	# wield best
	npc.item_wield_best_all()
	#breakp("create_kithguard_at 3")
	npc.item_wield(weapon_primary, item_wear_weapon_primary)

	npc.feat_add(feat_combat_reflexes, 0)

	npc.stat_base_set(stat_strength, 15)
	npc.stat_base_set(stat_dexterity, 18)
	npc.stat_base_set(stat_constitution, 12)
	npc.stat_base_set(stat_intelligence, 12)
	npc.stat_base_set(stat_wisdom, 8)
	npc.stat_base_set(stat_charisma, 8)

	dex = (npc.stat_level_get(stat_dexterity) - 10) / 2
	wis = (npc.stat_level_get(stat_wisdom) - 10) / 2
	inte = (npc.stat_level_get(stat_intelligence) - 10) / 2
	cha = (npc.stat_level_get(stat_charisma) - 10) / 2

	npc.skill_ranks_set(skill_balance, 9 - dex)
	npc.skill_ranks_set(skill_hide, 15 - dex)
	npc.skill_ranks_set(skill_intimidate, 6 - cha)
	npc.skill_ranks_set(skill_listen, 11 - wis)
	npc.skill_ranks_set(skill_move_silently, 15 - dex)
	npc.skill_ranks_set(skill_open_lock, 9 - dex)
	npc.skill_ranks_set(skill_search, 7 - inte)
	npc.skill_ranks_set(skill_spot, 11 - wis)
	npc.skill_ranks_set(skill_wilderness_lore, 5 - wis)
	npc.skill_ranks_set(skill_tumble, 9 - dex)

	npc.make_class(stat_level_rogue, 3)
	#breakp("create_kithguard_at npc_generate_hp")
	npc_generate_hp(npc)
	return npc

def do_setup_chests():
	obj = game.obj_create(PROTO_CONTAINER_CHEST_WOODEN_MEDIUM, sec2loc(453, 513))
	obj.rotation = radians(135)
	obj_scripts_clear(obj)
	obj.scripts[sn_use] = 6112
	return

def chest_san_use( attachee, triggerer, already_used, marker):
	if (already_used): return RUN_DEFAULT

	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)

	#if (marker == 11): #L1Door1
	do_encounter_l1a()
	return SKIP_DEFAULT
