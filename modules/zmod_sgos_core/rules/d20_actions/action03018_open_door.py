import toee, tpactions, tpdp, debug

def GetActionName():
	return "Open Door"

def GetActionDefinitionFlags():
	return toee.D20ADF_TargetContainer
	
def GetTargetingClassification():
	return toee.D20TC_ItemInteraction

def GetActionCostType():
	return toee.D20ACT_Move_Action

def AddToSequence(d20action, action_seq, tb_status):
	assert isinstance(d20action, tpdp.D20Action)
	print("Open Door:: AddToSequence")
	path_length = d20action.performer.can_find_path_to_obj(d20action.target, toee.PQF_DOORS_ARE_BLOCKING | toee.PQF_IGNORE_CRITTERS)
	if path_length > 50:
		print("Close Door:: AEC_ACTION_INVALID, path_length: {}".format(path_length))
		return toee.AEC_ACTION_INVALID

	action_seq.add_action(d20action)
	return toee.AEC_OK