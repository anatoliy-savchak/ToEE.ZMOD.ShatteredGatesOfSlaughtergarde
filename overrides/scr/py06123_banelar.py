from toee import *
from debugg import *
import utils_obj
from const_toee import *
import utils_storage
import utils_tactics
import utils_spell
import utils_npc
import utils_npc_spells
import utils_target_list

def banelar_init_storage(npc):
	storage = utils_storage.obj_storage(npc)
	o = BanelarStorage("banelar")
	storage.data[o.name] = o
	return

def san_exit_combat(attachee, triggerer):
	o = utils_storage.obj_storage(attachee).data["banelar"]
	game.particles_kill(o.part_id_mage_armor)
	return RUN_DEFAULT

def san_enter_combat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	#breakp("san_enter_combat banelar start")
	o = utils_storage.obj_storage(attachee).data["banelar"]
	o.round = 0
	o.free_spell_casts_left = 1

	stat_class = stat_level_wizard
	spell_level = 3

	#utils_npc.npc_spell_ensure(attachee, spell_stinking_cloud, stat_class, spell_level)
	#utils_npc.npc_spell_ensure(attachee, spell_mage_armor, stat_class, spell_level)
	#3
	o.spells.add_spell(spell_stinking_cloud, stat_class, spell_level)
	#2
	o.spells.add_spell(spell_lightning_bolt, stat_class, spell_level, 2)
	o.spells.add_spell(spell_invisibility, stat_class, spell_level)
	o.spells.add_spell(spell_melfs_acid_arrow, stat_class, spell_level)
	o.spells.add_spell(spell_tashas_hideous_laughter, stat_class, spell_level)
	#1
	o.spells.add_spell(spell_color_spray, stat_class, spell_level, 2)
	o.spells.add_spell(spell_shocking_grasp, stat_class, spell_level)
	
	stat_class = stat_level_cleric
	#3
	o.spells.add_spell(spell_bestow_curse, stat_class, spell_level)
	o.spells.add_spell(spell_cure_serious_wounds, stat_class, spell_level, 2)
	o.spells.add_spell(spell_summon_monster_iii, stat_class, spell_level, 2)
	#2
	o.spells.add_spell(spell_death_knell, stat_class, spell_level)
	o.spells.add_spell(spell_hold_person, stat_class, spell_level)
	o.spells.add_spell(spell_protection_from_good, stat_class, spell_level)
	o.spells.add_spell(spell_summon_monster_ii, stat_class, spell_level)
	#spell_level = 1
	o.spells.add_spell(spell_shield_of_faith, stat_class, spell_level)
	o.spells.add_spell(spell_obscuring_mist, stat_class, spell_level)
	#o.spells.memorize_all(attachee)
	
	#attachee.spells_pending_to_memorized()
	o.part_id_mage_armor = do_spell_effect_mage_armor(attachee, spell_level)
	return RUN_DEFAULT

def san_start_combat(attachee, triggerer):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	ban = utils_storage.obj_storage(attachee).data["banelar"]
	assert isinstance(ban, BanelarStorage)
	ban.round += 1
	tac = utils_tactics.TacticsHelper("banelar")

	# Banelar Special Ability
	ban.free_spell_casts_left = 1
	strat = []
	caster_level = 3
	#breakp("san_start_combat")
	while(1==1):
		tl = utils_target_list.AITargetList(attachee, 1, 0, utils_target_list.AITargetMeasure.by_has_los()).rescan()
		if (not len(tl.list)):
			tac.add_five_foot_step()
			if (ban.spells.get_spell_count(spell_shield_of_faith)):
				tac.add_target_self()
				tac.add_cast_single_code(ban.spells.prep_spell(attachee, spell_shield_of_faith, 1))
				tac.add_target_closest()
				tac.add_approach()
				tac.add_attack()
				break
			if (ban.spells.get_spell_count(spell_summon_monster_iii)):
				tac.add_target_closest()
				tac.add_five_foot_step()
				tac.add_cast_single_code(ban.spells.prep_spell(attachee, spell_summon_monster_iii, 1))
				tac.add_clear_target()
				tac.add_target_closest()
				tac.add_attack()
				break


		if (ban.spells.get_spell_count(spell_stinking_cloud)):
			tac.add_target_closest()
			tac.add_five_foot_step()
			tac.add_cast_fireball_code(ban.spells.prep_spell(attachee, spell_stinking_cloud, 1))
			tac.add_attack()
			break

		hp_current = attachee.stat_level_get(stat_hp_current)
		if (ban.already_retreated == 0 and hp_current < 60):
			print("RETREAT")
			ban.already_retreated = 1
			tac.add_target_self()
			tac.add_cast_single_code(ban.spells.prep_spell(attachee, spell_invisibility, 1))
			tac.add_goto(497, 486)
			tac.add_target_self()
			tac.add_cast_single_code(ban.spells.prep_spell(attachee, spell_cure_serious_wounds, 1))
			tac.add_stop()
			break

		if (ban.spells.get_spell_count(spell_bestow_curse)):
			#breakp("measures")
			tac.add_target_closest()
			tac.add_cast_single_code(ban.spells.prep_spell(attachee, spell_bestow_curse, 1))
			tac.add_attack()
			break

		if (ban.spells.get_spell_count(spell_lightning_bolt)):
			tac.add_target_closest()
			tac.add_five_foot_step()
			tac.add_target_closest()
			tac.add_cast_party_code(ban.spells.prep_spell(attachee, spell_lightning_bolt, 1))
			tac.add_attack()
			break

		if ((ban.round >= caster_level) and ban.spells.get_spell_count(spell_summon_monster_iii)):
			tac.add_target_closest()
			tac.add_five_foot_step()
			tac.add_cast_single_code(ban.spells.prep_spell(attachee, spell_summon_monster_iii, 1))
			tac.add_clear_target()
			tac.add_target_closest()
			tac.add_attack()
			break

		if (hp_current < 60 and ban.spells.get_spell_count(spell_cure_serious_wounds)):
			tac.add_target_closest()
			tac.add_five_foot_step()
			tac.add_clear_target()
			tac.add_target_self()
			tac.add_cast_single_code(ban.spells.prep_spell(attachee, spell_cure_serious_wounds, 1))
			tac.add_target_closest()
			tac.add_attack()
			break

		if (ban.spells.get_spell_count(spell_hold_person)):
			tac.add_target_closest()
			tac.add_five_foot_step()
			tac.add_cast_single_code(ban.spells.prep_spell(attachee, spell_hold_person, 1))
			tac.add_attack()
			break

		if (ban.spells.get_spell_count(spell_color_spray)):
			tac.add_target_closest()
			tac.add_five_foot_step()
			tac.add_cast_area_code(ban.spells.prep_spell(attachee, spell_color_spray, 1))
			tac.add_approach()
			tac.add_attack()
			break

		if (ban.spells.get_spell_count(spell_obscuring_mist)):
			tac.add_target_closest()
			tac.add_five_foot_step()
			tac.add_cast_party_code(ban.spells.prep_spell(attachee, spell_obscuring_mist, 1))
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
	return RUN_DEFAULT

def san_spell_cast(attachee, triggerer, spell):
	assert isinstance(attachee, PyObjHandle)
	assert isinstance(triggerer, PyObjHandle)
	if (not game.combat_is_active()): return RUN_DEFAULT
	print("SAN_SPELL_CAST attachee: {}, triggerer: {}, spell: {}".format(attachee, triggerer, spell))
	if (triggerer.proto != 14835): 
		#print("triggerer.proto != 14835 exit...")
		return RUN_DEFAULT
	
	storage = utils_storage.obj_storage(triggerer)
	if ("banelar" in storage.data):
		o = utils_storage.obj_storage(triggerer).data["banelar"]
		if (not o is None and o.free_spell_casts_left > 0):
			o.free_spell_casts_left -= 1
			triggerer.refresh_turn()
			print("TRIGGERER.REFRESH_TURN()")
	breakp("san_spall_cast banelar")
	return RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	if (game.combat_is_active()): 
		attachee.scripts[sn_heartbeat] = 0
		return RUN_DEFAULT
	
	v = find_victim_at(attachee, attachee.location)
	#print("san_heartbeat found victim - {}".format(v))
	if (not v): return RUN_DEFAULT
	attachee.turn_towards(v)
	#print("san_heartbeat attachee.attack {}".format(v))
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
	def __init__(self, aname = None):
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
		self.color_spray_used = 0
		self.obscuring_mist_used = 0
		self.part_id_mage_armor = 0
		self.spells = utils_npc_spells.NPCSpells()
		return

def do_spell_effect_mage_armor(obj, caster_level):
	assert isinstance(obj, PyObjHandle)
	spell_duration = 600 * caster_level
	armor_bonus = 4
	obj.condition_add_with_args('sp-Mage Armor', spell_mage_armor, spell_duration, armor_bonus)
	# just skip it
	#part_id = game.particles("sp-Mage Armor", obj )
	part_id = 0
	return part_id