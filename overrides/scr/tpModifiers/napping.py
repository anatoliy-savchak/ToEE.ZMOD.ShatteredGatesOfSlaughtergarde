import toee, templeplus.pymod, debug, sys, tpdp

###################################################

def GetConditionName():
	return "Napping"

print("Registering " + GetConditionName())
###################################################

NAPPING_LISTEN_DISTANCE_DEFAULT = 15 # ft

def Napping_OnConditionAdd(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	#attachee.condition_add_with_args("sleeping", 1000, 0)
	#attachee.anim_goal_push_animate(64)
	attachee.fall_down()
	#attachee.condition_add_with_args("prone", 0, 0)
	attachee.critter_flag_set(toee.OCF_SLEEPING)
	return

def Napping_OnD20Query_Q_Unconscious(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, templeplus.pymod.EventArgs)
	assert isinstance(evt_obj, templeplus.pymod.EventObjD20Query)
	evt_obj.return_val = 1
	return 0

def Napping_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, templeplus.pymod.EventArgs)
	assert isinstance(evt_obj, templeplus.pymod.EventObjTooltip)
	evt_obj.append("Sleeping")
	return 0

def NappingRemove(attachee, args):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, templeplus.pymod.EventArgs)
	args.condition_remove()
	attachee.critter_flag_unset(toee.OCF_SLEEPING)
	#attachee.condition_remove("prone")
	print("NappingRemove")
	return

def Napping_Remove(attachee, args, evt_obj):
	NappingRemove(attachee, args)
	return

def TurnBasedStatusInitNoActions(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, templeplus.pymod.EventArgs)
	assert isinstance(evt_obj, templeplus.pymod.EventObjTurnBasedStatus)
	evt_obj.tb_status.hourglass_state = 0
	evt_obj.tb_status.flags |= 2
	return 0

def QuerySetReturnVal1(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, templeplus.pymod.EventArgs)
	assert isinstance(evt_obj, templeplus.pymod.EventObjD20Query)
	evt_obj.return_val = 1
	return 0

def QuerySetReturnVal0(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, templeplus.pymod.EventArgs)
	assert isinstance(evt_obj, templeplus.pymod.EventObjD20Query)
	evt_obj.return_val = 0
	return 0

class SkillDiceInfo:
	def __init__(self):
		self.dice20 = None
		self.npc_skill = None
		self.npcroll_result = None
		self.npcroll_total = None
		self.npc_skill_bonus = None
		self.distance = None
		return

	def RollNpc(self, npc):
		assert isinstance(npc, toee.PyObjHandle)
		self.dice20 = toee.dice_new("1d20")
		self.npc_skill = npc.skill_level_get(toee.skill_listen)
		self.npc_skill_bonus = -10 # PHB p79: A sleeping character may make Listen checks at a –10 penalty. A successful check awakens the sleeper.
		self.npcroll_result = self.dice20.roll()
		self.npcroll_total = self.npcroll_result + self.npc_skill + self.npc_skill_bonus
		print("LISTEN ROLL NPC ({}):{} = {} + skill_listen: {} + npc_skill_bonus: {}".format(npc.description, self.npcroll_total, self.npcroll_result, self.npc_skill, self.npc_skill_bonus))
		return

	@staticmethod
	def isTargetEligible(attachee, target):
		assert isinstance(attachee, toee.PyObjHandle)
		assert isinstance(target, toee.PyObjHandle)
		oflags = target.object_flags_get()
		if ((oflags & toee.OF_OFF) or (oflags & toee.OF_DESTROYED) or (oflags & toee.OF_DONTDRAW)): return 0
		if (attachee.allegiance_shared(target)): return 0
		if (not (target.critter_flags_get() & toee.OCF_MOVING_SILENTLY)):
			has_los = attachee.can_sense(target)
			if (not has_los): 
				print("No LOS")
				return 0
		return 1

	def CheckListenAgainst(self, attachee, target):
		assert isinstance(attachee, toee.PyObjHandle)
		assert isinstance(target, toee.PyObjHandle)

		if (self.dice20 is None):
			self.RollNpc(attachee)

		#debug.breakp("CheckListenAgainst1")
		target_distance = self.distance
		if (target_distance is None): 
			target_distance = attachee.distance_to(target)
		target_distance_bonus = int(target_distance // 10 + 1)
		target_battle_bonus = 0
		targetcritter_flags = target.critter_flags_get()
		if (targetcritter_flags & toee.OCF_COMBAT_MODE_ACTIVE): target_battle_bonus = -10
		target_skill = target.skill_level_get(toee.skill_move_silently)
		target_is_moving_silently = 0
		if (targetcritter_flags & toee.OCF_MOVING_SILENTLY): target_is_moving_silently = 1
		targetroll_result = 10
		if (target_is_moving_silently): targetroll_result = self.dice20.roll()
		targetroll_total = targetroll_result + target_skill + target_distance_bonus + target_battle_bonus
		print("MOVE SILENTLY ROLL target ({}):{} = {} + skill_move_silently: {} + dist bonus: {}, _battle_bonus: {}".format(target.description, targetroll_total, targetroll_result, target_skill, target_distance_bonus, target_battle_bonus))
		if (self.npcroll_total < targetroll_total):
			print("Did not hear")
		else:
			print("Awakes!")

			#npc_bonus_list = toee.PyBonusList()

			#npc_bonus_list = attachee.skill_bonus_list_get(toee.skill_listen)
			npc_bonus_list = tpdp.BonusList()
			debug.breakp("CheckListenAgainst2")
			tpdp.dispatch_skill(attachee, toee.skill_listen, npc_bonus_list, toee.OBJ_HANDLE_NULL, 1)
			if (self.npc_skill_bonus):
				#npc_bonus_list.add(npc_skill_bonus, 0, 101)
				#npc_bonus_list.add_text(self.npc_skill_bonus, 0, "Sleeping")
				npc_bonus_list.add(self.npc_skill_bonus, 0, "Sleeping")

			#target_bonus_list = toee.PyBonusList()
			target_bonus_list = tpdp.BonusList()
			tpdp.dispatch_skill(target, toee.skill_move_silently, target_bonus_list, toee.OBJ_HANDLE_NULL, 1)
			#target_bonus_list = target.skill_bonus_list_get(toee.skill_move_silently)
			if (target_distance_bonus):
				#target_bonus_list.add(target_distance_bonus, 0, 101)
				#target_bonus_list.add_text(target_distance_bonus, 0, "Distance {:.0f} ft".format(target_distance))
				target_bonus_list.add(target_distance_bonus, 0, "Distance {:.0f} ft".format(target_distance))

			if (target_battle_bonus):
				#target_bonus_list.add(target_battle_bonus, 0, 101)
				#target_bonus_list.add_text(target_battle_bonus, 0, "Battle")
				target_bonus_list.add(target_battle_bonus, 0, "Battle")

			#if (target_is_moving_silently):
				#target_bonus_list.add(0, 0, 101)
				#target_bonus_list.add_text(0, 0, "Moving Silently")

			target_battle_bonus_str = ""
			if (target_battle_bonus != 0):
				target_battle_bonus_str = "+ Battle {}".format(target_battle_bonus)

			msg = "{} failed to stay silent from {}!\n\n".format(target.description, attachee.description)
			#msg = "{} failed to stay silent from {}! Listen {} + roll {} + Sleeping {} ".format(target.description, attachee.description, self.npc_skill, self.npcroll_result, self.npc_skill_bonus)
			print(msg)
			#toee.game.create_history_freeform(msg)
			#msg = "Listen {} + roll {} + Sleeping {} = {} >= DC {:.0f} = Move Silently {} + roll {} + Distance {:.0f}ft => {:.0f} {}\n\n".format(self.npc_skill, self.npcroll_result, self.npc_skill_bonus, self.npcroll_total, targetroll_total, target_skill, targetroll_result, target_distance, target_distance_bonus, target_battle_bonus_str)
			msg = "DC = Listen {} + roll {} + Sleeping {} = {}\n\n".format(self.npc_skill, self.npcroll_result, self.npc_skill_bonus, self.npcroll_total)
			print(msg)
			#debug.breakp("Napping_OnBeginRound msg2")
			#toee.game.create_history_freeform(msg)
			attachee.float_text_line("Awakes!", 1)

			#debug.breakp("create_history_type6_opposed_check")
			#toee.game.create_history_type6_opposed_check(attachee, target, npc_bonus_list, target_bonus_list, self.npcroll_result, targetroll_result, 5125, 102, 1)
			hist_id = tpdp.create_history_type6_opposed_check(attachee, target, self.npcroll_result, targetroll_result, npc_bonus_list, target_bonus_list, 5125, 102, 1)
			toee.game.create_history_from_id(hist_id)
			return 1
		return 0

def Napping_OnBeginRound(attachee, args, evt_obj):
	try:
		assert isinstance(attachee, toee.PyObjHandle)
		assert isinstance(args, templeplus.pymod.EventArgs)
		assert isinstance(evt_obj, templeplus.pymod.DispIoD20Signal)
		print("Napping_OnBeginRound")
		if (not args.get_arg(0)): 
			print("Not enabled")
			return 0 # not enabled

		dice_info = None
		listen_distance = args.get_arg(1)
		if (not listen_distance): listen_distance = NAPPING_LISTEN_DISTANCE_DEFAULT
		objs = toee.game.obj_list_range(attachee.location, listen_distance, toee.OLC_PC) # removed for perfomance toee.OLC_PC | toee.OLC_NPC
		
		if (objs):
			print("Processing {} targets...".format(len(objs)))
			for target in objs:
				if (not SkillDiceInfo.isTargetEligible(attachee, target)): 
					print("Target is not eligible: {}".format(target))
					continue
				if (dice_info is None):
					dice_info = SkillDiceInfo()
				dice_info.distance = None
				heard = dice_info.CheckListenAgainst(attachee, target)
				if (heard): 
					NappingRemove(attachee, args)
					break
		else: print("No immidiate targets found")

	except Exception, e:
		print "Shout Napping_OnBeginRound error:", sys.exc_info()[0]
		print(str(e))
		debug.breakp("Napping_OnBeginRound error")
	return 0

def Napping_OnGetAC(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, templeplus.pymod.EventArgs)
	assert isinstance(evt_obj, templeplus.pymod.EventObjAttack)
	if (evt_obj.attack_packet.get_flags() & toee.D20CAF_RANGED):
		evt_obj.bonus_list.add(4, 0, 162) # {162}{~Prone~[TAG_PRONE]}
	else:
		evt_obj.bonus_list.add(-4, 0, 162) # {162}{~Prone~[TAG_PRONE]}
	return 0

def Napping_OnGetACBonus2(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, templeplus.pymod.EventArgs)
	assert isinstance(evt_obj, templeplus.pymod.EventObjAttack)
	if (not (evt_obj.attack_packet.get_flags() & toee.D20CAF_RANGED)):
		evt_obj.bonus_list.add(-4, 0, 162) # {162}{~Prone~[TAG_PRONE]}
	return 0

def Napping_Broadcast_Action(attachee, args, evt_obj):
	if (not args.get_arg(0)): return 0 # not enabled
	print("Napping_Broadcast_Action:")
	if (not toee.game.combat_is_active()): 
		print("Not game.combat_is_active, exiting")
		return 0

	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, templeplus.pymod.EventArgs)
	assert isinstance(evt_obj, templeplus.pymod.DispIoD20Signal)
	if (not evt_obj.data1): 
		print("evt_obj.data1 is 0, exiting")
		return 0
	d20a = evt_obj.get_d20_action()
	if (not d20a):
		print("d20a is null, exiting")
		return 0
	if (not d20a.performer): 
		print("d20a.performer is null, exiting")
		return 0
	target = d20a.performer
	print("d20: {}, performer: {}".format(d20a.action_type, target))

	listen_distance = args.get_arg(1)
	if (not listen_distance): listen_distance = NAPPING_LISTEN_DISTANCE_DEFAULT

	distance = attachee.distance_to(target)
	if (distance > listen_distance): 
		print("d20a.performer distance {:.1f} is too big, exiting".format(distance))
		return 0

	if (not SkillDiceInfo.isTargetEligible(attachee, target)): 
		print("d20a.performer {} is not eligible, exiting".format(target))
		return 0

	print("Checking ...")
	dice_info = SkillDiceInfo()
	dice_info.distance = distance
	heard = dice_info.CheckListenAgainst(attachee, target)
	if (heard): 
		NappingRemove(attachee, args)

	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - check Listen: 1
modObj.AddHook(toee.ET_OnConditionAdd, toee.EK_NONE, Napping_OnConditionAdd, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_Unconscious, Napping_OnD20Query_Q_Unconscious, ())
modObj.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, Napping_OnGetTooltip, ())
modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_Attack_Made, Napping_Remove, ()) # gets triggered at the end of the damage calculation
modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_Killed, Napping_Remove, ())
modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_HP_Changed, Napping_Remove, ())
modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_AID_ANOTHER_WAKE_UP, Napping_Remove, ())
modObj.AddHook(toee.ET_OnBeginRound, toee.EK_NONE, Napping_OnBeginRound, ())
#modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_BeginTurn, Napping_OnBeginRound, ())
# not implemented modObj.AddHook(toee.ET_OnGetSkillLevel, toee.EK_SKILL_LISTEN, ., ())
#modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_EnterCombat, Napping_Test, ())
#modObj.AddHook(toee.ET_OnInitiative, toee.EK_Q_EnterCombat, Napping_Test, ())
modObj.AddHook(toee.ET_OnD20Signal, toee.EK_S_Broadcast_Action, Napping_Broadcast_Action, ())

# sleeping duplicate
#modObj.AddHook(toee.ET_OnTurnBasedStatusInit, toee.EK_NONE, TurnBasedStatusInitNoActions, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_SneakAttack, QuerySetReturnVal1, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_Helpless, QuerySetReturnVal1, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_CannotCast, QuerySetReturnVal1, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_AOOPossible, QuerySetReturnVal0, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_CoupDeGrace, QuerySetReturnVal1, ())

# prone duplicate
modObj.AddHook(toee.ET_OnGetAC, toee.EK_NONE, Napping_OnGetAC, ())
modObj.AddHook(toee.ET_OnGetACBonus2, toee.EK_NONE, Napping_OnGetACBonus2, ())
modObj.AddHook(toee.ET_OnD20Query, toee.EK_Q_Prone, QuerySetReturnVal1, ())
