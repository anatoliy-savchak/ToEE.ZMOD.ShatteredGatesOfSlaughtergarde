import toee, tpactions, tpdp, debug

def GetActionName():
	return "Throw Net"

def GetActionDefinitionFlags():
	return toee.D20ADF_TargetSingleExcSelf | toee.D20ADF_Breaks_Concentration | toee.D20ADF_TriggersCombat | toee.D20ADF_UseCursorForPicking
	
def GetTargetingClassification():
	return toee.D20TC_SingleExcSelf

def GetActionCostType():
	return toee.D20ACT_Standard_Action

def AddToSequence(d20action, action_seq, tb_status):
	assert isinstance(d20action, tpdp.D20Action)
	print("Throw Net:: AddToSequence")
	path_length = d20action.performer.can_find_path_to_obj(d20action.target, toee.PQF_DOORS_ARE_BLOCKING | toee.PQF_IGNORE_CRITTERS | toee.PQF_STRAIGHT_LINE)
	if path_length > 50:
		print("Throw Net:: AEC_ACTION_INVALID, path_length: {}".format(path_length))
		return toee.AEC_ACTION_INVALID

	action_seq.add_action(d20action)
	return toee.AEC_OK

def ProjectileHit(d20action, proj, obj2):
	assert isinstance(d20action, tpdp.D20Action)
	assert isinstance(proj, toee.PyObjHandle)
	assert isinstance(obj2, toee.PyObjHandle)
	
	print("Throw Net: Projectile Hit")

	toee.game.create_history_from_id(d20action.roll_id_1)
	toee.game.create_history_from_id(d20action.roll_id_2)
	toee.game.create_history_from_id(d20action.roll_id_0)
	print("deal_attack_damage attacker: {}, d20_data: {}, flags: {}, actionType: {}".format(d20action.performer, d20action.data1, d20action.flags, d20action.action_type))
	#d20action.target.deal_attack_damage(d20action.performer, d20action.data1, d20action.flags, d20action.action_type)
	#proj.obj_set_obj(toee.obj_f_last_hit_by, d20action.target)
	d20action.performer.obj_set_obj(toee.obj_f_last_hit_by, d20action.target)
	d20action.performer.apply_projectile_hit_particles(proj, d20action.flags)
	return 1