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
	o = utils_storage.obj_storage(attachee).data["banelar"]
	o.round = 0
	o.free_spell_casts_left = 1

	stat_class = stat_level_wizard
	spell_level = 6
	npc_spell_ensure(attachee, spell_mage_armor, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_stinking_cloud, stat_class, spell_level)

	npc_spell_ensure(attachee, spell_lightning_bolt, stat_class, spell_level)
	# bug will make it cast two time due to spell_quicken_all
	#npc_spell_ensure(attachee, spell_lightning_bolt, stat_class, spell_level)
	#spell_level = 2
	npc_spell_ensure(attachee, spell_invisibility, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_melfs_acid_arrow, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_tashas_hideous_laughter, stat_class, spell_level)
	#spell_level = 1
	npc_spell_ensure(attachee, spell_color_spray, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_shocking_grasp, stat_class, spell_level)
	# bug will make it cast two time due to spell_quicken_all
	#npc_spell_ensure(attachee, spell_color_spray, stat_class, spell_level)
	
	stat_class = stat_level_cleric
	spell_level = 6
	npc_spell_ensure(attachee, spell_bestow_curse, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_cure_serious_wounds, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_cure_serious_wounds, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_summon_monster_iii, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_summon_monster_iii, stat_class, spell_level)
	#spell_level = 2
	npc_spell_ensure(attachee, spell_death_knell, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_hold_person, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_protection_from_good, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_summon_monster_ii, stat_class, spell_level)
	#spell_level = 1
	npc_spell_ensure(attachee, spell_shield_of_faith, stat_class, spell_level)
	npc_spell_ensure(attachee, spell_obscuring_mist, stat_class, spell_level)
	
	attachee.spells_pending_to_memorized()
	
	#attachee.set_initiative(50)
	#game.update_combat_ui()	
	#breakp("san_enter_combat banelar end")
	return RUN_DEFAULT

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	ban = utils_storage.obj_storage(attachee).data["banelar"]
	assert isinstance(ban, BanelarStorage)
	ban.round += 1
	# Banelar Special Ability
	ban.free_spell_casts_left = 1
	print("round: {}".format(ban.round))

	# reset back, was set to make it go first
	if (attachee.stat_base_get(stat_dexterity) > 30):
		attachee.stat_base_set(stat_dexterity, 13)

	# had to do it due to bug
	if (ban.lightning_bolt_count == 1):
		npc_spell_ensure(attachee, spell_lightning_bolt, stat_level_wizard, 6)
		npc_spell_ensure(attachee, spell_color_spray, stat_level_wizard, 6)

	#breakp("san_start_combat banelar")
	strat = []
	class_wizard = "class_wizard"
	class_cleric = "class_cleric"
	caster_level = 6

	tac = utils_tactics.TacticsHelper("banelar")
	#if (ban.round == 1):
	#	tac.add_target_self()
	#	tac.add_cast_single(utils_spell.spell_name(spell_mage_armor), class_wizard, "3")
	#	tac.add_cast_single(utils_spell.spell_name(spell_protection_from_good), class_cleric, "2")
	# tac.add_cast_single(utils_spell.spell_name(spell_summon_monster_iii), class_cleric, "3")
	#tac.add_cast_party(utils_spell.spell_name(spell_lightning_bolt), class_wizard, "3")
	while(1==1):
		if (ban.round == 1):
			ban.free_spell_casts_left = 2
			tac.add_target_self()
			# this one should have been before encounter
			tac.add_cast_single(utils_spell.spell_name(spell_mage_armor), class_wizard, caster_level)
			tac.add_cast_single(utils_spell.spell_name(spell_shield_of_faith), class_cleric, caster_level)
			tac.add_clear_target()
			tac.add_target_low_ac()
			# Stinking Cloud
			tac.add_cast_fireball(utils_spell.spell_name(spell_stinking_cloud), class_wizard, caster_level)
			tac.add_clear_target()
			break

		hp_current = attachee.stat_level_get(stat_hp_current)
		if (ban.already_retreated == 0 and hp_current < 60):
			print("RETREAT")
			ban.already_retreated = 2
			obj_beacon = game.obj_create(14074, utils_obj.sec2loc(497, 486))
			obj_beacon.object_flag_set(OF_DONTDRAW)
			obj_beacon.object_flag_set(OF_CLICK_THROUGH)
			obj_beacon.move(utils_obj.sec2loc(497, 486),0,0)
			can_path = attachee.can_find_path_to_obj(obj_beacon, 0)
			if (not can_path):
				print("cannot find path!")
				breakp("attachee.can_find_path_to_obj failed")
				obj_beacon.destroy()
			else:
				obj_beacon.stat_base_set( stat_dexterity, -30 )
				obj_beacon.faction_add(1)
				obj_beacon.attack(game.leader)
				obj_beacon.add_to_initiative()
				game.timevent_add(on_kill_beacon_obj, ( obj_beacon), 1000, 1)

				tac.add_clear_target()
				tac.add_target_friend_low_ac()
				tac.add_approach()
				tac.add_clear_target()

				tac.add_target_self()
				tac.add_cast_single(utils_spell.spell_name(spell_invisibility), class_wizard, caster_level)

				#tac.add_target_self()
				#tac.add_cast_single(utils_spell.spell_name(spell_cure_serious_wounds), class_cleric, "3")
				tac.add_clear_target()
				break

		if ((ban.round >= caster_level or ban.cured_s_times or ban.already_retreated) and ban.summoned_times < 2):
			ban.summoned_times += 1
			tac.add_target_closest()
			tac.add_cast_single(utils_spell.spell_name(spell_summon_monster_iii), class_cleric, caster_level)
			if (hp_current < 60 and ban.cured_s_times < 2):
				ban.cured_s_times += 1
				tac.add_target_self()
				tac.add_cast_single(utils_spell.spell_name(spell_cure_serious_wounds), class_cleric, caster_level)
				tac.add_clear_target()
			elif (ban.summoned_times < 2):
				ban.summoned_times += 1
				tac.add_target_closest()
				tac.add_cast_single(utils_spell.spell_name(spell_summon_monster_iii), class_cleric, caster_level)
				tac.add_five_foot_step()
			else:
				tac.add_target_closest()
				tac.add_attack()
			break

		if (not ban.already_cursed):
			ban.already_cursed = 1
			tac.add_target_closest()
			tac.add_cast_single(utils_spell.spell_name(spell_bestow_curse), class_cleric, caster_level)
			if (hp_current < 60 and ban.cured_s_times < 2):
				ban.cured_s_times += 1
				tac.add_target_self()
				tac.add_cast_single(utils_spell.spell_name(spell_cure_serious_wounds), class_cleric, caster_level)
				tac.add_clear_target()
				tac.add_five_foot_step()
			else:
				tac.add_target_closest()
				tac.add_attack()
			break

		if (hp_current < 60 and ban.cured_s_times < 2):
			ban.cured_s_times += 1
			tac.add_target_self()
			tac.add_cast_single(utils_spell.spell_name(spell_cure_serious_wounds), class_cleric, caster_level)
			tac.add_clear_target()
			if (hp_current < 60 and ban.cured_s_times < 2):
				ban.cured_s_times += 1
				tac.add_target_self()
				tac.add_cast_single(utils_spell.spell_name(spell_cure_serious_wounds), class_cleric, caster_level)
				tac.add_clear_target()
				tac.add_five_foot_step()
			else:
				tac.add_target_closest()
				tac.add_attack()
			break

		if (ban.lightning_bolt_count < 2):
			ban.lightning_bolt_count += 1
			tac.add_target_closest()
			tac.add_cast_party(utils_spell.spell_name(spell_lightning_bolt), class_wizard, caster_level)
			tac.add_cast_party(utils_spell.spell_name(spell_color_spray), class_wizard, caster_level)
			#tac.add_attack()
			break

		if (not ban.hold_person_used):
			ban.hold_person_used += 1
			tac.add_target_closest()
			tac.add_cast_single(utils_spell.spell_name(spell_hold_person), class_cleric, caster_level)
			tac.add_cast_single(utils_spell.spell_name(spell_summon_monster_ii), class_cleric, caster_level)
			tac.add_five_foot_step()
			#tac.add_attack()
			break

		if (not ban.shocking_grasp_used):
			ban.shocking_grasp_used += 1
			tac.add_target_high_ac()
			tac.add_cast_single(utils_spell.spell_name(spell_tashas_hideous_laughter), class_wizard, caster_level)
			tac.add_target_closest()
			tac.add_cast_single(utils_spell.spell_name(spell_shocking_grasp), class_wizard, caster_level)
			tac.add_approach()
			tac.add_attack()
			break

		if (not ban.obscuring_mist_used):
			ban.obscuring_mist_used += 1
			tac.add_target_closest()
			tac.add_cast_party(utils_spell.spell_name(spell_obscuring_mist), class_cleric, caster_level)
			tac.add_attack()
			break

		tac.add_target_closest()
		tac.add_attack()
		break

	if (tac.count > 0):
		tac.make_name()
		strat = tac.custom_tactics
		print("set strategy: {}".format(strat))
		attachee.ai_strategy_set_custom(strat)
	print("san_start_combat end")
	#breakp("san_start_combat end")
	return RUN_DEFAULT

def san_spell_cast(attachee, triggerer, spell):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	if (not game.combat_is_active()): return RUN_DEFAULT
	print("SAN_SPELL_CAST attachee: {}, triggerer: {}, spell: {}".format(attachee, triggerer, spell))
	if (triggerer.proto != 14835): 
		print("triggerer.proto != 14835 exit...")
		return RUN_DEFAULT
	
	storage = utils_storage.obj_storage(triggerer)
	if ("banelar" in storage.data):
		o = utils_storage.obj_storage(triggerer).data["banelar"]
		if (not o is None and o.free_spell_casts_left > 0):
			o.free_spell_casts_left -= 1
			triggerer.refresh_turn()
			print("TRIGGERER.REFRESH_TURN()")
	#breakp("san_spall_cast banelar")
	return RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	if (game.combat_is_active()): 
		attachee.scripts[sn_heartbeat] = 0
		return RUN_DEFAULT
	
	v = find_victim_at(attachee, attachee.location)
	print("san_heartbeat found victim - {}".format(v))
	if (not v): return RUN_DEFAULT
	attachee.turn_towards(v)
	print("san_heartbeat attachee.attack {}".format(v))
	attachee.set_initiative(30)
	attachee.attack(v)
	game.update_combat_ui()	
	#npc_cast_spell_forced(attachee, v, spell_magic_missile, stat_level_wizard, 3)

	return RUN_DEFAULT

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

class BanelarStorage(object):
	def __init__(self, aname):
		self.name = aname
		self.round = 0
		self.spells_acquired = 0
		self.has_mage_armor_cast = 0
		self.already_retreated = 0
		self.summoned_times = 0
		self.already_cursed = 0
		self.lightning_bolt_count = 0
		self.free_spell_casts_left = 0
		self.cured_s_times = 0
		self.hold_person_used = 0
		self.shocking_grasp_used = 0
		self.obscuring_mist_used = 0
		return

def npc_spell_ensure(npc, spell_id, stat_class, spell_level, memorize = 0):
	assert isinstance(npc, PyObjHandle)
	npc.spell_known_add(spell_id, stat_class, spell_level)
	npc.spell_memorized_add(spell_id, stat_class, spell_level)
	if (memorize):
		npc.spells_pending_to_memorized()
	return 1

def on_kill_beacon_obj(obj):
	obj.destroy()
	return