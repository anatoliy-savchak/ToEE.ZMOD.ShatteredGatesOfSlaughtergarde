from toee import *
from debugg import breakp
from const_toee import *
import tpdp, utils_obj

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
	value_total = npc.skill_level_get(skill_id)
	ranks = npc.skill_ranks_get(skill_id)
	delta = target_skill_value - value_total
	ranks += delta
	npc.skill_ranks_set(skill_id, ranks)
	return delta

def npc_is_alive(npc, dead_when_negative_hp = 0):
	assert isinstance(npc, PyObjHandle)
	object_flags = npc.object_flags_get()
	if ((object_flags & OF_DESTROYED) or (object_flags & OF_OFF)): return 0
	result = npc.d20_query(Q_Dead)
	if (result): return 0
	result = npc.d20_query(Q_Dying)
	if (result): return 0
	hp = npc.stat_level_get(stat_hp_current)
	if (dead_when_negative_hp and hp < 0):
		return0
	if (hp <= -10): return 0
	return 1

def npc_hp_current_percent(npc):
	assert isinstance(npc, PyObjHandle)
	maxhp = npc.stat_level_get(stat_hp_max)
	hp = npc.stat_level_get(stat_hp_current)
	if (maxhp):
		return 100 * hp / maxhp
	return 100

def npc_find_nearest_pc(npc, distance_ft, should_see):
	assert isinstance(npc, PyObjHandle)
	nearest = None
	nearest_dist = 10000
	for obj in game.obj_list_range(npc.location, distance_ft, OLC_NPC):
		assert isinstance(obj, PyObjHandle)
		if (should_see):
			if (not npc.can_see(obj)): continue
		obj_dist = npc.distance_to(obj)
		if (obj_dist < nearest_dist):
			nearest = obj
			nearest_dist = obj_dist
	return nearest

def print_npc_vicinity(leader = None):
	if (not leader):
		leader = game.leader
	for npc in game.obj_list_vicinity(leader.location, OLC_NPC):
		print("{}: {}, distance: {} or {}".format(npc, npc.id, npc.distance_to(leader), leader.distance_to(npc)))
	return

def print_distances_at_origin(locx, locy):
	print("Distances locx, locy: {}, {}".format(locx, locy))
	loc = utils_obj.sec2loc(locx, locy)
	for npc in game.obj_list_vicinity(loc, OLC_NPC | OLC_PC):
		dist = npc.distance_to(loc)
		print("{}: distance: {:06.2f} | id: {}".format(npc, dist, npc.id))
	return

def find_npc_by_proto(loc, proto):
	for obj in game.obj_list_vicinity(loc, OLC_NPC):
		assert isinstance(obj, PyObjHandle)
		if (obj.proto == proto): return obj
	return OBJ_HANDLE_NULL

def npc_get_cr(npc):
	cr = 0
	if (npc.type == obj_t_npc):
		cr = npc.obj_get_int(obj_f_npc_challenge_rating)
	level_cr = npc.stat_level_get(stat_level)
	result = cr + level_cr
	return result

def npc_get_cr_exp(pc, cr):
	pc_cr = pc.stat_level_get(stat_level)
	if (pc_cr <= 3):
		if (cr == 1): return 300
		if (cr == 2): return 600
		if (cr == 3): return 900
		if (cr == 4): return 1350
		if (cr == 5): return 1800
		if (cr == 6): return 2700
		if (cr == 7): return 3600
		if (cr == 8): return 5400
		if (cr == 9): return 7200
	return 0

def find_pc_closest_to_origin(loc):
	f = None
	fdist = 0.0
	for obj in game.party:
		assert isinstance(obj, PyObjHandle)
		if (f is None): 
			f = obj
			fdist = obj.distance_to(loc)
			continue
		dist = obj.distance_to(loc)
		if (dist < fdist):
			f = obj
			fdist = dist
	return f, fdist
