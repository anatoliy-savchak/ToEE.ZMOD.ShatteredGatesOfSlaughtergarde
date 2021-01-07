import toee, templeplus.pymod, sys

###################################################

def GetConditionName():
	return "Lethal_Shock"

print("Registering " + GetConditionName())
###################################################

def Lethal_Shock_Check(attachee, args, evt_obj):
	return 1

def Lethal_Shock_Perform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	try:
		#debugg.breakp("Lethal_Shock_Perform")
		caster = attachee
		#print("caster: {}".format(caster))
		toee.game.create_history_freeform("{} performs Lethal Shock (Su)!\n\n".format(caster.description))
		toee.game.particles("sp-Call Lightning", caster)
		affected = toee.game.obj_list_range(caster.location, 20, toee.OLC_CRITTERS)
		#print("found: {}".format(affected))
		dce = toee.dice_new("4d8")
		for target in affected:
			assert isinstance(target, toee.PyObjHandle)
			if (target == caster): continue
			if (target.type != toee.obj_t_npc and target.type != toee.obj_t_pc): continue
			f = target.object_flags_get()
			if ((f & toee.OF_OFF) or (f & toee.OF_DESTROYED) or (f & toee.OF_DONTDRAW)): continue
			#print("processing target: {}".format(target))
			saved = target.saving_throw(12, toee.D20_Save_Reflex, toee.D20STD_F_NONE, caster)
			#print("saved: {}".format(saved))
			reduction = 100
			if (saved): reduction = toee.DAMAGE_REDUCTION_HALF
			target.damage_with_reduction(caster, toee.D20DT_ELECTRICITY, dce, toee.D20DAP_NORMAL, reduction, toee.D20A_CLASS_ABILITY_SA)
			toee.game.particles("sp-Call Lightning-hit", target)

		if (len(affected) > 0 and caster.anim_goal_push_attack(affected[0], toee.game.random_range(0, 2), 1, 0)):
			new_anim_id = caster.anim_goal_get_new_id()
			#print("pushed new anim id: {}".format(new_anim_id))
			d20action.flags |= toee.D20CAF_NEED_ANIM_COMPLETED
			d20action.anim_id = new_anim_id
	except Exception, e:
		print "Lethal_Shock_Perform error:", sys.exc_info()[0]
		print(str(e))
		#debugg.breakp("error")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 2) # reserved
modObj.AddHook(toee.ET_OnD20PythonActionCheck, 3001, Lethal_Shock_Check, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3001, Lethal_Shock_Perform, ())
