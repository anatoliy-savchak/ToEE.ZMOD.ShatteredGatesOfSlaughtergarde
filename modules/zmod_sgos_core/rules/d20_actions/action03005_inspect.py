import toee, tpactions, debug

def GetActionName():
	return "Inspect"

def GetActionDefinitionFlags():
	return toee.D20ADF_TargetSingleExcSelf | toee.D20ADF_UseCursorForPicking | toee.D20ADF_MagicEffectTargeting | toee.D20ADF_Breaks_Concentration
	
def GetTargetingClassification():
	return toee.D20TC_CastSpell

def GetActionCostType():
	return toee.D20ACT_NULL

def AddToSequence(d20action, action_seq, tb_status):
	action_seq.add_action(d20action)
	return toee.AEC_OK

def ModifyPicker(picker_args):
	assert isinstance(picker_args, tpactions.PickerArgs)
	picker_args.set_mode_target_flag(tpactions.ModeTarget.Single)
	return 1
