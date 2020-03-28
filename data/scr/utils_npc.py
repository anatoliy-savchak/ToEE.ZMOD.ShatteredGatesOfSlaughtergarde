from toee import *
from debugg import breakp
from const_toee import *
import tpdp

def npc_feats_print(npc):
	assert isinstance(npc, PyObjHandle)
	feats = npc.feats
	for f in feats:
		print("Feat Code: {}".format(f))
		print("Feat Name{}".format(game.get_feat_name(f)))
	return

def npc_generate_hp(npc):
	assert isinstance(npc, PyObjHandle)
	npc.obj_set_int(obj_f_hp_pts, -65535)
	hp = npc.stat_level_get(stat_hp_current)
	#print("Current HP: {}".format(hp))
	return hp

def npc_money_set(npc, copper):
	assert isinstance(npc, PyObjHandle)
	assert isinstance(copper, int)
	diff = npc.money_get()
	diff = copper - diff
	npc.money_adj(diff)
	return diff

def npc_stat_generate(npc):
	assert isinstance(npc, PyObjHandle)
	result = ""
	breakp("npc_stat_generate")

	hp = npc.stat_level_get(stat_hp_max)
	hd = npc.hit_dice_num
	result = "hp {} ({} HD)".format(hp, hd)

	q = EK_Q_Critter_Has_Condition - EK_Q_Helpless
	has_fast_healing = npc.d20_query_has_condition("Monster Fast Healing")
	if (has_fast_healing):
		result = result + " fast healing"
	result = result + "\p"

	gender = npc.stat_level_get(stat_gender)
	if (gender == 0):
		result = result + "Male"
	elif (gender == 1):
		result = result + "Female"

	return result

def npc_spell_ensure(npc, spell_id, stat_class, spell_level, memorize = 0):
	assert isinstance(npc, PyObjHandle)
	print("{}.npc_spell_ensure(spell_id: {}, stat_class: {}, spell_level: {})".format(npc, spell_id, stat_class, spell_level))
	npc.spell_known_add(spell_id, stat_class, spell_level)
	npc.spell_memorized_add(spell_id, stat_class, spell_level)
	if (memorize):
		npc.spells_pending_to_memorized()
	return 1

def npc_skill_ensure(npc, skill_id, target_skill_value):
	assert isinstance(npc, PyObjHandle)
	value = npc.skill_level_get(skill_id)
	delta = target_skill_value - value
	npc.skill_ranks_set(skill_id, delta)
	return delta