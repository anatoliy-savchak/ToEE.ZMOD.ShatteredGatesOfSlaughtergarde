import toee, tpactions, tpdp, debug

def GetActionName():
	return "Open Door"

def GetActionDefinitionFlags():
	return toee.D20ADF_None
	
def GetTargetingClassification():
	return toee.D20TC_SingleIncSelf

def GetActionCostType():
	return toee.D20ACT_NULL

def AddToSequence(d20action, action_seq, tb_status):
	assert isinstance(d20action, tpdp.D20Action)
	action_seq.add_action(d20action)
	return toee.AEC_OK