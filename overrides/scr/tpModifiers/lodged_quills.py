import toee, templeplus.pymod, tpdp, debug, sys

###################################################

def GetConditionName():
	return "Lodged_Quills"

print("Registering " + GetConditionName())
###################################################

LODGED_QUILLS_PENALTY_MESSAGE = "Penalty due to {} lodged Quills"
LODGED_QUILLS_TOOLTIP = "Lodged Quills ({})"
LODGED_QUILLS_TOOLTIP_SUFFIX = " (-{} on attack, saves and skill checks)"

def Lodged_Quills_OnToHitBonus2(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	
	lodged_quills = args.get_arg(0)
	if (lodged_quills):
		evt_obj.bonus_list.add(-lodged_quills, 12, LODGED_QUILLS_PENALTY_MESSAGE.format(lodged_quills))
	return 0

def Lodged_Quills_OnSaveThrowLevel(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	
	lodged_quills = args.get_arg(0)
	if (lodged_quills):
		evt_obj.bonus_list.add(-lodged_quills, 12, LODGED_QUILLS_PENALTY_MESSAGE.format(lodged_quills))
	return 0

def Lodged_Quills_OnGetSkillLevel(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	
	lodged_quills = args.get_arg(0)
	if (lodged_quills):
		evt_obj.bonus_list.add(-lodged_quills, 12, LODGED_QUILLS_PENALTY_MESSAGE.format(lodged_quills))
	return 0

def Lodged_Quills_OnBuildRadialMenuEntry(attachee, args, evt_obj):
	radial_action = tpdp.RadialMenuEntryPythonAction("Remove Quills", toee.D20A_PYTHON_ACTION, 3004, 0, "TAG_INTERFACE_HELP")
	#assert isinstance(radial_action, tpdp.RadialMenuEntryParent)
	radial_action.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Skills)
	return 0

def Lodged_Quills_OnD20PythonActionCheck(attachee, args, evt_obj):
	return 1

def Lodged_Quills_OnD20PythonActionPerform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	#debug.breakp("Lodged_Quills_OnD20PythonActionPerform start")
	try:
		lodged_quills = args.get_arg(0)
		if (lodged_quills):
			target = evt_obj.d20a.target
			#toee.game.create_history_freeform("{} removes lodged Quill...\n\n".format(attachee.description))
			check = attachee.skill_roll(toee.skill_heal, 20, 0)
			if (check):
				attachee.float_text_line("Quill removed successfully!", toee.tf_green)
			else:
				dice = toee.dice_new("1d6")
				target.damage(toee.OBJ_HANDLE_NULL, toee.D20DT_BLOOD_LOSS, dice, toee.D20DAP_NORMAL, toee.D20A_UNSPECIFIED_ATTACK)
				attachee.float_text_line("Quill removed with some blood loss!", toee.tf_red)
			args.set_arg(0, lodged_quills - 1)
		if (not args.get_arg(0)):
			args.condition_remove()
	except Exception, e:
		print "Lodged_Quills_OnD20PythonActionPerform error:", sys.exc_info()[0]
		print(str(e))
		#debug.breakp("Lodged_Quills_OnD20PythonActionPerform error")
	return 1

def Lodged_Quills_OnGetTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjTooltip)
	lodged_quills = args.get_arg(0)
	evt_obj.append(LODGED_QUILLS_TOOLTIP.format(lodged_quills))
	return 0

def Lodged_Quills_OnGetEffectTooltip(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjEffectTooltip)
	lodged_quills = args.get_arg(0)
	if (lodged_quills):
		evt_obj.append(tpdp.hash("LODGED_QUILLS"), -2, LODGED_QUILLS_TOOLTIP_SUFFIX.format(lodged_quills))
	return 0

def Lodged_Quills_OnConditionAddPre(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjModifier)
	
	# check if same one wants to be added, if so, deny, but increase quills
	if (evt_obj.is_modifier(GetConditionName())):
		args.set_arg(args.get_arg(0) + 1)
		evt_obj.return_val = 0
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2, 0) # 0 - number of quills lodged
modObj.AddHook(toee.ET_OnToHitBonus2, toee.EK_NONE, Lodged_Quills_OnToHitBonus2, ())
modObj.AddHook(toee.ET_OnSaveThrowLevel, toee.EK_NONE, Lodged_Quills_OnSaveThrowLevel, ())
modObj.AddHook(toee.ET_OnGetSkillLevel, toee.EK_NONE, Lodged_Quills_OnGetSkillLevel, ())
modObj.AddHook(toee.ET_OnBuildRadialMenuEntry, toee.EK_NONE, Lodged_Quills_OnBuildRadialMenuEntry, ())
modObj.AddHook(toee.ET_OnD20PythonActionCheck, 3004, Lodged_Quills_OnD20PythonActionCheck, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3004, Lodged_Quills_OnD20PythonActionPerform, ())
modObj.AddHook(toee.ET_OnGetTooltip, toee.EK_NONE, Lodged_Quills_OnGetTooltip, ())
modObj.AddHook(toee.ET_OnGetEffectTooltip, toee.EK_NONE, Lodged_Quills_OnGetEffectTooltip, ())
modObj.AddHook(toee.ET_OnConditionAddPre, toee.EK_NONE, Lodged_Quills_OnConditionAddPre, ())