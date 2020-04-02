import toee
import tpactions
import tpdp
import sys

def GetActionName():
	return "Lethal Shock"

def GetActionDefinitionFlags():
	return toee.D20ADF_None
	
def GetTargetingClassification():
	return toee.D20TC_Target0

def GetActionCostType():
	return toee.D20ACT_Standard_Action

def AddToSequence(d20action, action_seq, tb_status):
	try:
		assert isinstance(action_seq, tpactions.ActionSequence)
		assert isinstance(d20action, tpdp.D20Action)
		caster = action_seq.performer
		toee.game.create_history_freeform("{} performs Lethal Shock (Su)!\n\n".format(caster.description))
		toee.game.particles("sp-Call Lightning", caster)
		affected = toee.game.obj_list_range(caster.location, 20, toee.OLC_CRITTERS)
		dce = toee.dice_new("4d8")
		first_target = toee.OBJ_HANDLE_NULL
		for target in affected:
			assert isinstance(target, toee.PyObjHandle)
			if (target == caster): continue
			if (target.type != toee.obj_t_npc and target.type != toee.obj_t_pc): continue
			f = target.object_flags_get()
			if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
			if (not first_target): first_target = target
			saved = target.saving_throw(12, toee.D20_Save_Reflex, D20STD_F_NONE, caster)
			reduction = 100
			if (saved): reduction = toee.DAMAGE_REDUCTION_HALF
			target.damage_with_reduction(caster, toee.D20DT_ELECTRICITY, dce, toee.D20DAP_NORMAL, reduction, toee.D20A_UNSPECIFIED_ATTACK)
			toee.game.particles("sp-Call Lightning-hit", target)

		action_seq.tb_status.hourglass_state = toee.D20ACT_NULL

		if (first_target and caster.anim_goal_push_attack(first_target, toee.game.random_range(0, 2), 1, 0)):
			new_anim_id = caster.anim_goal_get_new_id()
			print("pushed new anim id: {}".format(new_anim_id))
			d20action.flags |= toee.D20CAF_NEED_ANIM_COMPLETED
			d20action.anim_id = new_anim_id

		caster.d20_send_signal(toee.S_Spell_Cast, 0)
		#caster.object_script_execute(caster, )
	except Exception, e:
		print "Lethal Shock AddToSequence error:", sys.exc_info()[0]
		print(str(e))
	return toee.AEC_OK