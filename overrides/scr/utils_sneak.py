from toee import *
from debugg import *

def npc_is_observed(npc, target):
	assert isinstance(npc, PyObjHandle)
	assert isinstance(target, PyObjHandle)
	# todo
	return 1

def npc_can_hide_in_plain_sight(npc):
	assert isinstance(npc, PyObjHandle)
	# todo
	return 1

def npc_get_concealment100(npc, target):
	assert isinstance(npc, PyObjHandle)
	assert isinstance(target, PyObjHandle)
	# todo
	return 0

def npc_can_improved_diversion(npc):
	assert isinstance(npc, PyObjHandle)
	bluff = npc.skill_level_get(skill_bluff)
	if (bluff >= 4): return 1
	return 0

def npc_perform_improved_diversion(npc):
	assert isinstance(npc, PyObjHandle)

	npc_skill = npc.skill_level_get(skill_bluff)
	npc_roll_dice = dice_new("1d20")
	npcroll_result = npc_roll_dice.roll()
	npcroll_total = npcroll_result + npc_skill
	print("npc_perform_improved_diversion ROLL NPC:{} = {} + skill_bluff: {}".format(npcroll_total, npcroll_result, npc_skill))
	
	target_skill = target.skill_level_get(skill_sense_motive)
	target_roll_dice = dice_new("1d20")
	targetroll_result = target_roll_dice.roll()
	targetroll_total = targetroll_result + target_skill
	print("npc_perform_improved_diversion ROLL target:{} = {} + skill_sense_motive: {}".format(targetroll_total, targetroll_result, target_skill))

	if (targetroll_total >= npcroll_total):
		print("diversion failed")
		return 0
	
	print("diversion success")
	return 1


def npc_has_cover_against(npc, target):
	assert isinstance(npc, PyObjHandle)
	assert isinstance(target, PyObjHandle)
	# todo
	return 1

def npc_overcome_observed(npc, target):
	assert isinstance(npc, PyObjHandle)
	assert isinstance(target, PyObjHandle)
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
	assert isinstance(npc, PyObjHandle)
	assert isinstance(target, PyObjHandle)
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
	npc_skill = npc.skill_level_get(skill_hide)
	npc_roll_dice = dice_new("1d20")
	npcroll_result = npc_roll_dice.roll()
	npcroll_total = npcroll_result + npc_skill
	print("perform_sneak_for_attack ROLL NPC:{} = {} + npc_skill: {}".format(npcroll_total, npcroll_result, npc_skill))
	
	target_skill = target.skill_level_get(skill_spot)
	target_roll_dice = dice_new("1d20")
	targetroll_result = target_roll_dice.roll()
	targetroll_total = targetroll_result + target_skill
	print("perform_sneak_for_attack ROLL target:{} = {} + skill_spot: {}".format(targetroll_total, targetroll_result, target_skill))

	if (targetroll_total >= npcroll_total):
		print("HIDE failed")
		return 0
	
	print("HIDE success")
	return 1

def npc_make_hide(npc, ignore_observed):
	assert isinstance(npc, PyObjHandle)
	if (not ignore_observed): return 0 # implement it later

	dice20 = dice_new("1d20")
	npc_skill = npc.skill_level_get(skill_hide)
	npcroll_result = dice20.roll()
	npcroll_total = npcroll_result + npc_skill
	print("perform_sneak_for_attack ROLL NPC ({}):{} = {} + npc_skill: {}".format(npc.description, npcroll_total, npcroll_result, npc_skill))

	hidden_not_from_count = 0
	objects = game.obj_list_vicinity(npc.location, OLC_PC | OLC_NPC)
	if (objects):
		foes = []
		for obj in objects:
			if (obj == npc): continue
			f = obj.object_flags_get()
			if ((f & OF_OFF) or (f & OF_DESTROYED) or (f & OF_DONTDRAW)): continue
			if (obj.allegiance_shared(npc)): continue
			if (not obj.can_see(npc)): continue
			foes.append(obj)
		if (foes):
			for target in foes:
				target_skill = target.skill_level_get(skill_spot)
				targetroll_result = dice20.roll()
				targetroll_total = targetroll_result + target_skill
				print("perform_sneak_for_attack ROLL target ({}):{} = {} + skill_spot: {}".format(target.description, targetroll_total, targetroll_result, target_skill))
				if (targetroll_total >= npcroll_total):
					hidden_not_from_count += 1
					game.create_history_freeform("{} failed to Hide from {}!\n\nSpot({})+1d20({}) = {} > Hide DC({})\n\n".format(npc.description, target.description, target_skill, targetroll_result, targetroll_total, npcroll_total))
					target.float_text_line("Hey!", 2)
					npc.float_text_line("(Failed to Hide)", 1)
					print("Faield to Hide")
					break

	if (hidden_not_from_count): return 0
	print("HIDDEN!")
	npc.anim_goal_interrupt()
	npc.critter_flag_set(OCF_MOVING_SILENTLY)
	return 1