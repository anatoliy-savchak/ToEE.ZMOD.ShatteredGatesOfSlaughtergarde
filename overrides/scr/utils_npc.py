import toee, debug, tpdp, utils_obj, const_toee

def npc_feats_print(npc):
	assert isinstance(npc, toee.PyObjHandle)
	feats = npc.feats
	for f in feats:
		print("Feat Code: {}".format(f))
		print("Feat Name{}".format(toee.game.get_feat_name(f)))
	return

def npc_generate_hp(npc):
	assert isinstance(npc, toee.PyObjHandle)
	npc.obj_set_int(toee.obj_f_hp_pts, -65535)
	hp = npc.stat_level_get(toee.stat_hp_current)
	#print("Current HP: {}".format(hp))
	return hp

def npc_money_set(npc, copper):
	assert isinstance(npc, toee.PyObjHandle)
	assert isinstance(copper, int)
	diff = npc.money_get()
	diff = copper - diff
	npc.money_adj(diff)
	return diff

def npc_stat_generate(npc):
	assert isinstance(npc, toee.PyObjHandle)
	result = ""
	breakp("npc_stat_generate")

	hp = npc.stat_level_get(toee.stat_hp_max)
	hd = npc.hit_dice_num
	result = "hp {} ({} HD)".format(hp, hd)

	has_fast_healing = npc.d20_query_has_condition("Monster Fast Healing")
	if (has_fast_healing):
		result = result + " fast healing"
	result = result + "\p"

	gender = npc.stat_level_get(toee.stat_gender)
	if (gender == 0):
		result = result + "Male"
	elif (gender == 1):
		result = result + "Female"

	return result

def npc_spell_ensure(npc, spell_id, stat_class, spell_level, memorize = 0):
	assert isinstance(npc, toee.PyObjHandle)
	print("{}.npc_spell_ensure(spell_id: {}, stat_class: {}, spell_level: {})".format(npc, spell_id, stat_class, spell_level))
	npc.spell_known_add(spell_id, stat_class, spell_level)
	npc.spell_memorized_add(spell_id, stat_class, spell_level)
	if (memorize):
		npc.spells_pending_to_memorized()
	return 1

def npc_skill_ensure(npc, skill_id, target_skill_value):
	assert isinstance(npc, toee.PyObjHandle)
	value_total = npc.skill_level_get(skill_id)
	ranks = npc.skill_ranks_get(skill_id)
	delta = target_skill_value - value_total
	ranks += delta
	npc.skill_ranks_set(skill_id, ranks)
	return delta

def npc_is_alive(npc, dead_when_negative_hp = 0):
	assert isinstance(npc, toee.PyObjHandle)
	object_flags = npc.object_flags_get()
	if ((object_flags & toee.OF_DESTROYED) or (object_flags & toee.OF_OFF)): 
		#print("destroyed: {}".format(npc))
		return 0
	result = npc.d20_query(toee.Q_Dead)
	if (result): return 0
	result = npc.d20_query(toee.Q_Dying)
	if (result): return 0
	hp = npc.stat_level_get(toee.stat_hp_current)
	if (dead_when_negative_hp and hp < 0):
		return 0
	if (hp <= -10): return 0
	return 1

def npc_hp_current(npc):
	assert isinstance(npc, toee.PyObjHandle)
	hp = npc.stat_level_get(toee.stat_hp_current)
	return hp

def npc_hp_current_percent(npc):
	assert isinstance(npc, toee.PyObjHandle)
	maxhp = npc.stat_level_get(toee.stat_hp_max)
	hp = npc.stat_level_get(toee.stat_hp_current)
	if (maxhp):
		return 100 * hp / maxhp
	return 100

def npc_find_nearest_pc(npc, distance_ft, should_see):
	assert isinstance(npc, toee.PyObjHandle)
	nearest = None
	nearest_dist = 10000
	for obj in toee.game.obj_list_range(npc.location, distance_ft, toee.OLC_NPC | toee.OLC_PC):
		assert isinstance(obj, toee.PyObjHandle)
		if (should_see):
			if (not npc.can_see(obj)): continue
		obj_dist = npc.distance_to(obj)
		if (obj_dist < nearest_dist):
			nearest = obj
			nearest_dist = obj_dist
	return nearest

def npc_find_nearest_pc_loc(loc, distance_ft):
	nearest = None
	nearest_dist = 10000
	for obj in toee.game.obj_list_range(loc, distance_ft, toee.OLC_NPC | toee.OLC_PC):
		assert isinstance(obj, toee.PyObjHandle)
		obj_dist = obj.distance_to(loc)
		if (obj_dist < nearest_dist):
			nearest = obj
			nearest_dist = obj_dist
	return nearest

def print_npc_vicinity(leader = None):
	if (not leader):
		leader = toee.game.leader
	for npc in toee.game.obj_list_vicinity(leader.location, toee.OLC_NPC):
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
	for obj in toee.game.obj_list_vicinity(loc, OLC_NPC):
		assert isinstance(obj, toee.PyObjHandle)
		if (obj.proto == proto): return obj
	return OBJ_HANDLE_NULL

def npc_get_cr(npc):
	cr = 0
	if (npc.type == toee.obj_t_npc):
		cr = npc.obj_get_int(toee.obj_f_npc_challenge_rating)
	level_cr = npc.stat_level_get(toee.stat_level)
	result = cr + level_cr
	return result

def npc_get_cr_exp(pc, cr):
	pc_cr = pc.stat_level_get(toee.stat_level)
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
		assert isinstance(obj, toee.PyObjHandle)
		if (f is None): 
			f = obj
			fdist = obj.distance_to(loc)
			continue
		dist = obj.distance_to(loc)
		if (dist < fdist):
			f = obj
			fdist = dist
	return f, fdist

def pc_travel_time_calc_hours(miles):
	assert isinstance(miles, int)
	# see PH 162, Table: Movement and Distance

	min_speed = None
	for pc in toee.game.party:
		if (not npc_is_alive(pc)): continue
		speed = pc.stat_level_get(toee.stat_movement_speed)
		if (min_speed is None): min_speed = speed
		elif(min_speed > speed): min_speed = speed
	
	if (min_speed is None): 
		print("pc_travel_time_calc_hours => None")
		return

	print("min_speed raw: {}".format(min_speed))
	if (min_speed < 15): min_speed = 15
	elif (min_speed > 40): min_speed = 40
	print("min_speed: {}".format(min_speed))

	minute_speed = min_speed * 10
	hour_speed = minute_speed * 60
	if (min_speed <= 15): hour_speed = 1.5
	elif (min_speed < 20): hour_speed = 2
	elif (min_speed <= 30): hour_speed = 3
	else: hour_speed = 4

	#len_feet = miles * 5280.00
	#result = len_feet / hour_speed
	result = miles / hour_speed
	print("minute_speed: {}, hour_speed: {}, result(hours): {}".format(minute_speed, hour_speed, result))
	return result

def travel_hours_to_day_hours(travel_hours):
	assert isinstance(travel_hours, float)
	max_traveling_time_per_day_in_hours = 8
	days = (int)(travel_hours / max_traveling_time_per_day_in_hours)
	leftover = travel_hours - days * max_traveling_time_per_day_in_hours
	result = days * 24 + leftover
	print("travel_hours: {}, days: {}, leftover: {}, result: {}".format(travel_hours, days, leftover, result))
	return result

def pc_turn_all(rotation):
	for pc in toee.game.party:
		pc.rotation = rotation
	return

def pc_award_experience_all(xp_awarded_each):
	for pc in toee.game.party:
		pc.award_experience(xp_awarded_each)
	return

def npc_kill_foes():
	# placeholder
	killer = toee.game.leader
	for npc in toee.game.obj_list_vicinity(killer.location, toee.OLC_NPC):
		print("Check {}".format(npc))
		if (npc.type == toee.obj_t_pc): continue
		if (not npc.is_active_combatant(killer)): 
			print("skip, is not is_active_combatant")
			continue
		if (npc.allegiance_shared(toee.game.leader)): 
			print("skip, allegiance_shared")
			continue
		npcleader = npc.leader_get()
		if (npcleader and (npcleader.type == toee.obj_t_pc)): 
			print("skip, leader is pc")
			continue
		#if (npc.reaction_get(killer) > 0): 
		#	print("skip, reaction is >0")
		#	continue
		if (npc.is_friendly(killer)): 
			print("skip, is friendly")
			continue
		if (npc.object_flags_get() & toee.OF_DONTDRAW): 
			print("skip, OF_DONTDRAW")
			continue

		print("killing: {}".format(npc))
		npc.critter_kill_by_effect(killer)
	return