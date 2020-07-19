import toee, tpactions, tpdp

def GetActionName():
	return "Smash Object"

def GetActionDefinitionFlags():
	return toee.D20ADF_None | toee.D20ADF_TargetContainer | toee.D20ADF_UseCursorForPicking
	
def GetTargetingClassification():
	return toee.D20TC_ItemInteraction

def GetActionCostType():
	return toee.D20ACT_Standard_Action

def AddToSequence(d20action, action_seq, tb_status):
	assert isinstance(d20action, tpdp.D20Action)
	assert isinstance(tb_status, tpdp.TurnBasedStatus)
	assert isinstance(action_seq, tpactions.ActionSequence)

	performer = action_seq.performer
	target = d20action.target
	dist = performer.distance_to(target)
	print("dist: {}, target: {}, performer: {}".format(dist, target, performer))

	if (dist > 7):
		performer.float_text_line("Too far!", toee.tf_red)
		return toee.AEC_TARGET_TOO_FAR

	if performer.d20_query(toee.Q_Prone):
		d20aGetup = d20action
		d20aGetup.action_type = toee.D20A_STAND_UP
		action_seq.add_action(d20aGetup)

	if 0:
		d20aApproach = tpdp.D20Action(tpdp.D20ActionType.Move)
		#d20aApproach.action_type = tpdp.D20ActionType.Move
		d20aApproach.target = d20action.target
		d20aApproach.performer = d20action.performer
		d20aApproach.data1 = d20action.data1
		d20aApproach.loc = d20action.loc
		action_seq.add_action(d20aApproach)

	#if (performer.anim_goal_push_attack(target, toee.game.random_range(0, 2), 1, 0)):
	#	new_anim_id = performer.anim_goal_get_new_id()
	#	d20action.flags |= toee.D20CAF_NEED_ANIM_COMPLETED
	#	d20action.anim_id = new_anim_id

	if (0): #todo - change to full attack with always hit
		print("d20action.action_type: {}".format(d20action.action_type))
		print("hourglass_state: {}".format(tb_status.hourglass_state))
		if (tb_status.hourglass_state == toee.D20ACT_Standard_Action):
			tb_status.hourglass_state = toee.D20ACT_Full_Round_Action
			d20action.flags |= toee.D20CAF_ALWAYS_HIT
	action_seq.add_action(d20action)
	return toee.AEC_OK