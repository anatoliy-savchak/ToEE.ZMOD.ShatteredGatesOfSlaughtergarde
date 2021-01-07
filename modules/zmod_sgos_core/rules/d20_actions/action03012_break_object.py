import toee, tpactions, tpdp

def GetActionName():
	return "Break Object"

def GetActionDefinitionFlags():
	return toee.D20ADF_None | toee.D20ADF_TargetContainer | toee.D20ADF_UseCursorForPicking
	
def GetTargetingClassification():
	return toee.D20TC_ItemInteraction

def GetActionCostType():
	return toee.D20ACT_Standard_Action

def AddToSequence(d20action, action_seq, tb_status):
	assert isinstance(D20Action, tpdp.D20Action)
	performer = action_seq.performer
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

	action_seq.add_action(d20action)
	return toee.AEC_OK