import toee, templeplus.pymod, debug, sys, tpdp, traceback

###################################################

def GetConditionName():
	return "Net_Throw"

print("Registering " + GetConditionName())
###################################################

def Net_Throw_OnBuildRadialMenuEntry(attachee, args, evt_obj):
	radial_action = tpdp.RadialMenuEntryPythonAction("Net Throw", toee.D20A_PYTHON_ACTION, 3014, 0, "TAG_INTERFACE_HELP")
	radial_action.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Offense)
	return 0

def Net_Throw_OnD20PythonActionPerform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	try:
		print("Net_Throw_OnD20PythonActionPerform")
		#debug.breakp("Net_Throw_OnD20PythonActionPerform")
		histid = toee.game.create_history_from_pattern(62, attachee, evt_obj.d20a.target)
		evt_obj.d20a.flags |= toee.D20CAF_RANGED | toee.D20CAF_TOUCH_ATTACK #| toee.D20CAF_THROWN_GRENADE
		evt_obj.d20a.to_hit_processing()
		hit = evt_obj.d20a.flags & toee.D20CAF_HIT
		print("hit: ".format(hit))
		if (not evt_obj.d20a.roll_id_1): evt_obj.d20a.roll_id_1 = histid

		if attachee.anim_goal_push_attack(evt_obj.d20a.target, toee.game.random_range(0,2), 0, 0):
			new_anim_id = attachee.anim_goal_get_new_id()
			print "new anim id: " + str(new_anim_id)
			evt_obj.d20a.flags |= toee.D20CAF_NEED_ANIM_COMPLETED
			evt_obj.d20a.anim_id = new_anim_id

	except Exception, e:
		print "Net_Throw_OnD20PythonActionPerform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debugg.breakp("error")
	return 0

def Net_Throw_OnD20PythonActionFrame(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	try:
		print("Net_Throw_OnD20PythonActionFrame")

		tgt = evt_obj.d20a.target
		print "Net_Throw_OnD20PythonActionFrame: " + str(tgt)
		if (tgt):
			projectileProto = 3009 # dart
			projectileHandle = evt_obj.d20a.create_projectile_and_throw(projectileProto, tgt)
			projectileHandle.obj_set_float(toee.obj_f_offset_z, 60.0)
			if evt_obj.d20a.projectile_append(projectileHandle, toee.OBJ_HANDLE_NULL):
				print "Net_Throw_OnD20PythonActionFrame: Projectile Appended"
				attachee.apply_projectile_particles(projectileHandle, evt_obj.d20a.flags)
				evt_obj.d20a.flags |= toee.D20CAF_NEED_PROJECTILE_HIT
	except Exception, e:
		print "Net_Throw_OnD20PythonActionFrame error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debugg.breakp("error")
	return 0

def Net_Throw_OnProjectileDestroyed(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	try:
		print("Net_Throw_OnProjectileDestroyed")
		tgt = evt_obj.attack_packet.target
		print("target: {}".format(tgt))
		if (not tgt):
			tgt = attachee.obj_get_obj(toee.obj_f_last_hit_by)
			print("target2: {}".format(tgt))
		#proj.obj_get_obj(toee.obj_f_last_hit_by, d20action.target) ammo_item
		flags = evt_obj.attack_packet.get_flags()
		hit = flags & toee.D20CAF_HIT
		print("hit: {}, flags: {}".format(hit, flags))
		if (hit and tgt):
			dc_break_free = args.get_arg(0)
			if (not dc_break_free): dc_break_free = 6
			dc_escape = args.get_arg(0)
			if (not dc_escape): dc_escape = 12
			print("adding condition netted to {}".format(tgt))
			tgt.condition_add_with_args("netted", dc_break_free, dc_escape)
		else: print("missed")
	except Exception, e:
		print "Net_Throw_OnProjectileDestroyed error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debugg.breakp("error")
	return 0

def Net_Throw_OnDealingDamage(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjDamage)
	try:
		print("Net_Throw_OnDealingDamage")
		tgt = evt_obj.attack_packet.target
		print("target: {}".format(tgt))
		print("event_key: {}".format(evt_obj.attack_packet.event_key))
		flags = evt_obj.attack_packet.get_flags()
		hit = flags & toee.D20CAF_HIT
		print("hit: {}, flags: {}".format(hit, flags))
		if (hit and tgt):
			print("adding condition netted to {}".format(tgt))
			dc_BreakFree = args.get_arg(0)
			dc_EscapeArtist = args.get_arg(1)
			tgt.condition_add_with_args("netted", dc_BreakFree, dc_EscapeArtist)
		else: print("missed")
		evt_obj.damage_packet.final_damage = 0
	except Exception, e:
		print "Net_Throw_OnDealingDamage error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debugg.breakp("error")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 0 - dc break free, 1 - dc escape artist
modObj.AddHook(toee.ET_OnBuildRadialMenuEntry, toee.EK_NONE, Net_Throw_OnBuildRadialMenuEntry, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3014, Net_Throw_OnD20PythonActionPerform, ())
modObj.AddHook(toee.ET_OnD20PythonActionFrame, 3014, Net_Throw_OnD20PythonActionFrame, ())
modObj.AddHook(toee.ET_OnProjectileDestroyed, toee.EK_NONE, Net_Throw_OnProjectileDestroyed, ())
#modObj.AddHook(toee.ET_OnDealingDamage, 3014, Net_Throw_OnDealingDamage, ())
