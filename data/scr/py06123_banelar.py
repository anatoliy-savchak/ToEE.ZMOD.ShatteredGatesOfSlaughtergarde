from toee import *
from debugg import *
import utils_obj
from const_toee import *
import utils_storage
import utils_tactics
import utils_spell

def banelar_init_storage(npc):
	storage = utils_storage.obj_storage(npc)
	o = BanelarStorage("banelar")
	storage.data[o.name] = o
	return

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	#breakp("san_enter_combat banelar start")
	utils_storage.obj_storage(attachee).data["banelar"].round = 0


	stat_class = stat_level_wizard
	spell_level = 3
	npc_spell_ensure(attachee, spell_mage_armor, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_stinking_cloud, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_lightning_bolt, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_fireball, stat_class, spell_level)
	spell_level = 2
	npc_spell_ensure(attachee, spell_invisibility, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_melfs_acid_arrow, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_tashas_hideous_laughter, stat_class, spell_level)
	
	stat_class = stat_level_cleric
	spell_level = 3
	npc_spell_ensure(attachee, spell_bestow_curse, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_cure_serious_wounds, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_summon_monster_iii, stat_class, spell_level)
	spell_level = 2
	npc_spell_ensure(attachee, spell_death_knell, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_hold_person, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_protection_from_good, stat_class, spell_level)
	attachee.spells_pending_to_memorized()
	
	#breakp("san_enter_combat banelar end")
	return RUN_DEFAULT

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	ban = utils_storage.obj_storage(attachee).data["banelar"]
	assert isinstance(ban, BanelarStorage)
	ban.round += 1
	print("round: {}".format(ban.round))
	#breakp("san_start_combat banelar")
	spellId = 0
	strat = []

	tac = utils_tactics.TacticsHelper("banelar")
	if (ban.round == 1):
		tac.add_target_self()
		tac.add_cast_single(utils_spell.spell_name(spell_mage_armor), "class_wizard", "3")
		tac.add_cast_single(utils_spell.spell_name(spell_protection_from_good), "class_cleric", "2")
	elif (ban.round == 2):
		tac.add_target_closest()
		tac.add_cast_single(utils_spell.spell_name(spell_bestow_curse), "class_cleric", "3")
		tac.add_attack()
	else:
		tac.add_target_closest()
		tac.add_attack()

	if (tac.count >0):
		tac.make_name()
		strat = tac.custom_tactics
		print("set strategy: {}".format(strat))
		attachee.ai_strategy_set_custom(strat)
	print("san_start_combat end")
	breakp("san_start_combat end")
	return RUN_DEFAULT

def san_spell_cast(attachee, triggerer, spell):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	if (not game.combat_is_active()): return RUN_DEFAULT
	#if (triggerer.proto != 14835): return RUN_DEFAULT
	#Spell_Quicken_All did not work
	print("attachee.refresh_turn()")
	attachee.refresh_turn()
	#breakp("san_spall_cast banelar")
	return RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	if (game.combat_is_active()): 
		attachee.scripts[sn_heartbeat] = 0
		return RUN_DEFAULT
	
	ban = utils_storage.obj_storage(attachee).data["banelar"]
	assert isinstance(ban, BanelarStorage)
	if (not ban.has_mage_armor_cast):
		#npc_cast_spell_forced(attachee, attachee, spell_mage_armor, stat_level_wizard, 6)
		ban.has_mage_armor_cast = 1

	v = find_victim_at(attachee, attachee.location)
	print("san_heartbeat found victim - {}".format(v))
	if (not v): return RUN_DEFAULT
	attachee.turn_towards(v)
	print("san_heartbeat attachee.attack {}".format(v))
	attachee.attack(v)
	#npc_cast_spell_forced(attachee, v, spell_magic_missile, stat_level_wizard, 3)

	return RUN_DEFAULT

def do_banelar_stinking_cloud(npc, loc, fire):
	assert isinstance(npc, PyObjHandle)
	victim = find_victim_at(npc, loc)
	print(victim)
	#breakp("do_banelar_stinking_cloud fire:{}".format(fire))
	if (victim is None): return

	spellId = spell_stinking_cloud
	npc.spell_known_add(spellId, stat_level_wizard, 6)
	npc.spell_memorized_add(spellId, stat_level_wizard, 6)
	npc.spells_pending_to_memorized()

	print("making do_banelar_stinking_cloud")
	if (fire):
		npc.cast_spell(spellId, victim)
		npc.refresh_turn()
	else:
		npc.attack(victim)
	return 1

def find_victim_at(npc, loc):
	assert isinstance(npc, PyObjHandle)
	victim = None
	for i in range(1, 8):
		victims = game.obj_list_range(loc, 5*i, OLC_PC)
		if (len(victims) == 0): continue
		for v in victims:
			if (not npc.has_los(v)): continue
			victim = v
			break
		if (not victim is None):
			break
	return victim

def npc_cast_spell_forced(npc, target, spell_id, stat_class, spell_level):
	assert isinstance(npc, PyObjHandle)
	assert isinstance(target, PyObjHandle)
	npc.spell_known_add(spell_id, stat_class, spell_level)
	npc.spell_memorized_add(spell_id, stat_class, spell_level)
	npc.spells_pending_to_memorized()
	npc.cast_spell(spell_id, target)
	game.new_sid = 0
	#npc.spells_pending_to_memorized()
	return 1

def get_tactics_spell_cast(spell_name, cast_method, class_name, class_level):
	tactics_name = "banelar {}".format(spell_name)
	spell_code = "'{}' {} {}".format(spell_name, class_name, class_level)
	strat = [tactics_name \
			, cast_method, "", spell_code \
			, "attack", "", "" \
			]
	return strat

def get_tactics_spell_cast_self(spell_name, cast_method, class_name, class_level):
	tactics_name = "banelar {}".format(spell_name)
	spell_code = "'{}' {} {}".format(spell_name, class_name, class_level)
	strat = [tactics_name \
			, "target self", "", "" \
			, cast_method, "", spell_code \
			, "target closest", "", "" \
			, "attack", "", "" \
			]
	return strat

class BanelarStorage(object):
	def __init__(self, aname):
		self.name = aname
		self.round = 0
		self.spells_acquired = 0
		self.has_mage_armor_cast = 0
		return

def npc_spell_ensure(npc, spell_id, stat_class, spell_level, memorize = 0):
	assert isinstance(npc, PyObjHandle)
	npc.spell_known_add(spell_id, stat_class, spell_level)
	npc.spell_memorized_add(spell_id, stat_class, spell_level)
	if (memorize):
		npc.spells_pending_to_memorized()
	return 1
