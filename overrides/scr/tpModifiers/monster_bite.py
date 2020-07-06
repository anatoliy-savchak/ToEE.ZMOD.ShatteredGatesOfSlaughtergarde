import toee, templeplus.pymod, sys, tpdp, math, traceback, debug

###################################################
#unfinished!!
def GetConditionName():
	return "Monster_Bite"

print("Registering " + GetConditionName())
###################################################

def Monaster_Bite_Check(attachee, args, evt_obj):
	return 1

def Monaster_Bite_Perform(attachee, args, evt_obj):
	assert isinstance(attachee, toee.PyObjHandle)
	assert isinstance(args, tpdp.EventArgs)
	assert isinstance(evt_obj, tpdp.EventObjD20Action)
	try:
		debug.breakp("Monaster_Bite_Perform")
		d20a = evt_obj.d20a
		d20a.action_type = toee.D20A_UNSPECIFIED_ATTACK
		#attachee.anim_goal_push_attack(evt_obj.d20a.target, 2, 0, 1)
		evt_obj.d20a.anim_id = attachee.anim_goal_get_new_id()
		evt_obj.d20a.flags |= toee.D20CAF_NEED_ANIM_COMPLETED
		evt_obj.d20a.data1 = 1000
		evt_obj.d20a.to_hit_processing()
	except Exception, e:
		print "Monaster_Bite_Perform:"
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60		
		debugg.breakp("error")
	return 0

modObj = templeplus.pymod.PythonModifier(GetConditionName(), 3) # natural_attack_num, used_this_turn
modObj.AddHook(toee.ET_OnD20PythonActionCheck, 3011, Monaster_Bite_Check, ())
modObj.AddHook(toee.ET_OnD20PythonActionPerform, 3011, Monaster_Bite_Perform, ())
