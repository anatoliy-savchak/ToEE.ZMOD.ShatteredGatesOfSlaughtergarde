import toee, templeplus.pymod, debug, sys, tpdp, traceback

###################################################

def GetConditionName():
	return "Belch_Fire"

print("Registering " + GetConditionName())
###################################################

def OnD20PythonActionPerform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	try:
		print("Belch_Fire_OnD20PythonActionPerform")
		#debug.breakp("Belch_Fire_OnD20PythonActionPerform")
		histid = toee.game.create_history_from_pattern(67, attachee, evt_obj.d20a.target)
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
		print "Belch_Fire_OnD20PythonActionPerform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debugg.breakp("error")
	return 0

def OnD20PythonActionFrame(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	try:
		print("Belch_Fire_OnD20PythonActionFrame")

		tgt = evt_obj.d20a.target
		print "Belch_Fire_OnD20PythonActionFrame: " + str(tgt)
		if (tgt):
			toee.game.particles("su-Ball_of_Fire-conjure", tgt)
			projectileProto = 3017 # ball of fire
			projectileHandle = evt_obj.d20a.create_projectile_and_throw(projectileProto, tgt)
			projectileHandle.obj_set_float(toee.obj_f_offset_z, 60.0)
			projectileHandle.obj_set_int(toee.obj_f_projectile_part_sys_id, toee.game.particles( 'su-Ball_of_Fire-proj', projectileHandle) )

			if evt_obj.d20a.projectile_append(projectileHandle, toee.OBJ_HANDLE_NULL):
				print "Belch_Fire_OnD20PythonActionFrame: Projectile Appended"
				#attachee.apply_projectile_particles(projectileHandle, evt_obj.d20a.flags)
				evt_obj.d20a.flags |= toee.D20CAF_NEED_PROJECTILE_HIT
	except Exception, e:
		print "Belch_Fire_OnD20PythonActionFrame error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debugg.breakp("error")
	return 0

def OnProjectileDestroyed(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjAttack)
	try:
		print("Belch_Fire_OnProjectileDestroyed")
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
			dc = 19
			#tgt.damage_with_reduction(attachee, toee.D20DT_FIRE, toee.dice_new("6d6"), toee.D20DAP_NORMAL, )
			tgt.reflex_save_and_damage(attachee, dc, toee.D20_Save_Reduction_Half, toee.D20STD_F_NONE, toee.dice_new("6d6"), toee.D20DT_FIRE, toee.D20DAP_NORMAL, toee.D20A_NONE, 0)
			toee.game.particles("su-Ball_of_Fire-Hit", tgt)
			range = 6
			adj_dice = toee.dice_new("3d6")
			for obj in toee.game.obj_list_range(tgt.location, range, toee.OLC_PC | toee.OLC_NPC):
				if (obj == tgt): continue
				f = obj.object_flags_get()
				if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
				obj.reflex_save_and_damage(attachee, dc, toee.D20_Save_Reduction_Half, toee.D20STD_F_NONE, adj_dice, toee.D20DT_FIRE, toee.D20DAP_NORMAL, toee.D20A_NONE, 0)
				#toee.game.particles("sp-Spheres of Fire-hit", obj)
				
		else: print("missed")
	except Exception, e:
		print "Belch_Fire_OnProjectileDestroyed error:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debugg.breakp("error")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # 
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3019, OnD20PythonActionPerform, ())
modObj.AddHook(toee.ET_OnD20PythonActionFrame, 3019, OnD20PythonActionFrame, ())
modObj.AddHook(toee.ET_OnProjectileDestroyed, toee.EK_NONE, OnProjectileDestroyed, ())
