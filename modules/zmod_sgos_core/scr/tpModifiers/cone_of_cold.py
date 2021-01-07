import toee, templeplus.pymod, sys, tpdp, math, traceback, debug

###################################################

def GetConditionName():
	return "Cone_Of_Cold"

print("Registering " + GetConditionName())
###################################################

def Cone_Of_Cold_Check(attachee, args, evt_obj):
	return 1

def Cone_Of_Cold_Perform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	try:
		caster = attachee
		toee.game.particles("sp-evocation-conjure", caster)

		radius = args.get_arg(0)
		if (not radius): radius = 30
		damage_multiplier = args.get_arg(1)
		if (not damage_multiplier): damage_multiplier = 1
		dc = args.get_arg(2)
		if (not dc): dc = 13
		targets = toee.game.obj_list_cone(caster, toee.OLC_CRITTERS, radius, -45, 90)

		print(targets)
		furthest = None
		if (targets):
			if (not furthest): furthest = targets[0]
			target_loc = furthest.location
			target_loc_off_x = furthest.off_x
			target_loc_off_y = furthest.off_y
			target_loc_off_z = furthest.obj_get_int(toee.obj_f_offset_z)
			caster.turn_towards(furthest)

			toee.game.create_history_freeform("{} performs Breath Weapon (Su)!\n\n".format(caster.description))
			toee.game.particles("sp-Cone of Cold", caster )
			toee.game.pfx_lightning_bolt(caster, target_loc, target_loc_off_x, target_loc_off_y, target_loc_off_z )
			affected = targets
			dce = toee.dice_new("{}d4".format(damage_multiplier))
			for target in affected:
				assert isinstance(target, toee.PyObjHandle)
				if (target == caster): continue
				if (target.type != toee.obj_t_npc and target.type != toee.obj_t_pc): continue
				f = target.object_flags_get()
				if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
				descriptor = toee.D20STD_F_NONE #toee.D20STD_F_SPELL_DESCRIPTOR_ACID todo
				if (target.reflex_save_and_damage(caster, dc, toee.DAMAGE_REDUCTION_HALF, descriptor, dce, toee.D20DT_COLD, toee.D20DAP_NORMAL, toee.D20A_CLASS_ABILITY_SA, 0)):
					target.float_mesfile_line("mes\\spell.mes", 30001)
				else: 
					target.float_mesfile_line("mes\\spell.mes", 30002)
				#toee.game.particles("sp-Call Lightning-hit", target)

			if (furthest > 0 and caster.anim_goal_push_attack(furthest, toee.game.random_range(0, 2), 1, 0)):
				new_anim_id = caster.anim_goal_get_new_id()
				#print("pushed new anim id: {}".format(new_anim_id))
				evt_obj.d20a.flags |= toee.D20CAF_NEED_ANIM_COMPLETED
				evt_obj.d20a.anim_id = new_anim_id
	except Exception, e:
		print "Cone_Of_Cold_Perform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debug.breakp("error")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 3) # radius, damage multiplier, dc
modObj.AddHook(toee.ET_OnD20PythonActionCheck, 3010, Cone_Of_Cold_Check, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3010, Cone_Of_Cold_Perform, ())
