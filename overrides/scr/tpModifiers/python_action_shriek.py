import toee, templeplus.pymod, tpdp, debug, sys

###################################################

def GetConditionName():
	return "Python_Action_Shriek"

print("Registering " + GetConditionName())
###################################################

D20STD_SPELL_DESCRIPTOR_FEAR = 0x100000

def Python_Action_Shriek_Check(attachee, args, evt_obj):
	return 1

def Python_Action_Shriek_Perform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	try:
		#debugg.breakp("Python_Action_Shriek_Perform")
		caster = attachee
		print("caster: {}".format(caster))
		toee.game.create_history_freeform("{} performs Shriek (Su)!\n\n".format(caster.description))
		affected = toee.game.obj_list_range(caster.location, 60, toee.OLC_CRITTERS)
		print("found: {}".format(affected))
		dce = toee.dice_new("2d4")
		dc = args.get_arg(0)
		if (not dc):
			dc = 12
		furthest = None
		furthest_dist = 0
		for target in affected:
			assert isinstance(target, toee.PyObjHandle)
			if (target == caster): continue
			if (target.type != toee.obj_t_npc and target.type != toee.obj_t_pc): continue
			f = target.object_flags_get()
			if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
			if (not target.can_see(caster)):
				print("{}::not target.can_see({}), skip".format(GetConditionName(), target))
				continue
			if (target.d20_query(toee.EK_Q_Critter_Is_Deafened - toee.EK_Q_Helpless)):
				print("{}::target.d20_query(toee.EK_Q_Critter_Is_Deafened - toee.EK_Q_Helpless)({}), skip".format(GetConditionName(), target))
				continue
			print("processing target: {}".format(target))
			dist = target.distance_to(caster)
			if (not furthest or furthest_dist < dist):
				furthest = target
				furthest_dist = dist
			saved = target.saving_throw(dc, toee.D20_Save_Will, D20STD_SPELL_DESCRIPTOR_FEAR, caster)
			if (saved): continue
			remaining = dce.roll()
			#part = toee.game.particles('sp-Fear-Hit', target)
			target.condition_add_with_args("Paralyzed", remaining, 0)
			target.float_mesfile_line( 'mes\\combat.mes', 149, 1) # {149}{Paralyzed!}

		if (furthest):
			caster.turn_towards(furthest)
		toee.game.particles("sp-Fear", caster)

		if (len(affected) > 0 and caster.anim_goal_push_attack(affected[0], toee.game.random_range(0, 2), 1, 0)):
			new_anim_id = caster.anim_goal_get_new_id()
			#print("pushed new anim id: {}".format(new_anim_id))
			d20action.flags |= toee.D20CAF_NEED_ANIM_COMPLETED
			d20action.anim_id = new_anim_id
	except Exception, e:
		print "Python_Action_Shriek error:", sys.exc_info()[0]
		print(str(e))
		#debugg.breakp("error")
	return 1

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # reserved
modObj.AddHook(toee.ET_OnD20PythonActionCheck, 3003, Python_Action_Shriek_Check, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3003, Python_Action_Shriek_Perform, ())
