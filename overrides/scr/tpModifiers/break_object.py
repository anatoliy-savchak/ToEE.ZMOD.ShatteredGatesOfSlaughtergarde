import toee, templeplus.pymod, sys, tpdp, math, traceback, debug

###################################################
def GetConditionName():
	return "Break_Object"

print("Registering " + GetConditionName())
###################################################

def Break_Object_Check(attachee, args, evt_obj):
	return 1

def Break_Object_Perform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	try:
		target = evt_obj.d20a.target
		assert isinstance(target, toee.PyObjHandle)
		print(target)
		target_type = 0
		if (target):
			target_type = target.type
		if (not target or not (target_type == toee.obj_t_container or target_type == toee.obj_t_portal)):
			message = "Please popup Break action on Container or Portal!"
			target.float_text_line(message, toee.tf_red)
			#toee.game.alert_show(message, "Close")
			return 0

		dc = 23
		if (target_type == toee.obj_t_container):
			container_flags = target.container_flags_get()
			dc = target.obj_get_int(toee.obj_f_container_pad_i_1)
			if (not dc):
				dc = 23
			if (not container_flags & toee.OCOF_LOCKED):
				target.float_text_line("Not Locked!", toee.tf_yellow)
				return 0
			if (container_flags & toee.OCOF_ALWAYS_LOCKED):
				target.float_text_line("Cannot be Broken!", toee.tf_red)
				return 0
			if (container_flags & toee.OCOF_MAGICALLY_HELD):
				target.float_text_line("Cannot be Broken! Magically held.", toee.tf_red)
				return 0

		if (target_type == toee.obj_t_portal):
			portal_flags = target.portal_flags_get()
			dc = target.obj_get_int(toee.obj_f_portal_pad_i_1)
			if (not dc):
				dc = 23
			if (not portal_flags & toee.OPF_LOCKED):
				target.float_text_line("Not Locked!", toee.tf_yellow)
				return 0
			if (portal_flags & toee.OPF_ALWAYS_LOCKED):
				target.float_text_line("Cannot be Broken!", toee.tf_red)
				return 0
			if (portal_flags & toee.OPF_MAGICALLY_HELD):
				target.float_text_line("Cannot be Broken! Magically held.", toee.tf_red)
				return 0

		
		#text = "Break an Object"
		text = "Break {}".format(target.description)
		#debug.breakp("bonuslist")
		bonuslist = tpdp.BonusList()
		bonus = tpdp.dispatch_stat(attachee, toee.stat_str_mod, bonuslist)
		dice = toee.dice_new("1d20")
		roll = dice.roll()
		check = roll + bonus >= dc 
		hist_id = tpdp.create_history_dc_roll(attachee, dc, dice, roll, text, bonuslist)
		toee.game.create_history_from_id(hist_id)

		if (check):
			if (target.type == toee.obj_t_container):
				target.container_flag_unset(toee.OCOF_LOCKED)
				target.container_flag_unset(toee.OCOF_JAMMED)
				target.container_flag_set(toee.OCOF_BUSTED)
				target.float_text_line("Success!", toee.tf_green)

			elif (target.type == toee.obj_t_portal):
				target.portal_flag_unset(toee.OPF_LOCKED)
				target.portal_flag_set(toee.OPF_BUSTED)
				target.float_text_line("Success!", toee.tf_green)
		else:
			if (bonus + 20 < dc):
				target.float_text_line("Impossible!", toee.tf_red)
			else:
				target.float_text_line("Failure!", toee.tf_red)
		
		attachee.anim_goal_use_object(target)
	except Exception, e:
		print "Break_Object_Perform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debug.breakp("error")
	return 0

def Break_Object_OnBuildRadialMenuEntry(attachee, args, evt_obj):
	radial_action = tpdp.RadialMenuEntryPythonAction("Break an Object", toee.D20A_PYTHON_ACTION, 3012, 0, "TAG_INTERFACE_HELP")
	#assert isinstance(radial_action, tpdp.RadialMenuEntryParent)
	radial_action.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Skills)
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 3) # natural_attack_num, used_this_turn
modObj.AddHook(toee.ET_OnD20PythonActionCheck, 3012, Break_Object_Check, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3012, Break_Object_Perform, ())
modObj.AddHook(toee.ET_OnBuildRadialMenuEntry, toee.EK_NONE, Break_Object_OnBuildRadialMenuEntry, ())