import toee, templeplus.pymod, tpdp, debug, sys

###################################################

def GetConditionName():
	return "Pull_Down_Ceiling"

print("Registering " + GetConditionName())
###################################################

def Pull_Down_Ceiling_Check(attachee, args, evt_obj):
	return 1

def Pull_Down_Ceiling_Perform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	try:
		#debugg.breakp("Pull_Down_Ceiling_Perform")
		caster = attachee
		#print("caster: {}".format(caster))
		toee.game.create_history_freeform("{} Pulls Down the Ceiling!\n\n".format(caster.description))
		toee.game.particles("ef-ripples-huge", caster)
		caster.float_text_line("Pulls Down the Ceiling!", 0)
		affected = toee.game.obj_list_range(caster.location, 15, toee.OLC_CRITTERS)
		#print("found: {}".format(affected))
		dce = toee.dice_new("6d6")
		for target in affected:
			assert isinstance(target, toee.PyObjHandle)
			if (target == caster): continue
			if (target.type != toee.obj_t_npc and target.type != toee.obj_t_pc): continue
			f = target.object_flags_get()
			if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
			#print("processing target: {}".format(target))
			saved = target.saving_throw(15, toee.D20_Save_Reflex, toee.D20STD_F_NONE, caster)
			#print("saved: {}".format(saved))
			reduction = 100
			if (saved): reduction = toee.DAMAGE_REDUCTION_HALF
			target.damage_with_reduction(caster, toee.D20DT_BLUDGEONING, dce, toee.D20DAP_NORMAL, reduction, toee.D20A_CLASS_ABILITY_SA)
			if (not saved and target.d20_query(toee.Q_Prone) == 0):
				target.fall_down()
				target.condition_add("Prone")
				target.float_mesfile_line('mes\\combat.mes', 104, 1 ) # Tripped!
			toee.game.particles("ef-splash", target)

		if (len(affected) > 0 and caster.anim_goal_push_attack(affected[0], toee.game.random_range(0, 2), 1, 0)):
			new_anim_id = caster.anim_goal_get_new_id()
			#print("pushed new anim id: {}".format(new_anim_id))
			d20action.flags |= toee.D20CAF_NEED_ANIM_COMPLETED
			d20action.anim_id = new_anim_id
	except Exception, e:
		print "Pull_Down_Ceiling_Perform error:", sys.exc_info()[0]
		print(str(e))
		#debugg.breakp("error")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # reserved
modObj.AddHook(toee.ET_OnD20PythonActionCheck, 3002, Pull_Down_Ceiling_Check, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3002, Pull_Down_Ceiling_Perform, ())
