import toee, templeplus.pymod, sys, tpdp, math, traceback, debug

###################################################
def GetConditionName():
	return "Smash_Object"

print("Registering " + GetConditionName())
###################################################

def Smash_Object_Check(attachee, args, evt_obj):
	return 1

def Smash_Object_Perform(attachee, args, evt_obj):
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
			message = "Must be Container or Portal!"
			target.float_text_line(message, toee.tf_red)
			#toee.game.alert_show(message, "Close")
			return 0

		ac = 5
		if (1):
			bonlistTarget = tpdp.BonusList()
			bonlistTarget.add(10, 0, 102) #{102}{Initial Value}
			bonlistTarget.add(-5, 0, 104) #{104}{~Dexterity~[TAG_DEXTERITY] Bonus}
			bonlistTarget.add(-2, 0, "Inanimate object")
			ac = bonlistTarget.get_total()

		atkBon = tpdp.EventObjAttack()
		bonus = atkBon.dispatch(attachee, target, toee.ET_OnToHitBonus2, toee.EK_D20A_UNSPECIFIED_ATTACK)
		flags = atkBon.attack_packet.get_flags()

		dice = toee.dice_new("1d20")
		roll = dice.roll()
		check = roll + bonus >= ac 

		crit_hist_id = None
		if (check):
			flags |= toee.D20CAF_HIT
			critThreatRange = 21 - tpdp.EventObjAttack().dispatch(attachee, toee.OBJ_HANDLE_NULL, toee.ET_OnGetCriticalHitRange, toee.EK_D20A_UNSPECIFIED_ATTACK);
			if (roll >= critThreatRange):
				critroll = dice.roll()
				#critroll = 15
				crit_hist_id = tpdp.create_history_attack_roll(attachee, target, critroll, atkBon.bonus_list, bonlistTarget, flags)
				if (critroll + bonus >= ac):
					flags |= toee.D20CAF_CRITICAL

		hist_id = tpdp.create_history_attack_roll(attachee, target, roll, atkBon.bonus_list, bonlistTarget, flags)
		toee.game.create_history_from_id(hist_id)
		if (crit_hist_id):
			toee.game.create_history_from_id(crit_hist_id)

		reduction = target.obj_get_int(toee.obj_f_hp_adj)
		hp0 = target.stat_level_get(toee.stat_hp_current)

		args.set_arg(2, reduction)
		target.deal_attack_damage(attachee, toee.EK_D20A_UNSPECIFIED_ATTACK, flags, toee.D20A_SUNDER)
		args.set_arg(2, 0)
		hp = target.stat_level_get(toee.stat_hp_current)
		print("HP changed from {} to {}".format(hp0, hp))

		if (hp > 0):
			target.float_text_line("{} hp left".format(hp), toee.tf_yellow)
			return 0

		if (target_type == toee.obj_t_portal):
			target.portal_flag_unset(toee.OPF_LOCKED)
			target.portal_flag_unset(toee.OPF_JAMMED)
			target.object_flag_set(toee.OF_DONTDRAW)
			#target.object_flag_set(toee.OF_EXTINCT)
			#target.portal_flag_set(toee.OPF_OPEN)
			portal_open_and_off(target)
		elif (target_type == toee.obj_t_container):
			target.container_flag_unset(toee.OCOF_LOCKED)
			target.container_flag_unset(toee.OCOF_JAMMED)
			target.container_flag_set(toee.OCOF_BUSTED)
			attachee.anim_goal_use_object(target)
	except Exception, e:
		args.set_arg(2, 0)
		print "Smash_Object_Perform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debug.breakp("error")
	return 0

def Smash_Object_OnBuildRadialMenuEntry(attachee, args, evt_obj):
	radial_action = tpdp.RadialMenuEntryPythonAction("Smash an Object", toee.D20A_PYTHON_ACTION, 3017, 0, "TAG_INTERFACE_HELP")
	#assert isinstance(radial_action, tpdp.RadialMenuEntryParent)
	radial_action.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Skills)
	return 0

def Smash_Object_OnDealingDamage(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjDamage)
	reduction = args.get_arg(2)
	if (not reduction): return 0
	evt_obj.damage_packet.add_physical_damage_res(reduction, toee.D20DAP_NORMAL, 126) #{126}{~Damage Reduction~[TAG_SPECIAL_ABILITIES_DAMAGE_REDUCTION]}
	return 0

def portal_open_and_off(portal):
	assert isinstance(portal, toee.PyObjHandle)
	portal.portal_toggle_open()
	toee.game.timevent_add(timevent_portal_off, (portal), 500, 1) # 1000 = 1 second
	return

def timevent_portal_off(obj):
	assert isinstance(obj, toee.PyObjHandle)
	#obj.destroy()
	obj.object_flag_set(toee.OF_OFF)
	return 1

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 3) # reserved, reserved, damage_reduction for target
modObj.AddHook(toee.ET_OnD20PythonActionCheck, 3017, Smash_Object_Check, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3017, Smash_Object_Perform, ())
modObj.AddHook(toee.ET_OnBuildRadialMenuEntry, toee.EK_NONE, Smash_Object_OnBuildRadialMenuEntry, ())
modObj.AddHook(toee.ET_OnDealingDamage, toee.EK_NONE, Smash_Object_OnDealingDamage, ())
