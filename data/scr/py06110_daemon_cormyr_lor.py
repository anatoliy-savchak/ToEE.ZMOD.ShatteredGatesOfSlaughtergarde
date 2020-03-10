from toee import *
from debug import *
from obj_utils import *
from toee_const import *
from item_utils import *
from npc_utils import *
from proto_armor_const import *
from proto_weapon_const import *

# SAN hooks
def san_use( attachee, triggerer ):
	assert isinstance(attachee, PyObjHandle)
	if (attachee.type == obj_t_portal):
		return door_san_use(attachee, triggerer)
	return RUN_DEFAULT

# DAEMON
def cormyr_lor_san_new_map( attachee, triggerer ):
	#breakp("cormyr_lor_san_new_map")

	do_daemon_doors()
	return SKIP_DEFAULT

def do_daemon_doors():
	# clear hooks and destroy on open door
	#breakp("do_daemon_doors")
	for obj in game.obj_list_range(game.party[0].location, 200, OLC_PORTAL ):
		assert isinstance(obj, PyObjHandle)
		print("door " + str(obj.proto) + " " + obj.description)
		obj_scripts_clear(obj)
		#st = obj.stat_level_get(stat_hp_max) 
		st = obj.obj_get_int(obj_f_hp_pts)
		print("door stat_hp_max: {}".format(st))
		#if (st == 55):
		#	breakp("stat")
		obj.scripts[sn_use] = 6110
		#obj.scripts[sn_dialog] = 406 #experimenting, will use in the future
	return SKIP_DEFAULT

# DOOR
def door_san_use( attachee, triggerer ):
	assert isinstance(attachee, PyObjHandle)
	print("obj_f_description {}".format(obj_f_description_correct))
	#breakp("cormyr door san_use")

	if (attachee.scripts[sn_dialog] != 0):
		game.party[0].begin_dialog(attachee, 1)
		return SKIP_DEFAULT

	st = attachee.obj_get_int(obj_f_hp_pts)
	obj_scripts_clear(attachee)
	# open, otherwise unfogged glitch
	attachee.portal_toggle_open()
	# destroy
	attachee.destroy()

	#st = attachee.stat_level_get(stat_hp_max) 
	print("door stat_hp_max: {}".format(st))
	if (st == 55): #L1Door1
		do_encounter_l1()
	return SKIP_DEFAULT

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
	newDescription = game.make_custom_name('Gatehouse Guard')
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
	newDescription = game.make_custom_name('Shadowslain Lizardfolk')
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

	newDescription = game.make_custom_name('Kithguard Maurran')
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

def throwbomb():
	loc = sec2loc(459, 523)
	obj = game.obj_create(12676, loc) # Smokestick
	obj.cast_spell(spell_fog_cloud, obj)
	obj.destroy()
	return