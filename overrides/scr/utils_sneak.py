import toee, tpdp, debugg

def npc_is_observed(npc, target):
	assert isinstance(npc, toee.PyObjHandle)
	assert isinstance(target, toee.PyObjHandle)
	# todo
	return 1

def npc_can_hide_in_plain_sight(npc):
	assert isinstance(npc, toee.PyObjHandle)
	# todo
	return 1

def npc_get_concealment100(npc, target):
	assert isinstance(npc, toee.PyObjHandle)
	assert isinstance(target, toee.PyObjHandle)
	# todo
	return 0

def npc_can_improved_diversion(npc):
	assert isinstance(npc, toee.PyObjHandle)
	bluff = npc.skill_level_get(toee.skill_bluff)
	if (bluff >= 4): return 1
	return 0

def npc_perform_improved_diversion(npc):
	assert isinstance(npc, toee.PyObjHandle)

	npc_skill = npc.skill_level_get(toee.skill_bluff)
	npc_roll_dice = toee.dice_new("1d20")
	npcroll_result = npc_roll_dice.roll()
	npcroll_total = npcroll_result + npc_skill
	print("npc_perform_improved_diversion ROLL NPC:{} = {} + skill_bluff: {}".format(npcroll_total, npcroll_result, npc_skill))
	
	target_skill = target.skill_level_get(toee.skill_sense_motive)
	target_roll_dice = toee.dice_new("1d20")
	targetroll_result = target_roll_dice.roll()
	targetroll_total = targetroll_result + target_skill
	print("npc_perform_improved_diversion ROLL target:{} = {} + skill_sense_motive: {}".format(targetroll_total, targetroll_result, target_skill))

	if (targetroll_total >= npcroll_total):
		print("diversion failed")
		return 0
	
	print("diversion success")
	return 1


def npc_has_cover_against(npc, target):
	assert isinstance(npc, toee.PyObjHandle)
	assert isinstance(target, toee.PyObjHandle)
	# todo
	return 1

def npc_overcome_observed(npc, target):
	assert isinstance(npc, toee.PyObjHandle)
	assert isinstance(target, toee.PyObjHandle)
	print("npc_overcome_observed, npc:{}, target:{}".format(npc, target))

	if (npc_can_hide_in_plain_sight(npc)):
		print("success npc_can_hide_in_plain_sight")
		return True

	concealment = npc_get_concealment100(npc, target)
	if (concealment>=50):
		print("success concealment>=50")
		return True

	cover = 0
	if (concealment == 0): cover = npc_has_cover_against(npc, target)
	if (concealment == 0 and cover == 0): return False
	
	print("success cover: {}, concealment: {}".format(cover, concealment))

	if (npc_can_improved_diversion(npc)):
		return npc_perform_improved_diversion(npc,target)
	return False

def perform_sneak_for_attack(npc, target):
	assert isinstance(npc, toee.PyObjHandle)
	assert isinstance(target, toee.PyObjHandle)
	print("perform_sneak_for_attack, npc:{}, target:{}".format(npc, target))

	if (not (npc.has_los(target))):
		print("success no LOS")
		return 1

	if (npc.can_sneak_attack(target) != 1):
		print("failed can_sneak_attack")
		return 0
	
	overcome_observed = True
	if (npc_is_observed(npc, target) != 0):
		overcome_observed = npc_overcome_observed(npc, target)
	
	if (not overcome_observed): return 0

	# hide vs spot check
	npc_skill = npc.skill_level_get(toee.skill_hide)
	npc_roll_dice = dice_new("1d20")
	npcroll_result = npc_roll_dice.roll()
	npcroll_total = npcroll_result + npc_skill
	print("perform_sneak_for_attack ROLL NPC:{} = {} + npc_skill: {}".format(npcroll_total, npcroll_result, npc_skill))
	
	target_skill = target.skill_level_get(toee.skill_spot)
	target_roll_dice = toee.dice_new("1d20")
	targetroll_result = target_roll_dice.roll()
	targetroll_total = targetroll_result + target_skill
	print("perform_sneak_for_attack ROLL target:{} = {} + skill_spot: {}".format(targetroll_total, targetroll_result, target_skill))

	if (targetroll_total >= npcroll_total):
		print("HIDE failed")
		return 0
	
	print("HIDE success")
	return 1

def npc_make_hide(npc, ignore_observed):
	assert isinstance(npc, toee.PyObjHandle)
	if (not ignore_observed): return 0 # implement it later

	dice20 = toee.dice_new("1d20")

	npc_bonus_list = tpdp.BonusList()
	npc_roll = dice20.roll()
	npc_score = tpdp.dispatch_skill(npc, toee.skill_hide, npc_bonus_list, toee.OBJ_HANDLE_NULL, 1)
	npc_score_total = npc_score + npc_roll
	print("npc hide roll: {}, skill: {}, total: {}".format(npc_roll, npc_score, npc_score_total))

	hidden_not_from_count = 0
	objects = toee.game.obj_list_vicinity(npc.location, toee.OLC_PC | toee.OLC_NPC)
	if (objects):
		foes = []
		for obj in objects:
			if (obj == npc): continue
			f = obj.object_flags_get()
			if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
			if (obj.allegiance_shared(npc)): continue
			if (not obj.can_see(npc)): continue
			foes.append(obj)
		if (foes):
			for target in foes:
				target_bonus_list = tpdp.BonusList()
				target_roll = dice20.roll()
				target_score = tpdp.dispatch_skill(target, toee.skill_spot, target_bonus_list, toee.OBJ_HANDLE_NULL, 1)
				target_score_total = target_score + target_roll
				print("target hide roll: {}, skill: {}, total: {}".format(target_roll, target_score, target_score_total))
				success = npc_score_total > target_score_total
				hist_id = tpdp.create_history_type6_opposed_check(npc, target, npc_roll, target_roll, npc_bonus_list, target_bonus_list, 5126, 103 - success, 1) # \overrides\tpmes\combat.mes" 
				toee.game.create_history_from_id(hist_id)
				if (not success):
					hidden_not_from_count += 1
					npc.float_text_line("(Failed to Hide)", toee.tf_red)
					print("Failed to Hide")
					break

	if (hidden_not_from_count): return 0
	if (foes): # make sure chars even see him
		npc.float_text_line("Hidden!", toee.tf_blue)
	print("HIDDEN!")
	npc.anim_goal_interrupt()
	npc.critter_flag_set(toee.OCF_MOVING_SILENTLY)
	return 1

def npc_make_hide_and_surprise(npc):
	assert isinstance(npc, toee.PyObjHandle)
	print("npc_make_hide_and_surprise: {}".format(npc))

	dice20 = toee.dice_new("1d20")

	npc_bonus_list = tpdp.BonusList()
	npc_roll = dice20.roll()
	npc_score = tpdp.dispatch_skill(npc, toee.skill_hide, npc_bonus_list, toee.OBJ_HANDLE_NULL, 1)
	npc_score_total = npc_score + npc_roll
	print("npc hide roll: {}, skill: {}, total: {}".format(npc_roll, npc_score, npc_score_total))

	hidden_not_from_count = 0
	hidden_from_count = 0
	objects = toee.game.obj_list_vicinity(npc.location, toee.OLC_PC | toee.OLC_NPC)
	if (objects):
		suprised_list = list()
		notsuprised_list = list()
		foes = []
		for obj in objects:
			if (obj == npc): continue
			f = obj.object_flags_get()
			if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
			if (obj.allegiance_shared(npc)): continue
			if (not obj.can_see(npc)): 
				suprised_list.append(obj)
				continue
			foes.append(obj)
		if (foes):
			for target in foes:
				target_bonus_list = tpdp.BonusList()
				target_roll = dice20.roll()
				target_score = tpdp.dispatch_skill(target, toee.skill_spot, target_bonus_list, toee.OBJ_HANDLE_NULL, 1)
				target_score_total = target_score + target_roll
				print("target hide roll: {}, skill: {}, total: {}".format(target_roll, target_score, target_score_total))
				success = npc_score_total > target_score_total
				hist_id = tpdp.create_history_type6_opposed_check(npc, target, npc_roll, target_roll, npc_bonus_list, target_bonus_list, 5126, 103 - success, 1) # \overrides\tpmes\combat.mes" 
				toee.game.create_history_from_id(hist_id)
				if (not success):
					hidden_not_from_count += 1
					notsuprised_list.append(target)
				else:
					suprised_list.append(target)
					hidden_from_count += 1

	if (hidden_from_count == 0): 
		print("no suprise round")
		npc.critter_flag_unset(toee.OCF_MOVING_SILENTLY)
		# no suprise round
		return 0

	if (hidden_not_from_count == 0):
		npc.float_text_line("Hidden!", toee.tf_blue)
		print("HIDDEN!")
		npc.anim_goal_interrupt()
		npc.critter_flag_set(toee.OCF_MOVING_SILENTLY)
	else:
		print("Failed to Hide")

	#npc.float_text_line("Surprise!", toee.tf_light_blue)

	for target in suprised_list:
		print("Surprised: {}".format(target))
		target.condition_add("Surprised2")
		target.float_text_line("Surprised!", toee.tf_red)

	for target in notsuprised_list:
		print("Not Surprised: {}".format(target))
		target.condition_add("SurpriseRound2")

	npc.condition_add("SurpriseRound2")
	return 1

def npc_move_silently_against_listener(npc, target):
	assert isinstance(npc, toee.PyObjHandle)
	assert isinstance(target, toee.PyObjHandle)

	dice20 = toee.dice_new("1d20")

	npc_bonus_list = tpdp.BonusList()
	npc_roll = dice20.roll()
	npc_score = tpdp.dispatch_skill(npc, toee.skill_move_silently, npc_bonus_list, toee.OBJ_HANDLE_NULL, 1)
	npc_score_total = npc_score + npc_roll
	print("npc hide roll: {}, skill: {}, total: {}".format(npc_roll, npc_score, npc_score_total))

	target_bonus_list = tpdp.BonusList()
	target_roll = dice20.roll()
	target_score = tpdp.dispatch_skill(target, toee.skill_listen, target_bonus_list, toee.OBJ_HANDLE_NULL, 1)
	target_score_total = target_score + target_roll
	print("target listen roll: {}, skill: {}, total: {}".format(target_roll, target_score, target_score_total))
	success = npc_score_total > target_score_total
	hist_id = tpdp.create_history_type6_opposed_check(npc, target, npc_roll, target_roll, npc_bonus_list, target_bonus_list, 5126, 103 - success, 1) # \overrides\tpmes\combat.mes" 
	toee.game.create_history_from_id(hist_id)
	return not success

def npc_listen_against_pc(npc, distance_threshhold):
	assert isinstance(npc, toee.PyObjHandle)
	assert isinstance(distance_threshhold, int)
	objects = toee.game.obj_list_vicinity(npc.location, toee.OLC_PC | toee.OLC_NPC)
	if (not objects): return None
	foes = []
	for obj in objects:
		assert isinstance(obj, toee.PyObjHandle)
		if (obj == npc): continue
		f = obj.object_flags_get()
		if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
		if (obj.allegiance_shared(npc)): continue
		dist = npc.distance_to(obj)
		if (dist > distance_threshhold): 
			continue
		print("distance: {}".format(dist))
		if (not obj.critter_flags_get() & toee.OCF_MOVING_SILENTLY): return obj
		foes.append(obj)
	if (not foes): return None

	dice20 = toee.dice_new("1d20")

	npc_bonus_list = tpdp.BonusList()
	npc_roll = dice20.roll()
	npc_score = tpdp.dispatch_skill(npc, toee.skill_listen, npc_bonus_list, toee.OBJ_HANDLE_NULL, 1)
	npc_score_total = npc_score + npc_roll
	print("npc listen roll: {}, skill: {}, total: {}".format(npc_roll, npc_score, npc_score_total))

	for target in foes:
		target_bonus_list = tpdp.BonusList()
		target_roll = dice20.roll()
		target_score = tpdp.dispatch_skill(target, toee.skill_move_silently, target_bonus_list, toee.OBJ_HANDLE_NULL, 1)
		target_score_total = target_score + target_roll
		print("target move silently roll: {}, skill: {}, total: {}".format(target_roll, target_score, target_score_total))
		success = npc_score_total > target_score_total
		hist_id = tpdp.create_history_type6_opposed_check(npc, target, npc_roll, target_roll, npc_bonus_list, target_bonus_list, 5125, 103 - success, 1) # \overrides\tpmes\combat.mes" 
		toee.game.create_history_from_id(hist_id)
		if (success): return target
	return None
