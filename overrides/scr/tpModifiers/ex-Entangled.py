from __main__ import game
from templeplus.pymod import PythonModifier
from toee import *
from debugg import *
import tpdp
import math

###################################################

def GetConditionName():
	return "ex-Entangled"

print("Registering " + GetConditionName())
###################################################

def exEntangled_OnAdd(attachee, args, evt_obj):
	attachee.float_text_line( "Entangled!", tf_red )
	partid = game.particles( 'sp-Web Hit', attachee )
	args.set_arg(3, partid)
	return 0

def exEntangled_OnRemove(attachee, args, evt_obj):
	partId = args.get_arg(3)
	if (partId > 0):
		args.set_arg(3, 0)
		game.particles_kill(partId)
	return 0

def exEntangled_OnPreAdd(attachee, args, evt_obj):
	val = evt_obj.is_modifier(GetConditionName())
	# TODO check EK_Q_Is_Ethereal
	# TODO check EK_Q_Critter_Has_Freedom_of_Movement
	if val:
		evt_obj.return_val = 0
		attachee.float_text_line( "Already Entangled!", tf_red )
	return 0

def exEntangled_OnD20Query_CritterHasCondition(attachee, args, evt_obj):
	condName = args.get_param(0)
	if (GetConditionName() == condName):
		evt_obj.return_val = 1
	return 0

def OnQueryReturnTrue(attachee, args, evt_obj):
	evt_obj.return_val = 1
	return 0

def OnQueryReturnFalse(attachee, args, evt_obj):
	evt_obj.return_val = 0
	return 0

def exEntangled_OnAbilityScoreLevel_DEX(attachee, args, evt_obj):
	evt_obj.bonus_list.add(-4, EK_STAT_DEXTERITY, 230) #bonus.mes: {230}{~Web~[TAG_SPELLS_WEB]}
	return 0

def exEntangled_OnToHitBonus2(attachee, args, evt_obj):
	evt_obj.bonus_list.add(-2, 12, 230) #bonus.mes: {230}{~Web~[TAG_SPELLS_WEB]}
	return 0

def exEntangled_OnGetMoveSpeed(attachee, args, evt_obj):
	movespeedCap = evt_obj.bonus_list.get_sum()
	if (movespeedCap > 5):
		movespeedCap = movespeedCap / 2
	#walk
	evt_obj.bonus_list.set_overall_cap(1, movespeedCap, 0, 230) #bonus.mes: {230}{~Web~[TAG_SPELLS_WEB]}
	#run?
	#evt_obj.bonus_list.set_overall_cap(2, movespeedCap, 0, 230) #bonus.mes: {230}{~Web~[TAG_SPELLS_WEB]}
	return 0

def exEntangled_Remove(attachee, args, evt_obj):
	partId = args.get_arg(3)
	if (partId > 0):
		game.particles_kill(partId)
	args.set_arg(3, 0)
	args.condition_remove()
	return 0

def exEntangled_OnGetEffectTooltip(attachee, args, evt_obj):
	#evt_obj.append(tpdp.hash("TAG_SPELLS_WEB"), -1, "Entangled")
	evt_obj.append(1054-1000+91, -1, "Entangled")
	
	return 0

def exEntangled_OnBuildRadialMenuEntry(attachee, args, evt_obj):
	radial_action = tpdp.RadialMenuEntryPythonAction("Break Free",D20A_PYTHON_ACTION, 6101, 0, "TAG_INTERFACE_HELP")
	radial_action.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Skills)
	return 0

def exEntangled_OnD20PythonActionPerform_BreakFree(attachee, args, evt_obj):
	dc = args.get_arg(1)
	obj_strength = attachee.stat_level_get(stat_strength)
	strMod = math.floor((obj_strength - 10)/2)
	roll_dice = dice_new("1d20")
	roll_dice.bonus = strMod;
	roll_result = roll_dice.roll()
	succ = roll_result >= dc
	succ = 1
	if (succ):
		s = "Break Free succeeded: {}({}) vs DC {}\n\n".format(roll_result, roll_dice, dc)
		game.create_history_freeform(s)
		attachee.float_text_line( 'Breake Free succeeded!', tf_green)
		exEntangled_Remove(attachee, args, evt_obj)
	else:
		s = "Break Free failed: {}({}) vs DC {}\n\n".format(roll_result, roll_dice, dc)
		game.create_history_freeform(s)
		attachee.float_text_line('Breake Free failed!', tf_red)
	return 0

modObj = PythonModifier(GetConditionName(), 4) # 0 - ?, 1 - dc
modObj.AddHook(ET_OnConditionAddPre, EK_NONE, exEntangled_OnPreAdd, ())
modObj.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Condition, exEntangled_OnD20Query_CritterHasCondition, ())
modObj.AddHook(ET_OnConditionAdd, EK_NONE, exEntangled_OnAdd, ())
modObj.AddHook(ET_OnConditionRemove, EK_NONE, exEntangled_OnRemove, ())
modObj.AddHook(ET_OnD20Query, EK_Q_AOOPossible, OnQueryReturnFalse, ())
modObj.AddHook(ET_OnD20Query, EK_Q_Is_BreakFree_Possible, OnQueryReturnTrue, ())
modObj.AddHook(ET_OnAbilityScoreLevel, EK_STAT_DEXTERITY, exEntangled_OnAbilityScoreLevel_DEX, ())
modObj.AddHook(ET_OnToHitBonus2, EK_NONE, exEntangled_OnToHitBonus2, ())
modObj.AddHook(ET_OnGetMoveSpeed, EK_NONE, exEntangled_OnGetMoveSpeed, ())
modObj.AddHook(ET_OnD20Signal, EK_S_Combat_End, exEntangled_Remove, ())
modObj.AddHook(ET_OnD20Signal, EK_S_Killed, exEntangled_Remove, ())
modObj.AddHook(ET_OnGetEffectTooltip, EK_NONE, exEntangled_OnGetEffectTooltip, ())
modObj.AddHook(ET_OnBuildRadialMenuEntry, EK_NONE, exEntangled_OnBuildRadialMenuEntry, ())
modObj.AddHook(ET_OnD20PythonActionPerform, 6101, exEntangled_OnD20PythonActionPerform_BreakFree, ())
# S_Teleport_Prepare? - skip for now
# S_Teleport_Reconnect ? - skip for now
# ET_OnGetTooltip - description
